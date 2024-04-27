class GameStats:
    def __init__(self, ai_game):  # 跟踪游戏的统计信息
        self.settings = ai_game.settings  # 初始化统计信息
        self.reset_stats()
        self.game_active = False  # 程序一开始为非激活状态，需要按下Play按钮才能开始
        self.high_score = 0  # 任何情况下都不应该重置最高得分

    def reset_stats(self):  # 初始化在游戏运行期间可能发生变化的统计信息
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
