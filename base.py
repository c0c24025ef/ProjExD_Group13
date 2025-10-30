import pygame as pg
import os
import sys
import random

# 1. 定数と初期設定
# pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEFT_BOUND = SCREEN_WIDTH // 3
RIGHT_BOUND = SCREEN_WIDTH * 2 // 3
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ADD_STAGE_BLOCK = 100
TILE_SIZE_X = 40
TILE_SIZE_Y = 40
GRAVITY = 0.8         # 重力
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
PLAYER_SPEED = 5      # 左右の移動速度
ENEMY_NUM = 4

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)   # プレイヤーの色
BROWN = (139, 69, 19)   # ブロックの色

#probsは生み出す確率リスト
def extend(map_data, add_stage_width, probs):
    """
    ステージを拡張する関数
    引数: 追加するブロックの数
    戻り値: 拡張したマップのリスト
    """  
    for i in range(len(map_data)):
        layer = -1 * (i + 1)
        if i < 2:
            for j in range(add_stage_width):
                map_data[layer].append(1)
        elif i < len(probs):
            for j in range(add_stage_width):
                pos = len(map_data[layer]) - 1
                generate_prob = random.randint(0,100) / 100
                if generate_prob < probs[layer] and map_data[layer + 1][pos] == 1 and map_data[layer + 1][pos + 1] == 1:
                    map_data[layer].append(1)
                else:
                    map_data[layer].append(0)
        else:
            for j in range(add_stage_width):
                map_data[layer].append(0)
    return map_data

def ground_surface(map_data):
    for i in range(len(map_data) - 2, 0, -1):
        for j in range(len(map_data[0])):  
            if map_data[i + 1][j] == 1 and map_data[i][j] == 0:
                map_data[i][j] = 2
    return map_data
            
def make_float_land(map_data: "list", add_range: "tuple", num):
    for i in range(num):
        width = random.randrange(2,4)
        X = random.randrange(10, len(map_data[0]))
        Y = random.randrange(add_range[0], add_range[1])
        if map_data[len(map_data) - Y][X] == 0 and map_data[len(map_data) - Y + 1][X] == 0 and map_data[len(map_data) - Y + 2][X] == 0:
            for j in width:
                map_data[len(map_data) - Y][X + j] = 3
    return map_data

# def extend(map_data, stage_width, max_ground_height = 5):
#     """
#     ステージを拡張する関数
#     引数: 追加するブロックの数
#     戻り値: 拡張したマップのリスト
#     """  
#     ini_stage_width = len(map_data[0])
#     for i in range(-1, -1 * len(map_data), -1):
#         if i >= -1 * max_ground_height:
#             probs = [0.2, 0.5, 0.8, 1.0, 1.0]
#             if i >= -2:
#                 for j in range(stage_width):
#                     map_data[i].append(1)
#                 else:
#                     continue

#             for j in range(stage_width):
#                 p = probs[i] if abs(i) < len(probs) else 0
#                 generate_prob = random.randint(0,100) / 100
#                 pos = len(map_data[0])
#                 if generate_prob <= p and map_data[i + 1][pos - 1] == 1:
#                     map_data[i].append(1)
#                 else:
#                     map_data[i].append(0)
#             else:
#                 map_data[i].append(2)
#         else:
#             for j in range(stage_width):
#                 map_data[i].append(0)
                                
#     return map_data

def gravity(instance, block_rects):
    instance.vy += GRAVITY # 重力を速度に加算
    instance.rect.y += instance.vy # Y方向に動かす
    instance.is_on_ground = False # 毎フレーム「接地していない」と仮定
    for block in block_rects:
        if instance.rect.colliderect(block):
                if instance.vy > 0: # 落下中に衝突
                    instance.rect.bottom = block.top # 足元をブロックの上端に合わせる
                    instance.vy = 0 # 落下速度をリセット
                    instance.is_on_ground = True   # 接地フラグを立てる
                elif instance.vy < 0: # ジャンプ中に衝突
                    instance.rect.top = block.bottom # 頭をブロックの下端に合わせる
                    instance.vy = 0 # 上昇速度をリセット（頭を打った）
 

# def Extend(map_data, stage_width):#実験用
#     """
#     ステージを拡張する関数
#     引数: 追加するブロックの数
#     戻り値: 拡張したマップのリスト
#     """
#     for h in range(stage_width):
#         for i in range(len(map_data)):
#             if i < len(map_data) - 3:
#                 if i == 4:
#                     map_data[i].append(random.randrange(0,2))
#                 else:
#                     map_data[i].append(0)
#             else:
#                 map_data[i].append(1)
#     return map_data

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pg.image.load("fig/syujinkou_yoko.png")
        self.img = pg.transform.rotozoom(self.img, 0, 0.03)
        self.rect = self.img.get_rect()
        self.vy = 0
        self.movex = 0
        self.screen_x = 0
        self.is_on_ground = False
        self.move_left = False
        self.move_right = False
    
    def update(self, stage_width, block_rect, camera_x):
        self.movex = 0
        if self.move_left:
            self.movex -= PLAYER_SPEED
        if self.move_right:
            self.movex += PLAYER_SPEED

        self.rect.x += self.movex # まずX方向に動かす
        self.screen_x = self.rect.x - camera_x # 画面内のプレイヤーの位置を確認
        if self.screen_x < LEFT_BOUND: # プレイヤーが左端ならカメラの位置を左にずらす
            camera_x = self.rect.x - LEFT_BOUND
        elif self.screen_x > RIGHT_BOUND: #プレイヤーが右端ならカメラの位置を右にずらす
            camera_x = self.rect.x - RIGHT_BOUND
        max_camera_x = stage_width * TILE_SIZE_X - SCREEN_WIDTH #カメラの動く範囲を総タイル数と画面のサイズから計算
        # print(max_camera_x)
        camera_x = max(0, min(camera_x, max_camera_x))

        # X方向の衝突チェック
        for block in block_rect:
            if self.rect.colliderect(block):
                if self.movex > 0: # 右に移動中に衝突
                    self.rect.right = block.left # 右端をブロックの左端に合わせる
                elif self.movex < 0: # 左に移動中に衝突
                    self.rect.left = block.right # 左端をブロックの右端に合わせる
        
        gravity(self, block_rects)
        
        return camera_x

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.img = pg.image.load("fig/syujinkou_yoko.png")
        self.img = pg.transform.rotozoom(self.img, 0, 0.1) # 修正予定 画像サイズは元画像の変更の方がよい
        self.rect = self.img.get_rect()
        self.rect.center = pos 
        self.vx = 1
        self.vy = 0
        self.is_on_ground = False

    def update(self):
        self.rect.center = (self.rect.centerx + 1 * self.vx, self.rect.centery)        

class Score:
    def __init__(self):
        self.pic = pg.font.Font(None, 80)
        self.value = 0
        # txt = self.pic.render(f"スコア: {self.value}", True, (255, 255, 255))
    
    def update(self):
        self.txt = self.pic.render(f"Score: {self.value}", True, (255, 255, 255))


def main():
    # 画面設定
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("2Dアクションゲーム デモ")
    clock = pg.time.Clock()

    # 2. ステージデータ (0=空, 1=ブロック)
    # 画面下部が地面、途中に浮島があるマップ
    map_data = [
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

    probs = [0.5, 0.7, 0.9, 1.0, 1.0]

    enemy_pos = (100, 100)

    # 3. ステージの「当たり判定用の四角形(Rect)」リストを作成
    # (ゲーム開始時に一度だけ計算する)
    map_data = extend(map_data, ADD_STAGE_BLOCK, probs)
    map_data = ground_surface(map_data)
    map_data = make_float_land(map_data, (5,7), 5)
    block_rects = []
    surface_rects = []
    floatland_rects = []
    for y, row in enumerate(map_data):
        for x, tile_type in enumerate(row):
            if tile_type == 1:
                # (x座標, y座標, 幅, 高さ) のRectを作成
                block_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))
            elif tile_type == 2:
                surface_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X, TILE_SIZE_Y / 2))
            elif tile_type == 3:
                floatland_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y + (TILE_SIZE_Y / 2), TILE_SIZE_X, TILE_SIZE_Y / 2))
    # 4. プレイヤー設定
    player = Player() #プレイヤー
    enemys = pg.sprite.Group()
    for i in range(ENEMY_NUM):
        enemys.add(Enemy(enemy_pos))
    score = Score()
    
    camera_x = 0 #カメラの位置を初期化

    # 5. ゲームループ
    running = True
    while running:
        
        # 6. イベント処理 (キー操作など)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            
            # キーが押された時
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move_left = True
                if event.key == pg.K_RIGHT:
                    player.move_right = True
                if event.key == pg.K_SPACE and player.is_on_ground:
                    player.vy = JUMP_STRENGTH # 上向きの速度を与える
                    player.is_on_ground = False
            
            # キーが離された時
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.move_left = False
                if event.key == pg.K_RIGHT:
                    player.move_right = False

        # 7. プレイヤーのロジック更新 (移動と当たり判定)

        # 8. 描画処理
        screen.fill(BLACK) # 画面を黒で塗りつぶし
        



        

        # プレイヤーを描画
        camera_x = player.update(len(map_data[0]), [surface_rects, floatland_rects], camera_x)
        # print(camera_x)
        screen.blit(player.img, (player.rect.x - camera_x, player.rect.y))
        
        # ステージ（ブロック）を描画
        for block in block_rects:
            draw_rect = pg.Rect(
                block.x - camera_x, #ブロックの出現位置を調整
                block.y,
                block.width,
                block.height
            )
            pg.draw.rect(screen, BROWN, draw_rect)
        for block in surface_rects:
            draw_rect = pg.Rect(
                block.x - camera_x,
                block.y,
                block.width,
                block.height
            )
            pg.draw.rect(screen, (255, 0, 255), draw_rect)
        for block in floatland_rects:
            draw_rect = pg.Rect(                
                block.x - camera_x,
                block.y,
                block.width,
                block.height)
            pg.draw.rect(screen, (255, 255, 255), draw_rect)
        # 画面を更新
        # pg.display.flip()
        score.update()
        screen.blit(score.txt, (SCREEN_WIDTH / 10, SCREEN_HEIGHT - SCREEN_HEIGHT / 10))
        pg.display.update()
        
        # 9. FPS (フレームレート) の制御
        clock.tick(60) # 1秒間に60回ループが回るように調整

# ループが終了したらPygameを終了
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
