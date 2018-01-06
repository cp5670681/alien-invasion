class BulletType:
    def __init__(self, ai_settings):
        self.type = 0
        self.ai_settings = ai_settings

    def thick_bullet(self):
        # 粗子弹
        self.ai_settings.bullet_width = 100


    def laser_bullet(self):
        # 激光弹
        self.ai_settings.bullet_height = self.ai_settings.screen_height
        self.ai_settings.bullet_speed_factor = 100
        self.ai_settings.fire_interval = 20

    def continuous_bullet(self):
        # 冲锋枪
        self.ai_settings.bullets_allowed = 10
        self.ai_settings.bullet_speed_factor = 5

    def scatter_bullet(self):
        # 散弹枪
        self.type = 1
        self.ai_settings.bullets_allowed = 9

    def initialize(self):
        self.ai_settings.initialize_dynamic_settings2()
        self.type = 0