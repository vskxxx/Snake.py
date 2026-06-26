
import pygame
from Kierunek import Kierunek
 
class Waz(pygame.sprite.Sprite):
    def __init__(self):
        #oryginalny obraz glowy
        self.oryginalny_obraz = pygame.image.load("images/head.png")
        #obraz pomocniczny, bedzie sie on zmienial przy zmienie kierunku gracza
        self.obraz = pygame.transform.rotate(self.oryginalny_obraz, 0)
        #wspolrzednie glowy
        self.rect = self.obraz.get_rect(center=(12*32+16, 9*32+16))
        #zmienne odpowiedzialne za kierunek, oraz nowy wyznaczony kierunek
        self.kierunek = Kierunek.GORA
        self.nowy_kierunek = Kierunek.GORA
 
    def zmien_kierunek(self, kierunek):
        zmiana_mozliwa = True
        if kierunek == Kierunek.GORA and self.kierunek == Kierunek.DOL:
            zmiana_mozliwa = False
        if kierunek == Kierunek.DOL and self.kierunek == Kierunek.GORA:
            zmiana_mozliwa = False
        if kierunek == Kierunek.LEWO and self.kierunek == Kierunek.PRAWO:
            zmiana_mozliwa = False
        if kierunek == Kierunek.PRAWO and self.kierunek == Kierunek.LEWO:
            zmiana_mozliwa = False
        if zmiana_mozliwa: 
            self.nowy_kierunek = kierunek
 
    def aktualizuj(self):
        self.kierunek = self.nowy_kierunek
        self.obraz = pygame.transform.rotate(self.oryginalny_obraz, (self.kierunek.value*-90))
 
        if self.kierunek == Kierunek.GORA:
            self.rect.move_ip(0, -32)
        if self.kierunek == Kierunek.PRAWO:
            self.rect.move_ip(32, 0)
        if self.kierunek == Kierunek.LEWO:
            self.rect.move_ip(-32, 0)
        if self.kierunek == Kierunek.DOL:
            self.rect.move_ip(0, 32)
import pygame
from Kierunek import Kierunek

class Waz(pygame.sprite.Sprite):
    def __init__(self):
        self.oryginalny_obraz = pygame.image.load("PYGAME/Snake/images/head.png")
        self.obraz = pygame.transform.rotate(self.oryginalny_obraz, 0)
        self.rect = self.obraz.get_rect(center=(12*32+16, 9*32+16))
        self.kierunek = Kierunek.GORA
        self.nowy_kierunek = Kierunek.GORA

    def zmien_kierunek(self, kierunek):
        zmiana_mozliwa = True
        if kierunek == Kierunek.GORA and self.kierunek == Kierunek.DOL:
            zmiana_mozliwa = False
        if kierunek == Kierunek.DOL and self.kierunek == Kierunek.GORA:
            zmiana_mozliwa = False
        if kierunek == Kierunek.LEWO and self.kierunek == Kierunek.PRAWO:
            zmiana_mozliwa = False
        if kierunek == Kierunek.PRAWO and self.kierunek == Kierunek.LEWO:
            zmiana_mozliwa = False
        if zmiana_mozliwa:
            self.nowy_kierunek = kierunek

    def aktualizuj(self):
        self.kierunek = self.nowy_kierunek
        self.obraz = pygame.transform.rotate(self.oryginalny_obraz, self.kierunek.value * -90)

        if self.kierunek == Kierunek.GORA:
            self.rect.move_ip(0, -32)
        if self.kierunek == Kierunek.PRAWO:
            self.rect.move_ip(32, 0)
        if self.kierunek == Kierunek.LEWO:
            self.rect.move_ip(-32, 0)
        if self.kierunek == Kierunek.DOL:
            self.rect.move_ip(0, 32)

def sprawdz_kolizje(self):
    #ugryzienie ogona
    for segment in self.segmenty:
        if self.rect.topleft == segment.pozycja.topleft:
            return True
    #wyjście poza ekran
    if self.rect.top < 0 or self.rect.top >= 608:
        return True
    if self.rect.left < 0 or self.rect.left >= 800:
        return True
    return False