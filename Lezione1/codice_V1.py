import pygame
import sys
import random
# Inizializza Pygame
pygame.init()
# Costanti schermo
LARGHEZZA = 400
ALTEZZA = 600
finestra = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Gioco dell'Uccello - Completo")
 
# Colori
AZZURRO = (135, 206, 235)
VERDE = (0, 200, 0)
ROSSO = (255, 0, 0)
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
 
# Uccello (quadrato)
DIMENSIONE_UCCELLO = 30
uccello_x = 100
uccello_y = ALTEZZA // 2
velocità_y = 0
gravità = 0.3 
salto = -5
 
# Muri (rettangoli)
LARGHEZZA_MURO = 60
SPAZIO_VUOTO = 150
velocità_muri = 3
lista_muri = []
 
# justin
def crea_muro():
   altezza_superiore = random.randint(100, 300)
   x = LARGHEZZA + 100
   return [x, altezza_superiore]
 
# Timer per generare muri ogni tot tempo
AGGIUNGI_MURO = pygame.USEREVENT + 1
pygame.time.set_timer(AGGIUNGI_MURO, 1500)
# Font per punteggio
font = pygame.font.SysFont(None, 40)
punteggio = 0
# Clock
orologio = pygame.time.Clock()
FPS = 60
# Stato del gioco
in_esecuzione = True
in_pausa = False
 
def mostra_testo(testo, colore, y):
   superficie = font.render(testo, True, colore)
   rett = superficie.get_rect(center=(LARGHEZZA // 2, y))
   finestra.blit(superficie, rett)
# Gioco principale
while in_esecuzione:
   orologio.tick(FPS)
   for evento in pygame.event.get():
       if evento.type == pygame.QUIT:
           in_esecuzione = False
       if evento.type == pygame.KEYDOWN:
           if evento.key == pygame.K_SPACE and not in_pausa:
               velocità_y = salto
           if evento.key == pygame.K_r and in_pausa:
               # Resetta il gioco
               uccello_y = ALTEZZA // 2
               velocità_y = 0
               lista_muri.clear()
               punteggio = 0
               in_pausa = False
       if evento.type == AGGIUNGI_MURO and not in_pausa:
           lista_muri.append(crea_muro())
   if not in_pausa:
       # Movimento uccello
       velocità_y += gravità
       uccello_y += velocità_y
       # Movimento muri
       for muro in lista_muri:
           muro[0] -= velocità_muri
       # Rimuovi muri fuori dallo schermo
       lista_muri = [m for m in lista_muri if m[0] + LARGHEZZA_MURO > 0]
       # Controlla collisioni
       rett_uccello = pygame.Rect(uccello_x, uccello_y, DIMENSIONE_UCCELLO, DIMENSIONE_UCCELLO)
       for muro in lista_muri:
           x = muro[0]
           altezza_superiore = muro[1]
           rett_muro_sopra = pygame.Rect(x, 0, LARGHEZZA_MURO, altezza_superiore)
           rett_muro_sotto = pygame.Rect(x, altezza_superiore + SPAZIO_VUOTO, LARGHEZZA_MURO, ALTEZZA)
           if rett_uccello.colliderect(rett_muro_sopra) or rett_uccello.colliderect(rett_muro_sotto):
               in_pausa = True
       # Controlla se fuori dallo schermo
       if uccello_y < 0 or uccello_y + DIMENSIONE_UCCELLO > ALTEZZA:
           in_pausa = True
       # Aumenta punteggio
       for muro in lista_muri:
           if muro[0] + LARGHEZZA_MURO == uccello_x:
               punteggio += 1
   # Disegna sfondo
   finestra.fill(AZZURRO)
   # Disegna muri
   for muro in lista_muri:
       x = muro[0]
       altezza = muro[1]
       pygame.draw.rect(finestra, VERDE, (x, 0, LARGHEZZA_MURO, altezza))
       pygame.draw.rect(finestra, VERDE, (x, altezza + SPAZIO_VUOTO, LARGHEZZA_MURO, ALTEZZA - (altezza + SPAZIO_VUOTO)))
   # Disegna uccello
   pygame.draw.rect(finestra, ROSSO, (uccello_x, uccello_y, DIMENSIONE_UCCELLO, DIMENSIONE_UCCELLO))
   # Disegna punteggio
   testo_punti = font.render(f"Punteggio: {punteggio}", True, NERO)
   finestra.blit(testo_punti, (10, 10))
   # Se in pausa
   if in_pausa:
       mostra_testo("Hai perso!", ROSSO, ALTEZZA // 2 - 30)
       mostra_testo("Premi R per riprovare", NERO, ALTEZZA // 2 + 10)
   pygame.display.update()
pygame.quit()
sys.exit()
