import pygame
import os
pygame.font.init()

WIDTH,HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game")

WHITE = ((255,255,255))
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255 ,0)

BORDER =pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

FPS = 60
VEL = 5

BULLETS_VEL = 7
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55,40)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 270)

SPACE =pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))    
    WIN.blit(yellow_health_text, (10, 10)) 
        
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0 : #LEFT
        yellow.x -= VEL
        
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : #RIGHT
        yellow.x += VEL   
           
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL 
        
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: #DOWN
        yellow.y += VEL
        
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width : #LEFT
        red.x -= VEL
        
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #RIGHT
        red.x += VEL   
           
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL 
        
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: #DOWN
        red.y += VEL           

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullets in yellow_bullets:
        bullets.x += BULLETS_VEL
        if red.colliderect(bullets):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullets)
        elif bullets.x > WIDTH:
                yellow_bullets.remove(bullets)
     
    for bullets in red_bullets:
        bullets.x -= BULLETS_VEL
        if yellow.colliderect(bullets):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullets)     
        elif bullets.x < 0:
            red_bullets.remove(bullets)       

def main():
    red = pygame.Rect(700, 300, 55, 40)
    yellow = pygame.Rect(100, 300, 55, 40)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2 , 10, 5)
                    yellow_bullets.append(bullet)
                        
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2 , 10, 5)
                    red_bullets.append(bullet)        
            
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                
        winner_text = ""        
        if red_health <=0:
            winner_text ='Yello Wins !'   
        
        if yellow_health <=0:
            winner_text ='Red Wins !'    
        
        if winner_text != "":
           pass # SOMEONE WON            
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)   
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
        
    pygame.quit()
    
if __name__ == "__main__":
    main()               