import pygame, sys
from mundos_menu import seleccion_mundo
from utils.colores import *

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guardianes de los Métodos")

# --- FUENTES ---
fuente_titulo = pygame.font.SysFont("Segoe UI Black", 70)
fuente_boton = pygame.font.SysFont("Segoe UI", 38)
clock = pygame.time.Clock()

# --- CLASE BOTÓN ---
class Boton:
    def __init__(self, texto, x, y, ancho, alto):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color_actual = AZUL_BASE

    def dibujar(self, pantalla, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color_actual = AZUL_HOVER
        else:
            self.color_actual = AZUL_BASE

        sombra = self.rect.move(0, 5)
        pygame.draw.rect(pantalla, (10, 15, 30), sombra, border_radius=12)
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=12)
        texto_render = fuente_boton.render(self.texto, True, BLANCO)
        pantalla.blit(texto_render, texto_render.get_rect(center=self.rect.center))

    def fue_click(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

# --- MENÚ PRINCIPAL ---
def menu_principal():
    boton_jugar = Boton("JUGAR", ANCHO//2 - 150, 400, 300, 70)
    boton_salir = Boton("SALIR", ANCHO//2 - 150, 500, 300, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        dibujar_degradado(pantalla, ANCHO, ALTO, DEGRADADO_SUPERIOR, FONDO_OSCURO)

        titulo = fuente_titulo.render("GUARDIANES DE LOS MÉTODOS", True, BLANCO_AZULADO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO//2, 200)))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.fue_click(mouse_pos):
                    seleccion_mundo(pantalla, ANCHO, ALTO)
                if boton_salir.fue_click(mouse_pos):
                    pygame.quit(); sys.exit()

        boton_jugar.dibujar(pantalla, mouse_pos)
        boton_salir.dibujar(pantalla, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

# --- EJECUTAR ---
if __name__ == "__main__":
    menu_principal()
