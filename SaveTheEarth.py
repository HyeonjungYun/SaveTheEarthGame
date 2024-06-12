import pygame
import random
import sys

# 게임 초기화
pygame.init()
is_game_over = False
is_game_clear = False

# 화면 설정
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 제목
pygame.display.set_caption("PyShooting: 지구를 지켜라")

# FPS 설정
clock = pygame.time.Clock()

# 배경 이미지
background = pygame.image.load('img/background.png')

# 전투기 이미지
fighter = pygame.image.load('img/fighter.png')
fighter_size = fighter.get_rect().size
fighter_width = fighter_size[0]
fighter_height = fighter_size[1]
fighter_x_pos = (screen_width / 2) - (fighter_width / 2)
fighter_y_pos = screen_height - fighter_height - 10
fighter_speed = 5

# 폭발 이미지
explosion_image = pygame.image.load('img/explosion.png')

# 미사일 이미지 로드
small_missile_image = pygame.image.load('img/small_missile.png')
small_double_missile_image = pygame.image.load('img/small_double_missile.png')
small_triple_missile_image = pygame.image.load('img/small_triple_missile.png')
medium_missile_image = pygame.image.load('img/medium_missile.png')
medium_double_missile_image = pygame.image.load('img/medium_double_missile.png')
medium_triple_missile_image = pygame.image.load('img/medium_triple_missile.png')

missile_images = [
    small_missile_image, small_double_missile_image, small_triple_missile_image,
    medium_missile_image, medium_double_missile_image, medium_triple_missile_image,
]
current_missile_index = 0
missile_image = missile_images[current_missile_index]
missile_size = missile_image.get_rect().size
missile_width = missile_size[0]
missile_height = missile_size[1]
current_missile_power = 1  # 초기 미사일 파워 설정

# 운석 이미지 파일 목록
asteroid_images = ['img/rock1.png', 'img/rock2.png', 'img/rock3.png', 'img/rock4.png',
                   'img/rock5.png', 'img/rock6.png', 'img/rock7.png', 'img/rock8.png']

# 배경 음악
pygame.mixer.music.load('audio/background.mp3')
pygame.mixer.music.play(-1)

# 미사일 발사 사운드
missile_sound = pygame.mixer.Sound('audio/missile.wav')

# 미사일 리스트
missiles = []

# 운석 리스트
asteroids = []

# 운석 폭발 시간 관리
explosions = []

# 충돌 시 필요 변수 설정
flash_duration = 200  # 플래시 지속 시간 (밀리초)
flash_start_time = None

# 아이템 이미지 파일 경로
upgrade_item_image = pygame.image.load('img/upgrade_item.png')
pierce_item_image = pygame.image.load('img/pierce_item.png')
speed_item_image = pygame.image.load('img/speed_item.png')
life_item_image = pygame.image.load('img/heart.png')

# 아이템 리스트
items = []

# 초기 목숨 설정
lives = 5

# 목숨 이미지 로드
heart_image = pygame.image.load('img/heart.png')
heart_size = heart_image.get_rect().size
heart_width = heart_size[0]
heart_height = heart_size[1]

# 점수 변수 -운석의 낙하 속도에 따라 점수가 다름
total_score = 0
speed_bonus = 0

# 현재 스테이지 및 시간
current_stage = 1
stage_start_time = pygame.time.get_ticks()

# 스테이지 클리어 시 사용하는 변수
stage_clear = False

# 운석 생성 시 사용되는 int값
astoreid_speed_min = 1
astoreid_speed_max = 3
asteroid_frequency = 3
asteroid_frequency_min = 1
asteroid_frequency_max = 100

# 난이도 상승 기준을 측정하는 변수
present_score = 0

# 아이템 생성 확률
item_generate = 0.15

# 운석 생성 함수
def create_asteroid():
    asteroid_img = pygame.image.load(random.choice(asteroid_images))
    asteroid_x_pos = random.randint(0, screen_width - asteroid_img.get_rect().width)
    asteroid_y_pos = 0 - asteroid_img.get_rect().width
    asteroid_speed = random.randint(1, 3)
    max_hp = 3 + (total_score // 500)  # 운석의 최대 체력 설정
    asteroid_hp = max_hp  # 초기 체력을 최대 체력으로 설정
    return [asteroid_img, asteroid_x_pos, asteroid_y_pos, asteroid_speed, asteroid_hp, max_hp]

# 게임 오버 화면 출력 함수
def game_over():
    global is_game_over, total_score, astoreid_speed_min, astoreid_speed_max, font_s, item_generate, \
        current_missile_power, missile_width, fighter_speed, asteroid_frequency, missile_height
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() - 20))
    restart_button = draw_button('Restart', screen_width / 2, screen_height / 2 + 10)
    quit_button = draw_button('Quit', screen_width / 2, screen_height / 2 + 70)

    # 게임 오버시 점수 표시
    font_s = pygame.font.Font(None, 36)
    text_s = font.render("Score: " + str(total_score), True, (0, 0, 255))
    screen.blit(text_s, (screen_width / 2 - text_s.get_width() / 2, 250))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    is_game_over = False
                    total_score = 0
                    current_missile_index = 0
                    current_missile_power = 1
                    astoreid_speed_min = 1
                    astoreid_speed_max = 3
                    missile_image = missile_images[current_missile_index]
                    missile_size = missile_image.get_rect().size
                    missile_width = missile_size[0]
                    missile_height = missile_size[1]
                    fighter_speed = 5
                    astoreid_speed_min = 1
                    astoreid_speed_max = 3
                    asteroid_frequency = 3
                    item_generate = 0.15
                    return  # 게임 재시작

                elif quit_button.collidepoint(event.pos):
                    pygame.quit()  # 게임 종료
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

# 게임 클리어 화면 출력 함수
def game_clear():
    global is_game_clear, total_score
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Clear", True, (0, 255, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() - 20))

    # 게임 클리어 시 점수 표시
    font_s = pygame.font.Font(None, 36)
    text_s = font.render("Score: " + str(total_score), True, (0, 0, 255))
    screen.blit(text_s, (screen_width / 2 - text_s.get_width() / 2, 250))

    quit_button = draw_button('Quit', screen_width / 2, screen_height / 2 + 70)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

# 버튼 생성 함수
def draw_button(button_text, center_x, center_y, action=None):
    font = pygame.font.Font(None, 36)
    text = font.render(button_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(center_x, center_y))
    button_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(screen, (0, 128, 255), button_rect)
    screen.blit(text, text_rect)
    return button_rect

# 게임 시작 화면
def start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Save the Earth!!!", True, (0, 255, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() - 20))
    start_button = draw_button("Game Start", screen_width / 2, screen_height / 2 + 10)
    quit_button = draw_button("Quit", screen_width / 2, screen_height / 2 + 70)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):  # 게임 시작 버튼
                    return
                elif quit_button.collidepoint(event.pos):  # 게임 종료 버튼
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 인게임 점수판
def show_score():
    global total_score
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(total_score), True, (255, 255, 255))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, 20))

# 점수 획득 - 낙하속도에 따라 점수량 다름
def get_score(speed_bonus):
    global total_score, present_score
    basic_score = 10
    total_score += basic_score * speed_bonus
    present_score += basic_score * speed_bonus

# 체력 바
def draw_HPbar(x, y, hp, max_hp):
    bar_length = 75  # 바의 최대 길이 설정
    health_ratio = hp / max_hp  # 현재 체력 비율 계산
    current_bar_length = bar_length * health_ratio
    if health_ratio > 0.6:
        color = (0, 255, 0)
    elif health_ratio > 0.3:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)
    pygame.draw.rect(screen, color, (x, y - 10, current_bar_length, 5))

# 아이템 생성 함수
def create_item(x, y):
    global current_missile_power, fighter_speed, pierce_count, lives
    possible_items = []
    if current_missile_power < 30:
        possible_items.append('upgrade')
    if pierce_count < 5:
        possible_items.append('pierce')
    if fighter_speed < 15:
        possible_items.append('speed')
    if lives < 5:
        possible_items.append('life')

    if possible_items:
        item_type = random.choice(possible_items)
        if item_type == 'upgrade':
            return [upgrade_item_image, x, y, 'upgrade']
        elif item_type == 'pierce':
            return [pierce_item_image, x, y, 'pierce']
        elif item_type == 'speed':
            return [speed_item_image, x, y, 'speed']
        elif item_type == 'life':
            return [life_item_image, x, y, 'life']
    return []  # 생성 가능한 아이템이 없으면 빈 리스트 반환

# 현재 공격력과 속도 표시
def show_stats():
    font = pygame.font.Font(None, 36)
    attack_power_text = font.render(f"Power: {current_missile_power}", True, (255, 255, 255))
    speed_text = font.render(f"Speed: {fighter_speed}", True, (255, 255, 255))
    screen.blit(attack_power_text, (screen_width - attack_power_text.get_width() - 20, 20))
    screen.blit(speed_text, (screen_width - speed_text.get_width() - 20, 60))

# 현재 스테이지 표시
def show_stage():
    global current_stage
    font = pygame.font.Font(None, 36)
    stage_text = font.render("Stage: " + str(current_stage), True, (255, 255, 255))
    screen.blit(stage_text, (10, 50))

# 스테이지 클리어 화면
def stage_clear_screen(stage):
    font = pygame.font.Font(None, 74)
    text = font.render(f"Stage {stage}", True, (0, 255, 0))
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 2000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(fighter, (fighter_x_pos, fighter_y_pos))

        for item in items:
            screen.blit(item[0], (item[1], item[2]))

        # 인게임 점수
        show_score()

        # 현재 공격력과 속도 표시
        show_stats()

        # 현재 스테이지 표시
        show_stage()

        # 목숨 표시
        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_width + 10), 10))

        # "Stage ?" 표시
        screen.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)


# 보스 몬스터 이미지 로드
boss_image = pygame.image.load('img/boss.png')
boss_size = boss_image.get_rect().size
boss_width = boss_size[0]
boss_height = boss_size[1]

# 보스 몬스터 생성 함수
def create_boss():
    boss_x_pos = (screen_width / 2) - (boss_width / 2)
    boss_y_pos = -boss_height
    boss_speed = 0.2  
    boss_hp = 100000  # 보스 몬스터 체력
    return [boss_image, boss_x_pos, boss_y_pos, boss_speed, boss_hp]

# 보스 몬스터 체력 바
def show_boss_hp(boss):
    x, y, hp = boss[1], boss[2], boss[4]
    max_hp = 100000  # 보스 몬스터 최대 체력
    bar_x = 50  
    bar_y = 50  
    bar_length = screen_width - 100  # 체력 바의 길이
    pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_length, 20))  # 전체 체력 바
    pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_length * (hp / max_hp), 20))  # 현재 체력
    
# 보스 원거리 공격 이미지
boss_rock_image = pygame.image.load('img/boss_rock.png')
boss_rock_size = boss_rock_image.get_rect().size
boss_rock_width = boss_rock_size[0]
boss_rock_height = boss_rock_size[1]

# 보스 원거리 공격
def create_boss_rocks(boss_x, boss_y):
    num_rocks = random.randint(2, 5)
    rocks = []
    for _ in range(num_rocks):
        rock_x = boss_x + boss_width // 2 - boss_rock_width // 2
        rock_y = boss_y + boss_height
        rock_speed = random.randint(1, 3)
        rocks.append([rock_x, rock_y, rock_speed])
    return rocks

# 보스 스테이지
def boss_stage():
    global missiles, explosions, total_score, is_game_over, is_game_clear, lives, current_stage, present_score, fighter_x_pos, fighter_y_pos

    boss = create_boss()
    boss_appeared = True
    boss_rock_image = pygame.image.load('img/boss_rock.png') 
    boss_attacks = []

    last_attack_time = pygame.time.get_ticks()
    attack_interval = 5000  # 5초마다 공격

    while boss_appeared:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missile_x_pos = fighter_x_pos + (fighter_width / 2) - (missile_width / 2)
                    missile_y_pos = fighter_y_pos
                    missiles.append([missile_x_pos, missile_y_pos, pierce_count])
                    missile_sound.play()

        # fighter_speed만큼 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and fighter_x_pos > 0:
            fighter_x_pos -= fighter_speed
        if keys[pygame.K_RIGHT] and fighter_x_pos < screen_width - fighter_width:
            fighter_x_pos += fighter_speed

        # 미사일 위치 업데이트
        missiles = [[m[0], m[1] - 10, m[2]] for m in missiles if m[1] > 0]

        # 보스 위치 업데이트
        boss[2] += boss[3]

        # 보스의 원거리 공격
        if current_time - last_attack_time > attack_interval:
            num_rocks = random.randint(2, 5)
            for _ in range(num_rocks):
                rock_x_pos = boss[1] + boss_width / 2
                rock_y_pos = boss[2] + boss_height
                angle = random.uniform(-1, 1)  # 랜덤한 각도로 퍼져나감
                boss_attacks.append([boss_rock_image, rock_x_pos, rock_y_pos, angle])
            last_attack_time = current_time

        # 보스 공격 위치 업데이트
        boss_attacks = [[b[0], b[1] + 5 * b[3], b[2] + 5, b[3]] for b in boss_attacks if b[2] < screen_height]

        # 보스 몬스터와 미사일 충돌 처리
        for missile in missiles:
            missile_rect = pygame.Rect(missile[0], missile[1], missile_width, missile_height)
            boss_rect = pygame.Rect(boss[1], boss[2], boss_width, boss_height)
            if missile_rect.colliderect(boss_rect):
                boss[4] -= current_missile_power  # 현재 미사일 파워만큼 보스 몬스터 체력 감소
                missile[2] -= 1  # 미사일의 남은 관통 횟수 감소
                if missile[2] < 0:
                    missiles.remove(missile)
                if boss[4] <= 0:
                    explosions.append([explosion_image, boss[1], boss[2], pygame.time.get_ticks()])
                    boss_appeared = False
                    is_game_clear = True
                    return True  # 보스 클리어
                break

        # 전투기와 보스 몬스터 충돌 처리
        fighter_rect = pygame.Rect(fighter_x_pos, fighter_y_pos, fighter_width, fighter_height)
        boss_rect = pygame.Rect(boss[1], boss[2], boss_width, boss_height)
        if fighter_rect.colliderect(boss_rect):
            is_game_over = True
            return False

        # 전투기와 보스 공격 충돌 처리
        for attack in boss_attacks:
            for attack in boss_attacks:attack_rect = pygame.Rect(attack[1], attack[2], attack[0].get_rect().width, attack[0].get_rect().height)
            if fighter_rect.colliderect(attack_rect):
                lives -= 1  
                boss_attacks.remove(attack)
                flash_start_time = pygame.time.get_ticks()
                if lives <= 0:  
                    is_game_over = True
                    return False
        

        # 화면 그리기
        screen.blit(background, (0, 0))
        screen.blit(fighter, (fighter_x_pos, fighter_y_pos))

        for missile in missiles:
            screen.blit(missile_image, (missile[0], missile[1]))

        screen.blit(boss[0], (boss[1], boss[2]))

        for attack in boss_attacks:
            screen.blit(attack[0], (attack[1], attack[2]))

        # 보스 체력 바
        show_boss_hp(boss)

        for explosion in explosions:
            screen.blit(explosion[0], (explosion[1], explosion[2]))

        # 목숨 표시
        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_width + 10), 10))

        pygame.display.update()
        clock.tick(60)


# 게임 플레이
def game_play():
    global missiles, asteroids, explosions, items, fighter_x_pos, fighter_y_pos, is_game_over, is_game_clear, lives, total_score, speed_bonus, \
        fighter_speed, current_missile_index, missile_image, missile_width, missile_height, current_missile_power, \
        astoreid_speed_min, astoreid_speed_max, present_score, asteroid_frequency, asteroid_frequency_min, asteroid_frequency_max, \
        current_missile_power, current_stage, flash_start_time, flash_duration, pierce_count, boss_rocks, item_generate, stage_clear

    # 우주선 운석 위치 조정 및 재조정
    fighter_x_pos = (screen_width / 2) - (fighter_width / 2)
    fighter_y_pos = screen_height - fighter_height - 10
    asteroids = []
    missiles = []
    explosions = []
    items = []
    lives = 5
    stage_start_time = pygame.time.get_ticks()
    flash_start_time = None  # 플래시 효과 초기화
    pierce_count = 1  # 관통력 초기화
    boss_rocks = []  # 보스의 원거리 공격 리스트 초기화

    # 게임 실행
    while not is_game_over and not is_game_clear:
        if present_score >= 500:
            if current_stage == 1 and total_score >= 5000:
                current_stage += 1
                item_generate = 0.1
                asteroids = []  # 기존 운석 제거
                stage_clear = True
                stage_clear_start_time = pygame.time.get_ticks()
            if current_stage == 2 and total_score >= 20000:
                current_stage += 1
                item_generate = 0.03
                asteroids = []  # 기존 운석 제거
                stage_clear = True
                stage_clear_start_time = pygame.time.get_ticks()
            if astoreid_speed_min <= 20:
                astoreid_speed_min += 3
                astoreid_speed_max += 3
            if asteroid_frequency <= 30:
                asteroid_frequency += 1
            present_score = total_score % 500

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missile_x_pos = fighter_x_pos + (fighter_width / 2) - (missile_width / 2)
                    missile_y_pos = fighter_y_pos
                    missiles.append([missile_x_pos, missile_y_pos, pierce_count])
                    missile_sound.play()

        # fighter_speed만큼 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and fighter_x_pos > 0:
            fighter_x_pos -= fighter_speed
        if keys[pygame.K_RIGHT] and fighter_x_pos < screen_width - fighter_width:
            fighter_x_pos += fighter_speed

        # 미사일 위치 업데이트
        missiles = [[m[0], m[1] - 10, m[2]] for m in missiles if m[1] > 0]

        if not stage_clear:  # 스테이지 클리어 상태가 아닌 경우에만 운석 생성
            # 운석 생성
            if random.randint(asteroid_frequency_min, asteroid_frequency_max) < asteroid_frequency:
                asteroids.append(create_asteroid())

            # 운석 위치 업데이트
            asteroids = [[a[0], a[1], a[2] + a[3], a[3], a[4], a[5]] for a in asteroids if a[2] < screen_height]

        # 충돌 처리
        for missile in missiles:
            for asteroid in asteroids:
                missile_rect = pygame.Rect(missile[0], missile[1], missile_width, missile_height)
                asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid[0].get_rect().width, asteroid[0].get_rect().height)
                if missile_rect.colliderect(asteroid_rect):
                    asteroid[4] -= current_missile_power  # current_missile_power만큼 운석의 체력 감소
                    if asteroid[4] <= 0:
                        asteroids.remove(asteroid)
                        explosions.append([explosion_image, asteroid[1], asteroid[2], pygame.time.get_ticks()])
                        get_score(asteroid[3])
                        if random.random() < item_generate:  # 15% 확률로 아이템 생성
                            items.append(create_item(asteroid[1], asteroid[2]))
                    missile[2] -= 1  # 미사일의 남은 관통 횟수 감소
                    if missile[2] < 0:
                        missiles.remove(missile)
                    break

        # 전투기와 운석 충돌 처리
        for asteroid in asteroids:
            fighter_rect = pygame.Rect(fighter_x_pos, fighter_y_pos, fighter_width, fighter_height)
            asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid[0].get_rect().width, asteroid[0].get_rect().height)
            if fighter_rect.colliderect(asteroid_rect):
                lives -= 1
                asteroids.remove(asteroid)
                flash_start_time = pygame.time.get_ticks()  # 플래시 효과 시작 시간 설정
                if lives == 0:
                    is_game_over = True

        # 아이템 위치 업데이트
        items = [[i[0], i[1], i[2] + 3, i[3]] for i in items if i and i[2] < screen_height]

        # 아이템과 전투기 충돌 처리
        for item in items[:]:
            if not item:
                items.remove(item)
                continue
            
            fighter_rect = pygame.Rect(fighter_x_pos, fighter_y_pos, fighter_width, fighter_height)
            item_rect = pygame.Rect(item[1], item[2], item[0].get_rect().width, item[0].get_rect().height)
            if fighter_rect.colliderect(item_rect):
                if item[3] == 'upgrade' and current_missile_power < 30:
                    current_missile_power += 1
                    missile_index = min(current_missile_power // 10, len(missile_images) - 1)
                    missile_image = missile_images[missile_index]
                    missile_size = missile_image.get_rect().size
                    missile_width = missile_size[0]
                    missile_height = missile_size[1]
                elif item[3] == 'pierce' and pierce_count < 5:
                    pierce_count += 1  # 관통 횟수 증가
                elif item[3] == 'speed' and fighter_speed < 15:
                    fighter_speed += 1
                elif item[3] == 'life' and lives < 5:
                    lives += 1
                items.remove(item)
                break
 
         # 화면 그리기
        screen.blit(background, (0, 0))
        screen.blit(fighter, (fighter_x_pos, fighter_y_pos))

        for missile in missiles:
            screen.blit(missile_image, (missile[0], missile[1]))

        for asteroid in asteroids:
            screen.blit(asteroid[0], (asteroid[1], asteroid[2]))
            draw_HPbar(asteroid[1], asteroid[2], asteroid[4], asteroid[5])

        for item in items:
            screen.blit(item[0], (item[1], item[2]))

        # 인게임 점수
        show_score()

        # 현재 공격력과 속도 표시
        show_stats()

        # 현재 스테이지 표시
        show_stage()
        
        # 폭발 효과 그리기
        current_time = pygame.time.get_ticks()
        explosions = [explosion for explosion in explosions if current_time - explosion[3] < 500]
        for explosion in explosions:
            screen.blit(explosion[0], (explosion[1], explosion[2]))
        
        # 목숨 표시
        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_width + 10), 10))
        
        # 충돌 시각적 효과
        if flash_start_time and current_time - flash_start_time < flash_duration:
            flash_alpha = 128 * (1 - (current_time - flash_start_time) / flash_duration)  # 반투명 효과로 변경 (기존 255에서 128로 변경)
            flash_surface = pygame.Surface((screen_width, screen_height))
            flash_surface.set_alpha(flash_alpha)
            flash_surface.fill((255, 0, 0))  # 붉은 색으로 플래시 효과
            screen.blit(flash_surface, (0, 0))
        
        # 스테이지 클리어 메시지 표시
        if stage_clear:
            font = pygame.font.Font(None, 74)
            text = font.render(f"Stage {current_stage}", True, (0, 255, 0))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            if current_time - stage_clear_start_time > 2000:  # 2초가 지나면 스테이지 클리어 상태 해제
                stage_clear = False
        
        # 보스 등장 처리
        if total_score >= 30000:
            explosions = []  # 이전 스테이지의 폭발 효과 제거
            if boss_stage():
                is_game_clear = True
        
        pygame.display.update()
        clock.tick(60)


# 게임 시작 화면 호출
start_screen()

# 게임 루프
while True:
    if not is_game_over and not is_game_clear:
        game_play()
    elif is_game_over:
        game_over()
    elif is_game_clear:
        game_clear()
