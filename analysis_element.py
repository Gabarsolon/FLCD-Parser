class AnalysisElement:
    def __init__(self, production, prefix_position):
        self.production = production
        self.prefix_position = prefix_position

    def __eq__(self, other):
        return self.production == other.production and self.prefix_position == other.prefix_position

    def __repr__(self) -> str:
        return str(self.production) + " prefix position: " + str(self.prefix_position)
