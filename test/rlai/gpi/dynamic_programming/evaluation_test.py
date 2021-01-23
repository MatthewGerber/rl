import os
import pickle

import numpy as np
import pytest
from numpy.random import RandomState

from rlai.agents.mdp import StochasticMdpAgent
from rlai.environments.gridworld import Gridworld
from rlai.gpi.dynamic_programming.evaluation import evaluate_v_pi, evaluate_q_pi, check_termination_criteria
from rlai.policies.tabular import TabularPolicy


def test_evaluate_v_pi():

    random_state = RandomState(12345)

    mdp_environment: Gridworld = Gridworld.example_4_1(random_state, None)

    mdp_agent = StochasticMdpAgent(
        'test',
        random_state,
        TabularPolicy(None, mdp_environment.SS),
        1
    )

    v_pi, _ = evaluate_v_pi(
        agent=mdp_agent,
        environment=mdp_environment,
        theta=0.001,
        num_iterations=None,
        update_in_place=True
    )

    v_pi_not_in_place, _ = evaluate_v_pi(
        agent=mdp_agent,
        environment=mdp_environment,
        theta=0.001,
        num_iterations=None,
        update_in_place=False
    )

    assert list(v_pi.keys()) == list(v_pi_not_in_place.keys())

    assert np.allclose(list(v_pi.values()), list(v_pi_not_in_place.values()), atol=0.01)

    # uncomment the following line and run test to update fixture
    # with open(f'{os.path.dirname(__file__)}/fixtures/test_iterative_policy_evaluation_of_state_value.pickle', 'wb') as file:
    #     pickle.dump(v_pi, file)

    with open(f'{os.path.dirname(__file__)}/fixtures/test_iterative_policy_evaluation_of_state_value.pickle', 'rb') as file:
        fixture = pickle.load(file)

    assert v_pi == fixture


def test_evaluate_q_pi():

    random_state = RandomState(12345)

    mdp_environment: Gridworld = Gridworld.example_4_1(random_state, None)

    mdp_agent = StochasticMdpAgent(
        'test',
        random_state,
        TabularPolicy(None, mdp_environment.SS),
        1
    )

    q_pi, _ = evaluate_q_pi(
        agent=mdp_agent,
        environment=mdp_environment,
        theta=0.001,
        num_iterations=100,
        update_in_place=True
    )

    q_pi_not_in_place, _ = evaluate_q_pi(
        agent=mdp_agent,
        environment=mdp_environment,
        theta=0.001,
        num_iterations=200,
        update_in_place=False
    )

    assert list(q_pi.keys()) == list(q_pi_not_in_place.keys())

    for s in q_pi:
        for a in q_pi[s]:
            assert np.allclose(q_pi[s][a], q_pi_not_in_place[s][a], atol=0.01)

    # uncomment the following line and run test to update fixture
    # with open(f'{os.path.dirname(__file__)}/fixtures/test_iterative_policy_evaluation_of_action_value.pickle', 'wb') as file:
    #     pickle.dump(q_pi, file)

    with open(f'{os.path.dirname(__file__)}/fixtures/test_iterative_policy_evaluation_of_action_value.pickle', 'rb') as file:
        fixture = pickle.load(file)

    assert q_pi == fixture


def test_check_termination_criteria():

    assert check_termination_criteria(0, 1) == (None, 1)
    assert check_termination_criteria(-1, 1) == (None, 1)
    assert check_termination_criteria(1, 0) == (1, None)
    assert check_termination_criteria(1, -1) == (1, None)

    with pytest.raises(ValueError):
        check_termination_criteria(None, None)

    with pytest.raises(ValueError):
        check_termination_criteria(0, None)

    with pytest.raises(ValueError):
        check_termination_criteria(None, 0)

    assert check_termination_criteria(1, 2) == (1, 2)
