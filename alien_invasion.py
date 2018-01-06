import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import bullet
from bullet_type import BulletType
import game_functions as gf

def run_game():
    # 初始化游戏并创建一个屏幕对象 
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建子弹类型
    bullet_type = BulletType(ai_settings)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    boss_bullets = Group()
    # 外星人编组
    aliens = Group()
    bosss = Group()
    # 食物编组
    foods = Group()
    # 设置背景色
    bg_color = (230, 230, 230)
    # 创建一群外星人
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 开始游戏的主循环 
    while True:
    # 监视键盘和鼠标事件 
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, foods, bosss, bullets, bullet_type)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bosss,
                              bullets, boss_bullets, foods, bullet_type)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets)
            gf.update_foods(ai_settings, ship, foods, bullet_type)
            gf.update_bosss()
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bosss,
                         bullets, boss_bullets, foods, play_button)
        #bullet_type.continuous_bullet()
run_game()
