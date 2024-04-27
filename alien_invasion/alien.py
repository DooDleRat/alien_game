import pygame
from pygame.sprite import Sprite

class Alien(Sprite):  # 表示外星人的类
    def __init__(self, ai_game):
        # 初始化外星人并设置其起始位置
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')  # 加载外星人图像
        self.rect = self.image.get_rect()  # 设置其rect（矩形）属性
        # Python在处理图像时，我们使用 get_rect() 函数来获取属性rect，即便游戏元素的形状并不是矩形。

        self.rect.x = self.rect.width  # 每个外星人的初始位置都在屏幕的左上方
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)  # 存储外星人的精确水平位置

    def check_edges(self):
        # 检查外星人是否撞到了边缘，如果撞到了边缘就返回True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # 向左或向右移动外星人
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
