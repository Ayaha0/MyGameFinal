
import pygame
import random
import os
import math
from pygame import Vector2
import pandas as pd
from int_page import *
import pandas as pd


# 常數
WIDTH = 500
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CADMIUM_YELLOW = (253, 218, 13)
RED = (255, 0, 0)


# 初始化內容
pygame.init()
all_sprites = pygame.sprite.Group()  # 所有物件集合
all_player_bullets = pygame.sprite.Group()  # 所有玩家子彈集合
all_enemies = pygame.sprite.Group()  # 所有敵方物件集合
all_enemies_bullets = pygame.sprite.Group()  # 所有敵方子彈集合

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("遊戲名稱")

running = True
show_init = True
stage = 1


# 圖片載入
background_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "background.png")).convert(), (WIDTH, HEIGHT))
player_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "player.png")).convert(), (50, 38))
life_img = pygame.transform.scale(pygame.image.load(
    os.path.join("img", "life.png")).convert(), (30, 30))
life_img.set_colorkey((0, 0, 0))
bullet1_img = pygame.image.load(
    os.path.join("img", "bullet1.png")).convert()


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(你所要載入的所有東西(圖片檔等)，或是其他你想要增加的全域變數)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓

# enemy1_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
#      os.path.join("img", "enemy1.png")).convert(), (30, 30)), 180)

boss_enemy_img=pygame.transform.rotate(pygame.transform.scale(pygame.image.load
                (os.path.join("img", "enemy_boss.png")).convert(), (80,80)),180)
boss_enemy_bullet_imags=[]
for i in range(2,6):
    boss_enemy_bullet_imag=pygame.transform.rotate(pygame.transform.scale(pygame.image.load
                (os.path.join("img", f"boss_enemy_bullet{i}.png")).convert(),(20,20)),0)
    boss_enemy_bullet_imags.append(boss_enemy_bullet_imag)
# boss_enemy_bullet.set_colorkey(WHITE)
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(你所要載入的所有東西(圖片檔等)，或是其他你想要增加的全域變數)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# 音樂載入

# 遊戲中的界面(血量、道具等)


def draw_game_interface(win, player):
    draw_text(win, "血量："+str(player.hp), 25, 70, 30, WHITE)
    for i in range(player.life):
        win.blit(life_img, (WIDTH-50-50*i, 20))


# Player物件


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-50)
        self.bullet_clock = pygame.time.get_ticks()

        # 玩家相關數據
        self.speedx = 5
        self.speedy = 5
        self.life = 3
        self.hp = 1000

        # 自動加入群組
        all_sprites.add(self)

    def shoot(self):
        Bullet(self.rect.centerx, self.rect.top, bullet1_img, 0, -10, 10, self)

    # 玩家碰到敵方戰艦時，要被扣血

    def player_collide_with_enemy(self, enemy):
        now = pygame.time.get_ticks()
        if now-enemy.time_get_hit > 500:
            self.hp -= 50
            enemy.time_get_hit = now

    # 玩家碰到敵方子彈射中時，要被扣血

    def player_collide_with_enemy_bullets(self, bullet):
        self.hp -= bullet.attack

    def update(self):
        # WASD操控
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_w]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_s]:
            self.rect.y += self.speedy

        # 判斷是否出界
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # 判斷空白鍵射擊(有限定兩個子彈間的秒數0.3秒)
        if key_pressed[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.bullet_clock >= 300:
                self.shoot()
                self.bullet_clock = now

        # 判斷玩家是否已經死亡
        if self.hp <= 0 and self.life >= 0:
            self.hp = 100
            self.life -= 1

        if self.life < 0:
            global show_init
            show_init = True

# 敵方單位物件


class Enemy(pygame.sprite.Sprite):
    def __init__(self, img, hp, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.time_get_hit = pygame.time.get_ticks()
        self.bullet_clock = pygame.time.get_ticks()
        # 敵方相關數據
        self.hp = hp

        # 自動加入所屬群組
        all_sprites.add(self)
        all_enemies.add(self)

    # 被子彈射到時，被扣血的函式(不同的子彈有不同的攻擊力)
    def get_hit(self, bullet):
        self.hp -= bullet.attack


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(繼承Enemy之後，寫出你的敵人class)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
# class BasicEnemy(Enemy):
#     def __init__(self, img, hp, x, y):
#         super().__init__(img, hp, x, y)
#         self.ori_x = x
#         self.speedx = 1
#         self.bullet_img = pygame.transform.scale(pygame.image.load(
#             os.path.join("img", "enemy_bullet1.png")).convert(), (15, 20))
#
#     def shoot(self):
#         now = pygame.time.get_ticks()
#         if (now - self.bullet_clock > 200):
#             self.bullet_clock = now
#             Bullet(self.rect.centerx, self.rect.bottom+10,
#                    self.bullet_img, 0, 10, 10, self)
#
#     def update(self):
#         if self.rect.y < 200:
#             self.rect.y += 1
#         elif self.rect.y > 200:
#             self.rect.y = 200
#         elif self.rect.y == 200:
#
#             if self.rect.x < (self.ori_x-100):
#                 self.speedx = 1
#             if self.rect.x > (self.ori_x+100):
#                 self.speedx = -1
#
#             self.rect.x += self.speedx
#             self.shoot()
#
#         if self.hp <= 0:
#             self.kill()

#新增class
class Boss_enemy(Enemy):
    def __init__(self,img,hp,x,y,player):
        super().__init__(img,hp,x,y)
        self.speedx=random.randint(-10,10)
        self.speedy=random.randint(-10,10)
        self.mode_tick=pygame.time.get_ticks()
        self.mode2_points=pd.DataFrame([[100,200]],columns=["x","y"])
        self.move_mode=1
        self.radius=40

        self.set_mode2_movepoint()
        self.move_mode2tick=pygame.time.get_ticks()
        self.mode2_movetopoint=Vector2(self.mode2_points.loc[0]["x"],self.mode2_points.loc[0]["y"])
    def set_mode2_movepoint(self):
        for i in range(2):
            point=[self.mode2_points.loc[i]["x"]+150,self.mode2_points.loc[i]["y"]]
            self.mode2_points.loc[len(self.mode2_points.index)]=point
        for i in range(3):
                point=[self.mode2_points.loc[i]["x"],self.mode2_points.loc[0]["y"]+100]
                self.mode2_points.loc[len(self.mode2_points.index)]=point
        for i in range(3):
                point=[self.mode2_points.loc[i]["x"],self.mode2_points.loc[0]["y"]+200]
                self.mode2_points.loc[len(self.mode2_points.index)]=point




    def move_mode1(self):
        mode_start=pygame.time.get_ticks()
        print(mode_start)
        if self.rect.left<0:
            self.speedx=random.randint(0,10)
            self.speedy=random.randint(-10,10)
            if self.rect.top<0:
                self.speedy=random.randint(0,10)
            if self.rect.bottom>HEIGHT:
                self.speedy=random.randint(-10,0)
        if self.rect.right> WIDTH:
            self.speedx = random.randint(-10, 0)
            self.speedy = random.randint(-10, 10)
            if self.rect.top < 0:
                self.speedy = random.randint(0, 10)
            if self.rect.bottom > HEIGHT:
                self.speedy = random.randint(-10, 0)
        if self.rect.bottom> HEIGHT:
            mode_end = pygame.time.get_ticks()
            print(mode_end)
            self.speedx = random.randint(-10, 10)
            self.speedy = random.randint(-10, 0)
            if self.rect.left < 0:
                self.speedx = random.randint(0, 10)
            if self.rect.right > WIDTH:
                self.speedx = random.randint(-10, 0)
        if self.rect.top < 0:
            self.speedy = random.randint(0,10)
            self.speedx= random.randint(-10,10)
            if self.rect.left<0:
                self.speedx = random.randint(0,10)
            if self.rect.right>HEIGHT:
                self.speedx = random.randint(-10, 0)
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    def rotate_1(self):
        pygame.transform.rotate(self.image, )

    def shoot_mode1(self):
        now=pygame.time.get_ticks()
        if now- self.bullet_clock >300:
            self.bullet_clock=now
            b=Bullet_angle(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[0],0,3,10, self,0)
            b=Bullet_angle(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[1],0,-3,10,self,0)
            b=Bullet_angle(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[2],3,0,10,self,0)
            b=Bullet_angle(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[3],-3,0,10,self,0)
    def move_mode2(self):
        if self.rect.x>self.mode2_movetopoint.x :
            self.rect.x-=self.speedx
        if self.rect.x<self.mode2_movetopoint.x:
            self.rect.x+=self.speedx
        if self.rect.y>self.mode2_movetopoint.y :
            self.rect.y-=self.speedy
        if self.rect.y<self.mode2_movetopoint.y:
            self.rect.y+=self.speedy
        now=pygame.time.get_ticks()
        print(now-self.move_mode2tick)
        if now-self.move_mode2tick>5000 :
            i=random.randint(0,8)
            while self.mode2_movetopoint.x==self.mode2_points.loc[i]["x"] and self.mode2_movetopoint.y == self.mode2_points.loc[i]["y"]:
                i=random.randint(0,8)
            self.mode2_movetopoint.x=self.mode2_points.loc[i]["x"]
            self.mode2_movetopoint.y=self.mode2_points.loc[i]["y"]
            print(self.mode2_movetopoint.x)
            print(self.mode2_movetopoint.y)
            self.move_mode2tick=now

    def shoot_mode2(self):
        now=pygame.time.get_ticks()
        if now- self.bullet_clock >800:
            self.bullet_clock=now
            for angle in range(0,361,90):
                b=Bullet_angle(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[2],0,3,10, self,angle)
    def move_mode3(self):
        if self.rect.centerx>WIDTH/2 :
            self.speedx=-1
        if self.rect.centerx<WIDTH/2 :
            self.speedx=1
        if self.rect.centery>HEIGHT/2 :
            self.speedy=-1
        if self.rect.centery<HEIGHT/2 :
            self.speedy=1
        print(self.rect.centerx,self.rect.centery)
        if self.rect.centerx==WIDTH/2 or self.rect.centery==HEIGHT/2 :
            if self.rect.centery==HEIGHT/2 :
                print("中心y==400")
                self.speedy=0
            if self.rect.centerx==WIDTH/2 :
                self.speedx=0
        self.rect.x += self.speedx
        self.rect.y += self.speedy


    def shoot_mode3(self) :
        if self.rect.centerx == WIDTH / 2 and self.rect.centery==HEIGHT / 2:
            now=pygame.time.get_ticks()
            if now- self.bullet_clock >800:
                self.bullet_clock=now
                for angle in range(0,361,45):
                    b=Bullet_refect(self.rect.centerx,self.rect.centery,boss_enemy_bullet_imags[1],3,0,10,self,2,angle)

                # b = Bullet_refect(self.rect.centerx, self.rect.centery, boss_enemy_bullet, 3, 0, 10, self, 5, 45)

    def update(self):
        now=pygame.time.get_ticks()
        print(self.move_mode)
        if now-self.mode_tick>20000:
            if self.move_mode==1 :
                self.speedx=3
                self.speedy=3
                self.move_mode=2
            elif self.move_mode==2 :
                self.speedx = 0
                self.speedy = 0
                self.move_mode=3;
            elif self.move_mode==3:
                self.speedx = random.randint(-10, 10)
                self.speedy = random.randint(-10, 10)
                self.move_mode = 1;

            self.mode_tick=now

        if self.move_mode==1 :
            self.move_mode1()
            self.shoot_mode1()
        elif self.move_mode==2 :
            self.speedx = 3
            self.speedy = 3
            self.move_mode2()
            self.shoot_mode2()
        elif self.move_mode==3:
            self.move_mode3()
            self.shoot_mode3()














# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(繼承Enemy之後，寫出你的敵人class)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


        



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, speedx, speedy, attack, who):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        # 子彈相關數據
        self.speedx = speedx
        self.speedy = speedy
        self.attack = attack

        # 自動加入所屬群組
        all_sprites.add(self)
        if isinstance(who, Player):
            all_player_bullets.add(self)
        if isinstance(who, Enemy):
            all_enemies_bullets.add(self)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > HEIGHT:
            self.kill()
        if self.rect.left > WIDTH:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        


class Bullet_refect(Bullet):
    def __init__(self, x, y, img, speedx, speedy, attack, who,count,angle):
        super().__init__(x, y, img, speedx, speedy, attack, who)
        self.count=count
        self.angle=angle
        self.speed=Vector2(speedx,speedy)
        self.set_speed()
        self.radius = 20
    def set_speed(self):
        self.speed.rotate_ip(self.angle)
        self.speedx=self.speed.x
        self.speedy=self.speed.y
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        pos=Vector2(self.speedx,self.speedy)
        if self.rect.top <= 0 :
            angle=random.randint(0,180)
            pos.rotate_ip(angle)
            self.speedx=pos.x
            self.speedy=pos.y
            self.count-=1
        if self.rect.bottom >= HEIGHT:
            angle=random.randint(180,360)
            pos.rotate_ip(angle)
            self.speedx=pos.x
            self.speedy=pos.y
            self.count-=1
        if self.rect.right > WIDTH:

            angle=random.randint(1,180)
            pos.rotate_ip(angle)
            self.speedx=pos.x
            self.speedy=pos.y
            self.count-=1
        if self.rect.left < 0:
            angle=random.randint(-270,270)
            pos.rotate_ip(angle)
            self.speedx=pos.x
            self.speedy=pos.y
            self.count-=1
        if self.count==0 :
            self.kill()

class Bullet_angle(Bullet):
    def __init__(self, x, y, img, speedx, speedy, attack, who,angle):
        super().__init__(x, y, img, speedx, speedy, attack, who)
        self.angle=angle
        self.speed=Vector2(speedx,speedy)
        self.set_speed()
        self.radius = 20
    def set_speed(self):
        self.speed.rotate_ip(self.angle)
        self.speedx=self.speed.x
        self.speedy=self.speed.y


def main():
    global running
    global show_init
    global stage

    while running:

        # 畫面顯示
        win.fill(BLACK)
        win.blit(background_img, (0, 0))

        if show_init == True:
            running = draw_init(clock, win, background_img)
            show_init = False

            # 消除所有sprite，以防前一場遊戲剩下的sprite沒清乾淨
            for sprite in all_sprites:
                sprite.kill()

            # 確認遊戲開始後，初始化物件
            player = Player()

            # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓測試用(建立你所寫的敵人物件)↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
            # BasicEnemy(enemy1_img, 50, 350, 0)
            # BasicEnemy(enemy1_img, 50, 100, 0)
            Boss_enemy(boss_enemy_img, 100, 400, 0,player)

            # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑測試用(建立你所寫的敵人物件)↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        clock.tick(FPS)

        # 輸入判定
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 演算各種碰撞判斷
        # 玩家與敵方戰艦相撞
        hits = pygame.sprite.spritecollide(
            player, all_enemies, False)  # hits 回傳所有玩家碰撞到的eneny list
        for hit in hits:
            player.player_collide_with_enemy(hit)

        # 敵方與玩家子彈碰撞
        hits = pygame.sprite.groupcollide(
            all_enemies, all_player_bullets, False, True)  # hits 回傳一個字典 被射到的enemy物件：[所有射中該enemy的子彈list]
        for hit in hits:
            length = len(hits[hit])
            for i in range(0, length):
                hit.get_hit(hits[hit][i])

        # 玩家與敵方子彈碰撞
        hits = pygame.sprite.spritecollide(
            player, all_enemies_bullets, True)  # hits 回傳所有玩家碰撞到的敵方子彈 list
        for hit in hits:
            player.player_collide_with_enemy_bullets(hit)

        # 更新遊戲
        all_sprites.update()
        all_sprites.draw(win)
        draw_game_interface(win, player)

        # 測試是否所有sprite都有正常被加入與刪除
        # count_sprite=0
        # for i in all_sprites:
        #     count_sprite+=1
        # print(count_sprite)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
