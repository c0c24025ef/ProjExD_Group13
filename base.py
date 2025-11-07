import pygame as pg
import os
import random
import math
import sys
import time


# 1. 定数と初期設定
pg.init()  # pgを初期化
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
TILE_SIZE = 40
GRAVITY = 0.8         # 重力
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
PLAYER_SPEED = 5      # 左右の移動速度

# 色の定義
BLACK = (255, 255, 255)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)   # プレイヤーの色
BLACK = (0, 0, 0)   # ブロックの色

# 画面設定
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("2Dアクションゲーム デモ")
clock = pg.time.Clock()

class BombEnemy(pg.sprite.Sprite):
    """
    爆弾の敵に関するクラス
    """
    def __init__(self):
        super().__init__()
        bomb_img = pg.image.load("fig/bakudan.png")
        self.image = pg.transform.rotozoom(bomb_img, 0, 1)
        self.rect = pg.Rect(800, 300, TILE_SIZE, TILE_SIZE)
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.vx = random.choice([-3, 3])
        # --- 追加: 垂直速度と接地フラグを初期化（プレイヤーと同様） ---
        self.vy = 0.0
        self.on_ground = False
        self.next_throw = random.randint(60, 120)

    def update(self, blocks):
        # 横移動
        self.rect.x += int(self.vx)
        self.image_rect.center = self.rect.center

        # ブロックとの横衝突（反転）
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vx > 0:
                    self.rect.right = block.left
                else:
                    self.rect.left = block.right
                self.vx = -self.vx
                self.image_rect.center = self.rect.center
                break

        # Y方向：重力を加算して移動
        self.vy += GRAVITY
        self.rect.y += int(self.vy)

        # Y方向の衝突チェック
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vy > 0:  # 落下中に衝突
                    self.rect.bottom = block.top
                    self.vy = 0
                    self.on_ground = True
                    self.image_rect.center = self.rect.center
                elif self.vy < 0:  # 上昇中に衝突
                    self.rect.top = block.bottom
                    self.vy = 0
                    self.image_rect.center = self.rect.center
                break

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

    def get_throw_velocity(self) -> tuple[float, float]:
        """
        プレイヤー方向への投擲初速ベクトルを返す（既存仕様維持）
        """
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return 0.0, 0.0
        speed = 8.0
        return dx / dist * speed, dy / dist * speed


class Bomb(pg.sprite.Sprite):
    """
    投げられた爆弾に関するクラス
    """
    def __init__(self, bomb_enemy: BombEnemy):
        super().__init__()
        # 爆弾の初速ベクトル
        vx, vy = bomb_enemy.get_throw_velocity()
        self.vx = vx
        self.vy = vy -0.5
        # 画像と角度合わせ
        bomb_img = pg.image.load("fig/bom3.png")
        angle = math.degrees(math.atan2(-self.vy, self.vx))
        self.image = pg.transform.rotozoom(bomb_img, angle, 1)
        self.rect = self.image.get_rect()
        
        # 発射位置を敵の中心から上方向にオフセット
        self.rect.center = bomb_enemy.image_rect.center
        self.rect.y -= 20  # 上方向に20ピクセル移動
        
        # 発射方向へのオフセット
        offset = max(bomb_enemy.rect.width, bomb_enemy.rect.height) // 2 + 6
        if not (vx == 0 and vy == 0):
            norm = math.hypot(vx, vy)
            if norm != 0:
                self.rect.centerx += int(vx / norm * offset)
                self.rect.centery += int(vy / norm * offset)

        # 爆発状態管理
        self.exploded = False
        self.boom_life = 0  # 爆発表示残フレーム数

    def update(self, blocks):
        if self.exploded:
            # 爆発中はカウントダウンして寿命が尽きたら削除
            self.boom_life -= 1
            if self.boom_life <= 0:
                self.kill()
            return

        # 少し重力を加えて落下させる
        self.vy += GRAVITY * 0.08
        # 位置更新（小数切り捨てで位置を進める）
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # 地面との衝突判定（衝突したら爆発表示に移行）
        for block in blocks:
            if self.rect.colliderect(block):
                # 衝突前の爆弾中心を保存（boom をここから表示する）
                old_center = self.rect.center
                # boom 画像に切り替え
                try:
                    boom_img = pg.image.load("fig/boom.png")
                except Exception:
                    boom_img = None

                if boom_img:
                    self.image = pg.transform.rotozoom(boom_img, 0, 1)
                    self.rect = self.image.get_rect(center=old_center)
                # 移動停止して爆発状態に切替
                self.vx = 0.0
                self.vy = 0.0
                self.exploded = True
                self.boom_life = 30  # 表示フレーム（必要に応じて調整）
                break

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class SlotEnemy(pg.sprite.Sprite):
    """
    スロットの敵に関するクラス
    """
    def __init__(self, x: int | None = None, y: int | None = None):
        super().__init__()
        slot_img = pg.image.load("fig/slot.png")
        self.image = pg.transform.rotozoom(slot_img, 0, 1)
        self.rect = pg.Rect(800, 150, TILE_SIZE, TILE_SIZE)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = self.rect.center

        if x is not None and y is not None:
            self.rect.centerx = int(x)
            self.rect.centery = int(y)
            self.image_rect.center = self.rect.center

        # 移動速度を遅めに設定
        self.speed = 1.5  # プレイヤーの移動速度(5)より遅く
        self.vx = 0.0
        self.vy = 0.0

        self.next_shot = random.randint(60, 180)
        self.weapon_speed = 8.0

    def update(self, blocks=None):
        # プレイヤーの方向を計算
        dx = player_rect.centerx - self.rect.centerx
        dy = 0  # Y方向は移動しない

        # 方向の正規化（単位ベクトル化）
        dist = abs(dx)
        if dist != 0:
            # X方向の速度を設定（正規化して speed を掛ける）
            self.vx = (dx / dist) * self.speed

        # 横移動
        self.rect.x += int(self.vx)
        self.image_rect.center = self.rect.center

        # ブロックとの横衝突で反転
        if blocks:
            for block in blocks:
                if self.rect.colliderect(block):
                    if self.vx > 0:
                        self.rect.right = block.left
                    else:
                        self.rect.left = block.right
                    self.vx = -self.vx
                    self.image_rect.center = self.rect.center
                    break

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)


class FireEnemy(pg.sprite.Sprite):
    """
    炎の敵に関するクラス
    """
    def __init__(self):
        super().__init__()
        fire_img = pg.image.load("fig/fire_enemy.png")
        fire_img = pg.transform.flip(fire_img, True, False)
        self.image = pg.transform.rotozoom(fire_img, 0, 1)
        self.rect = pg.Rect(700, 300, TILE_SIZE, TILE_SIZE)
        self.image_rect = self.image.get_rect(center=self.rect.center)
        self.vx = random.choice([-2, 2])
        # --- 追加: 垂直速度と接地フラグを初期化 ---
        self.vy = 0.0
        self.on_ground = False
        self.next_shot = random.randint(60, 180)
        self.weapon_speed = 6.0

    def update(self, blocks):
        # 横移動
        self.rect.x += int(self.vx)
        self.image_rect.center = self.rect.center

        # ブロックとの横衝突（反転）
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vx > 0:
                    self.rect.right = block.left
                else:
                    self.rect.left = block.right
                self.vx = -self.vx
                self.image_rect.center = self.rect.center
                break

        # Y方向：重力を加算して移動
        self.vy += GRAVITY
        self.rect.y += int(self.vy)

        # Y方向の衝突チェック（プレイヤーと同じロジック）
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block):
                if self.vy > 0:
                    self.rect.bottom = block.top
                    self.vy = 0
                    self.on_ground = True
                    self.image_rect.center = self.rect.center
                elif self.vy < 0:
                    self.rect.top = block.bottom
                    self.vy = 0
                    self.image_rect.center = self.rect.center
                break

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

class SlotWeapon(pg.sprite.Sprite):
    """
    スロットから発射される弾
    """
    def __init__(self, sx: int, sy: int, vx: float, vy: float):
        super().__init__()
        weapon_img = pg.image.load("fig/slot_weapon.png")
        angle = math.degrees(math.atan2(-vy, vx))
        self.image = pg.transform.rotozoom(weapon_img, angle, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (int(sx), int(sy))
        self.vx = float(vx)
        self.vy = float(vy)

    def update(self, blocks=None):
        self.rect.move_ip(int(self.vx), int(self.vy))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class FireWeapon(pg.sprite.Sprite):
    """
    炎の敵から発射される弾
    """
    def __init__(self, sx: int, sy: int, vx: float):
        super().__init__()
        weapon_img = pg.image.load("fig/fire.png")
        self.image = pg.transform.rotozoom(weapon_img, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = (int(sx), int(sy))
        self.vx = float(vx)
        self.base_y = float(sy - 80) 
        self.time = 0
        
    def update(self, blocks=None):
        self.rect.x += int(self.vx)
        # Y座標(振幅10ピクセルの範囲で動かす）
        self.time += 0.1
        self.rect.y = int(self.base_y + math.sin(self.time) * 10)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 3. ステージの「当たり判定用の四角形(Rect)」リストを作成
# (ゲーム開始時に一度だけ計算する)
block_rects = []
for y, row in enumerate(map_data):
    for x, tile_type in enumerate(row):
        if tile_type == 1:
            # (x座標, y座標, 幅, 高さ) 
            block_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 4. プレイヤー設定
# プレイヤーを (幅20, 高さ40) の四角形として定義
player_rect = pg.Rect(100, 100, TILE_SIZE // 2, TILE_SIZE) # 初期位置(100,100)
player_velocity_y = 0  # プレイヤーの垂直方向の速度
is_on_ground = False     # 地面（ブロック）に接地しているか
player_move_left = False # 左に移動中か
player_move_right = False# 右に移動中か

# --- 追加: フレームタイマーをここで初期化（tmrが使用される前に必ず定義） ---
tmr = 0

# 爆弾の敵
bomb_enemies = pg.sprite.Group()
bomb_enemy = BombEnemy()
bomb_enemies.add(bomb_enemy)

# 炎の敵を追加
fire_enemies = pg.sprite.Group()
fire_enemy = FireEnemy()
fire_enemies.add(fire_enemy)

# 炎の弾のグループを追加
fire_weapons = pg.sprite.Group()

# 投げた爆弾のグループ
bombs = pg.sprite.Group()

# ここにスロット敵用のグループを追加
slot_enemies = pg.sprite.Group()
# スロットから発射される弾のグループ
slot_weapons = pg.sprite.Group()
slot_enemies.add(SlotEnemy())

# タイマーを初期化（tmr が未定義だったため追加）
tmr = 0

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
                player_move_left = True
            if event.key == pg.K_RIGHT:
                player_move_right = True
            if event.key == pg.K_UP and is_on_ground:
                player_velocity_y = JUMP_STRENGTH # 上向きの速度を与える
                is_on_ground = False
        
        # キーが離された時
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player_move_left = False
            if event.key == pg.K_RIGHT:
                player_move_right = False

    # 7. プレイヤーのロジック更新 (移動と当たり判定)
    
    # --- 左右の移動と当たり判定 ---
    player_movement_x = 0
    if player_move_left:
        player_movement_x -= PLAYER_SPEED
    if player_move_right:
        player_movement_x += PLAYER_SPEED
    
    player_rect.x += player_movement_x # まずX方向に動かす
    
    # X方向の衝突チェック
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_movement_x > 0: # 右に移動中に衝突
                player_rect.right = block.left # 右端をブロックの左端に合わせる
            elif player_movement_x < 0: # 左に移動中に衝突
                player_rect.left = block.right # 左端をブロックの右端に合わせる

    # --- 垂直方向（重力・ジャンプ）の移動と当たり判定 ---
    player_velocity_y += GRAVITY # 重力を速度に加算
    player_rect.y += player_velocity_y # Y方向に動かす
    
    # Y方向の衝突チェック
    is_on_ground = False # 毎フレーム「接地していない」と仮定
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_velocity_y > 0: # 落下中に衝突
                player_rect.bottom = block.top # 足元をブロックの上端に合わせる
                player_velocity_y = 0 # 落下速度をリセット
                is_on_ground = True   # 接地フラグを立てる
            elif player_velocity_y < 0: # ジャンプ中に衝突
                player_rect.top = block.bottom # 頭をブロックの下端に合わせる
                player_velocity_y = 0 # 上昇速度をリセット（頭を打った）

    # 爆弾の敵がプレイヤーに向かって投げる1〜2秒ごとに
    for b_enemy in bomb_enemies:
        if tmr >= b_enemy.next_throw:
            bombs.add(Bomb(b_enemy))
            b_enemy.next_throw = tmr + random.randint(60, 120)

    # SlotEnemy からの発射処理（直線、同じ速さ、追尾なし）
    for s in slot_enemies:
        # s.next_shot はフレームカウント (tmr) ベース
        if tmr >= getattr(s, "next_shot", 0):
            # 位置は s.image_rect.center を起点にする
            sx, sy = s.image_rect.center
            # プレイヤー方向へ向かわせる（追尾しない -> 初速のみ設定）
            dx = player_rect.centerx - sx
            dy = player_rect.centery - sy
            dist = math.hypot(dx, dy)
            if dist == 0:
                vx = 0.0
                vy = 0.0
            else:
                vx = dx / dist * s.weapon_speed
                vy = dy / dist * s.weapon_speed
            # 弾を生成してグループへ追加
            slot_weapons.add(SlotWeapon(sx, sy, vx, vy))
            # 次の発射タイミングを設定（ランダム間隔）
            s.next_shot = tmr + random.randint(90, 240)
            
    # 炎の敵から発射処理
    for f_enemy in fire_enemies:
        if tmr >= getattr(f_enemy, "next_shot", 0):
            # 発射位置を設定（敵の中心から）
            sx, sy = f_enemy.image_rect.center
            # プレイヤーの方向に応じて速度の符号を決定
            vx = f_enemy.weapon_speed
            if player_rect.centerx < f_enemy.rect.centerx:
                vx = -f_enemy.weapon_speed
                # 左向きの場合、敵の左側から発射
                sx = f_enemy.rect.left - 5
            else:
                # 右向きの場合、敵の右側から発射
                sx = f_enemy.rect.right + 5
            
            # 弾を生成してグループへ追加（Y座標はそのまま中心を使用）
            fire_weapons.add(FireWeapon(sx, sy, vx))
            # 次の発射タイミングを設定
            f_enemy.next_shot = tmr + random.randint(90, 240)

    # 8. 描画処理
    screen.fill(WHITE) # 画面を黒で塗りつぶし
    
    # ステージ（ブロック）を描画
    for block in block_rects:
        pg.draw.rect(screen, BLACK, block)
        
    # プレイヤーを描画
    pg.draw.rect(screen, GREEN, player_rect)
    
    # 爆弾の敵の更新と描画
    for b_enemy in bomb_enemies:
        b_enemy.update(block_rects)
        b_enemy.draw(screen)

    # 炎の敵の更新と描画
    for f_enemy in fire_enemies:
        f_enemy.update(block_rects)
        f_enemy.draw(screen)

    # 投げられた爆弾の更新と描画
    for b in list(bombs):
        b.update(block_rects)
        b.draw(screen)
    
    # SlotEnemy の弾を更新・描画（画面外に出たら削除）
    for w in list(slot_weapons):
        w.update(block_rects)
        w.draw(screen)
        # 画面外チェックで削除
        if w.rect.right < 0 or w.rect.left > SCREEN_WIDTH or w.rect.bottom < 0 or w.rect.top > SCREEN_HEIGHT:
            slot_weapons.remove(w)
    
    # SlotEnemy の更新
    for s in slot_enemies:
        s.update(block_rects)

    # SlotEnemy を描画
    for s in slot_enemies:
        s.draw(screen)

    # 炎の弾の更新と描画
    for w in list(fire_weapons):
        w.update()
        w.draw(screen)
        # 画面外チェックで削除
        if w.rect.right < 0 or w.rect.left > SCREEN_WIDTH:
            fire_weapons.remove(w)

    # 画面を更新
    pg.display.flip()
    
    # 9. FPS (フレームレート) の制御
    clock.tick(60) # 1秒間に60回ループが回るように調整
    # タイマーを進める
    tmr += 1

# ループが終了したらpgを終了
pg.quit()