from flask import Flask, render_template, request
import numpy as np
from simulation import run_simulation

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    # 初期条件の設定
    mass1 = 1.0  # 物体1の質量
    mass2 = 1.0  # 物体2の質量
    pos1 = np.array([0.0, 0.0])    # 物体1の初期位置 [x, y]
    pos2 = np.array([5.0, 5.0])    # 物体2の初期位置 [x, y]
    angle1 = 45   # 物体1の初期角度（度）
    angle2 = 225  # 物体2の初期角度（度）
    speed1 = 2.0  # 物体1の初期速度（大きさ）
    speed2 = 2.5  # 物体2の初期速度（大きさ）
    radius1 = 0.5  # 物体1の半径
    radius2 = 0.5  # 物体2の半径
    simulation_time = 10.0  # シミュレーション時間
    time_step = 0.1         # シミュレーションの時間刻み
    decay = 0.97  # 速度の減衰係数

    if request.method == 'POST':
        # フォームからデータを取得
        mass1 = float(request.form['mass1'])
        mass2 = float(request.form['mass2'])
        pos1 = [float(request.form['pos1_x']), float(request.form['pos1_y'])]
        pos2 = [float(request.form['pos2_x']), float(request.form['pos2_y'])]
        angle1 = float(request.form['angle1'])
        angle2 = float(request.form['angle2'])
        speed1 = float(request.form['speed1'])
        speed2 = float(request.form['speed2'])

    # シミュレーションの実行
    positions1, positions2 = run_simulation(mass1, mass2,
                                            np.array(pos1), np.array(pos2),
                                            angle1, angle2, speed1, speed2,
                                            radius1, radius2,
                                            simulation_time, time_step, decay)

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
