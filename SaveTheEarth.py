import pygame
import random
import sys

# 게임 초기화
pygame.init()
is_game_over = False

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
missile_types = ["small", "small_double", "small_triple", "medium", "medium_double", "medium_triple"]
current_missile_index = 0
missile_image = missile_images[current_missile_index]
missile_size = missile_image.get_rect().size
missile_width = missile_size[0]
missile_height = missile_size[1]
current_missile_power = 1 # 초기 미사일 파워 설정

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

# 아이템 이미지 파일 경로
power_item_image = pygame.image.load('img/power_item.png')
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

#점수 변수 -운석의 낙하 속도에 따라 점수가 다름
total_score = 0
speed_bonus = 0

# 운석 생성 시 사용되는 int값
astoreid_speed_min = 1
astoreid_speed_max = 3
asteroid_frequency = 3
asteroid_frequency_min = 1
asteroid_frequency_max = 100

# 난이도 상승 기준을 측정하는 변수
present_score = 0

# 운석 생성 함수
def create_asteroid():
    asteroid_img = pygame.image.load(random.choice(asteroid_images))
    asteroid_x_pos = random.randint(0, screen_width - asteroid_img.get_rect().width)
    asteroid_y_pos = 0 - asteroid_img.get_rect().width
    asteroid_speed = random.randint(astoreid_speed_min, astoreid_speed_max)
    asteroid_hp = 3  # 운석의 체력을 3으로 설정
    return [asteroid_img, asteroid_x_pos, asteroid_y_pos, asteroid_speed, asteroid_hp]

# 게임 오버 화면 출력 함수
def game_over():
    global is_game_over, total_score, astoreid_speed_min, astoreid_speed_max
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() - 20))
    restart_button = draw_button('Restart', screen_width / 2, screen_height / 2 + 10)
    quit_button = draw_button('Quit', screen_width / 2, screen_height / 2 + 70)

    #게임 오버시 점수 표시
    font_s = pygame.font.Font(None, 36)
    text_s = font.render("Score: " + str(total_score), True, (0, 0, 255))
    screen.blit(text_s, (screen_width / 2 - text.get_width() / 2, 250))
    
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
                    return  # 게임 재시작
                
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()  # 게임 종료
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
def draw_HPbar(x, y, hp):
    if hp == 3:
        color = (0, 255, 0)
    elif hp == 2:
        color = (255, 255, 0)
    elif hp == 1:
        color = (255, 0, 0)
    pygame.draw.rect(screen, color, (x, y-10, 25*hp, 5))

# 아이템 생성 함수
def create_item(x, y):
    item_type = random.choice(['power', 'speed', 'life'])
    if item_type == 'power':
        return [power_item_image, x, y, 'power']
    elif item_type == 'speed':
        return [speed_item_image, x, y, 'speed']
    elif item_type == 'life':
        return [life_item_image, x, y, 'life']

# 게임 플레이 함수
def game_play():
    global missiles, asteroids, explosions, items, fighter_x_pos, fighter_y_pos, is_game_over, lives, total_score, speed_bonus, \
        fighter_speed, current_missile_index, missile_image, missile_width, missile_height, current_missile_power, \
            astoreid_speed_min, astoreid_speed_max, present_score, asteroid_frequency, asteroid_frequency_min, asteroid_frequency_max
    # 우주선 운석 위치 조정 및 재조정
    fighter_x_pos = (screen_width / 2) - (fighter_width / 2)
    fighter_y_pos = screen_height - fighter_height - 10
    asteroids = []
    missiles = []
    explosions = []
    items = []
    lives = 5

    # 게임 실행
    while not is_game_over:
        if (present_score >= 500):
            if (astoreid_speed_min <= 20):
                astoreid_speed_min += 3
                astoreid_speed_max += 3
            if asteroid_frequency <= 60:
                asteroid_frequency += 3
            present_score = total_score % 500

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    missile_x_pos = fighter_x_pos + (fighter_width / 2) - (missile_width / 2)
                    missile_y_pos = fighter_y_pos
                    missiles.append([missile_x_pos, missile_y_pos])
                    missile_sound.play()

        # fighter_speed만큼 이동
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and fighter_x_pos > 0:
            fighter_x_pos -= fighter_speed
        if keys[pygame.K_RIGHT] and fighter_x_pos < screen_width - fighter_width:
            fighter_x_pos += fighter_speed

        # 미사일 위치 업데이트
        missiles = [[m[0], m[1] - 10] for m in missiles if m[1] > 0]

        # 운석 생성
        if random.randint(asteroid_frequency_min, asteroid_frequency_max) < asteroid_frequency:
            asteroids.append(create_asteroid())

        # 운석 위치 업데이트
        asteroids = [[a[0], a[1], a[2] + a[3], a[3], a[4]] for a in asteroids if a[2] < screen_height]

        # 충돌 처리
        for missile in missiles:
            for asteroid in asteroids:
                missile_rect = pygame.Rect(missile[0], missile[1], missile_width, missile_height)
                asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid[0].get_rect().width, asteroid[0].get_rect().height)
                if missile_rect.colliderect(asteroid_rect):
                    missiles.remove(missile)
                    asteroid[4] -= current_missile_power # current_missile_power만큼 운석의 체력 감소
                    if asteroid[4] <= 0:
                        asteroids.remove(asteroid)
                        explosions.append([explosion_image, asteroid[1], asteroid[2], pygame.time.get_ticks()])
                        
                        get_score(asteroid[3])
                        
                        if random.random() < 0.15:  # 15% 확률로 아이템 생성
                            items.append(create_item(asteroid[1], asteroid[2]))
                    break

        # 전투기와 운석 충돌 처리
        for asteroid in asteroids:
            if ((fighter_x_pos + fighter_width / 3) < asteroid[1] + asteroid[0].get_rect().width / 3 < (fighter_x_pos + fighter_width - fighter_width / 3) or
                (fighter_x_pos + fighter_width / 3) < asteroid[1] + asteroid[0].get_rect().width - asteroid[0].get_rect().width / 3 < (fighter_x_pos + fighter_width - fighter_width / 3)) and \
               ((fighter_y_pos + fighter_height / 3) < asteroid[2] + asteroid[0].get_rect().height / 3 < (fighter_y_pos + fighter_height - fighter_height / 3) or
                (fighter_y_pos + fighter_height / 3) < asteroid[2] + asteroid[0].get_rect().height - asteroid[0].get_rect().height / 3 < (fighter_y_pos + fighter_height - fighter_height / 3)):
                lives -= 1
                asteroids.remove(asteroid)
                if lives == 0:
                    is_game_over = True

        # 아이템 위치 업데이트
        items = [[i[0], i[1], i[2] + 3, i[3]] for i in items if i[2] < screen_height]

        # 아이템과 전투기 충돌 처리
        for item in items:
            if (fighter_x_pos < item[1] < fighter_x_pos + fighter_width) and (fighter_y_pos < item[2] < fighter_y_pos + fighter_height):
                if item[3] == 'power':
                    if current_missile_index < len(missile_images) - 1:
                        current_missile_index += 1
                        current_missile_power += 1
                        missile_image = missile_images[current_missile_index]
                        missile_size = missile_image.get_rect().size
                        missile_width = missile_size[0]
                elif item[3] == 'speed':
                    fighter_speed += 1
                elif item[3] == 'life':
                    if lives < 5:
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
            draw_HPbar(asteroid[1], asteroid[2], asteroid[4])

        for item in items:
            screen.blit(item[0], (item[1], item[2]))

        # 인게임 점수
        show_score()

        # 폭발 효과 그리기
        current_time = pygame.time.get_ticks()
        explosions = [explosion for explosion in explosions if current_time - explosion[3] < 500]
        for explosion in explosions:
            screen.blit(explosion[0], (explosion[1], explosion[2]))

        # 목숨 표시
        for i in range(lives):
            screen.blit(heart_image, (10 + i * (heart_width + 10), 10))

        pygame.display.update()
        clock.tick(60)

# 게임 시작 화면 호출
start_screen()

# 게임 루프
while True:
    if not is_game_over:
        game_play()
    else:
        game_over()
