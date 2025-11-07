import pygame, sys
from utils.colores import *

pygame.init()

# --- Clase Boton ---
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


def niveles_menu_mundo4(pantalla, ancho, alto):
    fuente_titulo = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 80)
    fuente_subtitulo = pygame.font.SysFont("Georgia", 44, bold=True)
    fuente_boton = pygame.font.SysFont("Georgia", 28, bold=True)

    reloj = pygame.time.Clock()

    subniveles = [
        "T mínimos cuadrados",
        "Cuadrática Cúbica",
        "Lineal Cuadrática Función",
        "Línea Recta",
        "Otro",
        "Otro 2"
    ]

    # --- Colores ---
    color_boton = (10, 25, 60)        # azul marino oscuro
    color_hover = (30, 50, 100)       # azul más claro al pasar mouse
    color_borde = (180, 140, 90)      # dorado madera
    color_texto = (255, 240, 200)

    # --- Fondo ---
    fondo = pygame.image.load("assets/images/fondo2.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # --- Crear botones en dos columnas (3 y 3) ---
    botones = []
    espacio_y = 75
    ancho_boton = 500
    alto_boton = 55
    inicio_y = 230

    for i, nombre in enumerate(subniveles):
        if i < 3:
            x = ancho // 2 - 520      # columna izquierda
            y = inicio_y + i * espacio_y
        else:
            x = ancho // 2 + 20       # columna derecha
            y = inicio_y + (i - 3) * espacio_y

        botones.append(
            Boton(nombre, (x, y), (ancho_boton, alto_boton), fuente_boton,
                  color_boton, color_texto, color_hover, color_borde)
        )

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton.fue_click(mouse_pos):
                        print(f"Entrando al subnivel: {boton.texto}")
                        # Aquí puedes llamar a la función específica de cada subnivel

        # --- Fondo ---
        pantalla.blit(fondo, (0, 0))

        # --- Título con sombra ---
        sombra_titulo = fuente_titulo.render("MUNDO 4", True, (40, 20, 10))
        titulo = fuente_titulo.render("MUNDO 4", True, (255, 230, 180))
        pantalla.blit(sombra_titulo, (ancho//2 - sombra_titulo.get_width()//2 + 3, 63))
        pantalla.blit(titulo, (ancho//2 - titulo.get_width()//2, 60))

        # --- Subtítulo con sombra ---
        sombra_sub = fuente_subtitulo.render("Ajuste de curvas y regresión", True, (30, 15, 5))
        subtitulo = fuente_subtitulo.render("Ajuste de curvas y regresión", True, (255, 210, 150))
        pantalla.blit(sombra_sub, (ancho//2 - sombra_sub.get_width()//2 + 2, 138))
        pantalla.blit(subtitulo, (ancho//2 - subtitulo.get_width()//2, 135))

        # --- Dibujar botones ---
        for boton in botones:
            boton.actualizar(mouse_pos)
            boton.dibujar(pantalla)

        pygame.display.flip()
        reloj.tick(60)
