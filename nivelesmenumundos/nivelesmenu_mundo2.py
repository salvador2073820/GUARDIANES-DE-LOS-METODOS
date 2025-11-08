import pygame, sys
from utils.colores import *

# --- Importar niveles del Mundo 2 ---
from unidades.unidad2.nivel1 import nivel1
from unidades.unidad2.nivel2 import nivel2
from unidades.unidad2.nivel3 import nivel3
from unidades.unidad2.nivel4 import nivel4
from unidades.unidad2.nivel5 import nivel5

pygame.init()

# --- Clase Botón ---
class Boton:
    def __init__(self, texto, pos, tamaño, fuente, color_fondo, color_texto, color_hover, color_borde):
        self.texto = texto
        self.pos = pos
        self.tamaño = tamaño
        self.fuente = fuente
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.color_hover = color_hover
        self.color_borde = color_borde
        self.rect = pygame.Rect(pos, tamaño)
        self.hover = False

    def dibujar(self, pantalla):
        color = self.color_hover if self.hover else self.color_fondo
        pygame.draw.rect(pantalla, color, self.rect, border_radius=16)
        pygame.draw.rect(pantalla, self.color_borde, self.rect, 4, border_radius=16)
        texto_render = self.fuente.render(self.texto, True, self.color_texto)
        pantalla.blit(texto_render, texto_render.get_rect(center=self.rect.center))

    def actualizar(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def fue_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def niveles_menu_mundo2(pantalla, ancho, alto):
    fuente_titulo = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 80)
    fuente_subtitulo = pygame.font.SysFont("Georgia", 44, bold=True)
    fuente_boton = pygame.font.SysFont("Georgia", 28, bold=True)

    reloj = pygame.time.Clock()

    subniveles = [
        "Montante",
        "Gauss-Jordan",
        "Eliminación Gaussiana",
        "Gauss-Seidel",
        "Jacobi"
    ]

    # --- Colores ---
    color_boton = (10, 25, 60)        # azul marino oscuro
    color_hover = (30, 50, 100)       # azul más claro
    color_borde = (180, 140, 90)      # dorado madera
    color_texto = (255, 240, 200)

    # --- Fondo ---
    fondo = pygame.image.load("assets/images/fondo2.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # --- Crear botones centrados ---
    botones = []
    espacio_y = 80
    ancho_boton = 520
    alto_boton = 60
    inicio_y = 260

    for i, nombre in enumerate(subniveles):
        x = ancho // 2 - ancho_boton // 2
        y = inicio_y + i * espacio_y
        botones.append(
            Boton(nombre, (x, y), (ancho_boton, alto_boton), fuente_boton,
                  color_boton, color_texto, color_hover, color_borde)
        )

    # --- Diccionario de funciones de nivel ---
    funciones_niveles = {
        0: nivel1,
        1: nivel2,
        2: nivel3,
        3: nivel4,
        4: nivel5
    }

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, boton in enumerate(botones):
                    if boton.fue_click(mouse_pos):
                        print(f"🧭 Entrando al subnivel {i+1}: {boton.texto}")
                        funciones_niveles[i](pantalla, ancho, alto)

        # --- Fondo ---
        pantalla.blit(fondo, (0, 0))

        # --- Título con sombra ---
        sombra_titulo = fuente_titulo.render("MUNDO 2", True, (40, 20, 10))
        titulo = fuente_titulo.render("MUNDO 2", True, (255, 230, 180))
        pantalla.blit(sombra_titulo, (ancho//2 - sombra_titulo.get_width()//2 + 3, 63))
        pantalla.blit(titulo, (ancho//2 - titulo.get_width()//2, 60))

        # --- Subtítulo con sombra ---
        sombra_sub = fuente_subtitulo.render("Ecuaciones lineales y ajuste de curvas", True, (30, 15, 5))
        subtitulo = fuente_subtitulo.render("Ecuaciones lineales y ajuste de curvas", True, (255, 210, 150))
        pantalla.blit(sombra_sub, (ancho//2 - sombra_sub.get_width()//2 + 2, 138))
        pantalla.blit(subtitulo, (ancho//2 - subtitulo.get_width()//2, 135))

        # --- Dibujar botones ---
        for boton in botones:
            boton.actualizar(mouse_pos)
            boton.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)
