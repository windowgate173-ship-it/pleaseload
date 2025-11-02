import pygame, time, sys, random
pygame.init()
pygame.mixer.init()

W, H = 900, 700
s = pygame.display.set_mode((W, H))
pygame.display.set_caption("CoinCollector 2.0")
clock = pygame.time.Clock()
f = pygame.font.Font('Cheri 400.ttf')

try:
   pygame.mixer.music.load("01.Bad Piggies Theme.mp3")
   pygame.mixer.music.play(-1)
except:
    print(Music_nt_found("01.Bad Piggies Theme.mp3"))

try:
    coin_sound = pygame.mixer.Sound('coin-drop-1.wav')
    hit_sound = pygame.mixer.Sound('mixkit-metal-hammer-hit-833.wav')
except:
    coin_sound = hit_sound = None
    print(" Sound not found (coin-drop-1.wav, mixkit-metal-hammer-hit-833.wav)")

p = pygame.Rect(180, 180, 40, 40)
SPEED = 5
enemy = pygame.Rect(90, 90, 30, 30)
ex, ey = 6, 6
Lives = 5
score = 0

bg_log = pygame.image.load("mypygamemenu.png").convert()
bg_log = pygame.transform.scale(bg_log, (W, H))

TIME_LIMIT = 60
end_time = time.time() + TIME_LIMIT

COIN_TYPES = [
    ((255, 235, 0), +1),  # normal
    ((5, 250, 5), +2),  # extra heal
    ((210, 0, 0), -1),  # dangerous
    ((250, 250, 250), +5),  # superheal
    ((0, 0, 0), -5)]  # landmine

def new_coin():
    (r, g, b), value = random.choice(COIN_TYPES)
    return {"pos": (random.randint(20, W-20), random.randint(20, H-20)),
            "color": (r, g, b),
            "value": value}

coins = [new_coin() for _ in range(20)]

def show_menu():
   while True:
     for e in pygame.event.get():
         if e.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
         if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            return

         if bg: s.blit(bg, (0, 0))
         text = f.render("Collect all the coins!", True, (255, 255, 255))
         title = f.render("Click ENTER to start!", True, (10, 200, 100))
         s.blit(text, (100, 150));
         s.blit(title, (150, 150))
         pygame.display.flip()
         clock.tick(60)

def run_game():
    global score, Lives, ex, ey
    score = 0
    Lives = 5
    end_time = time.time() + TIME_LIMIT
    player.x, player.y = 180, 180
    enemy.x, enemy.y = 100, 100
    run = True
    reason = "time"

    while run:
       for e in pygame.event.get():
        if e.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

       k = pygame.key.get_pressed()
       if k[pygame.K_a]: p.x -= SPEED
       if k[pygame.K_d]: p.x += SPEED
       if k[pygame.K_w]: p.y -= SPEED
       if k[pygame.K_s]: p.y += SPEED

       player.x = max(0, min(W - player.w, player.x ))
       player.y = max(0, min(H - player.h, player.y ))

       enemy.x += ex
       enemy.y += ey
       if enemy.left <= 0 or enemy.right >= W: ex *= -1
       if enemy.top <= 0 or enemy.bottom >= H: ey *= -1

       if p.colliderect(enemy):
           Lives -= 1
           if hit_sound: hit_sound.play()
           player.x, player.y = 180, 180
           pygame.time.wait(300)
           if Lives <=0:
              reason == "Lives"
              break

       for c in coins:
           if p.collidepoint(c["pos"]):
              score += c["value"]
              if coin_sound: coin_sound.play()
              nc = new_coin()
              c["pos"], c["color"], c["value"] = nc["pos"], nc["color"], nc["value"]

    s.fill((30, 26, 115))
    pygame.draw.rect(s,(0, 200, 255), player)
    pygame.draw.rect(s, (200, 0, 0), enemy)
    for c in coins:
        pygame.draw.circle(s, c["color"], c["pos"], 10)

    t_left = max(0, int(end_time - time.time()))
    s.blit(f.render(f'Current score: {score}', True, (255, 2, 255)), (120, 200))
    s.blit(f.render(f'LivesLeft: {Lives}', True, (255, 2, 255)), (250, 200))
    s.blit(f.render(f'Timer: {t_left}', True, (2, 255, 255)), (320, 200))
    pygame.display.flip()
    clock.tick(60)

    if t_left == 0:
        reason == "Lives"
        run = False

    pygame.mixer.music.fadeout(1600)

    s.fill((0, 0, 0))
    msg = "GAME OVER" if reason == "Lives" else "OUT OF TIME!"
    s.blit(f.render(msg, True, (255, 2, 2)), (120, 200))
    s.blit(f.render(f"Total score: {score}", True, (2, 2, 255)), (250, 200))
    s.blit(f.render(f"Tap ENTER for main menu", True, (255, 255, 255), (200, 250)))

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                waiting = False

    try:
        pygame.mixer.music.play(-1)
    except:
        pass

show_menu()
while True:
    run_game()
    show_menu()