import pygame

from pygame.sprite import Sprite

class Ship(Sprite):  # 管理飞船的类
    def __init__(self, ai_game):

        """ 初始化飞船并设置其初始位置 """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')  # 获取加载飞船的图像并获取飞船的外接矩形
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom  # 对于每个新的飞船都放在底部的中央位置

        self.x = float(self.rect.x)  # 在飞船的属性x中存储小数值
        self.moving_right = False
        self.moving_left = False  # 移动标志

        super().__init__()

    def update(self):  # 根据移动标志调整飞船的位置
        # 更新飞船而不是rect对象的x值，限制飞船的活动范围
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 根据self.x更新rect对象
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)  # 在指定位置绘制飞船

    def center_ship(self):  # 将飞船放在底部中央
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
