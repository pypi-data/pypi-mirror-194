import numpy as np

from PyFlyt.core import Aviary

# the starting position and orientations
start_pos = np.array([[0.0, 200.0, 10.0]])
start_orn = np.array([[0.0, 0.0, 0.0]])

# environment setup
env = Aviary(
    start_pos=start_pos,
    start_orn=start_orn,
    render=True,
    drone_type="rocket",
    drone_model="rocket",
    use_camera=True,
)

# set to position control
env.set_mode(0)

env.drones[0].get_joint_info()

# simulate for 1000 steps (1000/120 ~= 8 seconds)
i = 0
while True:
    i += 1
    # print("----------------------------------------------------")
    # print(f"Fuel remaining: {env.drones[0].boosters.ratio_fuel_remaining}")
    # print(f"Throttle setting: {env.drones[0].boosters.throttle_setting}")
    # print(f"Ignition state: {env.drones[0].boosters.ignition_state}")
    # print(f"Fuel mass: {env.getDynamicsInfo(env.drones[0].Id, 0)[0]}")
    # print(f"Fuel inertia: {env.getDynamicsInfo(env.drones[0].Id, 0)[2]}")
    print(f"Rocket velocity: {env.drones[0].state[2]}")
    # print(f"Rocket position: {env.drones[0].state[3]}")

    # force_x, force_z, roll, ignition, thrust_setting, booster_gimbal_1, booster_gimbal_2
    env.drones[0].setpoint = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    env.step()
