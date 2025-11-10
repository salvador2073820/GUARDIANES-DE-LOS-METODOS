import pygame, sys
from mundos_menu import seleccion_mundo
from utils.colores import *

pygame.init()

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Guardianes de los Métodos")

clock = pygame.time.Clock()

# --- FUENTES PERSONALIZADAS ---
fuente_boton = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 42)

# --- IMÁGENES ---
fondo = pygame.image.load("assets/images/fondo.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

titulo_img = pygame.image.load("assets/images/titulo.png").convert_alpha()
titulo_rect = titulo_img.get_rect(center=(ANCHO//2, 180))

# --- COLORES ---
CAFE = (180, 140, 90)  # mismo color del borde del cuadro de créditos
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
BOTON_OSCURO = (25, 25, 40)  # color del interior del cuadro de créditos

# --- CLASE BOTÓN ---
class Boton:
    def __init__(self, texto, x, y, ancho, alto):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.base_color = BOTON_OSCURO
        self.hover_color = (40, 40, 65)
        self.borde_color = CAFE
        self.brillo = 0

    def dibujar_texto_con_borde(self, pantalla, texto, fuente, color_texto, color_borde, pos):
        """Dibuja texto con borde (efecto contorno)."""
        texto_surface = fuente.render(texto, True, color_texto)
        borde_surface = fuente.render(texto, True, color_borde)

        # Dibuja bordes alrededor (contorno negro)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            pantalla.blit(borde_surface, (pos[0] + dx, pos[1] + dy))
        pantalla.blit(texto_surface, pos)

    def dibujar(self, pantalla, mouse_pos):
        # Efecto hover
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
            self.brillo = min(self.brillo + 8, 80)
        else:
            color = self.base_color
            self.brillo = max(self.brillo - 8, 0)

        # Sombra
        sombra = self.rect.move(0, 6)
        pygame.draw.rect(pantalla, (10, 10, 20), sombra, border_radius=15)

        # Cuerpo del botón
        pygame.draw.rect(pantalla, color, self.rect, border_radius=15)
        pygame.draw.rect(pantalla, self.borde_color, self.rect, 4, border_radius=15)

        # Texto centrado con borde negro
        texto_render = fuente_boton.render(self.texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        self.dibujar_texto_con_borde(pantalla, self.texto, fuente_boton, BLANCO, NEGRO, texto_rect.topleft)

    def fue_click(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

# --- FUNCIÓN CRÉDITOS ---
def mostrar_creditos():
    """Muestra una ventana simple con los créditos."""
    ejecutando = True
    fuente_creditos = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 36)

    texto_creditos = [
        "Materia: Métodos numericos",
        "Desarrollado por:",
        "Mildred Urdiales",
        "Daniela Reyna",
        "Osmar Silva",
        "Emma Vera",
        "Salvador Hernandez",
        "",
        "Profesora: Dra. Oralia Zamora Pequeño",
    ]

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
                ejecutando = False  # Cierra la pantalla de créditos

        pantalla.blit(fondo, (0, 0))

        # --- Cuadro de créditos ---
        recto = pygame.Rect(ANCHO//2 - 350, ALTO//2 - 270, 700, 400) 
        pygame.draw.rect(pantalla, (20, 20, 40), recto, border_radius=20)
        pygame.draw.rect(pantalla, CAFE, recto, 5, border_radius=20)

        # --- Texto de créditos ---
        y = recto.y + 50
        for linea in texto_creditos:
            render = fuente_creditos.render(linea, True, BLANCO)
            rect_texto = render.get_rect(center=(ANCHO//2, y))
            pantalla.blit(render, rect_texto)
            y += 50

        pygame.display.flip()
        clock.tick(60)

# --- MENÚ PRINCIPAL ---
def menu_principal():
    boton_jugar = Boton("JUGAR", ANCHO//2 - 150, 400, 300, 70)
    boton_creditos = Boton("CRÉDITOS", ANCHO//2 - 150, 500, 300, 70)
    boton_salir = Boton("SALIR", ANCHO//2 - 150, 600, 300, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(titulo_img, titulo_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.fue_click(mouse_pos):
                    seleccion_mundo(pantalla, ANCHO, ALTO)
                if boton_creditos.fue_click(mouse_pos):
                    mostrar_creditos()
                if boton_salir.fue_click(mouse_pos):
                    pygame.quit(); sys.exit()

        boton_jugar.dibujar(pantalla, mouse_pos)
        boton_creditos.dibujar(pantalla, mouse_pos)
        boton_salir.dibujar(pantalla, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

# --- EJECUTAR ---
if __name__ == "__main__":
    menu_principal()
