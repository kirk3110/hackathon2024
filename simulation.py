import numpy as np

def run_simulation(mass1, mass2, pos1, pos2, angle1, angle2, speed1, speed2, radius1, radius2, simulation_time, time_step, decay):
    # シミュレーションの実行
    times = np.arange(0, simulation_time, time_step)
    positions1 = []
    positions2 = []

    vel1 = calculate_velocity(angle1, speed1)
    vel2 = calculate_velocity(angle2, speed2)

    for t in times:
        positions1.append(pos1.copy())
        positions2.append(pos2.copy())

        pos1 += vel1 * time_step  # 位置の更新
        pos2 += vel2 * time_step

        vel1 = vel1 * decay  # 摩擦力を速度減衰で再現
        vel2 = vel2 * decay

        if np.linalg.norm(vel1) <= 0.3:  # いつまでも微的な動きが続かないように停止判定
            vel1 = np.array([0, 0])
        if np.linalg.norm(vel2) <= 0.3:
            vel2 = np.array([0, 0])

        if np.linalg.norm(pos1 - pos2) <= (radius1 + radius2):  # 衝突判定
            # 完全弾性衝突の速度更新
            v1, v2 = vel1.copy(), vel2.copy()
            vel1 = v1 - 2 * mass2 / (mass1 + mass2) * np.dot(v1 - v2, pos1 - pos2) / np.linalg.norm(pos1 - pos2)**2 * (pos1 - pos2)
            vel2 = v2 - 2 * mass1 / (mass1 + mass2) * np.dot(v2 - v1, pos2 - pos1) / np.linalg.norm(pos2 - pos1)**2 * (pos2 - pos1)

    return positions1, positions2


def calculate_velocity(angle, speed):
    # 角度をラジアンに変換
    angle_rad = np.radians(angle)
    # 速度ベクトルを計算
    vx = speed * np.cos(angle_rad)
    vy = speed * np.sin(angle_rad)
    return np.array([vx, vy])