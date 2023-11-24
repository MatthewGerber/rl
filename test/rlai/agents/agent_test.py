import pytest
from numpy.random import RandomState

from rlai.actions import Action
from rlai.agents import Human
from rlai.agents.mdp import ActionValueMdpAgent
from rlai.environments.gridworld import Gridworld
from rlai.q_S_A.tabular.estimators import TabularStateActionValueEstimator
from rlai.states.mdp import MdpState


def test_agent_invalid_action():
    """
    Test.
    """

    random = RandomState()
    agent = ActionValueMdpAgent('foo', random, 1.0, TabularStateActionValueEstimator(Gridworld.example_4_1(random, None), None, None))

    # test None action
    agent.__act__ = lambda t: None

    with pytest.raises(ValueError, match='Agent returned action of None'):
        agent.act(0)

    # test infeasible action
    action = Action(1, 'foo')
    agent.__act__ = lambda t: action
    state = MdpState(1, [], False)
    agent.sense(state, 0)
    with pytest.raises(ValueError, match=f'Action {action} is not feasible in state {state}'):
        agent.act(0)


def test_human_agent():
    """
    Test.
    """

    agent = Human()

    a1 = Action(0, 'Foo')
    a2 = Action(1, 'Bar')

    state = MdpState(1, [a1, a2], False)
    agent.sense(state, 0)

    call_num = 0

    def mock_input(
            *_
    ) -> str:

        nonlocal call_num
        if call_num == 0:
            call_num += 1
            return 'asdf'
        else:
            return 'Bar'

    agent.get_input = mock_input  # MagicMock(return_value='Bar')

    assert agent.act(0) == a2

    with pytest.raises(NotImplementedError):
        rng = RandomState(12345)
        Human.init_from_arguments([], rng, Gridworld.example_4_1(rng, None))
