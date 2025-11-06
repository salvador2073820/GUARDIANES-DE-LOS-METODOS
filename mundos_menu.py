import pygame, sys, math, random
from utils.colores import *

pygame.font.init()
clock = pygame.time.Clock()

# Fuentes
fuente_titulo = pygame.font.SysFont("Garamond", 90, bold=True)
fuente_mundo = pygame.font.SysFont("Garamond", 26, bold=True)
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
    def __init__(self, nombre, x, y, icono, desbloqueado=True):
        self.nombre = nombre
        self.pos = (x, y)
        self.radio = 85
        self.icono = icono
        self.desbloqueado = desbloqueado

    def dibujar(self, pantalla, mouse_pos):
        hovered = self.rect().collidepoint(mouse_pos)
        color_borde = (212,175,55) if self.desbloqueado else (100,100,100)
        resplandor = (255,223,100) if hovered and self.desbloqueado else color_borde

        # Círculo dorado con resplandor
        pygame.draw.circle(pantalla, (20,10,0), self.pos, self.radio+5)
        pygame.draw.circle(pantalla, resplandor, self.pos, self.radio, width=4)

        # Ícono o símbolo
        texto_icono = fuente_titulo.render(self.icono, True, resplandor)
        texto_icono = pygame.transform.scale(texto_icono, (60,60))
        pantalla.blit(texto_icono, texto_icono.get_rect(center=self.pos))

        # Nombre
        nombre = fuente_mundo.render(self.nombre, True, BLANCO_AZULADO)
        texto_rect = nombre.get_rect(center=(self.pos[0], self.pos[1] + self.radio + 40))
        pantalla.blit(nombre, texto_rect)

    def rect(self):
        return pygame.Rect(self.pos[0]-self.radio, self.pos[1]-self.radio, self.radio*2, self.radio*2)

    def fue_click(self, mouse_pos):
        if not self.desbloqueado: return False
        dx, dy = mouse_pos[0]-self.pos[0], mouse_pos[1]-self.pos[1]
        return (dx*dx + dy*dy)**0.5 < self.radio

# --- Pantalla de mundos ---
def seleccion_mundo(pantalla, ancho, alto):
    # Posiciones distribuidas estilo mapa
    mundos = [
        Mundo("Interpolación y ecuaciones no lineales", 350, 220, "⚗️", True),
        Mundo("Ecuaciones lineales y ajuste de curvas", 900, 250, "📜", True),
        Mundo("Diferenciación e integración numérica", 750, 500, "📘", False),
        Mundo("Ecuaciones diferenciales ordinarias", 450, 520, "🕯️", False)
    ]
    # Partículas decorativas
    particulas = [Particula(random.randint(0, ancho), random.randint(0, alto)) for _ in range(60)]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Fondo pergamino dorado
        for y in range(alto):
            ratio = y/alto
            r = int(180 + 40*ratio)
            g = int(160 + 60*ratio)
            b = int(100 + 20*ratio)
            pygame.draw.line(pantalla, (r,g,b), (0,y), (ancho,y))

        # Polvo mágico
        for p in particulas:
            p.mover(alto)
            p.dibujar(pantalla)

        # Título
        titulo = fuente_titulo.render("NUMÉRIA", True, (255,230,150))
        pantalla.blit(titulo, titulo.get_rect(center=(ancho//2, 100)))
        subtitulo = fuente_subtitulo.render("El reino de los métodos numéricos", True, (240,230,200))
        pantalla.blit(subtitulo, subtitulo.get_rect(center=(ancho//2, 160)))

        # Caminos conectando mundos
        puntos = [m.pos for m in mundos]
        for i in range(len(puntos)-1):
            pygame.draw.lines(pantalla, (110,90,40), False, [puntos[i], puntos[i+1]], 8)
            # Punteado luminoso
            for j in range(0,100,8):
                t = j/100
                x = puntos[i][0]*(1-t) + puntos[i+1][0]*t
                y = puntos[i][1]*(1-t) + puntos[i+1][1]*t
                pygame.draw.circle(pantalla, (255,220,120), (int(x),int(y)), 2)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for m in mundos:
                    if m.fue_click(mouse_pos):
                        print(f"🏰 Entrando a {m.nombre}")
                        return

        # Dibujar mundos
        for m in mundos:
            m.dibujar(pantalla, mouse_pos)

        pygame.display.flip()
        clock.tick(60)
