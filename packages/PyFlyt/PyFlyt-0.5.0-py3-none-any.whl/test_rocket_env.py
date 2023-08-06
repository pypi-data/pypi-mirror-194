from pprint import pprint

import gymnasium
import numpy as np

import PyFlyt.gym_envs
from PyFlyt.core.abstractions.pid import PID

env = gymnasium.make("PyFlyt/Rocket-Landing-v0", render_mode="human")

pid_inner = PID(50.0, 0.0, 0.0, 1.0, (1 / 40))

pid_inner.reset()
obs, info = env.reset()

term, trunc = False, False
# while not term and not trunc:
while True:
    action = np.zeros((7,))
    vel_targ = -2 * (2.71828 ** (0.1 * (obs[12] - 40))) + 0.037
    action[4] = np.clip(pid_inner.step(obs[8], vel_targ), 0, 1)
    action[3] = float(action[4] > 0.0)

    # print(action[0])

    obs, rew, term, trunc, info = env.step(action)
    print(action[4], obs[12], obs[8])
    # print(
    #     np.linalg.norm(env.previous_lin_vel), obs[8]
    # )

    if info["fatal_collision"]:
        print("Dead")
        exit()

    if info["env_complete"]:
        print("Wooh")
        exit()

    if trunc:
        print("Too sloww")
        exit()
