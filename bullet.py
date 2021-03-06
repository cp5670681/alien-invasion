import pygame
from pygame.sprite import Sprite
import math

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    
    def __init__(self, ai_settings, screen, ship, angle = 0):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置 
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        #存储用小数表示的子弹位置 
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        self.angle = angle
    
    def update(self):
        """向上移动子弹"""
        #更新表示子弹位置的小数值
        self.y -= self.speed_factor
        angle = self.angle / 180 * math.pi # 化弧度
        self.x += math.tan(angle) * self.speed_factor
        #更新表示子弹的rect的位置
        self.rect.y = self.y
        self.rect.x = self.x
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class BossBullet(Sprite):
    """一个对boss发射的子弹进行管理的类"""

    def __init__(self, ai_settings, screen, boss, angle=0):
        """在飞船所处的位置创建一个boss子弹对象"""
        super().__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示boss子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, 3, 3)
        self.rect.centerx = boss.rect.centerx
        self.rect.bottom = boss.rect.bottom
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.boss_bullet_speed
        self.angle = angle

    def update(self):
        """向下移动子弹"""
        # 更新表示子弹位置的小数值
        self.y += self.speed_factor
        angle = self.angle / 180 * math.pi  # 化弧度
        self.x += math.tan(angle) * self.speed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)