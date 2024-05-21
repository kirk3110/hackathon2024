from flask import Flask, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
  # 初期条件の設定
  mass1 = 1.0  # 物体1の質量
  mass2 = 1.0  # 物体2の質量
  pos1 = np.array([0.0, 0.0])  # 物体1の初期位置 [x, y]
  pos2 = np.array([5.0, 5.0])  # 物体2の初期位置 [x, y]
  vel1 = np.array([2.0, 1.0])  # 物体1の初期速度 [vx, vy]
  vel2 = np.array([-1.0, -1.5])# 物体2の初期速度 [vx, vy]
  radius1 = 0.5  # 物体1の半径
  radius2 = 0.5  # 物体2の半径
  simulation_time = 10.0  # シミュレーション時間
  time_step = 0.1         # シミュレーションの時間刻み
  decay = 0.97 # 速度の減衰係数

  # シミュレーションの実行
  times = np.arange(0, simulation_time, time_step)
  positions1 = []
  positions2 = []

  for t in times:
    positions1.append(pos1.copy())
    positions2.append(pos2.copy())

    pos1 += vel1 * time_step #位置の更新
    pos2 += vel2 * time_step

    vel1 = vel1 * decay #摩擦力を速度減衰で再現
    vel2 = vel2 * decay


    if np.linalg.norm(pos1 - pos2) <= (radius1 + radius2):  # 衝突判定
      # 完全弾性衝突の速度更新
      v1, v2 = vel1.copy(), vel2.copy()
      vel1 = v1 - 2 * mass2 / (mass1 + mass2) * np.dot(v1 - v2, pos1 - pos2) / np.linalg.norm(pos1 - pos2)**2 * (pos1 - pos2)
      vel2 = v2 - 2 * mass1 / (mass1 + mass2) * np.dot(v2 - v1, pos2 - pos1) / np.linalg.norm(pos2 - pos1)**2 * (pos2 - pos1)

  # アニメーションのキーフレームを生成
  def generate_keyframes(positions, duration, scale):
    keyframes = ""
    for i, pos in enumerate(positions):
      percentage = (i / (len(positions) - 1)) * 100
      keyframes += f"{percentage:.2f}% {{ left: {pos[0]*scale}px; top: {pos[1]*scale}px; }}\n"
    return keyframes

  scale = 50  # 位置のスケーリングファクター（ピクセル変換用）
  frames1 = generate_keyframes(positions1, simulation_time, scale)
  frames2 = generate_keyframes(positions2, simulation_time, scale)

  return render_template('simulation.html',
                         frames1=frames1,
                         frames2=frames2,
                         duration=simulation_time,
                         diameter1=radius1*2*scale,
                         diameter2=radius2*2*scale)

if __name__ == '__main__':
  app.run(debug=True)
