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

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)   # プレイヤーの色
BROWN = (139, 69, 19)   # ブロックの色

def Extend(map_data, stage_width):#実験用
    """
    ステージを拡張する関数
    引数: 追加するブロックの数
    戻り値: 拡張したマップのリスト
    """
    for h in range(stage_width):
        for i in range(len(map_data)):
            if i < len(map_data) - 3:
                if i == 4:
                    map_data[i].append(random.randrange(0,2))
                else:
                    map_data[i].append(0)
            else:
                map_data[i].append(1)
    return map_data

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.img = pg.image.load("fig/syujinkou_yoko.png")
        self.img = pg.transform.rotozoom(self.img, 0, 0.03)
        self.rect = self.img.get_rect()
        self.vx = 0
        self.vy = 0
        self.movex = 0
        self.screen_x = 0
        self.is_on_ground = False
        self.move_left = False
        self.move_right = False




def main():
    # 画面設定
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("2Dアクションゲーム デモ")
    clock = pg.time.Clock()

    # 2. ステージデータ (0=空, 1=ブロック)
    # 画面下部が地面、途中に浮島があるマップ
    map_data = [
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]


    # 3. ステージの「当たり判定用の四角形(Rect)」リストを作成
    # (ゲーム開始時に一度だけ計算する)
    map_data = Extend(map_data, ADD_STAGE_BLOCK)
    block_rects = []
    edge_rects = []
    for y, row in enumerate(map_data):
        for x, tile_type in enumerate(row):
            if tile_type == 1:
                # (x座標, y座標, 幅, 高さ) のRectを作成
                block_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))
            elif tile_type ==2:
                edge_rects.append(pg.Rect(x * TILE_SIZE_X, y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y))
    # 4. プレイヤー設定
    player = Player() #プレイ
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
                if event.key == pg.K_SPACE and is_on_ground:
                    player.vy = JUMP_STRENGTH # 上向きの速度を与える
                    is_on_ground = False
            
            # キーが離された時
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.move_left = False
                if event.key == pg.K_RIGHT:
                    player.move_right = False

        # 7. プレイヤーのロジック更新 (移動と当たり判定)
        
        # --- 左右の移動と当たり判定 ---
        player.movex = 0
        if player.move_left:
            player.movex -= PLAYER_SPEED
        if player.move_right:
            player.movex += PLAYER_SPEED
        
        player.rect.x += player.movex # まずX方向に動かす
        player.screen_x = player.rect.x - camera_x # 画面内のプレイヤーの位置を確認
        if player.screen_x < LEFT_BOUND: # プレイヤーが左端ならカメラの位置を左にずらす
            camera_x = player.rect.x - LEFT_BOUND 
        elif player.screen_x > RIGHT_BOUND: #プレイヤーが右端ならカメラの位置を右にずらす
            camera_x = player.rect.x - RIGHT_BOUND
        max_camera_x = len(map_data[0]) * TILE_SIZE_X - SCREEN_WIDTH #カメラの動く範囲を総タイル数と画面のサイズから計算
        camera_x = max(0, min(camera_x, max_camera_x))
        
        # X方向の衝突チェック
        for block in block_rects:
            if player.rect.colliderect(block):
                if player.movex > 0: # 右に移動中に衝突
                    player.rect.right = block.left # 右端をブロックの左端に合わせる
                elif player.movex < 0: # 左に移動中に衝突
                    player.rect.left = block.right # 左端をブロックの右端に合わせる

        # --- 垂直方向（重力・ジャンプ）の移動と当たり判定 ---
        player.vy += GRAVITY # 重力を速度に加算
        player.rect.y += player.vy # Y方向に動かす
        
        # Y方向の衝突チェック
        is_on_ground = False # 毎フレーム「接地していない」と仮定
        for block in block_rects:
            if player.rect.colliderect(block):
                if player.vy > 0: # 落下中に衝突
                    player.rect.bottom = block.top # 足元をブロックの上端に合わせる
                    player.vy = 0 # 落下速度をリセット
                    is_on_ground = True   # 接地フラグを立てる
                elif player.vy < 0: # ジャンプ中に衝突
                    player.rect.top = block.bottom # 頭をブロックの下端に合わせる
                    player.vy = 0 # 上昇速度をリセット（頭を打った）
            # if player_rect.colliderect(edge):
                # player_rect.left = edge.right

        # 8. 描画処理
        screen.fill(BLACK) # 画面を黒で塗りつぶし
        

        # ステージ（ブロック）を描画
        for block in block_rects:
            draw_rect = pg.Rect(
                block.x - camera_x, #ブロックの出現位置を調整
                block.y,
                block.width,
                block.height
            )
            pg.draw.rect(screen, BROWN, draw_rect)

        # プレイヤーを描画
        screen.blit(player.img, (player.rect.x - camera_x, player.rect.y))
        
        # 画面を更新
        pg.display.flip()
        
        # 9. FPS (フレームレート) の制御
        clock.tick(60) # 1秒間に60回ループが回るように調整

# ループが終了したらPygameを終了
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
