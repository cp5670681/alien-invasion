import sys
import random
from time import sleep
import pygame
from bullet import Bullet, BossBullet
from alien import Alien, Boss
from food import Food
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        ship.fire_status = True
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        ship.fire_status = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, foods, bosss,
                 bullets, bullet_type):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, foods, bosss, bullets, mouse_x, mouse_y, bullet_type)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, foods, bosss, bullets, mouse_x, mouse_y, bullet_type):
    """在玩家单击Play按钮时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        ai_settings.initialize_dynamic_settings2()
        bullet_type.type = 0
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        foods.empty()
        bosss.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bosss, bullets,
                  boss_bullets, foods, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for boss_bullet in boss_bullets.sprites():
        boss_bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    foods.draw(screen)
    bosss.draw(screen)
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bosss, bullets, boss_bullets, foods, bullet_type):
    """更新子弹的位置，并删除已消失的子弹"""
    # 产生新子弹，设置子弹发射间隔
    if ship.fire_status:
        ai_settings.fire_now_number = (ai_settings.fire_now_number + 1) % ai_settings.fire_interval
        if ai_settings.fire_now_number == 1:
            fire_bullet(ai_settings, screen, ship, bullets, bullet_type)
    else:
        ai_settings.fire_now_number = 0
    # boss子弹
    for boss in bosss:
        if boss.blood % 10 == 0:
            for i in range(8):
                boss_fire(ai_settings, screen, boss, boss_bullets, -50 + 13 * i + 0.5 * (boss.blood % 20))
            boss.blood = boss.blood - 1
    # 中了boss子弹
    if pygame.sprite.spritecollideany(ship, boss_bullets):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets)

    # 更新子弹的位置
    bullets.update()
    boss_bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for boss_bullet in boss_bullets.copy():
        if boss_bullet.rect.top >= ai_settings.screen_height:
            boss_bullets.remove(boss_bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bosss, bullets, foods)

def boss_fire(ai_settings, screen, boss, boss_bullets, angle):
    new_boss_bullet = BossBullet(ai_settings, screen, boss, angle)
    boss_bullets.add(new_boss_bullet)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bosss, bullets, foods):
    """响应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    #子弹和boss碰撞
    collisions_boss = pygame.sprite.groupcollide(bullets, bosss, True, False)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    # boss处理
    if collisions_boss:
        for boss_list in collisions_boss.values():
            for boss in boss_list:
                boss.blood = boss.blood - 1
                if boss.blood == 0:
                    stats.score += stats.level * 100
                    sb. prep_score()
                    check_high_score(stats, sb)
                    bosss.remove(boss)
    if len(aliens) == 0 and len(bosss) == 0:
        # 删除现有的子弹并新建一群外星人，提高等级
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        appear_bosss(ai_settings, screen, bosss, blood = 10 * stats.level)
        appear_food(ai_settings, screen, foods)
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets, bullet_type):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        if bullet_type.type == 1:
            left_bullet = Bullet(ai_settings, screen, ship, -30)
            bullets.add(left_bullet)
            right_bullet = Bullet(ai_settings, screen, ship, 30)
            bullets.add(right_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def get_number_alien_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        # 更新记分牌
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        boss_bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        # 高分存文件
        with open("high_score",'w') as f:
            f.write(str(stats.high_score))
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, boss_bullets)
            break

def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def update_foods(ai_settings, ship, foods, bullet_type):
    height = ai_settings.screen_height
    for food in foods.copy():
        food.check_edges()
        if food.rect.bottom >= height:  # 删除消失的食物
            foods.remove(food)
    get_food = pygame.sprite.spritecollideany(ship, foods)
    if get_food:  # 吃到食物
        eat_food(get_food.food_str, bullet_type)
        foods.remove(get_food)
    foods.update()


def appear_food(ai_settings, screen, foods): #产生食物
    bullet_list = ['T','L','C','S']
    type = random.choice(bullet_list)
    new_food = Food(ai_settings, screen, type)
    foods.add(new_food)

def eat_food(food_str, bullet_type): #吃到食物
    bullet_type.initialize()
    if food_str == 'T':
        bullet_type.thick_bullet()
    elif food_str == 'L':
        bullet_type.laser_bullet()
    elif food_str == 'C':
        bullet_type.continuous_bullet()
    elif food_str == 'S':
        bullet_type.scatter_bullet()

def update_bosss():
    pass

def appear_bosss(ai_settings, screen, bosss, blood):
    # 产生boss
    new_boss = Boss(ai_settings, screen, blood)
    bosss.add(new_boss)