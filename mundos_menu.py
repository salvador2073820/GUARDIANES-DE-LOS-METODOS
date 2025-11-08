import pygame, sys, math, random
from utils.colores import *

# Importamos los menús de niveles de cada mundo
from nivelesmenumundos.nivelesmenu_mundo1 import niveles_menu_mundo1
from nivelesmenumundos.nivelesmenu_mundo2 import niveles_menu_mundo2
from nivelesmenumundos.nivelesmenu_mundo3 import niveles_menu_mundo3
from nivelesmenumundos.nivelesmenu_mundo4 import niveles_menu_mundo4

pygame.font.init()
clock = pygame.time.Clock()

# --- MÚSICA DE FONDO ---
pygame.mixer.init()
try:
    pygame.mixer.music.load("assets/music/medieval_theme.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    print("Música no encontrada")

# Fuentes
fuente_titulo = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 90)
fuente_mundo = pygame.font.SysFont("Garamond", 26, bold=True)
fuente_icono = pygame.font.SysFont("Segoe UI Emoji", 60)
fuente_subtitulo = pygame.font.SysFont("Georgia", 22)

# --- Partículas mágicas ---
class Particula:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radio = random.randint(1, 3)
        self.vel = random.uniform(0.2, 0.8)
        self.color = (255, random.randint(180, 220), 100)

    def mover(self, alto):
        self.y -= self.vel
        if self.y < 0:
            self.y = alto
            self.x = random.randint(0, 1280)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

# --- Clase Mundo ---
class Mundo:
    def __init__(self, nombre, x, y, icono, id_mundo, desbloqueado=True):
        self.nombre = nombre
        self.pos = (x, y)
        self.radio = 85
        self.icono = icono
        self.desbloqueado = desbloqueado
        self.id_mundo = id_mundo

    def dibujar(self, pantalla, mouse_pos, tiempo):
        hovered = self.rect().collidepoint(mouse_pos)
        pulso = (math.sin(tiempo * 2) + 1) / 2
        intensidad = 180 + int(75 * pulso)
        color_base = (212, 175, 55) if self.desbloqueado else (130, 130, 130)
        resplandor = (intensidad, intensidad - 30, 60) if hovered else color_base

        pygame.draw.circle(pantalla, (25, 10, 0), self.pos, self.radio + 6)
        pygame.draw.circle(pantalla, resplandor, self.pos, self.radio, width=5)

        texto_icono = fuente_icono.render(self.icono, True, resplandor)
        pantalla.blit(texto_icono, texto_icono.get_rect(center=self.pos))

        nombre = fuente_mundo.render(self.nombre, True, BLANCO_AZULADO)
        texto_rect = nombre.get_rect(center=(self.pos[0], self.pos[1] + self.radio + 40))
        pantalla.blit(nombre, texto_rect)

    def rect(self):
        return pygame.Rect(self.pos[0] - self.radio, self.pos[1] - self.radio, self.radio * 2, self.radio * 2)

    def fue_click(self, mouse_pos):
        dx, dy = mouse_pos[0] - self.pos[0], mouse_pos[1] - self.pos[1]
        return (dx * dx + dy * dy) ** 0.5 < self.radio

# --- Pantalla de mundos ---
def seleccion_mundo(pantalla, ancho, alto):
    mundos = [
        Mundo("Interpolación y ecuaciones no lineales", 350, 220, "⚗️", 1),
        Mundo("Ecuaciones lineales y ajuste de curvas", 900, 250, "📜", 2),
        Mundo("Diferenciación e integración numérica", 950, 530, "📘", 3),
        Mundo("Ecuaciones diferenciales ordinarias", 350, 550, "🕯️", 4)
    ]

    particulas = [Particula(random.randint(0, ancho), random.randint(0, alto)) for _ in range(60)]

    fondo = pygame.Surface((ancho, alto))
    for y in range(alto):
        ratio = y / alto
        r = int(180 + 40 * ratio)
        g = int(160 + 60 * ratio)
        b = int(100 + 20 * ratio)
        pygame.draw.line(fondo, (r, g, b), (0, y), (ancho, y))

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tiempo = pygame.time.get_ticks() / 1000
        pantalla.blit(fondo, (0, 0))

        for p in particulas:
            p.mover(alto)
            p.dibujar(pantalla)

        # Título y subtítulo
        titulo = fuente_titulo.render("NUMÉRIA", True, (255, 230, 150))
        pantalla.blit(titulo, titulo.get_rect(center=(ancho // 2, 100)))
        subtitulo = fuente_subtitulo.render("El reino de los métodos numéricos", True, (240, 230, 200))
        pantalla.blit(subtitulo, subtitulo.get_rect(center=(ancho // 2, 160)))

        # Dibujar caminos entre mundos
        puntos = [m.pos for m in mundos]
        for i in range(len(puntos) - 1):
            pygame.draw.lines(pantalla, (110, 90, 40), False, [puntos[i], puntos[i + 1]], 8)
            for j in range(0, 100, 8):
                t = j / 100
                x = puntos[i][0] * (1 - t) + puntos[i + 1][0] * t
                y = puntos[i][1] * (1 - t) + puntos[i + 1][1] * t
                pygame.draw.circle(pantalla, (255, 220, 120), (int(x), int(y)), 2)

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # ← Regresar al main.py si se presiona ESC
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for m in mundos:
                    if m.fue_click(mouse_pos):
                        # Redirige según el mundo clickeado
                        if m.id_mundo == 1:
                            niveles_menu_mundo1(pantalla, ancho, alto)
                        elif m.id_mundo == 2:
                            niveles_menu_mundo2(pantalla, ancho, alto)
                        elif m.id_mundo == 3:
                            niveles_menu_mundo3(pantalla, ancho, alto)
                        elif m.id_mundo == 4:
                            niveles_menu_mundo4(pantalla, ancho, alto)

        for m in mundos:
            m.dibujar(pantalla, mouse_pos, tiempo)

        pygame.display.flip()
        clock.tick(60)
