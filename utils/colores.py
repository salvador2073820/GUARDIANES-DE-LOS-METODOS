import pygame

# Paleta azul minimalista
FONDO_OSCURO = (15, 23, 42)
DEGRADADO_SUPERIOR = (30, 58, 138)
AZUL_BASE = (37, 99, 235)
AZUL_HOVER = (96, 165, 250)
AZUL_BLOQUEADO = (60, 80, 130)
BLANCO = (255, 255, 255)
BLANCO_AZULADO = (240, 249, 255)
DORADO = (255, 215, 0)

def dibujar_degradado(pantalla, ancho, alto, color_superior, color_inferior):
    """Dibuja un degradado vertical azul elegante."""
    for y in range(alto):
        ratio = y / alto
        r = int(color_superior[0] * (1 - ratio) + color_inferior[0] * ratio)
        g = int(color_superior[1] * (1 - ratio) + color_inferior[1] * ratio)
        b = int(color_superior[2] * (1 - ratio) + color_inferior[2] * ratio)
        pygame.draw.line(pantalla, (r, g, b), (0, y), (ancho, y))
