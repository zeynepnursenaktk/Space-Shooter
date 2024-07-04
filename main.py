import os
import pygame
import random
from laser import *
from ships import *
from settings import *

pygame.init()


# oyunun ana döngüsünü çalıştıracak olan fonks.
def main():  
    
    pygame.font.init()  # Fontları başlat
    pygame.display.set_caption("Space Shooter")
    
    
    run = True # oyunun devam etmesi, sonlandırılması için kullanılacak
    game_over = False 
    
    FPS = 60
    clock = pygame.time.Clock()

    start_time = pygame.time.get_ticks()
    
    aliens = [] # üretilen tüm uzaylılar bu listeye eklenir
    aliens_lasers = []   # üretilen bütün alien laserler bu listeye eklenir
        
    level = 0
    
    player_velocity = 5
    alien_velocity = 5
    
    laser_velocity = 3
    alien_length = 5

    
    player = Player(300,650)  
            
    #oyun ekranını güncellemek ve çizmek için kullanılan fonk.
    def draw_screen():
         
         WINDOWS.blit(BACKGROUND, (0, 0))
         player.draw(WINDOWS)
         
             
         for alien in aliens:
             alien.draw(WINDOWS)
             
                          
         # Oyuncunun oyunda kaldığı süre ekrana yazdırılır.    
         font = pygame.font.SysFont("comicsans", 30)  
         time_text = font.render("Süre: " + str(current_time // 1000) + " sn", True, (255,255,255))  
         WINDOWS.blit(time_text, (525, 40))
             
         # Oyuncunun leveli ekrana yazdırılır.
         level_text = font.render("Level: " + str(level), True, (255, 255, 255))
         WINDOWS.blit(level_text, (525, 5))
         
         
         
         #oyuncunun sağlığı 0 olunca game over yazdırılır.
         if player.health == 0:
            font = pygame.font.SysFont("comicsans", 80)
            game_over_text = font.render("Game Over", True, (255,255,255))
            WINDOWS.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
          
         pygame.display.update()
    
         
    #geçen süreyi güncellemek için kullanılır.     
    def update_time():   
        global current_time
        current_time = pygame.time.get_ticks() - start_time
        
            
    
    while run:
        
        clock.tick(FPS)
       
        update_time()  # Süre sayaçlarını güncelle
        draw_screen()  # Ekranı güncelle
        
        #BUTON İSLEMLERİ 
                
        keys = pygame.key.get_pressed()  
        
        
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.ship_image.get_width():
            player.x += player_velocity   #oyuncunun gemisi sağa hareket eder (player.x değeri artar).
            
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_velocity   #oyuncunun gemisi sola hareket eder (player.x değeri azalır).
            
        if keys[pygame.K_UP] and player.y > 0:
            player.y -=player_velocity    #oyuncunun gemisi yukarı hareket eder (player.y değeri azalır).
            
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player.ship_image.get_height():
            player.y +=player_velocity    #oyuncunun gemisi aşağı hareket eder (player.y değeri artar).
            
        if keys[pygame.K_SPACE]: 
            player.shoot()                #oyuncunun gemisi ateş eder (player.shoot() çağrılır).
                   
                                    
        if len(aliens) == 0: # liste her boşaldığında tekrar alien üretilecek.
            alien_velocity +=1
            alien_length +=3 #her level atlandığında alien sayısı artacak.
            level += 1
            player.health = 100
                    
            
            #her seferinde farklı yerlerden alien gelmesi için kullandıgım döngüü
            for i in range(alien_length):
                x = random.randrange(0, WIDTH )  
                y = random.randrange(0, int(HEIGHT/2 - 200))  
    
                alien = Alien(x, y, random.choice(["black","light_purple","dark_purple"]))
                aliens.append(alien)

        
        player.move_lasers(laser_velocity, aliens)    #Player move_lasers fonksiyonuyla belirtilen hızda lazer atar.    
        
        
        for alien in aliens:
            alien.move(alien_velocity)                 #Bütün alienlar move fonksiyonuyla belirtilen hızda hareket eder.
            alien.move_lasers(-laser_velocity, player) #Bütün alienlar move_lasers fonksiyonuyla belirtilen hızda lazer atar.
            if random.randrange(0, 20) == 1:           #alienların lazer atma olasılığını belirlemek için kullandık.
                                                       #random.randrange(0, 10) == 0 uzaylıların daha sık lazer atılır.
                alien.shoot()
            
            
            for laser in aliens_lasers:     #alienların laseri playera gelince canı azalacak.
                if collide(laser, player):
                   player.health -= 10
                   aliens_lasers.remove(laser)
                   
                   
                       
            #alienların kendisi playera denk gelince player ölür.
            if collide(alien, player):
               player.health -=1
                  
                
            if alien.y > HEIGHT:           #uzaylılar alt sınıra gelip tamamen kaybolunca oyunu bitir.
                aliens.remove(alien)
                game_over = True
                break
    
                
 
        for event in pygame.event.get():  # pygame olaylarını (event) kontrol ediyor
            if event.type == pygame.QUIT: # Eğer olayın türü pygame.QUIT ise,
                                          # yani kullanıcı oyunu kapatmak için X düğmesine tıkladıysa                                        
                run = False               # run değişkenini False olarak ayarlayarak oyun döngüsünü sonlandırıyoruz        
                
               
        
        # Game Over kontrolü ve işlemi
        if player.health == 0:
            player.reduce_health(10)
            if(player.lives == 0):
                game_over = True

        if game_over:
           WINDOWS.fill((0, 0, 0))  # Ekranı siyah renge doldur
           font = pygame.font.SysFont("comicsans", 95)  # Yazı boyutunu 150 olarak ayarla
           game_over_text = font.render("Game Over", True, (255, 255, 255))
           x = WIDTH/2 - game_over_text.get_width()/2
           y = HEIGHT/2 - game_over_text.get_height()/2
           WINDOWS.blit(game_over_text, (x, y))
           pygame.display.update()
           pygame.time.wait(3000)
           run = False  # Oyun döngüsünden çıkın


                
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WINDOWS.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WINDOWS.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_time = pygame.time.get_ticks()

                main()
                
                
main_menu()