import random
import pygame
from pygame.sprite import Sprite

class Food(Sprite):
    """表示单个食物的类"""

    def __init__(self, ai_settings, screen, food_str):
        """初始化食物并设置其起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.food_str = food_str
        # 设置字体
        self.text_color = (255, 30, 30)
        self.font = pygame.font.SysFont(None, 35)
        self.bg_color = (30, 255, 30)
        # 加载食物图像，并设置其rect属性
        self.image = self.font.render(self.food_str, True, self.text_color,
                                            self.bg_color)
        self.rect = self.image.get_rect()
        # 每个食物最初都在屏幕左上角附近
        self.rect.x = random.randint(0,self.ai_settings.screen_width)
        self.rect.y = self.rect.height
        # 存储食物的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 运动方向
        self.direction = 1

    def blitme(self):
        """在指定位置绘制食物"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """如果食物位于屏幕边缘，就调整方向"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            self.direction = self.direction * -1
        elif self.rect.left <= 0:
            self.direction = self.direction * -1

    def update(self):
        """向左或向右移动食物"""
        self.x += self.ai_settings.food_speed_x * self.direction
        self.y += self.ai_settings.food_speed_y
        self.rect.x = self.x
        self.rect.y = self.y