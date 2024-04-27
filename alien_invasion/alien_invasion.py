import sys  # 当玩家需要退出时需要用到的功能
import pygame  # 开发游戏时所需要用到的功能
from time import sleep

from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:  # 管理游戏资源和行为的类（整个程序的核心部分）
    def __init__(self):  # 初始化游戏并创建游戏资源
        pygame.init()  # 初始化背景设置
        self.settings = Settings()  # 设置背景色，外星人、飞船、子弹的移动速度等参数
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # 设置长和宽
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        '''将界面设置为全屏模式'''

        pygame.display.set_caption("Alien Invasion")  # 设置标题
        self.stats = GameStats(self)  # 创建一个用于存储游戏统计信息的实例
        self.sb = Scoreboard(self)
        self.ship = Ship(self)  # 初始化飞船变量
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self):  # 游戏开始的主循环
        while True:
            self._check_events()  # 检测游戏行为，并决定继续或者退出

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()  # 删除消失的子弹
                self._update_aliens()

            self._update_screen()  # 更新屏幕上的图像

    def _check_events(self):  # 响应按键和事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_botton(mouse_pos)

    def _check_play_botton(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  # 在玩家单击Play按钮时开始游戏
            self.settings.initialize_dynamic_settings()  # 重置游戏设置
            self.stats.reset_stats()
            self.stats.game_active = True  # 重置游戏统计信息
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # 清空剩余的子弹和外星人
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人并让飞船位于底部中央
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)  # 隐藏鼠标光标

    def _check_keydown_events(self, event):  # 响应按键
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):  # 响应松开
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # 创建一颗子弹，并将其加入编组bullets中
        if len(self.bullets) < self.settings.bullets_allowed:  # 限制每次连续可发射三颗子弹
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # 更新子弹的位置并删除消失的子弹
        self.bullets.update()
        # 删除消失在屏幕上方的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # 检查是否有子弹击中了外星人，如果是，则删除相应的子弹和外星人
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        # 删除现有的所有子弹，并创建一群新的外星人
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1  # 提高等级
            self.sb.prep_level()

    def _create_fleet(self):
        alien = Alien(self)  # 创建一个新的外星人
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)  # 确定一行可容纳多少个外星人
        number_aliens_x = available_space_x // (2 * alien_width)  # 每行外星人的数量

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)  # 确定每一列可容纳多少个外星人
        number_rows = available_space_y // (2 * alien_height)  # 每列外星人的数量

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)  # 创建外星人群


    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人，并将其放在当前行
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # 更新外星人群中所有外星人的位置并更新外星人群的整体位置
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()  # 检查是否有外星人到了屏幕底端

    def _ship_hit(self):  # 响应飞船被外星人撞到
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空剩余的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底部中央位置
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)  # 暂停

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):  # 检查外星人是否到了屏幕底端
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()  # 和飞船被撞到一样处理
                break

    def _check_fleet_edges(self):  # 检查是否撞到边缘，如果有就改变移动方向
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # 将外星人群整体向下移动，并在撞到边缘时改变移动方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()  # 显示得分图像
        if not self.stats.game_active:  # 如果处于非激活状态，则绘制Play按钮
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    '''创建游戏实例并运行'''
    ai = AlienInvasion()
    ai.run_game()