import pygame, sys

def nivel7(pantalla, ancho, alto):
    fuente = pygame.font.SysFont("Arial", 40)
    reloj = pygame.time.Clock()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return  # vuelve al menú de niveles

        pantalla.fill((30, 40, 60))
        texto = fuente.render("Nivel 7 mo", True, (255,255,255))
        pantalla.blit(texto, texto.get_rect(center=(ancho//2, alto//2)))
        pygame.display.flip()
        reloj.tick(60)