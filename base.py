import pygame as pg
import os
import sys
import random

#ーーーーーーーーー1.定数と初期設定ーーーーーーーーー
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600 # 画面のサイズ
LEFT_BOUND, RIGHT_BOUND = SCREEN_WIDTH // 3, SCREEN_WIDTH * 2 // 3 # スクロール判定
TILE_SIZE_X, TILE_SIZE_Y = 100, 40 # タイルのサイズ
ADD_STAGE_BLOCK = 100 # ステージの拡張幅
GRAVITY = 0.8         # 重力
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
HOVER_AIR_TIME = 60   # ホバーエフェクトの表示時間(フレーム単位)
PLAYER_SPEED = 10      # 左右の移動速度
PLAYER_HP = 5
NO_DAMAGE_TIME = 120 # 無敵時間(フレーム単位)
PLAYER_POWER = 10 # プレイヤーの攻撃力
ENEMY_NUM = 1         # 敵の数
ENEMY_SPEED = 1
#ーーーーーーーーーーーーーーーーーーーーーーーーーー
#---まだ
def start_page(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    スタート画面を表示する関数
    引数: スクリーンsurface, pgのクロック  
    戻り値: int(開始なら0, 終了なら-1)
    """
    bg_img = pg.image.load("fig/night_plain_bg.png")
    title = Text("GO KOUKATON (TUT)", 80, (100, 300))
    start_button = Text("Start", 80, (100, 100))
    end_button = Text("Quit", 80, (500, 100))

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウスの位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(title.txt, (title.x, title.y))
        screen.blit(start_button.txt, (start_button.x, start_button.y))
        screen.blit(end_button.txt, (end_button.x, end_button.y))
        
        if start_button.x < mouse_x < start_button.x + start_button.width and end_button.y < mouse_y < end_button.y + end_button.height:
            return 0 # スタートボタンをクリック
        if end_button.x < mouse_x < end_button.x + end_button.width and end_button.y < mouse_y < end_button.y + end_button.height:
            return -1 # Quitボタンをクリック
                
        pg.display.update()
        clock.tick(60)



# 画面設定


# enemy_image = pygame.image.load("fig/syujinkou_yoko.png")
# enemy_image = pygame.transform.rotozoom(enemy_image, 0, 0.1) # テスト用の敵を設定
# enemy_rect = enemy_image.get_rect()
# enemy_rect.center = (300,300)
# enemy_size = 1.0

def gameover(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    ゲームオーバー画面を表示する関数
    引数: スクリーンsurface, pgのクロック
    戻り値: int(開始なら0, 終了なら-1)    
    """
    bg_img = pg.image.load("fig/night_plain_bg.png")
    txt = Text("Game Over", 80, (100, 300))
    retry = Text("Retry", 80, (100, 100))
    quit = Text("Quit", 80, (500, 100))

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウス位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(txt.txt, (txt.x, txt.y))
        screen.blit(retry.txt, (retry.x, retry.y))
        screen.blit(quit.txt, (quit.x, quit.y))
        
        if retry.x < mouse_x < retry.x + retry.width and retry.y < mouse_y < retry.y + retry.height:
            return 0 # リトライを押された
        if quit.x < mouse_x < quit.x + quit.width and quit.y < mouse_y < quit.y + quit.height:
            return -1 # 終了を押された
        
        pg.display.update()
        clock.tick(60)
#ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

#ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
def game_clear(screen: pg.surface, clock: pg.time.Clock) -> int:
    """
    クリア画面を表示する関数
    引数: スクリーンsurface, pgのクロック
    戻り値: int(再プレイなら0, 終了なら-1)
    """
    bg_img = pg.image.load("fig/night_plain_bg.png")
    txt = Text("Game Clear", 80, (100, 300))
    retry = Text("Retry", 80, (100, 100))
    quit = Text("Quit", 80, (500, 100))

    mouse_x, mouse_y = -1000, -1000 # マウス位置をあり得ない位置で初期化

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1
        
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos # マウス位置を取得
 
        screen.blit(bg_img, (0, 0))
        screen.blit(txt.txt, (txt.x, txt.y))
        screen.blit(retry.txt, (retry.x, retry.y))
        screen.blit(quit.txt, (quit.x, quit.y))
        
        if retry.x < mouse_x < retry.x + retry.width and retry.y < mouse_y < retry.y + retry.height:
            return 0 # リトライを押された
        if quit.x < mouse_x < quit.x + quit.width and quit.y < mouse_y < quit.y + quit.height:
            return -1 # 終了を押された
        
        pg.display.update()
        clock.tick(60)
#------

def extend(map_data: list[list[int]], add_stage_width: int, probs: list[int]) -> list[list[int]]:
    """
    ステージを拡張する関数。地面ブロックとして追加する
    内容: 下2マスは確定で地面。それ以降は拡張幅まで、下のマスが地面 and 1つ前の下のマスが地面 の時に生成
    引数: 初期マップデータ, 追加するブロックの数, 生成する確率
    戻り値: 拡張したマップのリスト
    """  
    for i in range(len(map_data)):
        layer = -1 * (i + 1)  # 下の段から選択
        if i < 2:
            for j in range(add_stage_width):  # 下2段は地面ブロック(1)
                map_data[layer].append(1)
        elif i < len(probs):
            for j in range(add_stage_width):
                pos = len(map_data[layer]) - 1  # 現時点の自身の段のブロック数-1 が自身の位置
                generate_prob = random.randint(0,100) / 100 
                if generate_prob < probs[layer] and map_data[layer + 1][pos] == 1 and map_data[layer + 1][pos + 1] == 1:
                    map_data[layer].append(1)
                else:
                    map_data[layer].append(0)
        else:
            for j in range(add_stage_width):  # 地面を生成しない段
                map_data[layer].append(0)
    return map_data

def ground_surface(map_data: list[list[int]]) -> list[list[int]]:
    """
    地面ブロックの上に地表ブロックを配置する関数
    内容: 下のマスが地面 and 自分のマスが無 の時に生成
    引数: 現在のマップデータ
    戻り値: 地表追加後のマップデータ    
    """
    for i in range(len(map_data) - 2, 0, -1): #上段から調べる
        for j in range(len(map_data[0])):  
            if map_data[i + 1][j] == 1 and map_data[i][j] == 0:
                map_data[i][j] = 2
    return map_data

def make_float_land(map_data: list[list[int]], add_range: tuple[int], num: int) -> list[list[int]]:
    """
    浮島を生成する関数
    内容: 自身が無の時、下のマスが無 and 2マス下が無 の時に浮島を生成
    引数: 現在のマップ, 浮島を生成するレイヤー, 生成個数 
    戻り値: 浮島を追加したマップ
    """
    maked_floatland = 0 
    while maked_floatland <= num:
        width = random.randrange(2,4) # 生成する浮島の長さ
        X = random.randrange(10, len(map_data[0])) # 浮島のX座標
        Y = random.randrange(add_range[0], add_range[1] + 1) #浮島のY座標
        if map_data[len(map_data) - Y][X] == 0 and map_data[len(map_data) - Y + 1][X] == 0 and map_data[len(map_data) - Y + 2][X] == 0:
            maked_floatland += 1
            if X + width >= len(map_data[0]): # 生成位置がマップ範囲を超えてたらずらす
                X = len(map_data) - width
            for j in range(width):
                map_data[len(map_data) - Y][X + j] = 3
    
    for i in range(2):
        map_data[len(map_data)- 8][len(map_data[0]) - i - 1] = 3
    return map_data

#---修正
def walled(instance: object, blocks: list[tuple[object, int]]) -> None:
    """
    壁衝突判定を行う関数
    内容: 壁に衝突したとき、自身の位置を壁端に合わせる。
    引数: 衝突判定を行うオブジェクト, 衝突するブロックを保持したリスト
    """
    for block in blocks:
        if instance.rect.colliderect(block): 
            if instance.vx > 0: # 右に移動中に衝突
                instance.rect.right = block.left # 右端をブロックの左端に合わせる
            elif instance.vx < 0: # 左に移動中に衝突
                instance.rect.left = block.right # 左端をブロックの右端に合わせる
#-------

#---修正
def gravity(instance: object, blocks: list[tuple[object, int]]) -> None:
    """
    重力を適用し、地面との衝突判定を行う関数
    内容: 地面にぶつかった際、y方向の速度を0にし、座標を地面の上に合わせる
    引数: 重力を適用するオブジェクト, ブロックのリスト
    """
    instance.vy += GRAVITY # 重力を速度に加算
    instance.rect.y += instance.vy # Y方向に動かす
    instance.is_on_ground = False # 毎フレーム「接地していない」と仮定
    
    for block in blocks:
        if instance.rect.colliderect(block):
                if instance.vy > 0: # 落下中に衝突
                    instance.rect.bottom = block.top # 足元をブロックの上端に合わせる
                    instance.hover_num = 0
                    instance.vy = 0 # 落下速度をリセット
                    instance.is_on_ground = True   # 接地フラグを立てる
                elif instance.vy < 0: # ジャンプ中に衝突
                    instance.rect.top = block.bottom # 頭をブロックの下端に合わせる
                    instance.vy = 0 # 上昇速度をリセット（頭を打った）
#------

def no_damage(instance: object, flag: int = 0) -> None:
    """
    無敵時間中の処理を行う関数
    内容: 無敵時間中の画像表示、無敵時間の減算
    引数: 無敵時間を適用するインスタンス, フラグ(0なら無敵時間中, 1なら無敵になる前)
    """
    if instance.no_damage_time == 0 and flag == 1:
        instance.no_damage_time = NO_DAMAGE_TIME
    elif instance.no_damage_time > 0:
        if instance.no_damage_time % 10 == 0 and instance.no_damage_time % 20 != 0:
            instance.patarn = (instance.patarn[0], 0, "normal")
        elif instance.no_damage_time % 20 == 0:
            instance.patarn = (instance.patarn[0], 0, "no_damage")            
        instance.no_damage_time -= 1
    else:
        return

class Assets:
    def __init__(self):
        self.bg = pg.image.load("fig/night_plain_bg.png")
        self.ground = pg.image.load("fig/ground2.png")
        self.weeds = pg.image.load("fig/weeds(extend).png")
        self.cloud = pg.image.load("fig/cloud(extend).png")

        self.init_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.probs = [0.5, 0.7, 0.9, 1.0, 1.0] # ブロックを生成する確率(左から上段)

class Text:
    def __init__(self, string: str, str_size: int, pos: tuple[int,int]) -> None:
        self.txt = pg.font.Font(None, str_size)
        self.txt = self.txt.render(string, True, (255, 255, 255))
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.txt.get_width()
        self.height = self.txt.get_height()

#---修正
class Player(pg.sprite.Sprite):
    """
    操作キャラクターのクラス
    """
    def __init__(self):
        super().__init__()
        
        self.original = pg.image.load("fig/yoko1.png")
        # self.img = self.original
        self.flip = pg.transform.flip(self.original, True, False)
        self.punch = pg.image.load("fig/punch.png")
        self.imgs = [self.original, self.flip ]
        self.rect = self.imgs[0].get_rect()
        self.vx = 0
        self.vy = 0
        self.patarn = (1, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal") : self.imgs[0], (-1, 0, "normal") : self.imgs[1],
                              (1, 0, "no_damage") : pg.transform.laplacian(self.imgs[0]), (-1, 0, "no_damage") : pg.transform.laplacian(self.imgs[1]),
                              (1, 0, "punch") : self.punch, (-1, 0, "punch"): pg.transform.flip(self.punch, True, False)
                              }

        self.hover_num = 0
        self.hp = PLAYER_HP
        self.no_damage_time = NO_DAMAGE_TIME
        self.power = PLAYER_POWER
        self.attacking = False

        self.is_on_ground = False
        self.move_left, self.move_right = False, False


    
    def update(self, stage_width: "int", all_blocks: "list[object]", floar_blocks: "list[object]", camera_x: "int") -> "int":
        """
        自身の座標を更新する関数
        内容: キーに合わせて自身が移動する。移動に合わせてカメラ座標も取得する
        戻り値: カメラ用の係数       
        """  
        if self.move_left:
            self.vx = -PLAYER_SPEED
            if self.attacking == True:
                self.patarn = (-1, 0, "punch")           
            else:
                self.patarn = (-1, 0, "normal")
        if self.move_right:
            self.vx = PLAYER_SPEED
            if self.attacking == True:
                self.patarn = (1, 0, "punch")
            else:
                self.patarn = (1, 0, "normal")

        self.rect.x += self.vx

        walled(self, all_blocks)
        gravity(self, floar_blocks)
        no_damage(self, 0)

        if self.rect.x - camera_x < LEFT_BOUND: # プレイヤーが左端
            camera_x = self.rect.x - LEFT_BOUND # オブジェクトのずらし度を決定する。
        elif self.rect.x - camera_x > RIGHT_BOUND: #プレイヤーが右端ならカメラの位置を右にずらす
            camera_x = self.rect.x - RIGHT_BOUND 
        max_camera_x = stage_width * TILE_SIZE_X - SCREEN_WIDTH #カメラが右端を超えないように
        camera_x = max(0, min(camera_x, max_camera_x))
        
        return camera_x
    
    def hover(self) -> None:
        """
        ホバリングを行う関数
        内容: 上限まで連続して自身の上方速度を加算する。
        """
        if self.hover_num == 5:
            return
        self.vy += JUMP_STRENGTH
        self.hover_num += 1
        return
    
    # def no_damage(self,instance, flag = 0):
    #     if self.no_damage_time == 0 and flag == 1:
    #         self.no_damage_time = NO_DAMAGE_TIME
    #     elif self.no_damage_time > 0:
    #         if self.no_damage_time % 10 == 0 and self.no_damage_time % 20 != 0:
    #             self.dire = (self.dire[0], 0, 0)
    #         elif self.no_damage_time % 20 == 0:
    #             self.dire = (self.dire[0], 0, 1)            
    #         self.no_damage_time -= 1
    #     else:
    #         return
        
    def panch(self):
        attack = PlayerLeadAttack((50, 20), 600, "punch")
        self.patarn = (self.patarn[0], 0, "punch")
        self.attacking = True
        return attack

#---
class Absurb(pg.sprite.Sprite):
    def __init__(self, instance: object) -> None:
        """
        吸収判定を初期化する関数
        引数: 吸収機能を持つインスタンス
        """
        super().__init__()
        self.img = pg.image.load("fig/tatsumaki.png")
        self.img = pg.transform.rotozoom(self.img, 270, 0.05) #画像のサイズと向きを設定
        self.rect = self.img.get_rect()
        self.rect.center = ((instance.rect.centerx + 40, instance.rect.centery)) # 描写位置をプレイヤーのすぐ先に設定

    def update(self, player_rect: pg.Rect) -> None:
        """
        吸収判定を移動させる関数
        引数: プレイヤーの位置を表す矩形
        """
        self.rect.centerx = player_rect.centerx + 40 # 描写位置を再設定
        self.rect.centery = player_rect.centery

class HoverAir(pg.sprite.Sprite):
    def __init__(self, instance, flag, flag_air_dire):
        super().__init__()
        self.image = pg.image.load("fig/jumped_air.png")
        self.image = [self.image, pg.transform.flip(self.image, True, False)][flag_air_dire]
        self.time = HOVER_AIR_TIME
        self.rect = self.image.get_rect()
        self.rect.x = instance.rect.centerx + instance.imgs[0].get_width() * flag
        self.rect.y = instance.rect.centery

    def update(self):
        self.time -= 1
        self.rect.y += 1
        if self.time == 0:
            self.kill()

#---修正
class Enemy(pg.sprite.Sprite):
    """
    敵を司るクラス
    """
    def __init__(self):
        super().__init__()

        self.original = pg.image.load("fig/troia1.png")
        self.image = self.original
        self.flip = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (1000, 0) #テスト用で定数
        self.size = 1.0
        self.vx = ENEMY_SPEED
        self.vy = 0
        self.patarn = (1, 0, "normal")
        self.patarn_to_img = {(1, 0, "normal"): self.image, (-1, 0, "normal"): self.flip,
                              (1, 0, "no_damage"): pg.transform.laplacian(self.image), (1, 0, "no_damage"): pg.transform.laplacian(self.flip),
                              }

        self.hp = 5
        self.no_damage_time = NO_DAMAGE_TIME
        self.power = 1
        
        self.is_on_ground = False
        self.is_move_left, self.is_move_right = True, False

    def update(self, all_blocks: "list[object]", floar_blocks: "list[object]", camera_x: "int") -> None:
        """
        自身の位置を更新する関数
        """
        self.rect.x -= self.vx

        for block in all_blocks:
            if self.rect.colliderect(block):
                if self.is_move_left:
                    self.rect.left = block.right
                    self.is_move_right = True
                    self.is_move_left = False
                elif self.is_move_right:
                    self.rect.right = block.left
                    self.is_move_left = True
                    self.is_move_right = False
                self.vx *= -1
                # print(f"敵の速度{self.vx}")
                
        gravity(self, floar_blocks)
        # self.rect.centery -= (TILE_SIZE_Y/2)
#------

class PlayerLeadAttack(pg.sprite.Sprite):
    def __init__(self, size, time, type, ini_angle = 45):
        super().__init__()
        self.original = pg.Surface(size)
        self.original.fill((255, 0, 0))
        self.rect = self.original.get_rect()
        self.img = self.original
        self.time = time
        self.angle = ini_angle + 1
        self.type = type
        self.dire = (1, 0)


    def update(self, instance):
        if instance.move_left == True:
            self.dire = (-1, 0)
        elif instance.move_right == True:
            self.dire = (1, 0)

        if self.dire == (-1, 0):
            self.rect.x ,self.rect.y = instance.rect.left - 30, instance.rect.y + 50
        elif self.dire == (1, 0):
            self.rect.x ,self.rect.y = instance.rect.right + 30, instance.rect.y + 50
        if self.type == "punch":
            self.time -= 1
            # print(self.time)
            if self.time == 0:
                instance.attacking = False
                instance.patarn = (instance.patarn[0], 0, "normal")
                # instance.status = instance.imgs[0]
                self.kill()
                
    
class EnemyLeadAttack(pg.sprite.Sprite):
        def __init__(self, size,  time, type, ini_angle):
            self.original = pg.surface(size)
            self.img = self.original
            self.time = time
            self.angle = ini_angle + 1
            self.type = type        

        def update(self, fin_angle = 45):
            if self.type == "beam":
                self.angle += 1
                self.img = pg.transform.rotate(self.original, angle)
                if self.angle == fin_angle:
                    self.kill()

class BoundBalls(pg.sprite.Sprite):
    def __init__(self, stage_width, tile_num_y):
        super().__init__()
        self.img = pg.image.load("fig/virus.png")
        self.rect = self.img.get_rect()
        self.rect.center = (stage_width * TILE_SIZE_X, 0)
        self.vx = - 2
        self.vy = 1
        self.top_bordarline = 0
        self.bottom_bordarline = ((SCREEN_HEIGHT / TILE_SIZE_Y) - tile_num_y) * TILE_SIZE_Y

    def update(self):
        self.rect.x += self.vx
        if self.vy == 1:
            self.rect.y += 3 # Y方向に動かす
            # print(f"降下中{self.rect.y}")
            if self.rect.y >= self.bottom_bordarline:
                self.vy = -1
        elif self.vy == -1:
            self.rect.y -= 3
            # print("上昇中")
            if self.rect.y <= self.top_bordarline:
                self.vy = 1
        if self.rect.x <= 0:
            self.kill()

#------

#---まだ
class Goal(pg.sprite.Sprite):
    def __init__(self, map_data):
        super().__init__()
        self.image = pg.image.load("fig/goal(normal).png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = TILE_SIZE_X * len(map_data[0]) - TILE_SIZE_X * 1.5, SCREEN_HEIGHT - TILE_SIZE_Y * 9

    # def update(self, camera_x):
        # self.rect.x = camera_x
        
    
#------
class Hp:
    def __init__(self):
        self.pic = pg.font.Font(None, 80)
        self.txt = self.pic.render("HP: ", True, (0, 0, 0))

class Heart(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pg.image.load("fig/hearts1.png")

    def update(self, instance, num):
        if instance.hp < num:
            self.kill()


#---まだ
class Score:
    def __init__(self):
        self.pic = pg.font.Font(None, 80)
        self.value = 0
    
    def update(self):
        self.txt = self.pic.render(f"Score: {self.value}", True, (255, 255, 255))
#------

def main():
    # ーーーーー画面設定ーーーーー
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("2Dアクションゲーム デモ")
    clock = pg.time.Clock()
    # ーーーーーーーーーーーーーー
    respond = start_page(screen, clock)
    if respond == -1:
        return
    

    assets = Assets()

    bg_img = pg.image.load("fig/night_plain_bg.png")
    bg_width = bg_img.get_width()
    pg.mixer.music.load("fig/魔王魂(ファンタジー).mp3")
    pg.mixer.music.play(loops = -1)

    map_data = assets.init_map
    map_data = extend(map_data, ADD_STAGE_BLOCK, assets.probs)
    map_data = ground_surface(map_data)
    map_data = make_float_land(map_data, (6,10), 10)

    block_rects = []
    surface_rects = []
    floatland_rects = []
    for y, row in enumerate(map_data):
        for x, tile_type in enumerate(row):
            if tile_type == 1:
                block_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))
            elif tile_type == 2:
                surface_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X,TILE_SIZE_Y / 2))
            elif tile_type == 3:
                floatland_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X, TILE_SIZE_Y / 2))


    floar_blocks = surface_rects + floatland_rects
    all_blocks = block_rects + floar_blocks
    
    enemys = pg.sprite.Group()
    hearts = pg.sprite.Group()
    hovers = pg.sprite.Group()
    player_lead_attacks = pg.sprite.Group()
    bound_balls = pg.sprite.Group()
    absurbs = pg.sprite.Group()

    player = Player() 
    for i in range(ENEMY_NUM):
        enemys.add(Enemy())
    goal = Goal(map_data)
    for i in range(player.hp):
        hearts.add(Heart())
    bound_balls.add(BoundBalls(len(map_data[0]), 5))
    score = Score()
    hp = Hp()
    
    camera_x = 0
    time = 0

    #ーーーーーゲームスタートーーーーー
    while True:
    
        #ーーーーーイベント取得ーーーーー

        if player.rect.colliderect(goal):
            print("goal!!")
            respond = game_clear(screen, clock, 1)
            if respond == -1:
                return
            else:
                enemys = pg.sprite.Group()
                hearts = pg.sprite.Group()
                hovers = pg.sprite.Group()
                player_lead_attacks = pg.sprite.Group()
                bound_balls = pg.sprite.Group()

                player = Player() 
                for i in range(ENEMY_NUM):
                    enemys.add(Enemy())
                goal = Goal(map_data)
                for i in range(player.hp):
                    hearts.add(Heart())
                bound_balls.add(BoundBalls(len(map_data[0]), 5))
                score = Score()
                hp = Hp()
                
                camera_x = 0
                time = 0 
            
        if player.hp <= 0:
            print("failed")
            respond = gameover(screen, clock)
            if respond == -1:
                return 
            else: 
                enemys = pg.sprite.Group()
                hearts = pg.sprite.Group()
                hovers = pg.sprite.Group()
                player_lead_attacks = pg.sprite.Group()
                bound_balls = pg.sprite.Group()

                player = Player() 
                for i in range(ENEMY_NUM):
                    enemys.add(Enemy())
                goal = Goal(map_data)
                for i in range(player.hp):
                    hearts.add(Heart())
                bound_balls.add(BoundBalls(len(map_data[0]), 5))
                score = Score()
                hp = Hp()
                
                camera_x = 0
                time = 0                

        for event in pg.event.get():
            #ゲーム終了
            if event.type == pg.QUIT:
                return 
            
            # キーが押された時
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move_left = True
                if event.key == pg.K_RIGHT:
                    player.move_right = True
                if event.key == pg.K_SPACE:
                    player.hover()
                    hovers.add(HoverAir(player, -1, 1))
                    hovers.add(HoverAir(player, 1, 0))
                    player.is_on_ground = False
                if event.key == pg.K_p:
                    if not player.attacking:
                        player_lead_attacks.add(player.panch())
                if event.key == pg.K_a:
                    absurbs.add(Absurb(player))

            # キーが離された時
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.vx = 0
                    player.move_left = False
                if event.key == pg.K_RIGHT:
                    player.vx = 0
                    player.move_right = False
                if event.key == pg.K_a:
                    absurbs.empty()
        #ーーーーーーーーーーーーーーーー
        heart_num = len(hearts)
        for enemy in pg.sprite.spritecollide(player, enemys, False): 
            if player.no_damage_time == 0:
                player.hp -= 1
                for i in hearts:
                    i.update(player, heart_num)
                    heart_num -= 1
                no_damage(player,1)

        for enemy in pg.sprite.groupcollide(absurbs, enemys, False, False).keys():
            enemy.size -= 0.05
            enemy.img = pg.transform.rotozoom(enemy.original, 0, enemy.size)
            enemy.rect.centery += 10


        for bound_boll in bound_balls:
            if player.rect.colliderect(bound_boll):
                if player.no_damage_time == 0:
                    player.hp -= 1
                    for i in hearts:
                        i.update(player, heart_num)
                        heart_num -= 1
                    no_damage(player,1)              

        for enemy in pg.sprite.groupcollide(enemys, player_lead_attacks, False, False).keys():
            if enemy.no_damage_time == 0:
                enemy.hp -= 1
                no_damage(enemy, 1)
                # print("attacked")
            if enemy.hp == 0:
                enemy.kill()


        #----修正
        # no_damage(player, 0)
        camera_x = player.update(len(map_data[0]), all_blocks, floar_blocks, camera_x)
        # for i in player_lead_attacks:
        #     i.update(player)
        #     screen.blit(i.img, (100, 100))#(player.rect.x + 100, player.rect.y))
        scroll_x = -camera_x % bg_width
        #-------

        screen.blit(bg_img, (scroll_x - bg_width, -100))
        screen.blit(bg_img, (scroll_x, -100))
        #---修正
        screen.blit(player.patarn_to_img[player.patarn], (player.rect.x - camera_x, player.rect.y))
        hovers.update()
        for hover in hovers:
            screen.blit(hover.image, (hover.rect.x - camera_x, hover.rect.y))
        for i in player_lead_attacks:
            i.update(player)
            screen.blit(i.img, (i.rect.x - camera_x, i.rect.y))

        for i in absurbs:
            i.update(player)
            screen.blit(i.img, i.rect)


        for i in bound_balls:
            i.update()
            screen.blit(i.img, (i.rect.x - camera_x, i.rect.y))
        if time % 300 == 0:
            bound_balls.add(BoundBalls(len(map_data[0]), 5))

        enemys.update(all_blocks, floar_blocks, camera_x)
        for enemy in enemys:
            no_damage(enemy, 0)
            screen.blit(enemy.patarn_to_img[enemy.patarn], (enemy.rect.x - camera_x, enemy.rect.y))
        #------

        for block in block_rects:
            screen.blit(assets.ground, (block.x - camera_x, block.y, block.width, block.height))
        for block in surface_rects:
            screen.blit(assets.weeds, (block.x - camera_x,block.y))
        for block in floatland_rects:
            screen.blit(assets.cloud, (block.x - camera_x, block.y))
        screen.blit(goal.image, (goal.rect.x - camera_x, goal.rect.y))

        # hearts.update(player, len(hearts))
        for index, i in enumerate(hearts, 1):
            screen.blit(i.img, (10 + (80 * index), 0))
        screen.blit(hp.txt, (0, 5))
        score.update()
        screen.blit(score.txt, (SCREEN_WIDTH / 10, SCREEN_HEIGHT - SCREEN_HEIGHT / 10))
        
        time += 1
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()