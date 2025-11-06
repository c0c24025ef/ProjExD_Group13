import pygame as pg
import os
import time

# 1. 定数と初期設宁E
pg.init()
# サウンドミキサーを�E示皁E��初期化（周波数、ビチE��深度、チャンネル数を指定！E
pg.mixer.quit()  # 一度終亁E
pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
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
BROWN = (139, 69, 19)   # ブロチE��の色
RED = (255, 0, 0)       # 爁E��エフェクト�E色
ORANGE = (255, 165, 0)  # 爁E��エフェクト�E色

# ========================================
# 個人実裁E ボムコピ�E能力シスチE�� (C0C24001)
# カービィが敵を吸ぁE��んでコピ�Eする能力として実裁E
# ========================================
C0C24001_BOMB_FUSE_TIME = 3.0  # 爁E��の導火線�E時間(私E
C0C24001_BOMB_EXPLOSION_DURATION = 0.5  # 爁E��エフェクト�E表示時間(私E
C0C24001_BOMB_EXPLOSION_RADIUS = TILE_SIZE * 3  # 爁E��篁E��の半征E

# 画面設宁E
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("2Dアクションゲーム チE��")
clock = pg.time.Clock()

# 2. スチE�EジチE�Eタ (0=空, 1=ブロチE��)
# 画面下部が地面、E��中に浮島がある�EチE�E
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

# 3. スチE�Eジの「当たり判定用の四角形(Rect)」リストを作�E
# (ゲーム開始時に一度だけ計算すめE
block_rects = []
for y, row in enumerate(map_data):
    for x, tile_type in enumerate(row):
        if tile_type == 1:
            # (x座樁E y座樁E 幁E 高さ) のRectを作�E
            block_rects.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 3.5 ボムコピ�E能力シスチE��の定義
# ========================================
# 個人実裁E���E: ボムコピ�E能劁E(C0C24001)
# カービィが敵を吸ぁE��んでコピ�Eする能力として実裁E
# ========================================

class C0C24001_BombAbility:
    """ボムコピ�E能力クラス (C0C24001実裁E
    
    カービィが�E弾を持つ敵を吸ぁE��んだ後に使えるようになる�E劁E
    
    使ぁE��:
    1. 他�Eメンバ�Eの吸ぁE��みシスチE��から activate() を呼ぶ
    2. プレイヤーがBキーを押しためEuse_ability() を呼ぶ
    3. 返り値の爁E��オブジェクトを bombs リストに追加
    """
    def __init__(self):
        self.has_ability = False  # ボム能力を持ってぁE��ぁE
        
    def activate(self):
        """ボム能力を取征E敵を吸ぁE��んだ時に呼ばれる)"""
        self.has_ability = True
        print("【�Eム能力を取征E、E)
        
    def deactivate(self):
        """ボム能力を失ぁE""
        self.has_ability = False
        print("【�Eム能力を失った、E)
        
    def use_ability(self, player_pos, player_facing_right, ability_type="place"):
        """ボム能力を使用
        
        Args:
            player_pos: プレイヤーの位置 (rect)
            player_facing_right: プレイヤーの向き
            ability_type: "place"(設置), "throw"(投擲), "kick"(キチE��)
            
        Returns:
            爁E��オブジェクチEまた�E None
        """
        if not self.has_ability:
            return None
            
        # 爁E��を生成して返す
        if ability_type == "place":
            bomb_x = player_pos.centerx - TILE_SIZE // 2
            bomb_y = player_pos.bottom - TILE_SIZE
            return C0C24001_BombProjectile(bomb_x, bomb_y, velocity_x=0, velocity_y=1)
        elif ability_type == "throw":
            bomb_x = player_pos.centerx - TILE_SIZE // 2
            bomb_y = player_pos.centery - TILE_SIZE // 2
            throw_speed_x = 10 if player_facing_right else -10
            throw_speed_y = -8
            return C0C24001_BombProjectile(bomb_x, bomb_y, velocity_x=throw_speed_x, velocity_y=throw_speed_y)
        
        return None

class C0C24001_BombProjectile:
    """爁E��プロジェクタイルクラス (C0C24001実裁E
    
    ボム能力で生�Eされる�E弾オブジェクチE
    
    実裁E���E:
    - 物琁E��箁E重力、跳ね返り、摩擦)
    - 爁E��タイマ�EとエフェクチE
    - GIFアニメーション表示
    """
    def __init__(self, x, y, velocity_x=0, velocity_y=0):
        self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.placed_time = time.time()  # 設置時刻
        self.is_exploded = False  # 爁E��したぁE
        self.explosion_time = None  # 爁E��時刻
        self.velocity_x = velocity_x  # X方向�E速度
        self.velocity_y = velocity_y  # Y方向�E速度
        self.on_ground = False  # 地面に接地してぁE��ぁE
        
    def update(self, block_rects):
        """爁E��の状態を更新"""
        current_time = time.time()
        
        # まだ爁E��してぁE��ぁE��合、時間経過をチェチE��
        if not self.is_exploded:
            if current_time - self.placed_time >= C0C24001_BOMB_FUSE_TIME:
                self.is_exploded = True
                self.explosion_time = current_time
                return True  # 爁E��した
            
            # 速度がある場合、�E弾を移動させる
            if self.velocity_x != 0 or self.velocity_y != 0:
                # 重力を適用
                self.velocity_y += GRAVITY * 0.5  # 爁E��用の重力�E�少し弱めE��E
                
                # X方向�E移勁E
                self.rect.x += self.velocity_x
                
                # X方向�E衝突チェチE���E�壁で跳ね返る�E�E
                for block in block_rects:
                    if self.rect.colliderect(block):
                        if self.velocity_x > 0:  # 右に移動中
                            self.rect.right = block.left
                            self.velocity_x = -self.velocity_x * 0.5  # 跳ね返る�E�減衰�E�E
                        elif self.velocity_x < 0:  # 左に移動中
                            self.rect.left = block.right
                            self.velocity_x = -self.velocity_x * 0.5
                
                # 画面端で跳ね返る
                if self.rect.left < 0:
                    self.rect.left = 0
                    self.velocity_x = -self.velocity_x * 0.5
                elif self.rect.right > SCREEN_WIDTH:
                    self.rect.right = SCREEN_WIDTH
                    self.velocity_x = -self.velocity_x * 0.5
                
                # Y方向�E移勁E
                self.rect.y += self.velocity_y
                
                # Y方向�E衝突チェチE��
                self.on_ground = False
                for block in block_rects:
                    if self.rect.colliderect(block):
                        if self.velocity_y > 0:  # 落下中
                            self.rect.bottom = block.top
                            self.velocity_y = -self.velocity_y * 0.3  # 少し跳ねめE
                            self.on_ground = True
                            # 摩擦で減送E
                            self.velocity_x *= 0.9
                            if abs(self.velocity_x) < 0.5:
                                self.velocity_x = 0
                        elif self.velocity_y < 0:  # 上�E中
                            self.rect.top = block.bottom
                            self.velocity_y = 0
                
                # 画面下端チェチE��
                if self.rect.bottom > SCREEN_HEIGHT:
                    self.rect.bottom = SCREEN_HEIGHT
                    self.velocity_y = 0
                    self.on_ground = True
                    self.velocity_x *= 0.9
                    if abs(self.velocity_x) < 0.5:
                        self.velocity_x = 0
                        
        return False
    
    def is_explosion_finished(self):
        """爁E��エフェクトが終亁E��たか"""
        if self.is_exploded and self.explosion_time:
            return time.time() - self.explosion_time >= C0C24001_BOMB_EXPLOSION_DURATION
        return False
    
    def draw(self, surface, bomb_image, explosion_frames):
        """爁E��また�E爁E��エフェクトを描画"""
        if self.is_exploded:
            # 爁E��エフェクトを描画
            if explosion_frames and len(explosion_frames) > 0:
                # アニメーションフレームを表示
                elapsed_time = time.time() - self.explosion_time
                # フレームレーチE 0.05秒ごとに刁E��替ぁE20fps)
                frame_index = int(elapsed_time / 0.05) % len(explosion_frames)
                current_frame = explosion_frames[frame_index]
                
                explosion_center = self.rect.center
                explosion_rect = current_frame.get_rect(center=explosion_center)
                surface.blit(current_frame, explosion_rect.topleft)
            else:
                # 画像がなぁE��合�E冁E��表現
                explosion_center = self.rect.center
                # 外�Eの冁E赤)
                pg.draw.circle(surface, RED, explosion_center, C0C24001_BOMB_EXPLOSION_RADIUS, 0)
                # 中間�E冁Eオレンジ)
                pg.draw.circle(surface, ORANGE, explosion_center, C0C24001_BOMB_EXPLOSION_RADIUS * 2 // 3, 0)
                # 冁E�Eの冁E黁E��)
                pg.draw.circle(surface, (255, 255, 0), explosion_center, C0C24001_BOMB_EXPLOSION_RADIUS // 3, 0)
        else:
            # 爁E��画像を描画
            surface.blit(bomb_image, self.rect.topleft)
    
    def get_explosion_rect(self):
        """爁E��篁E��の矩形を返す"""
        if self.is_exploded:
            center = self.rect.center
            explosion_rect = pg.Rect(
                center[0] - C0C24001_BOMB_EXPLOSION_RADIUS,
                center[1] - C0C24001_BOMB_EXPLOSION_RADIUS,
                C0C24001_BOMB_EXPLOSION_RADIUS * 2,
                C0C24001_BOMB_EXPLOSION_RADIUS * 2
            )
            return explosion_rect
        return None

# 4. プレイヤー設宁E
# 画像を読み込み、E��刁E��サイズに縮小して表示
# img/bom2.png を使ぁE��見つからなぁE�E読み込めなぁE��合�E四角形で代替表示する、E
PLAYER_DISPLAY_SIZE = TILE_SIZE * 2.0  # 表示サイズをタイルの2倍に設宁E
try:
    player_image_original = pg.image.load(os.path.join("img", "bom2.png")).convert_alpha()
    original_width = player_image_original.get_width()
    original_height = player_image_original.get_height()
    print(f"プレイヤー画像を読み込みました: img/bom2.png (允E��イズ: {original_width}x{original_height})")
    # 表示サイズに合わせてスケーリング
    player_image_original = pg.transform.smoothscale(player_image_original, (int(PLAYER_DISPLAY_SIZE), int(PLAYER_DISPLAY_SIZE)))
    print(f"表示サイズに変更: {int(PLAYER_DISPLAY_SIZE)}x{int(PLAYER_DISPLAY_SIZE)}")
except Exception:
    # 画像がなぁE��合�EチE��ォルトサイズ
    PLAYER_DISPLAY_SIZE = TILE_SIZE * 2.0
    player_image_original = pg.Surface((TILE_SIZE // 2, TILE_SIZE), pg.SRCALPHA)
    player_image_original.fill(GREEN)
    print("プレイヤー画像が見つかりません。デフォルトサイズを使用します、E)

# 右向きと左向きの画像を用意！Elip も透過を保持�E�E
player_image_right = player_image_original
player_image_left = pg.transform.flip(player_image_original, True, False)
player_image = player_image_right  # チE��ォルト�E右向き

# 画像�E実際のサイズを取征E
PLAYER_IMAGE_WIDTH = PLAYER_DISPLAY_SIZE
PLAYER_IMAGE_HEIGHT = PLAYER_DISPLAY_SIZE

# プレイヤーの当たり判定用のRect(画像より少し小さめにして足允E��調整)
# 画像サイズに基づぁE��当たり判定を設宁E
player_rect = pg.Rect(100, 100, PLAYER_IMAGE_WIDTH * 0.6, PLAYER_IMAGE_HEIGHT * 0.5)
player_velocity_y = 0  # プレイヤーの垂直方向�E速度
is_on_ground = False     # 地面�E�ブロチE���E�に接地してぁE��ぁE
player_move_left = False # 左に移動中ぁE
player_move_right = False# 右に移動中ぁE
player_facing_right = True # プレイヤーの向き�E�Erue=右向き, False=左向き�E�E

# ========================================
# 個人実裁E 爁E��画像�E読み込み (C0C24001)
# ========================================
try:
    c0c24001_bomb_image = pg.image.load(os.path.join("img", "bom3.png")).convert_alpha()
    c0c24001_bomb_image = pg.transform.smoothscale(c0c24001_bomb_image, (TILE_SIZE, TILE_SIZE))
except Exception:
    # 画像がなぁE��合�E黒い冁E��代替
    c0c24001_bomb_image = pg.Surface((TILE_SIZE, TILE_SIZE), pg.SRCALPHA)
    pg.draw.circle(c0c24001_bomb_image, BLACK, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)

# 爁E��エフェクト画像�E読み込み�E�EIFアニメーション対応！E
try:
    from PIL import Image
    # PILでGIFを読み込んでフレームを抽出
    gif_path = os.path.join("img", "bakuha.gif")
    pil_gif = Image.open(gif_path)
    
    c0c24001_explosion_frames = []
    c0c24001_explosion_size = C0C24001_BOMB_EXPLOSION_RADIUS * 2
    
    # 全フレームを読み込む
    try:
        frame_index = 0
        while True:
            pil_gif.seek(frame_index)
            # PILイメージをPygameサーフェスに変換
            frame = pil_gif.convert("RGBA")
            frame_data = frame.tobytes()
            pygame_surface = pg.image.fromstring(frame_data, frame.size, "RGBA")
            # スケーリング
            pygame_surface = pg.transform.smoothscale(pygame_surface, (c0c24001_explosion_size, c0c24001_explosion_size))
            c0c24001_explosion_frames.append(pygame_surface)
            frame_index += 1
    except EOFError:
        pass  # 全フレーム読み込み完亁E
    
    if c0c24001_explosion_frames:
        print(f"爁E��エフェクト画像を読み込みました: img/bakuha.gif ({len(c0c24001_explosion_frames)}フレーム)")
    else:
        c0c24001_explosion_frames = None
        print("GIFフレームの読み込みに失敗しました")
        
except ImportError:
    c0c24001_explosion_frames = None
    print("警呁E Pillow (PIL) がインスト�EルされてぁE��せん")
    print("GIFアニメーションを使用するには 'pip install pillow' を実行してください")
    print("チE��ォルト�E冁E��エフェクトを使用します、E)
except Exception as e:
    c0c24001_explosion_frames = None
    print(f"爁E��エフェクト画像�E読み込みに失敁E {e}")
    print("チE��ォルト�E冁E��エフェクトを使用します、E)

# 背景画像�E読み込み
try:
    background_image = pg.image.load(os.path.join("img", "haikei.jpg")).convert()
    # 画面サイズに合わせてスケーリング
    background_image = pg.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("背景画像を読み込みました: img/haikei.jpg")
except Exception as e:
    # 画像がなぁE��合�E黒背景
    background_image = None
    print(f"背景画像�E読み込みに失敁E {e}")
    print("黒背景を使用します、E)

# 爁E��音の読み込み
explosion_sound = None
sound_paths = [
    os.path.join("bgm", "bom.mp3"),
    os.path.join("bgm", "bom.wav"),
    os.path.join("img", "bom.mp3"),
    os.path.join("img", "bom.wav"),
    "bom.mp3",
    "bom.wav"
]

for sound_path in sound_paths:
    try:
        if os.path.exists(sound_path):
            explosion_sound = pg.mixer.Sound(sound_path)
            print(f"爁E��音を読み込みました: {sound_path}")
            break
    except Exception as e:
        print(f"音声ファイル {sound_path} の読み込みに失敁E {e}")

if explosion_sound is None:
    print("警呁E 爁E��音ファイルが見つかりません、E)
    print("bgm/bom.mp3 また�E img/bom.wav を�E置してください、E)

# BGM�E�背景音楽�E��E読み込みと再生
print("BGMの読み込みを開姁E..")
# 褁E��の形式を試す！EGGを優先！E
bgm_files = [
    ("bgm", "music.ogg"),   # OGG形式（推奨�E�E
    ("bgm", "music.wav"),   # WAV形弁E
    ("bgm", "music.mp3"),   # MP3形式（互換性に問題がある場合あり！E
]

bgm_loaded = False
for folder, filename in bgm_files:
    bgm_path = os.path.join(folder, filename)
    if os.path.exists(bgm_path):
        print(f"ファイルが見つかりました: {bgm_path}")
        try:
            pg.mixer.music.load(bgm_path)
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(-1)
            print(f"✁EBGMの再生を開始しました: {filename}")
            bgm_loaded = True
            break
        except pg.error as e:
            print(f"✁E{filename} の読み込みに失敁E {e}")
            continue

if not bgm_loaded:
    print("=" * 60)
    print("【BGMが�E生できませんでした、E)
    print("MP3ファイルがPygameと互換性がなぁE��能性があります、E)
    print("")
    print("解決方法！E)
    print("1. https://convertio.co/ja/mp3-ogg/ で変換")
    print("2. music.mp3 めEOGG形式に変換")
    print("3. 変換したファイル(music.ogg)をbgmフォルダに保孁E)
    print("")
    print("ゲームは音楽なしで続行します、E)
    print("=" * 60)

# ========================================
# 個人実裁E 爁E��能力シスチE�� (C0C24001)
# ========================================
# 爁E��能力�Eネ�Eジャー�E�カービィのコピ�E能力として管琁E��E
c0c24001_bomb_ability = C0C24001_BombAbility()

# チE��ト用: 能力を初期状態で有効化（実際のゲームでは敵を吸ぁE��んで取得！E
# マ�Eジ時�E、吸ぁE��み機�E実裁E��E��c0c24001_bomb_ability.activate()を呼び出ぁE
c0c24001_bomb_ability.activate()
print("【テストモード】�E弾能力が有効化されました。�Eージ時�Eこ�E行を削除してください、E)

# 爁E��リスト（設置された�E弾を管琁E��E
c0c24001_bombs = []

# 5. ゲームルーチE
running = True
while running:
    
    # 6. イベント�E琁E(キー操作など)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        # キーが押された時
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_move_left = True
            if event.key == pg.K_RIGHT:
                player_move_right = True
            if event.key == pg.K_SPACE and is_on_ground:
                player_velocity_y = JUMP_STRENGTH # 上向き�E速度を与えめE
                is_on_ground = False
            
            # ========================================
            # 個人実裁E 爁E��操佁E(C0C24001)
            # ========================================
            if event.key == pg.K_b:
                # 爁E��能力を持ってぁE��場合�Eみ使用可能
                if c0c24001_bomb_ability.has_ability:
                    # Shiftキーが押されてぁE��場合�E投擲、それ以外�E設置
                    keys = pg.key.get_pressed()
                    if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                        # 爁E��を投擲�E�前方に投げる！E
                        bomb_x = player_rect.centerx - TILE_SIZE // 2
                        bomb_y = player_rect.centery - TILE_SIZE // 2
                        # プレイヤーの向きに応じて速度を設宁E
                        throw_speed_x = 10 if player_facing_right else -10
                        throw_speed_y = -8  # 上向きに投げめE
                        new_bomb = C0C24001_BombProjectile(bomb_x, bomb_y, velocity_x=throw_speed_x, velocity_y=throw_speed_y)
                        c0c24001_bombs.append(new_bomb)
                    else:
                        # 爁E��を設置�E��Eレイヤーの足允E��設置し、E��力で落下！E
                        bomb_x = player_rect.centerx - TILE_SIZE // 2
                        bomb_y = player_rect.bottom - TILE_SIZE
                        # 設置時に初期速度を設定（重力で落下させる�E�E
                        new_bomb = C0C24001_BombProjectile(bomb_x, bomb_y, velocity_x=0, velocity_y=1)
                        c0c24001_bombs.append(new_bomb)
            if event.key == pg.K_k:
                # 近くの爁E��をキチE��
                for bomb in c0c24001_bombs:
                    if not bomb.is_exploded and abs(bomb.velocity_x) < 1:  # 静止してぁE��爁E��のみ
                        # プレイヤーとの距離をチェチE��
                        distance = ((player_rect.centerx - bomb.rect.centerx) ** 2 + 
                                   (player_rect.centery - bomb.rect.centery) ** 2) ** 0.5
                        if distance < TILE_SIZE * 2:  # 2タイル以冁E
                            # プレイヤーの向きに応じて蹴めE
                            kick_speed = 8 if player_facing_right else -8
                            bomb.velocity_x = kick_speed
                            bomb.velocity_y = -3  # 少し浮かせめE
                            break  # 1つだけキチE��
        
        # キーが離された時
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                player_move_left = False
            if event.key == pg.K_RIGHT:
                player_move_right = False

    # 7. プレイヤーのロジチE��更新 (移動と当たり判宁E
    
    # --- 左右の移動と当たり判宁E---
    player_movement_x = 0
    if player_move_left:
        player_movement_x -= PLAYER_SPEED
        if player_facing_right:  # 右向きから左向きに変更
            player_image = player_image_left
            player_facing_right = False
    if player_move_right:
        player_movement_x += PLAYER_SPEED
        if not player_facing_right:  # 左向きから右向きに変更
            player_image = player_image_right
            player_facing_right = True
    
    player_rect.x += player_movement_x # まずX方向に動かぁE
    
    # X方向�E衝突チェチE��
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_movement_x > 0: # 右に移動中に衝突E
                player_rect.right = block.left # 右端をブロチE��の左端に合わせる
            elif player_movement_x < 0: # 左に移動中に衝突E
                player_rect.left = block.right # 左端をブロチE��の右端に合わせる

    # --- 垂直方向（重力�Eジャンプ）�E移動と当たり判宁E---
    player_velocity_y += GRAVITY # 重力を速度に加箁E
    player_rect.y += player_velocity_y # Y方向に動かぁE
    
    # Y方向�E衝突チェチE��
    is_on_ground = False # 毎フレーム「接地してぁE��ぁE��と仮宁E
    for block in block_rects:
        if player_rect.colliderect(block):
            if player_velocity_y > 0: # 落下中に衝突E
                player_rect.bottom = block.top # 足允E��ブロチE��の上端に合わせる
                player_velocity_y = 0 # 落下速度をリセチE��
                is_on_ground = True   # 接地フラグを立てめE
            elif player_velocity_y < 0: # ジャンプ中に衝突E
                player_rect.top = block.bottom # 頭をブロチE��の下端に合わせる
                player_velocity_y = 0 # 上�E速度をリセチE���E�頭を打った！E

    # --- 爁E��の更新処琁E(C0C24001) ---
    # 爁E��した爁E��、エフェクトが終亁E��た�E弾を削除
    c0c24001_bombs_to_remove = []
    for bomb in c0c24001_bombs:
        if bomb.update(block_rects):  # 爁E��した場合！Elock_rectsを渡す！E
            # 爁E��音を�E甁E
            if explosion_sound:
                explosion_sound.play()
            # 封E��皁E��ここで敵めE�Eレイヤーへのダメージ処琁E��追加
            pass
        
        # 爁E��エフェクトが終亁E��たら削除リストに追加
        if bomb.is_explosion_finished():
            c0c24001_bombs_to_remove.append(bomb)
    
    # 削除リスト�E爁E��を除去
    for bomb in c0c24001_bombs_to_remove:
        c0c24001_bombs.remove(bomb)

    # 8. 描画処琁E
    # 背景画像を描画�E�画像がある場合）また�E黒で塗りつぶぁE
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLACK)
    
    # スチE�Eジ�E�ブロチE���E�を描画
    for block in block_rects:
        pg.draw.rect(screen, BROWN, block)
    
    # 爁E��を描画 (C0C24001)
    for bomb in c0c24001_bombs:
        bomb.draw(screen, c0c24001_bomb_image, c0c24001_explosion_frames)
        
    # プレイヤーを描画(画像を使ぁE
    # 当たり判定Rectの中央下部に画像を配置(足允E��合わせる)
    player_draw_x = player_rect.centerx - PLAYER_IMAGE_WIDTH // 2
    player_draw_y = player_rect.bottom - PLAYER_IMAGE_HEIGHT  # 足允E��当たり判定�E底に合わせる
    screen.blit(player_image, (player_draw_x, player_draw_y))
    
    # 画面を更新
    pg.display.flip()
    
    # 9. FPS (フレームレーチE の制御
    clock.tick(60) # 1秒間に60回ループが回るように調整

# ループが終亁E��たらPygameを終亁E
pg.quit()
