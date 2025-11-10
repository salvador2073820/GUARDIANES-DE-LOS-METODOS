import pygame
import sys
import os 
import time # Necesario para la animación

# --- SOLUCIÓN AL ModuleNotFoundError (RUTA AJUSTADA) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))  
constantes_path = os.path.join(root_dir, "assets", "constantes")
sys.path.insert(0, constantes_path)
# --------------------------------------------------------

# Importamos las constantes y clases
# **ASUME que la nueva clase Character está en el archivo 'cons'**
from cons import (
    ANCHO, ALTO, BLUE, WHITE, FPS, BACKGROUND_IMAGE_NAME, Character, World
) 

# --- CARGA DE LA IMAGEN DEL JUGADOR ---
PLAYER_SPRITESHEET = None
PLAYER_IMAGE_NAME = "player_spritesheet.jpg" # <--- ¡ASEGÚRATE DE QUE EL NOMBRE Y EXTENSIÓN SEAN CORRECTOS!

try:
    PLAYER_IMAGE_PATH = os.path.join(root_dir, "assets", "images", PLAYER_IMAGE_NAME)

    if os.path.exists(PLAYER_IMAGE_PATH):
        # Usamos .convert() para JPGs (que no suelen tener transparencia)
        PLAYER_SPRITESHEET = pygame.image.load(PLAYER_IMAGE_PATH).convert() 
        print(f"Hoja de sprites '{PLAYER_IMAGE_NAME}' cargada con éxito.")
    else:
        print(f"ERROR: Archivo del jugador no encontrado '{PLAYER_IMAGE_NAME}'.")

except pygame.error as e:
    print(f"ERROR: Pygame falló al leer el archivo del jugador. {e}")
except Exception as e:
    print(f"ERROR INESPERADO al cargar la imagen del jugador: {e}")
# -------------------------------------------------------------------

# --- CARGA DE LA IMAGEN DE FONDO ---
IMAGEN_FONDO_RAW = None 
IMAGEN_FONDO_ESCALADA = None

try:
    IMAGE_PATH = os.path.join(root_dir, "assets", "images", BACKGROUND_IMAGE_NAME)

    if os.path.exists(IMAGE_PATH):
        IMAGEN_FONDO_RAW = pygame.image.load(IMAGE_PATH)
        print(f"Fondo '{BACKGROUND_IMAGE_NAME}' cargado RAW con éxito.")
    else:
        print(f"ERROR: Archivo no encontrado '{BACKGROUND_IMAGE_NAME}'. Ruta buscada: {IMAGE_PATH}")

except pygame.error as e:
    print(f"ERROR: Pygame falló al leer el archivo de fondo. {e}")
except Exception as e:
    print(f"ERROR INESPERADO al cargar la imagen: {e}")
# -------------------------------------------------------------------

def nivel1(pantalla, ancho, alto): 
    global IMAGEN_FONDO_ESCALADA, IMAGEN_FONDO_RAW

# --- CONVERSIÓN Y ESCALADO EXACTO DEL FONDO ---
    if IMAGEN_FONDO_RAW is not None and IMAGEN_FONDO_ESCALADA is None:
        try:
            IMAGEN_FONDO_ESCALADA = IMAGEN_FONDO_RAW.convert()

            screen_size = pantalla.get_size()  
            IMAGEN_FONDO_ESCALADA = pygame.transform.scale(IMAGEN_FONDO_ESCALADA, screen_size)

            IMAGEN_FONDO_RAW = None 
            print(f"Fondo ajustado exactamente a {screen_size[0]}x{screen_size[1]}.")
        except Exception as e:
            print(f"ERROR DE CONVERSIÓN/ESCALADO: {e}")
        IMAGEN_FONDO_ESCALADA = None

    # --- CREACIÓN DEL MUNDO Y PERSONAJE ---
    mi_mundo = World(ANCHO, ALTO, IMAGEN_FONDO_ESCALADA)
    #  ¡CAMBIO IMPORTANTE! Pasamos la imagen cargada al constructor
    player = Character(x=ANCHO // 2, y=ALTO // 2, spritesheet_image=PLAYER_SPRITESHEET) 

    fuente = pygame.font.SysFont("Arial", 40)
    reloj = pygame.time.Clock()
    running = True

    while running:
        # --- EVENTOS ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False 
                return 

        # --- MOVIMIENTO ---
        keys = pygame.key.get_pressed()
        dx = dy = 0
        moving = False # Variable para saber si el personaje se está moviendo

        if keys[pygame.K_LEFT]:
            dx = -player.speed; moving = True
        if keys[pygame.K_RIGHT]:
            dx = player.speed; moving = True
        if keys[pygame.K_UP]:
            dy = -player.speed; moving = True
        if keys[pygame.K_DOWN]:
            dy = player.speed; moving = True

        player.move(dx, dy)
        # Actualizamos la animación si hay movimiento
        if moving:
            player.update_animation() 
# --- DIBUJO ---
        mi_mundo.draw(pantalla)
        player.draw(pantalla) # Ahora dibuja la imagen animada
        texto = fuente.render("Nivel 1 - Animación de Personaje", True, WHITE)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO//2, 50)))

        pygame.display.flip()
        reloj.tick(FPS)

    print("Saliendo del Nivel 1.")