import pygame
import os
import random

# 1. 定数と初期設定
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
TILE_SIZE = 40
GRAVITY = 0.8         # 重力
JUMP_STRENGTH = -15   # ジャンプ力 (Y軸は上がマイナス)
PLAYER_SPEED = 5      # 左右の移動速度

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)   # プレイヤーの色
BROWN = (139, 69, 19)   # ブロックの色

# 画面設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2Dアクションゲーム デモ")
clock = pygame.time.Clock()

# 2. ステージデータ (0=空, 1=ブロック)
# 画面下部が地面、途中に浮島があるマップ
map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
block_rects = []

# ==== 追加：炎の玉 & かーびー ====
class FireBall:
    """炎の玉：横に飛び、寿命で消える"""
    def __init__(self, x, y, direction):
        try:
            self.image = pygame.image.load("fig/fire.jpg").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
        except Exception:
            self.image = None  # 画像が無い場合は自前描画
        # rect は中心位置で受け取るようにする
        self.rect = pygame.Rect(0, 0, 25, 25)
        self.rect.center = (x, y)
        self.speed = 12 * direction  # 水平速度
        # 垂直方向の物理 (重力 + バウンド)
        self.vy = 0
        self.gravity = 0.8
        self.damping = 0.6  # バウンドで減衰する係数
        # 寿命（フレーム数）
        self.life = 120  # バウンドさせるため少し長めにする

    def update(self, screen):
        # 移動（X 方向）
        self.rect.x += int(self.speed)

        # ブロックとの水平衝突で反転（壁に当たれば跳ね返る）
        for block in block_rects:
            if self.rect.colliderect(block):
                # 衝突の向きによって処理
                if self.speed > 0:
                    self.rect.right = block.left
                else:
                    self.rect.left = block.right
                # 水平速度を反転して減衰
                self.speed = -self.speed * 0.6

        # 垂直方向の物理（重力適用）
        self.vy += self.gravity
        self.rect.y += int(self.vy)

        # ブロックとの垂直衝突（地面や天井で跳ね返す）
        for block in block_rects:
            if self.rect.colliderect(block):
                if self.vy > 0:
                    # 落下中にブロックと衝突 => 足元をブロックの上に合わせ、反射
                    self.rect.bottom = block.top
                    self.vy = -self.vy * self.damping
                elif self.vy < 0:
                    # 上昇中に頭が当たった
                    self.rect.top = block.bottom
                    self.vy = 0

        # 寿命減少
        self.life -= 1

        # 画面外 or 寿命切れで消滅（横にはみ出し過ぎたら消す）
        if self.life <= 0 or self.rect.right < -50 or self.rect.left > SCREEN_WIDTH + 50:
            return False

        # 描画
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            # 発光風の炎（画像が無いとき用）
            import random
            r = random.randint(200, 255)
            g = random.randint(60, 150)
            y = random.randint(0, 60)
            color = (r, g, y)
            for i in range(3):
                radius = max(1, 10 - i * 3)
                pygame.draw.circle(screen, color, self.rect.center, radius)
        return True


class BreathParticle:
    """短距離の吐息（短命・ノー重力）"""
    def __init__(self, x, y, direction):
        # 向きと遅い速度（近距離ストリーム風）
        self.facing = direction
        self.speed = 4 * direction  # 以前より遅くしてストリーム感を出す
        self.life = 30
        img = None
        # 優先して吐息用画像を読み込む（fire_a.pngは参照しない）
        if direction >= 0:
            candidates = ("fig/fire_right.png", "fig/fire.jpg")
        else:
            candidates = ("fig/fire_reft.png", "fig/fire.jpg")
        for fname in candidates:
            try:
                img = pygame.image.load(fname).convert_alpha()
                break
            except Exception:
                img = None
        if img:
            # 吐息は横長にして少し大きめに
            w = 64
            h = 28
            img = pygame.transform.scale(img, (w, h))
            # 左向きなら反転（ファイルが左向きでない場合に備える）
            if direction < 0:
                img = pygame.transform.flip(img, True, False)
            self.image = img
            self.rect = self.image.get_rect()
            # 口元に沿わせるため、画像の左端/右端を口の位置に合わせる
            if direction >= 0:
                # 右向き: 画像の左端が口になるように設定
                self.rect.midleft = (x, y)
            else:
                # 左向き: 画像の右端が口になるように設定
                self.rect.midright = (x, y)
        else:
            # 画像がなければ円で表現
            self.image = None
            self.rect = pygame.Rect(0, 0, 12, 12)
            if direction >= 0:
                self.rect.midleft = (x, y)
            else:
                self.rect.midright = (x, y)

    def update(self, screen):
        # 水平方向に移動
        self.rect.x += int(self.speed)
        self.life -= 1

        # ブロックに当たれば消える
        for block in block_rects:
            if self.rect.colliderect(block):
                return False

        # 画面外で消える
        if self.life <= 0 or self.rect.right < -40 or self.rect.left > SCREEN_WIDTH + 40:
            return False

        # 描画（画像があれば画像、無ければ円）
        if self.image:
            # 少し上下にゆらぎを入れて炎らしく見せる
            dy = random.randint(-3, 3)
            # グロー（薄い半透明の円）を先に描く
            glow_surf = pygame.Surface((self.rect.width * 2, self.rect.height * 2), pygame.SRCALPHA)
            glow_color = (255, 180, 70, 80)
            pygame.draw.ellipse(glow_surf, glow_color, glow_surf.get_rect())
            screen.blit(glow_surf, (self.rect.centerx - glow_surf.get_width() // 2, self.rect.centery - glow_surf.get_height() // 2 + dy))
            # 本体を描画
            screen.blit(self.image, (self.rect.x, self.rect.y + dy))
        else:
            color = (255, 160, 60)
            pygame.draw.circle(screen, color, self.rect.center, 6)
        return True


class CrashEffect:
    """自己中心の爆発エフェクト（非破壊・視覚効果）"""
    def __init__(self, center):
        self.center = center
        self.life = 20
        self.max_radius = 90
        # 可能なら画像を読み込んで爆発に使う
        self.image = None
        try:
            img = pygame.image.load("fig/fire_crash.png").convert_alpha()
            self.image = img
        except Exception:
            self.image = None

    def update(self, screen):
        t = (20 - self.life) / 20.0
        radius = int(self.max_radius * t)
        # 画像があれば画像をスケールしてアルファで描画、無ければ半透明サーフェスで描画
        if self.image:
            # スケールサイズは現在の radius に合わせる（直径）
            size = max(2, radius * 2)
            try:
                img = pygame.transform.smoothscale(self.image, (size, size))
            except Exception:
                img = pygame.transform.scale(self.image, (size, size))
            # フェードアウトするアルファ
            alpha = int(220 * (1.0 - t))
            img.set_alpha(alpha)
            screen.blit(img, (self.center[0] - size // 2, self.center[1] - size // 2))
        else:
            surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            alpha = int(200 * (1.0 - t))
            pygame.draw.circle(surf, (255, 180, 80, alpha), (self.max_radius, self.max_radius), max(1, radius))
            screen.blit(surf, (self.center[0] - self.max_radius, self.center[1] - self.max_radius))
        self.life -= 1
        return self.life > 0


class kirby_fire:
    """かーびー本体（見た目＋炎の管理だけ。移動や当たり判定は既存ロジックを使用）"""
    def __init__(self, player_rect_ref):
        try:
            self.img = pygame.image.load("fig/kirby_fire.png").convert_alpha()
            self.img = pygame.transform.scale(self.img, (50, 50))
        except Exception:
            self.img = None  # 無ければ四角のまま
        self.rect = player_rect_ref  # 既存の player_rect を共有
        self.rect.size = (28, 28)  # かーびーのサイズに合わせる
        self.fireballs = []
        # 吐息（短距離）用
        self.breaths = []
        self.breathing = False
        self._breath_spawn_timer = 0
        # クラッシュ（範囲攻撃）用
        self.crashes = []
    # クールタイム無しにする（いつでも発動可能）
        # 向き（1=右, -1=左）
        self.facing = 1

    def handle_input(self, event, move_left, move_right):
        # 向き更新
        if move_left and not move_right:
            self.facing = -1
        elif move_right and not move_left:
            self.facing = 1
        # Zキーで炎発射（進行方向に飛ぶ）
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            direction = -1 if (move_left and not move_right) else 1
            # 発射位置：口の位置に合わせる（体の前方・少し上）
            fx = self.rect.centerx + self.facing * (self.rect.width // 2)
            fy = self.rect.centery - 6
            self.fireballs.append(FireBall(fx, fy, direction))

        # Xキーで吐息（押している間持続）
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.breathing = True
        if event.type == pygame.KEYUP and event.key == pygame.K_x:
            self.breathing = False

        # Cキーでクラッシュ（単発・クールタイム無し）
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            # クールダウンなしで常に発動可能にする
            self.crashes.append(CrashEffect(self.rect.center))
    def draw_and_update(self, screen):

        # 炎の更新＆描画（生存管理）
        alive = []
        for fb in self.fireballs:
            if fb.update(screen):
                alive.append(fb)
        self.fireballs = alive

        # 吐息のスポーン（押している間）
        if self.breathing:
            self._breath_spawn_timer -= 1
            if self._breath_spawn_timer <= 0:
                # 発射位置は口のすぐ前（中心から幅の半分だけ前）
                fx = self.rect.centerx + self.facing * (self.rect.width // 2)
                fy = self.rect.centery - 4
                self.breaths.append(BreathParticle(fx, fy, self.facing))
                self._breath_spawn_timer = 2  # 連射速度（小さくして連続感を強める）

        # 吐息更新
        alive_b = []
        for bp in self.breaths:
            if bp.update(screen):
                alive_b.append(bp)
        self.breaths = alive_b

        # クラッシュエフェクト更新
        alive_c = []
        for ce in self.crashes:
            if ce.update(screen):
                alive_c.append(ce)
        self.crashes = alive_c

        # 本体描画（画像があれば画像）
        if self.img:
            screen.blit(self.img, self.rect)
        else:
            pygame.draw.rect(screen, (50, 200, 50), self.rect)
# ==== 追加ここまで ====


for y, row in enumerate(map_data):
    for x, tile_type in enumerate(row):
        if tile_type == 1:
            # (x座標, y座標, 幅, 高さ) のRectを作成
            block_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 4. プレイヤー設定
# プレイヤーを (幅20, 高さ40) の四角形として定義
player_rect = pygame.Rect(100, 100, TILE_SIZE // 2, TILE_SIZE) 
player_velocity_y = 0  # プレイヤーの垂直方向の速度
is_on_ground = False     # 地面（ブロック）に接地しているか
player_move_left = False # 左に移動中か
player_move_right = False# 右に移動中か
kirby = kirby_fire(player_rect)  # かーびーオブジェクトを作成


# 5. ゲームループ
running = True
while running:
    
    # 6. イベント処理 (キー操作など)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # キーが押された時
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move_left = True
            if event.key == pygame.K_RIGHT:
                player_move_right = True
            if event.key == pygame.K_SPACE and is_on_ground:
                player_velocity_y = JUMP_STRENGTH # 上向きの速度を与える
                is_on_ground = False
        
        # キーが離された時
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_move_left = False
            if event.key == pygame.K_RIGHT:
                player_move_right = False
        kirby.handle_input(event, player_move_left, player_move_right)

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

    # 8. 描画処理
    screen.fill((255, 255, 255)) # 画面塗りつぶし
    
    # ステージ（ブロック）を描画
    for block in block_rects:
        pygame.draw.rect(screen, BROWN, block)
        
    # プレイヤーを描画
    kirby.draw_and_update(screen)

    
    # 画面を更新
    pygame.display.flip()
    
    # 9. FPS (フレームレート) の制御
    clock.tick(60) # 1秒間に60回ループが回るように調整

# ループが終了したらPygameを終了
pygame.quit()