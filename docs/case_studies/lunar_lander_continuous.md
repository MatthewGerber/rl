# Lunar Lander with Continuous Control
* Content
{:toc}

# Introduction

You can read more about this environment [here](https://gym.openai.com/envs/LunarLanderContinuous-v2/). Many of the 
issues involved in solving this environment are addressed in the 
[continuous mountain car](mountain_car_continuous.md) case study, so we will focus here on details specific to the 
continuous lunar lander environment.

# Development
A few key points of development are worth mentioning.

### Fuel Level
Similar to the continuous mountain car environment, the continuous lunar lander does not include the concept of fuel. 
Within RLAI, an initial fuel level of 1.0 is set at the start of each episode, and throttle use depletes the fuel level 
accordingly. See 
[here](https://github.com/MatthewGerber/rlai/blob/07950806a0f46801a5117656f75e9f72466c156d/src/rlai/environments/openai_gym.py#L193)
for details.

### Reward
Looking at the OpenAI Gym reward calculation 
[code](https://github.com/openai/gym/blob/2754d9737e7033bbdca7e69c9e5e08156facc7f4/gym/envs/box2d/lunar_lander.py#L360-L385)
for the lunar lander, one sees a complicated arrangement of scaling factors and transformations. A goal in this case 
study was to simplify this reward function. The ideal terminal state is easy to describe:  zeros across the position and 
movement state variables. This portion of the reward function is calculated as follows:
```
state_reward = -np.abs(observation[0:6]).sum()
```
In addition to rewarding the state variables as above, fuel is rewarded if the state is good. Rewarding for remaining 
fuel unconditionally can cause the agent to veer out of bounds immediately and thus sacrifice state reward for fuel 
reward. The terminating state is considered good if the lander is within the goal posts (which are at x = +/-0.2) and 
the other orientation variables (y position, x and y velocity, angle and angular velocity) are near zero.

The full code 
for the continuous lunar lander reward can be found 
[here](https://github.com/MatthewGerber/rlai/blob/07950806a0f46801a5117656f75e9f72466c156d/src/rlai/environments/openai_gym.py#L227-L245)


# Training
The following command trains an agent for the continuous lunar lander environment using policy gradient optimization 
with a baseline state-value estimator:

```
rlai train --random-seed 12345 --agent rlai.agents.mdp.StochasticMdpAgent --gamma 1.0 --environment rlai.environments.openai_gym.Gym --gym-id LunarLanderContinuous-v2 --render-every-nth-episode 100 --video-directory ~/Desktop/lunarlander_continuous_videos --force --plot-environment --T 500 --train-function rlai.policy_gradient.monte_carlo.reinforce.improve --num-episodes 50000 --plot-state-value --v-S rlai.v_S.function_approximation.estimators.ApproximateStateValueEstimator --feature-extractor rlai.environments.openai_gym.ContinuousLunarLanderFeatureExtractor --function-approximation-model rlai.models.sklearn.SKLearnSGD --loss squared_loss --sgd-alpha 0.0 --learning-rate constant --eta0 0.0001 --policy rlai.policies.parameterized.continuous_action.ContinuousActionBetaDistributionPolicy --policy-feature-extractor rlai.environments.openai_gym.ContinuousLunarLanderFeatureExtractor --plot-policy --alpha 0.0001 --update-upon-every-visit True --save-agent-path ~/Desktop/continuous_lunarlander_agent.pickle
```

The argument are explained below.

### RLAI
* `train`:  Train the agent. 
* `--random-seed 12345`:  For reproducibility.

### Agent
* `--agent rlai.agents.mdp.StochasticMdpAgent`:  Standard stochastic MDP agent. 
* `--gamma 1.0`:  Do not discount.

### Environment
* `--environment rlai.environments.openai_gym.Gym`:  Environment class.
* `--gym-id LunarLanderContinuous-v2`:  OpenAI Gym environment identifier.
* `--render-every-nth-episode 100`:  Render a video every 100 episodes.
* `--video-directory ~/Desktop/lunarlander_continuous_videos`:  Where to store rendered videos.
* `--force`:  Overwrite videos in the video directory.
* `--plot-environment`:  Show a real-time plot of state and reward values.
* `--T 500`:  Limit episodes to 500 steps.

### Training Function and Episodes
* `--train-function rlai.policy_gradient.monte_carlo.reinforce.improve`:  Run the REINFORCE policy gradient optimization
algorithm.
* `--num-episodes 50000`:  Run 50000 episodes.

### Baseline State-Value Estimator
* `--plot-state-value`:  Show a real-time plot of the estimated baseline state value.
* `--v-S rlai.v_S.function_approximation.estimators.ApproximateStateValueEstimator`:  Baseline state-value estimator.  
* `--feature-extractor rlai.environments.openai_gym.ContinuousLunarLanderFeatureExtractor`:  Feature extractor for the
baseline state-value estimator.
* `--function-approximation-model rlai.models.sklearn.SKLearnSGD`:  Use SKLearn's SGD for the baseline state-value 
estimator.
* `--loss squared_loss`:  Use a squared loss within the baseline state-value estimator.
* `--sgd-alpha 0.0`:  Do not use regularization.
* `--learning-rate constant`:  Use a constant learning rate schedule.
* `--eta0 0.0001`:  Learning rate.

### Policy
* `--policy rlai.policies.parameterized.continuous_action.ContinuousActionBetaDistributionPolicy`:  Use the beta
distribution to model the action-density distribution within the policy.
* `--policy-feature-extractor rlai.environments.openai_gym.ContinuousLunarLanderFeatureExtractor`:  Feature extractor
for the policy gradient optimizer.
* `--plot-policy`:  Show a real-time display of the action that is selected at each step.
* `--alpha 0.0001`:  Learning rate for policy gradient updates.
* `--update-upon-every-visit True`:  Update the policy's action-density distribution every time a state is encountered
  (as opposed to the first visit only).

### Output
* `--save-agent-path ~/Desktop/continuous_lunarlander_agent.pickle`:  Where to save the final agent.

# Results

The following video shows the final agent after 50000 training episodes:

{% include youtubePlayer.html id="5n27V-ACLPg" %}
