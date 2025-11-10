# Archivo de Constantes (cons.py)
# ESTE ARCHIVO SOLO CONTIENE DEFINICIONES Y CLASES, NO HACE CARGA DE IMÁGENES.

# --- 1. CONSTANTES DE JUEGO ---
ANCHO = 800
ALTO = 600
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
FPS = 60 # Fotogramas por segundo

# Nombre del archivo de imagen (solo el nombre, sin ruta)
BACKGROUND_IMAGE_NAME = "brown.jpg"


# --- 2. CLASES DE JUEGO UNIVERSALES ---

class World:
    """Clase para gestionar el mapa del juego (fondo, límites)."""
    def __init__(self, width, height, background_img):
        self.width = width
        self.height = height
        self.background_img = background_img 

    def draw(self, pantalla):
        """
        Dibuja el fondo. Primero limpia la pantalla a negro para estabilidad.
        """
        import pygame # Importación local
        # Limpiar la pantalla a negro (color seguro) en cada frame.
        pantalla.fill((0, 0, 0)) 
        
        if self.background_img:
            # Si la imagen se cargó correctamente, se dibuja sobre el fondo negro.
            pantalla.blit(self.background_img, (0, 0))
        # Si la imagen falló (None), la pantalla queda simplemente en negro.
        
class Character:
    """Clase base para el personaje del jugador."""
    def __init__(self, x, y, speed=5, image_name="player.png"):
        import pygame, os

        self.x = x
        self.y = y
        self.speed = speed
        self.direction = "down"

        # Intentamos cargar la imagen del personaje
        self.image = None
        try:
            base_path = os.path.dirname(os.path.dirname(__file__))  # sube a raíz del proyecto
            image_path = os.path.join(base_path, "assets", "images", image_name)

            if os.path.exists(image_path):
                self.image = pygame.image.load(image_path).convert_alpha()
                # Escala la imagen si es muy grande (ajústalo a tu gusto)
                self.image = pygame.transform.scale(self.image, (64, 64))
                self.rect = self.image.get_rect(center=(self.x, self.y))
                print(f"Personaje '{image_name}' cargado con éxito.")
            else:
                print(f"⚠️ Imagen del personaje no encontrada: {image_path}")
        except Exception as e:
            print(f"ERROR al cargar personaje: {e}")
            self.image = None

    def draw(self, pantalla):
        """Dibuja el personaje (imagen o cuadrado si no hay imagen)."""
        import pygame

        if self.image:
            pantalla.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(pantalla, (0, 0, 255), (self.x, self.y, 32, 32))

    def move(self, dx, dy):
        """Mueve al personaje y lo limita a los bordes de la pantalla."""
        self.x = max(0, min(self.x + dx, ANCHO - 64))
        self.y = max(0, min(self.y + dy, ALTO - 64))
