import pygame, sys
from utils.colores import *

# --- Importar niveles del Mundo 2 ---
from unidades.unidad2.nivel1 import nivel1
from unidades.unidad2.nivel2 import nivel2
from unidades.unidad2.nivel3 import nivel3
from unidades.unidad2.nivel4 import nivel4
from unidades.unidad2.nivel5 import nivel5
from unidades.unidad2.nivel6 import nivel6
from unidades.unidad2.nivel7 import nivel7
from unidades.unidad2.nivel8 import nivel8
from unidades.unidad2.nivel9 import nivel9
from unidades.unidad2.nivel10 import nivel10

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
    fuente_boton = pygame.font.SysFont("Georgia", 24, bold=True)  # Reducido para más espacio

    reloj = pygame.time.Clock()

    # Subniveles originales (lado izquierdo)
    subniveles_izquierda = [
        "Montante",
        "Gauss-Jordan",
        "Eliminación Gaussiana",
        "Gauss-Seidel",
        "Jacobi"
    ]

    # Nuevos subniveles (lado derecho)
    subniveles_derecha = [
        "Lineal Recta",
        "Cuadrática",
        "Cúbica",
        "Lineal con Función",
        "Cuadrática con Función"
    ]

    # --- Colores ---
    color_boton = (10, 25, 60)        # azul marino oscuro
    color_hover = (30, 50, 100)       # azul más claro
    color_borde = (180, 140, 90)      # dorado madera
    color_texto = (255, 240, 200)

    # --- Fondo ---
    fondo = pygame.image.load("assets/images/fondo2.png").convert()
    fondo = pygame.transform.scale(fondo, (ancho, alto))

    # --- Crear botones del lado izquierdo ---
    botones_izquierda = []
    espacio_y = 70  # Reducido para caber 10 botones
    ancho_boton = 450  # Ancho reducido para dos columnas
    alto_boton = 55    # Altura reducida
    inicio_y = 260

    for i, nombre in enumerate(subniveles_izquierda):
        x = ancho // 4 - ancho_boton // 2  # Columna izquierda
        y = inicio_y + i * espacio_y
        botones_izquierda.append(
            Boton(nombre, (x, y), (ancho_boton, alto_boton), fuente_boton,
                  color_boton, color_texto, color_hover, color_borde)
        )

    # --- Crear botones del lado derecho ---
    botones_derecha = []
    for i, nombre in enumerate(subniveles_derecha):
        x = 3 * ancho // 4 - ancho_boton // 2  # Columna derecha
        y = inicio_y + i * espacio_y
        botones_derecha.append(
            Boton(nombre, (x, y), (ancho_boton, alto_boton), fuente_boton,
                  color_boton, color_texto, color_hover, color_borde)
        )

    # --- Combinar todos los botones ---
    botones = botones_izquierda + botones_derecha

    # --- Diccionario de funciones de nivel ---
    funciones_niveles = {
        # Niveles originales (0-4)
        0: nivel1,
        1: nivel2,
        2: nivel3,
        3: nivel4,
        4: nivel5,
        # Nuevos niveles (5-9)
        5: nivel6,
        6: nivel7,
        7: nivel8,
        8: nivel9,
        9: nivel10
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
                        nivel_id = i
                        print(f"🧭 Entrando al subnivel {nivel_id+1}: {boton.texto}")
                        if nivel_id in funciones_niveles:
                            funciones_niveles[nivel_id](pantalla, ancho, alto)
                        else:
                            print(f"❌ Error: No se encontró la función para el nivel {nivel_id+1}")

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

        # --- Títulos de columnas ---
        fuente_columna = pygame.font.SysFont("Georgia", 32, bold=True)
        
        # Columna izquierda
        titulo_izquierda = fuente_columna.render("Métodos de Solución", True, (255, 220, 140))
        pantalla.blit(titulo_izquierda, (ancho//4 - titulo_izquierda.get_width()//2, 200))
        
        # Columna derecha
        titulo_derecha = fuente_columna.render("Ajuste de Curvas", True, (255, 220, 140))
        pantalla.blit(titulo_derecha, (3*ancho//4 - titulo_derecha.get_width()//2, 200))

        # --- Dibujar botones ---
        for boton in botones:
            boton.actualizar(mouse_pos)
            boton.dibujar(pantalla)

        # --- Instrucciones ---
        fuente_instrucciones = pygame.font.SysFont("Arial", 18)
        instrucciones = fuente_instrucciones.render("Presiona ESC para volver al menú principal", True, (200, 200, 200))
        pantalla.blit(instrucciones, (ancho//2 - instrucciones.get_width()//2, alto - 40))

        pygame.display.flip()
        reloj.tick(60)