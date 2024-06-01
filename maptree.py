import random
from collections import defaultdict


class MapTree:
    class Node:
        def __init__(self, node_id, arrows_to_next=[]):
            self.node_id = node_id
            self.arrows_to_next = arrows_to_next

        def set_arrows_to_next(self, arrows_to_next):
            self.arrows_to_next = arrows_to_next

    def __init__(self, current_node_id, tree):
        self.tree = tree
        self.current_node_id = current_node_id

    def goto(self, next_node_id):
        # 次のノードに移動
        self.current_node_id = next_node_id

    def map(self):
        # シリアライズ可能な形式に変換
        return {
            'tree': {step: [{
                'node_id': node.node_id,
                'arrows_to_next': node.arrows_to_next
            } for node in nodes] for step, nodes in self.tree.items()},
            'current_node_id': self.current_node_id
        }

    # ランダムマップを生成するファクトリ関数
    @staticmethod
    def create_map_tree():
        success = False
        tree = defaultdict(list)
        while not success:
            tree.clear()
            success = True
            # スタートとゴール
            tree[0] = [MapTree.Node(2, ["left", "straight", "right"])]
            tree[9] = [MapTree.Node(92, [])]

            # スタート直後とゴール手前のステップには3つのノードを配置
            tree[1] = [MapTree.Node(11, []),  # 後で接続を設定
                       MapTree.Node(12, []),
                       MapTree.Node(13, [])]
            tree[8] = [MapTree.Node(81, ["right"]),
                       MapTree.Node(82, ["straight"]),
                       MapTree.Node(83, ["left"])]

            # それ以外のステップについて、次のステップのノードへのルートをランダムに決定
            for i in range(1, 8):
                already_appended = set()
                # 一つ左のnodeが右下に進んだ場合は左下には進めないので、それを判定するフラグ
                cant_go_left = False
                for node in sorted(tree[i], key=lambda x: x.node_id):
                    if node.node_id % 10 == 0:
                        # 一番左（mod10=0）のnodeは真下か右下にしか行けない
                        if i == 7:
                            arrows_to_next = ["right"]
                        else:
                            num_to_choose = random.choice([1, 1, 2])
                            arrows_to_next = random.sample(["straight", "right"], num_to_choose)
                    elif node.node_id % 10 == 4:
                        # 一番右（mod10=4）のnodeは真下か左下にしか行けない
                        if i == 7:
                            arrows_to_next = ["left"]
                        elif cant_go_left:
                            arrows_to_next = ["straight"]
                        else:
                            num_to_choose = random.choice([1, 1, 2])
                            arrows_to_next = random.sample(["left", "straight"], num_to_choose)
                    else:
                        # それ以外のnodeは真下か左下か右下に行ける
                        if cant_go_left:
                            num_to_choose = random.choice([1, 1, 2])
                            arrows_to_next = random.sample(["straight", "right"], num_to_choose)
                        else:
                            num_to_choose = random.choice([1, 1, 1, 2, 2, 2, 3])
                            arrows_to_next = random.sample(["left", "straight", "right"], num_to_choose)

                        # 下から2番目のステップだけ、次のステップのノードへのルートを制限
                        if i == 7:
                            if node.node_id % 10 == 1:
                                arrows_to_next = [arrow for arrow in arrows_to_next if arrow != "left"]
                                if not arrows_to_next:
                                    arrows_to_next = ["straight"]
                            elif node.node_id % 10 == 3:
                                arrows_to_next = [arrow for arrow in arrows_to_next if arrow != "right"]
                                if not arrows_to_next:
                                    arrows_to_next = ["straight"]
                            elif node.node_id % 10 == 4:
                                # 一番右（mod10=4）のnodeが存在するとき、そこからは必ず左下に来ているので、右下には進めない
                                if (i*10+4) in set([node.node_id for node in tree[i]]):
                                    arrows_to_next = [arrow for arrow in arrows_to_next if arrow != "right"]
                                    if not arrows_to_next:
                                        arrows_to_next = ["straight"]

                    node.set_arrows_to_next(arrows_to_next)
                    if i != 7:
                        if "left" in arrows_to_next and node.node_id+9 not in already_appended:
                            tree[i+1].extend([MapTree.Node(node.node_id+9)])
                            already_appended.add(node.node_id+9)
                        if "straight" in arrows_to_next and node.node_id+10 not in already_appended:
                            tree[i+1].extend([MapTree.Node(node.node_id+10)])
                            already_appended.add(node.node_id+10)
                        if "right" in arrows_to_next and node.node_id+11 not in already_appended:
                            tree[i+1].extend([MapTree.Node(node.node_id+11)])
                            already_appended.add(node.node_id+11)
                    if "right" in arrows_to_next:
                        cant_go_left = True

            node_70 = [node for node in tree[i] if node.node_id % 10 == 0]
            node_71 = [node for node in tree[i] if node.node_id % 10 == 1]
            node_72 = [node for node in tree[i] if node.node_id % 10 == 2]
            node_73 = [node for node in tree[i] if node.node_id % 10 == 3]
            node_74 = [node for node in tree[i] if node.node_id % 10 == 4]
            # node 81に到達するnodeがない
            if not node_70 and \
               (not node_71 or node_71 and "straight" not in node_71[0].arrows_to_next) and \
               (not node_72 or node_72 and "left" not in node_72[0].arrows_to_next):
                success = False
            # node 82に到達するnodeがない
            elif (not node_71 or node_71 and "right" not in node_71[0].arrows_to_next) and \
                 (not node_72 or node_72 and "straight" not in node_72[0].arrows_to_next) and \
                 (not node_73 or node_73 and "right" not in node_73[0].arrows_to_next):
                success = False
            # node 83に到達するnodeがない
            elif (not node_72 or node_72 and "right" not in node_72[0].arrows_to_next) and \
                 (not node_73 or node_73 and "straight" not in node_73[0].arrows_to_next) and \
                 not node_74:
                success = False

        return MapTree(2, tree)
