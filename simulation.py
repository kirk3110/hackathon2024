import numpy as np
import math

def run_simulation(object1, object2, pos1, pos2, vel1, vel2, simulation_time, time_step, decay, walls):
    # シミュレーションの実行
    times = np.arange(0, simulation_time, time_step)
    positions1 = []
    positions2 = []
    rps1_timeline = {}
    rps2_timeline = {}
    stop_time1 = None
    stop_time2 = None
    collision_points = []
    mass1 = object1.mass
    mass2 = object2.mass
    radius1 = object1.radius
    radius2 = object2.radius
    restitution1 = object1.restitution
    restitution2 = object2.restitution
    decay1 = object1.decay
    decay2 = object2.decay
    rps1 = object1.rps
    rps2 = object2.rps

    for t in times:
        positions1.append(pos1.copy())
        positions2.append(pos2.copy())

        pos1 += vel1 * time_step  # 位置の更新
        pos2 += vel2 * time_step

        vel1 = vel1 * decay * decay1  # 摩擦力を速度減衰で再現 共通係数 * 個別係数
        vel2 = vel2 * decay * decay2

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

            # 衝突時に互いのrpsを減衰させる
            # decayが小さいほど減衰率が低くなる
            # radiusに対するmassが重いほど減衰率が低くなる
            rps1 = rps1 * (1 - decay1 * radius1 / mass1)
            rps2 = rps2 * (1 - decay2 * radius2 / mass2)
            rps1_timeline[t] = rps1
            rps2_timeline[t] = rps2

            restitution1 = restitution1 * (rps1 / object1.rps)
            restitution2 = restitution2 * (rps2 / object2.rps)

            # 先にrpsが0になった方が負け
            if rps1 <= 0.03 and stop_time1 is None:
                stop_time1 = t
            if rps2 <= 0.03 and stop_time2 is None:
                stop_time2 = t
            if stop_time1 is not None and stop_time2 is not None:
                break

    return positions1, positions2, rps1_timeline, rps2_timeline, stop_time1, stop_time2, collision_points
