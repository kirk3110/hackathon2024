from flask import Flask, render_template, request, redirect, url_for
import numpy as np

from custom_part import CustomPart
from object import Object
from simulation import run_simulation

app = Flask(__name__)

object1 = Object(1.0, 0.5)


@app.route('/', methods=['GET', 'POST'])
def home():
    # 初期状態では描画しない
    show_simulation = False

    # 初期条件の設定
    initial_conditions = {
        "pos1_x": 0.0,
        "pos1_y": 0.0,
        "pos2_x": 5.0,
        "pos2_y": 5.0,
        "vel1_x": 0.0,
        "vel1_y": 0.0,
        "vel2_x": 3.0,
        "vel2_y": 4.0,
        "simulation_time": 60.0,
        "time_step": 0.1,
        "decay": 0.97
    }
    object2 = Object(1.0, 0.5)
    scale = 50  # 位置のスケーリングファクター（ピクセル変換用）
    winner = None

    if request.method == 'POST':
        show_simulation = True
        # フォームからデータを取得し、initial_conditionsを更新
        for key in initial_conditions:
            if key in request.form:
                initial_conditions[key] = float(request.form[key])

        # シミュレーションの実行
        positions1, positions2, stop_time1, stop_time2, collision_points = run_simulation(
            object1.mass, object2.mass,
            np.array([initial_conditions["pos1_x"], initial_conditions["pos1_y"]]),
            np.array([initial_conditions["pos2_x"], initial_conditions["pos2_y"]]),
            np.array([initial_conditions["vel1_x"], initial_conditions["vel1_y"]]),
            np.array([initial_conditions["vel2_x"], initial_conditions["vel2_y"]]),
            object1.radius, object2.radius,
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
                keyframes += f"{percentage:.2f}% {{ left: {pos[0] * scale}px; top: {pos[1] * scale}px; }}\n"
            keyframes += f"100% {{ left: {positions[-1][0] * scale}px; top: {positions[-1][1] * scale}px; }}"
            return keyframes

        duration = max(stop_time1, stop_time2) if stop_time1 and stop_time2 else \
        initial_conditions["simulation_time"]
        frames1 = generate_keyframes(positions1, duration, scale)
        frames2 = generate_keyframes(positions2, duration, scale)

        return render_template('simulation.html',
                               show_simulation=show_simulation,
                               frames1=frames1,
                               frames2=frames2,
                               collision_points=collision_points,
                               duration=duration,
                               scale=scale,
                               diameter1=object1.radius*2*scale,
                               diameter2=object2.radius*2*scale,
                               winner=winner,
                               object1_mass=object1.mass,
                               object2_mass=object2.mass,
                               initial_conditions=initial_conditions)

    return render_template('simulation.html',
                           show_simulation=show_simulation,
                           diameter1=object1.radius*2*scale,
                           diameter2=object2.radius*2*scale,
                           object1_mass=object1.mass,
                           object2_mass=object2.mass,
                           initial_conditions=initial_conditions)


# 報酬選択画面
@app.route('/reward', methods=['GET', 'POST'])
def reward():
    # 一旦決め打ち。いずれファイルかDBから読み込む
    custom_parts = {
        1: CustomPart("Lightning Body", "Halve the mass.",
                      mass_value=0.5, mass_calculation='*'),
        2: CustomPart("Giant Growth", "Double the diameter.",
                      radius_value=2.0, radius_calculation='*'),
        3: CustomPart("Super Lightning Body", "Quarter the mass.",
                      mass_value=0.25, mass_calculation='*'),
        4: CustomPart("Super Giant Growth", "Quadruple the diameter.",
                      radius_value=4.0, radius_calculation='*'),
    }

    # GETリクエストの場合、報酬としてカスタムパーツを表示
    if request.method == 'GET':
        print("get")
        # カスタムパーツリストからランダムに3つ選択
        import random
        selected_parts_keys = random.sample(list(custom_parts.keys()), 3)
        return render_template('reward.html',
                               reward_1_id=selected_parts_keys[0],
                               reward_1_title=custom_parts[selected_parts_keys[0]].title,
                               reward_1_text=custom_parts[selected_parts_keys[0]].text,
                               reward_2_id=selected_parts_keys[1],
                               reward_2_title=custom_parts[selected_parts_keys[1]].title,
                               reward_2_text=custom_parts[selected_parts_keys[1]].text,
                               reward_3_id=selected_parts_keys[2],
                               reward_3_title=custom_parts[selected_parts_keys[2]].title,
                               reward_3_text=custom_parts[selected_parts_keys[2]].text,
                               )

    # POSTリクエストの場合は、選択されたカスタムパーツを適用
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        selected_part = custom_parts[int(data['id'])]
        if 'mass_value' in selected_part.__dict__:
            expression = f"{object1.mass}{selected_part.mass_calculation}{selected_part.mass_value}"
            object1.mass = eval(expression)
        if 'radius_value' in selected_part.__dict__:
            expression = f"{object1.radius}{selected_part.radius_calculation}{selected_part.radius_value}"
            object1.radius = eval(expression)

        # シミュレーション画面にリダイレクト
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
