from flask import Flask, render_template, request
import numpy as np
from simulation import run_simulation

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    # 初期状態では描画しない
    show_simulation = False

    # 初期条件の設定
    initial_conditions = {
        "mass1": 1.0,
        "mass2": 1.0,
        "pos1_x": 0.0,
        "pos1_y": 0.0,
        "pos2_x": 5.0,
        "pos2_y": 5.0,
        "vel1_x": 0.0,
        "vel1_y": 0.0,
        "vel2_x": 3.0,
        "vel2_y": 4.0,
        "radius1": 0.5,
        "radius2": 0.5,
        "simulation_time": 60.0,
        "time_step": 0.1,
        "decay": 0.97
    }
    winner = None

    if request.method == 'POST':
        show_simulation = True
        # フォームからデータを取得し、initial_conditionsを更新
        for key in initial_conditions:
            if key in request.form:
                initial_conditions[key] = float(request.form[key])

        # シミュレーションの実行
        positions1, positions2, stop_time1, stop_time2, collision_points = run_simulation(
            initial_conditions["mass1"], initial_conditions["mass2"],
            np.array([initial_conditions["pos1_x"], initial_conditions["pos1_y"]]),
            np.array([initial_conditions["pos2_x"], initial_conditions["pos2_y"]]),
            np.array([initial_conditions["vel1_x"], initial_conditions["vel1_y"]]),
            np.array([initial_conditions["vel2_x"], initial_conditions["vel2_y"]]),
            initial_conditions["radius1"], initial_conditions["radius2"],
            initial_conditions["simulation_time"], initial_conditions["time_step"],
            initial_conditions["decay"])

        if stop_time1 is None and stop_time2 is None or stop_time1 == stop_time2:
            winner = "Draw"
        elif stop_time1 is not None and (stop_time2 is None or stop_time1 < stop_time2):
            winner = "Object 2 Win!"
        elif stop_time2 is not None and (stop_time1 is None or stop_time2 < stop_time1):
            winner = "Object 1 Win!"

        # アニメーションのキーフレームを生成
        def generate_keyframes(positions, duration, scale):
            keyframes = ""
            num_positions = len(positions)
            for i, pos in enumerate(positions):
                # 各キーフレームの時間を計算
                time = (i / (num_positions - 1)) * duration
                percentage = (time / duration) * 100
                keyframes += f"{percentage:.2f}% {{ left: {pos[0]*scale}px; top: {pos[1]*scale}px; }}\n"
            keyframes += f"100% {{ left: {positions[-1][0]*scale}px; top: {positions[-1][1]*scale}px; }}"
            return keyframes

        scale = 50  # 位置のスケーリングファクター（ピクセル変換用）
        duration = max(stop_time1, stop_time2) if stop_time1 and stop_time2 else initial_conditions["simulation_time"]
        frames1 = generate_keyframes(positions1, duration, scale)
        frames2 = generate_keyframes(positions2, duration, scale)

        return render_template('simulation.html',
                               show_simulation=show_simulation,
                               frames1=frames1,
                               frames2=frames2,
                               collision_points = collision_points,
                               duration=duration,
                               scale=scale,
                               diameter1=initial_conditions["radius1"]*2*scale,
                               diameter2=initial_conditions["radius1"]*2*scale,
                               winner=winner,
                               initial_conditions=initial_conditions)

    return render_template('simulation.html',
                           show_simulation=show_simulation,
                           initial_conditions=initial_conditions)


if __name__ == '__main__':
    app.run(debug=True)