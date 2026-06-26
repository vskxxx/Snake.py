import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Game constants
SZEROKOSC_OBRAZU = 800
WYSOKOSC_OBRAZU = 600
ROZMIAR_KOMORKI = 32
SZEROKOSC_PLANSZY = SZEROKOSC_OBRAZU // ROZMIAR_KOMORKI
WYSOKOSC_PLANSZY = WYSOKOSC_OBRAZU // ROZMIAR_KOMORKI

# Colors
CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)

class Snake:
    def __init__(self):
        self.pozycje = [(SZEROKOSC_PLANSZY // 2, WYSOKOSC_PLANSZY // 2)]
        self.kierunek = (1, 0)  # Right
        self.rosnij = False
        
        # Load images
        try:
            self.glowa_obraz = pygame.image.load("Snake.py/Images.py/head.png")
            self.segment_obraz = pygame.image.load("Snake.py/Images.py/segment.png")
        except pygame.error:
            # Fallback if images not found - use colored rectangles
            self.glowa_obraz = pygame.Surface((ROZMIAR_KOMORKI, ROZMIAR_KOMORKI))
            self.glowa_obraz.fill(ZIELONY)
            self.segment_obraz = pygame.Surface((ROZMIAR_KOMORKI, ROZMIAR_KOMORKI))
            self.segment_obraz.fill((0, 200, 0))
    
    def zmien_kierunek(self, nowy_kierunek):
        # Prevent snake from going backwards
        if (nowy_kierunek[0] * -1, nowy_kierunek[1] * -1) != self.kierunek:
            self.kierunek = nowy_kierunek
    
    def ruszaj(self):
        glowa = self.pozycje[0]
        nowa_glowa = (glowa[0] + self.kierunek[0], glowa[1] + self.kierunek[1])
        
        # Check wall collision
        if (nowa_glowa[0] < 0 or nowa_glowa[0] >= SZEROKOSC_PLANSZY or
            nowa_glowa[1] < 0 or nowa_glowa[1] >= WYSOKOSC_PLANSZY):
            return False
        
        # Check self collision
        if nowa_glowa in self.pozycje:
            return False
        
        self.pozycje.insert(0, nowa_glowa)
        
        if not self.rosnij:
            self.pozycje.pop()
        else:
            self.rosnij = False
        
        return True
    
    def rysuj(self, ekran):
        for i, pozycja in enumerate(self.pozycje):
            x = pozycja[0] * ROZMIAR_KOMORKI
            y = pozycja[1] * ROZMIAR_KOMORKI
            
            if i == 0:  # Head
                ekran.blit(self.glowa_obraz, (x, y))
            else:  # Body segment
                ekran.blit(self.segment_obraz, (x, y))

class Apple:
    def __init__(self):
        self.pozycja = (0, 0)
        self.generuj_pozycje()
        
        try:
            self.obraz = pygame.image.load("Snake.py/Images.py/apple.png")
        except pygame.error:
            # Fallback if image not found
            self.obraz = pygame.Surface((ROZMIAR_KOMORKI, ROZMIAR_KOMORKI))
            self.obraz.fill(CZERWONY)
    
    def generuj_pozycje(self):
        self.pozycja = (random.randint(0, SZEROKOSC_PLANSZY - 1), 
                       random.randint(0, WYSOKOSC_PLANSZY - 1))
    
    def rysuj(self, ekran):
        x = self.pozycja[0] * ROZMIAR_KOMORKI
        y = self.pozycja[1] * ROZMIAR_KOMORKI
        ekran.blit(self.obraz, (x, y))

class Game:
    def __init__(self):
        self.ekran = pygame.display.set_mode((SZEROKOSC_OBRAZU, WYSOKOSC_OBRAZU))
        pygame.display.set_caption("Snake Game")
        self.zegar = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple()
        self.wynik = 0
        self.font = pygame.font.Font(None, 36)
        
        # Load background
        try:
            self.tlo = pygame.image.load("Snake.py/Images.py/background (1).png")
            self.tlo = pygame.transform.scale(self.tlo, (SZEROKOSC_OBRAZU, WYSOKOSC_OBRAZU))
        except pygame.error:
            # Create simple background
            self.tlo = pygame.Surface((SZEROKOSC_OBRAZU, WYSOKOSC_OBRAZU))
            self.tlo.fill((50, 50, 50))
    
    def obsluż_zdarzenia(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.zmien_kierunek((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.snake.zmien_kierunek((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.snake.zmien_kierunek((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.zmien_kierunek((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def aktualizuj(self):
        if not self.snake.ruszaj():
            return False  # Game over
        
        # Check if snake ate apple
        if self.snake.pozycje[0] == self.apple.pozycja:
            self.wynik += 10
            self.snake.rosnij = True
            # Generate new apple position (avoid snake body)
            while self.apple.pozycja in self.snake.pozycje:
                self.apple.generuj_pozycje()
        
        return True
    
    def rysuj(self):
        self.ekran.blit(self.tlo, (0, 0))
        self.snake.rysuj(self.ekran)
        self.apple.rysuj(self.ekran)
        
        # Draw score
        tekst_wynik = self.font.render(f"Wynik: {self.wynik}", True, BIALY)
        self.ekran.blit(tekst_wynik, (10, 10))
        
        pygame.display.flip()
    
    def pokaz_game_over(self):
        overlay = pygame.Surface((SZEROKOSC_OBRAZU, WYSOKOSC_OBRAZU))
        overlay.set_alpha(128)
        overlay.fill(CZARNY)
        self.ekran.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.Font(None, 72)
        restart_font = pygame.font.Font(None, 36)
        
        game_over_text = game_over_font.render("GAME OVER", True, CZERWONY)
        final_score_text = restart_font.render(f"Końcowy wynik: {self.wynik}", True, BIALY)
        restart_text = restart_font.render("Naciśnij SPACJĘ aby zagrać ponownie lub ESC aby wyjść", True, BIALY)
        
        # Center the text
        game_over_rect = game_over_text.get_rect(center=(SZEROKOSC_OBRAZU // 2, WYSOKOSC_OBRAZU // 2 - 50))
        score_rect = final_score_text.get_rect(center=(SZEROKOSC_OBRAZU // 2, WYSOKOSC_OBRAZU // 2))
        restart_rect = restart_text.get_rect(center=(SZEROKOSC_OBRAZU // 2, WYSOKOSC_OBRAZU // 2 + 50))
        
        self.ekran.blit(game_over_text, game_over_rect)
        self.ekran.blit(final_score_text, score_rect)
        self.ekran.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def uruchom(self):
        gra_dziala = True
        game_over = False
        
        while gra_dziala:
            if not game_over:
                gra_dziala = self.obsluż_zdarzenia()
                if gra_dziala:
                    game_over = not self.aktualizuj()
                    self.rysuj()
            else:
                # Game over state
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gra_dziala = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Restart game
                            self.snake = Snake()
                            self.apple = Apple()
                            self.wynik = 0
                            game_over = False
                        elif event.key == pygame.K_ESCAPE:
                            gra_dziala = False
                
                self.pokaz_game_over()
            
            self.zegar.tick(8)  # Snake speed
        
        pygame.quit()
        sys.exit()

# Run the game
if __name__ == "__main__":
    gra = Game()
    gra.uruchom()