import pytest
from numpy.random import RandomState

from rlai.agents.mdp import ActionValueMdpAgent
from rlai.environments.gridworld import Gridworld
from rlai.gpi.temporal_difference.evaluation import evaluate_q_pi, Mode
from rlai.q_S_A.tabular import TabularStateActionValueEstimator


def test_evaluate_q_pi_invalid_n_steps():

    random_state = RandomState(12345)
    mdp_environment: Gridworld = Gridworld.example_4_1(random_state, None)
    epsilon = 0.05
    mdp_agent = ActionValueMdpAgent(
        'test',
        random_state,
        1,
        TabularStateActionValueEstimator(mdp_environment, epsilon, None)
    )

    with pytest.raises(ValueError):
        evaluate_q_pi(
            agent=mdp_agent,
            environment=mdp_environment,
            num_episodes=5,
            num_updates_per_improvement=None,
            alpha=0.1,
            mode=Mode.Q_LEARNING,
            n_steps=-1,
            planning_environment=None
        )
