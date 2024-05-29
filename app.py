import os

from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np

from custom_part import CustomPart
from object import Object, Wall
from simulation import run_simulation

app = Flask(__name__)
# 環境変数からシークレットキーを取得
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')


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
        "decay": 0.99
    }
    default_object = Object(1.5, 0.5, 0.98, 1.0, 15.0)
    if 'object1' in session:
        try:
            object1 = Object(**session['object1'])
        except TypeError:
            object1 = default_object
    else:
        object1 = default_object
    session['object1'] = object1.map()
    object2 = Object(1.0, 0.5, 0.98, 1.0, 10.0)
    scale = 50  # 位置のスケーリングファクター（ピクセル変換用）
    winner = None

    walls = []
    walls.append(Wall(np.array([5, 0]), np.array([0, 1])))
    walls.append(Wall(np.array([0, 5]), np.array([1, 0])))
    walls.append(Wall(np.array([5, 10]), np.array([0, -1])))
    walls.append(Wall(np.array([10, 5]), np.array([-1, 0])))

    if request.method == 'POST':
        show_simulation = True
        # フォームからデータを取得し、initial_conditionsを更新
        for key in initial_conditions:
            if key in request.form:
                initial_conditions[key] = float(request.form[key])

        # シミュレーションの実行
        positions1, positions2, stop_time1, stop_time2, collision_points = run_simulation(
            object1, object2,
            np.array([initial_conditions["pos1_x"], initial_conditions["pos1_y"]]),
            np.array([initial_conditions["pos2_x"], initial_conditions["pos2_y"]]),
            np.array([initial_conditions["vel1_x"], initial_conditions["vel1_y"]]),
            np.array([initial_conditions["vel2_x"], initial_conditions["vel2_y"]]),
            initial_conditions["simulation_time"], initial_conditions["time_step"],
            initial_conditions["decay"],
            walls
        )

        if stop_time1 is None and stop_time2 is None or stop_time1 == stop_time2:
            winner = None
        elif stop_time1 is not None and (stop_time2 is None or stop_time1 < stop_time2):
            winner = 2
        elif stop_time2 is not None and (stop_time1 is None or stop_time2 < stop_time1):
            winner = 1

        # アニメーションのキーフレームを生成
        def generate_keyframes(positions, duration, scale, radius):
            keyframes = ""
            num_positions = len(positions)
            for i, pos in enumerate(positions):
                # 各キーフレームの時間を計算
                time = (i / (num_positions - 1)) * duration
                percentage = (time / duration) * 100
                keyframes += f"{percentage:.2f}% {{ left: {(pos[0] - radius) * scale}px; top: {(pos[1] - radius) * scale}px; }}\n"
            keyframes += f"100% {{ left: {(positions[-1][0] - radius) * scale}px; top: {(positions[-1][1] - radius) * scale}px; }}"
            return keyframes

        duration = max(stop_time1, stop_time2) if stop_time1 and stop_time2 else \
        initial_conditions["simulation_time"]
        frames1 = generate_keyframes(positions1, duration, scale, object1.radius)
        frames2 = generate_keyframes(positions2, duration, scale, object2.radius)

        return render_template('simulation.html',
                               show_simulation=show_simulation,
                               frames1=frames1,
                               frames2=frames2,
                               collision_points=collision_points,
                               duration=duration,
                               scale=scale,
                               object1=object1.map(),
                               object2=object2.map(),
                               diameter1=object1.radius*2*scale,
                               diameter2=object2.radius*2*scale,
                               winner=winner,
                               loser_stop_time = min(stop_time1 or duration, stop_time2 or duration),
                               initial_conditions=initial_conditions,
                               walls = walls
        )

    return render_template('simulation.html',
                           show_simulation=show_simulation,
                           diameter1=object1.radius*2*scale,
                           diameter2=object2.radius*2*scale,
                           scale=scale,
                           object1=object1.map(),
                           object2=object2.map(),
                           initial_conditions=initial_conditions,
                           walls = walls
    )


# 報酬選択画面
@app.route('/reward', methods=['GET', 'POST'])
def reward():
    # 一旦決め打ち。いずれファイルかDBから読み込む
    custom_parts = {
        1: CustomPart("Gravity Negator", "Half the mass.",
                      mass_value=0.5, mass_calculation='multiple'),
        2: CustomPart("Giant Growth", "Double the diameter.",
                      radius_value=2.0, radius_calculation='multiple'),
        3: CustomPart("Overencumbered", "Double the mass.",
                      mass_value=2.0, mass_calculation='multiple'),
        4: CustomPart("Shrink", "Half the diameter.",
                      radius_value=0.5, radius_calculation='multiple'),
        5: CustomPart("Full Steam Ahead", "Improve velocity decay by 10%.",
                      improve_decay_value=0.1),
        6: CustomPart("Rage Reflection", "Increase restitution by 10%. (Maximum 2.0)",
                      restitution_value=0.1, restitution_calculation='add')
    }
    if 'object1' in session:
        object1 = Object(**session['object1'])
    else:
        # セッションにオブジェクトがない場合は最初に戻る
        return redirect(url_for('home'))

    # GETリクエストの場合、報酬としてカスタムパーツを表示
    if request.method == 'GET':
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
        selected_part = custom_parts[int(data['id'])]
        selected_part.update(object1)
        session['object1'] = object1.map()

        # シミュレーション画面にリダイレクト
        return redirect(url_for('home'))


@app.route('/restart')
def clear_session():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
