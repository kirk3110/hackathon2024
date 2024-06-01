import random


class CustomPart:
    def __init__(self, title, text, rarity, **kwargs):
        self.title = title
        self.text = text
        self.rarity = rarity
        self.update_methods = {
            'mass_value': self.update_mass,
            'radius_value': self.update_radius,
            'improve_decay_value': self.update_decay,
            'restitution_value': self.update_restitution,
            'rps_value': self.update_rps,
        }

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update_mass(self, object_):
        if self.mass_calculation == 'multiple':
            object_.mass *= self.mass_value

    def update_radius(self, object_):
        if self.radius_calculation == 'multiple':
            object_.radius *= self.radius_value

    def update_decay(self, object_):
        object_.decay = 1 - (1 - object_.decay) * (1 - self.improve_decay_value)

    def update_restitution(self, object_):
        if self.restitution_calculation == 'multiple':
            object_.restitution = min(2.0, object_.restitution * self.restitution_value)

    def update_rps(self, object_):
        if self.rps_calculation == 'multiple':
            object_.rps = min(40.0, object_.rps * self.rps_value)

    def update(self, object_):
        for attribute, update_method in self.update_methods.items():
            if hasattr(self, attribute):
                update_method(object_)

    @staticmethod
    def get_random_keys(n):
        # レアリティに応じた重みを設定
        weights = {
            'common': 5,
            'rare': 1,
        }

        # パーツのリストとそれぞれの重みを作成
        keys = list(CUSTOM_PARTS_DICT.keys())
        rarities = [part.rarity for part in CUSTOM_PARTS_DICT.values()]
        weights = [weights[rarity] for rarity in rarities]
        # 重複なしでランダムに3つのCustomPartを選択
        selected_keys = random.choices(keys, weights=weights, k=3)
        while len(set(selected_keys)) < 3:  # 重複がないようにチェック
            selected_keys = random.choices(keys, weights=weights, k=3)
        return selected_keys

    @staticmethod
    def get_part_by_id(id_):
        return CUSTOM_PARTS_DICT[id_]


CUSTOM_PARTS_DICT = {
    1: CustomPart("Gravity Negator", "Half the mass.", "common",
                  mass_value=0.5, mass_calculation='multiple'),
    2: CustomPart("Giant Growth", "Double the diameter.", "common",
                  radius_value=2.0, radius_calculation='multiple'),
    3: CustomPart("Overencumbered", "Double the mass.", "rare",
                  mass_value=2.0, mass_calculation='multiple'),
    4: CustomPart("Shrink", "Half the diameter.", "common",
                  radius_value=0.5, radius_calculation='multiple'),
    5: CustomPart("Full Steam Ahead", "Improve velocity decay by 10%.", "common",
                  improve_decay_value=0.1),
    6: CustomPart("Rage Reflection",
                  "Increase restitution by 10%. (Maximum 2.0)",
                  "common",
                  restitution_value=1.1, restitution_calculation='multiple'),
    7: CustomPart("Spin Engine", "Increase rotation speed by 50%. (Maximum 40)", "rare",
                  rps_value=1.5, rps_calculation='multiple'),
}