class Production:
    def __init__(self, left_hand_side, right_hand_side):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    def __eq__(self, other):
        return self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side

    def __repr__(self):
        return str(self.left_hand_side) + "->" + str(self.right_hand_side)
