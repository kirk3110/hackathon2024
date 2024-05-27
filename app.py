import json
import random
from flask import Flask, render_template, request, jsonify, session
import numpy as np
from simulation import run_simulation
from object import Object, Field

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

simulation_time = 60.0
time_step = 0.1


# プレイヤーキャラクターのパラメータをセッションから取得
def get_player_parameters():
    player_parameters = session.get('player_parameters')
    if player_parameters is not None:
        return Object(player_parameters['mass'], np.array(player_parameters['pos']),
                      player_parameters['angle'], player_parameters['speed'], player_parameters['radius'])
    else:
        return Object(1.0, np.array([2.0, 2.0]), 45, 5.0, 0.5)


# 敵キャラクターのパラメータを事前に設定したパターンから選択
def get_enemy_parameters():
    enemy_patterns = [
        Object(1.5, np.array([5.0, 5.0]), 225, 10.5, 0.5),
        Object(2.0, np.array([7.0, 7.0]), 180, 12.0, 0.6),
        Object(1.2, np.array([6.0, 6.0]), 270, 9.5, 0.4)
    ]
    return random.choice(enemy_patterns)


# 敵キャラクターのパラメータを事前に設定したパターンから選択
def get_field_parameters():
    field_patterns = [
        Field(0.97),
    ]
    return random.choice(field_patterns)


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


@app.route('/', methods=['GET', 'POST'])
def index():
    # 初期状態では描画しない
    show_simulation = False

    field = get_field_parameters()
    winner = None

    player = get_player_parameters()
    enemy = get_enemy_parameters()
    if request.method == 'POST':
        show_simulation = True

        # シミュレーションの実行
        positions1, positions2, stop_time1, stop_time2, collision_points = run_simulation(
            player.mass, enemy.mass
            , player.pos, enemy.pos
            , player.angle, enemy.angle
            , player.speed, enemy.speed
            , player.radius, enemy.radius
            , simulation_time, time_step, field.decay
        )

        if stop_time1 is None and stop_time2 is None or stop_time1 == stop_time2:
            winner = "Draw"
        elif stop_time1 is not None and (stop_time2 is None or stop_time1 < stop_time2):
            winner = "Player Lose..."
        elif stop_time2 is not None and (stop_time1 is None or stop_time2 < stop_time1):
            winner = "Player Win!"

        scale = 50  # 位置のスケーリングファクター（ピクセル変換用）
        duration = max(stop_time1, stop_time2) if stop_time1 and stop_time2 else simulation_time
        frames1 = generate_keyframes(positions1, duration, scale)
        frames2 = generate_keyframes(positions2, duration, scale)

        return render_template('simulation.html',
                               show_simulation=show_simulation,
                               frames1=frames1,
                               frames2=frames2,
                               collision_points = collision_points,
                               duration=duration,
                               scale=scale,
                               player_diameter=player.radius*2*scale,
                               player_speed=player.speed,
                               player_mass=player.mass,
                               enemy_diameter=enemy.radius*2*scale,
                               enemy_speed=enemy.speed,
                               enemy_mass=enemy.mass,
                               winner=winner)

    return render_template('simulation.html',
                           show_simulation=show_simulation)


# プレイヤーキャラクターのパラメータを更新
@app.route('/update_player', methods=['POST'])
def update_player():
    session['player_parameters'] = request.get_json()
    return jsonify({'message': 'Player parameters updated successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)