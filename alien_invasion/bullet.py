import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):  # 管理飞船所发射的子弹的类
    def __init__(self, ai_game):
        # 创建一个子弹对象
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 再（0，0）处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed  # 向上移动子弹，更新表示子弹位置的小数值
        self.rect.y = self.y  # 更新表示子弹的rect（矩形）的位置

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)  # 在屏幕上绘制子弹