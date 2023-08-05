import typing as t
from collections import defaultdict
from statistics import mean

from bavard_ml_utils.utils import ImportExtraError


try:
    import networkx as nx
except ImportError:
    raise ImportExtraError("ml", __name__)

from bavard_ml_utils.types.conversations.actions import Actor
from bavard_ml_utils.types.conversations.conversation import ConversationDataset
from bavard_ml_utils.types.conversations.dialogue_turns import DialogueTurn


class DSTuple(t.NamedTuple):
    """
    A dialogue state, as defined by Gritta et al. in "Conversation Graph: Data Augmentation, Training and Evaluation for
    Non-Deterministic Dialogue Management" (2021). It represents the state of a conversation at a given turn.
    """

    bs: t.FrozenSet[str] = frozenset()  # the set of dialogue slots that are populated
    action: t.Optional[str] = None  # the action that was taken
    # The actor that took the action, one of "HUMAN", "AGENT" (chatbot), or `None` (in the case of the starting root
    # node of the graph).
    actor: t.Optional[str] = None


class ConvGraph:
    """
    Implementation of Algorithm (1) in "Conversation Graph: Data Augmentation, Training and Evaluation for
    Non-Deterministic Dialogue Management" by Gritta et al. (2021). Can convert a `ConversationDataset` into
    a conversation graph, which is useful for visualizing the different paths that an agent's conversations take,
    as well as for evaluating dialogue act predictions using _soft_ metrics. The graph can also be used for
    dataset augmentation in a task-oriented-dialogue training setting.

    Each node in the graph is a unique dialogue state, where a dialogue state is defined as a tuple of 1) the current
    belief state, 2) the action that was taken, and 3) the type of actor who took that action (human or chatbot).
    A belief state is the set of dialogue slots that are populated at a given turn.
    """

    def __init__(self, data: ConversationDataset):
        self.graph = nx.DiGraph()
        for conv in data:
            last_state = DSTuple()  # the starting node of the graph
            self.add_node(last_state)
            for turn in conv.turns:
                if turn.actor == Actor.HUMAN_AGENT:
                    continue
                ds = self.encode_dialogue_state(turn)
                self.add_node(ds)
                if not self.graph.has_edge(last_state, ds):
                    self.graph.add_edge(last_state, ds, weight=1)
                else:
                    self.graph[last_state][ds]["weight"] += 1
                last_state = ds

    def add_node(self, ds: DSTuple):
        """
        The `ds` tuple is used as the node's unique id, but we also add the attributes of `ds` as attributes of the
        node, so they can be interacted with easily in the graph.
        """
        if not self.graph.has_node(ds):
            bs_str = ", ".join(sorted(ds.bs))
            self.graph.add_node(ds, bs=bs_str, action=ds.action, actor=ds.actor)

    def soft_accuracy(self, y_pred: t.List[str], last_turns: t.List[DialogueTurn]):
        """
        Calcuates the soft accuracy, which is accuracy when there is more than one acceptable answer for a prediction.

        Parameters
        ----------
        y_pred : list of str
            A list of agent action predictions.
        last_turns : list of DialogueTurn
            A list, having the same length as `y_pred`, of the dialogue turns the agent action predictions in `y_pred`
            are following. For example, `y_pred[i]` should be the agent action which was predicted as coming after the
            turn `last_turns[i]`.
        """
        num_correct = 0
        for pred, last_turn in zip(y_pred, last_turns):
            num_correct += self.is_pred_correct(pred, last_turn)
        return num_correct / len(last_turns)

    def balanced_soft_accuracy(self, y_pred: t.List[str], last_turns: t.List[DialogueTurn]):
        """Same as `ConvGraph.soft_accuracy`, but equally weights the accuracy calculation of each class, or action."""
        correct = defaultdict(int)
        out_of = defaultdict(int)
        for pred, last_turn in zip(y_pred, last_turns):
            valid_next_actions = self.get_valid_next_actions(last_turn)
            if pred in valid_next_actions:
                # The prediction was right, so give full credit.
                correct[pred] += 1
                out_of[pred] += 1
            else:
                # The prediction was wrong, so equally penalize each of the classes that were valid.
                for label in valid_next_actions:
                    out_of[label] += 1 / len(valid_next_actions)
        # Compute the soft accuracy for each class/action, then return the mean of those.
        print("correct:", correct, "out_of:", out_of)
        return mean(correct[action] / out_of[action] for action in out_of.keys())

    def is_pred_correct(self, pred: str, last_turn: DialogueTurn):
        valid_next_actions = self.get_valid_next_actions(last_turn)
        return pred in valid_next_actions

    def get_valid_next_actions(self, turn: DialogueTurn) -> t.Set[str]:
        """
        Given the dialogue state of `turn`, find the actions of all dialogue states that directly follow `turn` in the
        conversation graph. In other words, return the valid next actions that appear after `turn` in the training data
        the conversation graph was constructed from.
        """
        ds = self.encode_dialogue_state(turn)
        return {v[1] for u, v in self.graph.out_edges(ds)}

    def avg_num_valid_next_actions(self):
        """
        The average out-degree of the conversation graph, which is equal to the average number of correct agent actions
        for each dialogue state in the graph.
        """
        return mean(n for _, n in self.graph.out_degree)

    def save(self, path: str):
        nx.write_graphml(self.graph, path)

    @staticmethod
    def encode_dialogue_state(turn: DialogueTurn):
        belief_state_keys = list(turn.state.slotValues.keys()) if turn.state else []
        action = turn.agentAction.name if turn.actor == Actor.AGENT else turn.userAction.intent
        return DSTuple(bs=frozenset(belief_state_keys), action=action, actor=turn.actor.value)
