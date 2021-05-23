import pygame, sys, random

#affiche le sol
def draw_floor():
    window.blit(floor_surface,(floor_x,440))
    window.blit(floor_surface, (floor_x+288,440))

def create_pipe():
    random_size=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(450,random_size))
    top_pipe=pipe_surface.get_rect(midbottom=(450,random_size-100))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=512:
            window.blit(pipe_surface, pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            window.blit(flip_pipe,pipe)

def collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top<=-100 or bird_rect.bottom>=450:
        return False
    return True

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,bird_mouvment*-5, 1)
    return new_bird

def bird_animation():
    new_bird=bird_frames[bird_index]
    new_bird_rect=new_bird.get_rect(center=(35,bird_rect.centery))
    return new_bird, new_bird_rect

def display_score(game_state):
    if game_state=="main_game":
        score_surface=game_font.render("score:"+str(int(score/2)), True, (255, 0, 0))
        score_rect=score_surface.get_rect(center= (144, 50))
        window.blit(score_surface, score_rect)
    if game_state=="game_over":
        high_score_surface=game_font.render("high score:"+str(int(high_score)), True, (255, 0, 0))
        high_score_rect=high_score_surface.get_rect(center= (144, 425))
        window.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score>high_score:
        high_score=score
    return high_score

def pipe_scorecheck():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 47 < pipe.centerx < 52 and can_score:
                score+=1
                can_score=False
            if pipe.centerx<0:
                can_score=True


# initialisation de pygame
pygame.init()

# variable du jeux
gravity=0.1
bird_mouvment=0
spawn_pipe=pygame.USEREVENT
pygame.time.set_timer(spawn_pipe,1200)
pipe_height=[200, 300, 400]      
game_activated=True
bird_flap=pygame.USEREVENT+1
pygame.time.set_timer(bird_flap,200)
high_score=0
score=0
can_score=True
game_font=pygame.font.Font("SnowtopCaps.otf", 30)


# initialisation de la fenetre, dimensions prise selon les textures/images
window = pygame.display.set_mode((288, 512))
# ajout d'une clock pour adapter le jeu à toute les vitesse de PC( si mouvement de 5px/frame, diffenrent selon fps)
clock = pygame.time.Clock()

#charge la surface du fond
bg_surface=pygame.image.load("Assets/background-night.PNG").convert()

#charge la surface du sol
floor_surface=pygame.image.load("Assets/base.PNG").convert()
floor_x=0

#charge la surface de l'oiseau et la met dans un rectangle pour gérer les collisions
birdup_surface=pygame.image.load("Assets/redbird-upflap.PNG").convert_alpha()
birddown_surface=pygame.image.load("Assets/redbird-downflap.PNG").convert_alpha()
birdmid_surface=pygame.image.load("Assets/redbird-midflap.PNG").convert_alpha()

bird_frames=[birddown_surface,birdmid_surface,birdup_surface]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=birdup_surface.get_rect(center=(35,256))
game_over_surface=pygame.image.load("Assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,250))
game_over_surface2=pygame.image.load("Assets/gameover.png").convert_alpha()
game_over_rect2 = game_over_surface2.get_rect(center = (144,50))


pipe_surface=pygame.image.load("Assets/pipe-green.PNG")
#pipe_rect=pipe_surface.get_rect(midtop=(144,256))
pipe_list=[]

while True:
    # écoute tt les événements du PC (souris clavier temps...)
    for event in pygame.event.get():
        # si on appuie sur la croix 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_mouvment=0
                bird_mouvment-=3
            if game_activated==False and event.key==pygame.K_SPACE:
                game_activated= True 
                pipe_list.clear()
                bird_rect.center=(35,256)
                bird_mouvment= 0
                score=0

        if event.type==spawn_pipe:
            pipe_list.extend(create_pipe())
        
        if event.type==bird_flap:
            if bird_index<2:
                bird_index+=1
            else:
                bird_index=0
            bird_surface,bird_rect=bird_animation()

    #affiche le fond d'écran
    window.blit(bg_surface,(0,0)) 

    
    if game_activated:

        #oiseau
        bird_mouvment+=gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery+=bird_mouvment
        window.blit(rotated_bird,bird_rect)

        # appelle de la fonction collisions
        game_activated=collisions(pipe_list)

        #pipe
        pipe_list=move_pipe(pipe_list)
        draw_pipes(pipe_list)


        pipe_scorecheck()
        display_score("main_game")
    else:
        window.blit(game_over_surface2, game_over_rect2)
        window.blit(game_over_surface, game_over_rect)
        high_score=update_score(score, high_score)
        display_score("game_over")



    #décale le sol de 1pixel a gauche
    floor_x-=1
    #affiche le sol
    draw_floor()
    #remet le sol a zero
    if floor_x<=-288:
        floor_x=0

    # prend les changements d'avant et les applique à l'affichage
    pygame.display.update()
    # limitation à 120fps
    clock.tick(120)

