import pygame

class Jugador:
    """
    Representa al personaje controlable del juego, con física, 
    movimiento, colisiones y animación.
    """
    def __init__(self, x, y):
        # ==== COLLIDER (CUADRO) ====
        # El rectángulo principal para la física y colisiones
        self.rect = pygame.Rect(x, y, 40, 40)

        # ==== FÍSICA ====
        self.vel_x = 0
        self.vel_y = 0
        self.gravedad = 1
        self.fuerza_salto = -18
        self.en_suelo = False
        self.velocidad_movimiento = 6

        # ==== ANIMACIONES ====
        self.estado = "idle"  # idle, run, jump, fall
        self.frame_index = 0
        self.frame_timer = 0
        # Controla la velocidad de la animación (cuanto más bajo, más lento)
        self.velocidad_anim = 0.15 

        # === FRAMES IDLE (Cargados o Fallback) ===
        try:
            # Intentar cargar las imágenes de animación
            self.frames_idle = [
                pygame.image.load("assets/images/guardian132.png").convert_alpha(),
                pygame.image.load("assets/images/guardian232.png").convert_alpha(),
            ]
            # Escalar los sprites al tamaño del collider (40x40)
            self.frames_idle = [pygame.transform.scale(f, (self.rect.width, self.rect.height)) for f in self.frames_idle]

        except pygame.error:
            # Fallback si las imágenes no se encuentran
            print("Error al cargar sprites del jugador. Usando cuadros de color de reemplazo.")
            self.frames_idle = self._crear_fallback_sprites((0, 255, 0)) # Cuadros verdes

        # (Opcionales) frames correr — se usa el mismo fallback si no están definidos
        self.frames_run = self.frames_idle # Usaremos el idle para run si no hay frames de correr
        
        # Sprite actual
        self.sprite_actual = self.frames_idle[0]

        # Para invertir sprite si se mueve a la izquierda
        self.mirando_derecha = True

    def _crear_fallback_sprites(self, color):
        """Crea superficies de color de 40x40 como sprites de reemplazo."""
        sprite1 = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite1.fill(color)
        # Un segundo frame ligeramente diferente para simular animación
        sprite2 = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        sprite2.fill((color[0]-20 if color[0]>20 else 0, color[1]-20 if color[1]>20 else 0, color[2]-20 if color[2]>20 else 0))
        return [sprite1, sprite2]

    # =====================================================
    #                       ANIMACIÓN
    # =====================================================
    def actualizar_animacion(self):
        """Selecciona los frames, actualiza el índice y voltea el sprite si es necesario."""
        
        # 1. Determinar el conjunto de frames
        if self.estado == "idle":
            frames = self.frames_idle
        elif self.estado == "run" and self.frames_run:
            # Si hay frames de correr, úsalos
            frames = self.frames_run
        else:
            # Fallback: idle para todos los demás estados si no hay animaciones dedicadas
            frames = self.frames_idle

        # 2. Actualizar el índice del frame (lógica de bucle)
        self.frame_timer += self.velocidad_anim
        if self.frame_timer >= 1:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.frame_timer = 0

        # 3. Obtener el sprite base
        sprite = frames[self.frame_index]

        # 4. Invertir sprite si mira a la izquierda
        if not self.mirando_derecha:
            sprite = pygame.transform.flip(sprite, True, False)

        self.sprite_actual = sprite

    # =====================================================
    #                       MOVIMIENTO
    # =====================================================
    def mover(self, teclas, colisiones):
        """Procesa la entrada del usuario, aplica física y gestiona colisiones."""
        
        self.vel_x = 0
        self.en_suelo_antes = self.en_suelo # Guardar estado antes del movimiento Y

        # --- Movimiento Horizontal ---
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x = self.velocidad_movimiento
            self.mirando_derecha = True
            self.estado = "run"
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel_x = -self.velocidad_movimiento
            self.mirando_derecha = False
            self.estado = "run"
        else:
            # Si no hay movimiento horizontal
            if self.en_suelo:
                self.estado = "idle"

        # ---- Aplicar movimiento X ----
        self.rect.x += self.vel_x
        self.colisiones_x(colisiones)

        # ---- Gravedad ----
        self.vel_y += self.gravedad
        # Limitar la velocidad de caída (opcional, para evitar caídas muy rápidas)
        if self.vel_y > 15:
            self.vel_y = 15

        # ---- Salto ----
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.en_suelo:
            self.vel_y = self.fuerza_salto
            self.en_suelo = False # Se debe reevaluar en colisiones_y

        # ---- Aplicar movimiento Y ----
        self.rect.y += self.vel_y
        self.en_suelo = False # Asumir que ya no está en el suelo antes de la colisión
        self.colisiones_y(colisiones)

        # Ajustar estado aéreo si no está en el suelo
        if not self.en_suelo:
            # Si estaba en el suelo y ahora salta (vel_y negativa)
            if self.vel_y < 0:
                self.estado = "jump"
            # Si no estaba en el suelo y está cayendo (vel_y positiva)
            elif self.vel_y > 0 and not self.en_suelo_antes:
                self.estado = "fall"
        
        # Si está en el suelo, su estado ya fue manejado por las teclas o se mantuvo "idle"

    # =====================================================
    #               COLISIONES SEPARADAS X/Y
    # =====================================================
    def colisiones_x(self, objetos):
        """Gestiona las colisiones en el eje X."""
        for o in objetos:
            if self.rect.colliderect(o):
                if self.vel_x > 0:
                    self.rect.right = o.left
                elif self.vel_x < 0:
                    self.rect.left = o.right
                # Detener el movimiento X al colisionar
                self.vel_x = 0 

    def colisiones_y(self, objetos):
        """Gestiona las colisiones en el eje Y y actualiza el estado 'en_suelo'."""
        for o in objetos:
            if self.rect.colliderect(o):
                if self.vel_y > 0:  # cayendo (colisión inferior)
                    self.rect.bottom = o.top
                    self.vel_y = 0
                    self.en_suelo = True
                    # Si aterrizó, cambiar a idle
                    if self.estado == "fall" or self.estado == "jump":
                         self.estado = "idle"

                elif self.vel_y < 0:  # subiendo (colisión superior)
                    self.rect.top = o.bottom
                    self.vel_y = 0

    # =====================================================
    #                         DIBUJAR
    # =====================================================
    def dibujar(self, pantalla, camara_x):
        """Dibuja el sprite actual del jugador en la pantalla, aplicando el desplazamiento de la cámara."""
        # Dibuja el sprite actual (ya animado y volteado)
        pantalla.blit(self.sprite_actual, (self.rect.x - camara_x, self.rect.y))
        
        # Opcional: Dibujar el rectángulo del collider para depuración
        # pygame.draw.rect(pantalla, (255, 0, 0, 100), (self.rect.x - camara_x, self.rect.y, self.rect.width, self.rect.height), 1)