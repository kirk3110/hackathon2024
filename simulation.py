import numpy as np
import math
from object import Wall

def run_simulation(object1, object2, pos1, pos2, vel1, vel2, simulation_time, time_step, decay):
    # シミュレーションの実行
    times = np.arange(0, simulation_time, time_step)
    positions1 = []
    positions2 = []
    stop_time1 = None
    stop_time2 = None
    collision_points = []
    mass1 = object1.mass
    mass2 = object2.mass
    radius1 = object1.radius
    radius2 = object2.radius
    restitution1 = object1.restitution
    restitution2 = object2.restitution

    walls = []
    walls.append(Wall(np.array([0, 0]), np.array([0, 1])))
    walls.append(Wall(np.array([0, 0]), np.array([1, 0])))
    walls.append(Wall(np.array([10, 10]), np.array([0, -1])))
    walls.append(Wall(np.array([10, 10]), np.array([-1, 0])))

    for t in times:
        positions1.append(pos1.copy())
        positions2.append(pos2.copy())

        pos1 += vel1 * time_step  # 位置の更新
        pos2 += vel2 * time_step

        vel1 = vel1 * decay * object1.decay  # 摩擦力を速度減衰で再現 共通係数 * 個別係数
        vel2 = vel2 * decay * object2.decay

        if stop_time1 is None and np.linalg.norm(vel1) <= 0.3:  # いつまでも微的な動きが続かないように停止判定
            stop_time1 = t
            vel1 = np.array([0, 0])
        if stop_time2 is None and np.linalg.norm(vel2) <= 0.3:
            stop_time2 = t
            vel2 = np.array([0, 0])
        if stop_time1 and stop_time2:
            break

        for wall in walls:
            if wall.detect_collision(radius1, pos1):
                vel1 = wall.reflect(vel1) * restitution1
            if wall.detect_collision(radius2, pos2):
                vel2 = wall.reflect(vel2) * restitution2

        k = 9.81*math.sin(math.radians(10))  #重力加速度(平面方向)
        pos0 = np.array([5.0, 5.0]) #原点座標
        acc1 = k * (pos0 - pos1)  #原点方向の加速度
        vel1 = vel1 + acc1 * time_step #速度更新 
        acc2 = k * (pos0 - pos2) 
        vel2 = vel2 + acc2 * time_step
            
        if np.linalg.norm(pos1 - pos2) <= (radius1 + radius2):  # 衝突判定
            # 完全弾性衝突の速度更新
            v1, v2 = vel1.copy(), vel2.copy()
            vel1 = v1 - 2 * mass2 / (mass1 + mass2) * np.dot(v1 - v2, pos1 - pos2) / np.linalg.norm(pos1 - pos2)**2 * (pos1 - pos2)
            vel2 = v2 - 2 * mass1 / (mass1 + mass2) * np.dot(v2 - v1, pos2 - pos1) / np.linalg.norm(pos2 - pos1)**2 * (pos2 - pos1)
            collision_points.append((t, (pos1 * radius2 + pos2 * radius1) / (radius1 + radius2)))

    return positions1, positions2, stop_time1, stop_time2, collision_points
