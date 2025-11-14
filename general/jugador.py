import pygame

class Jugador:
    def __init__(self, x, y, ancho_pantalla, alto_pantalla):
        # Tamaño del jugador
        self.PLAYER_SIZE = 140
        self.rect = pygame.Rect(x, y, self.PLAYER_SIZE, self.PLAYER_SIZE)
        
        # Propiedades de física
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.gravedad = 1
        self.salto_fuerza = -18
        self.en_suelo = False
        
        # Propiedades de animación
        self.current_frame_index = 0
        self.animation_timer = 0
        self.ANIMATION_SPEED = 10
        self.is_moving = False
        self.facing_right = True
        self.current_animation_type = "idle"
        
        # Cargar imágenes del jugador
        self.player_idle_images = None
        self.player_run_images = None
        self._cargar_imagenes()
        
        # Dimensiones de pantalla para límites
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
    
    def _cargar_imagenes(self):
        """Carga las imágenes de animación del jugador"""
        try:
            # Cargar frames de idle (2 frames)
            guardian1_img = pygame.image.load("assets/images/guardianpose1.png").convert_alpha()
            guardian2_img = pygame.image.load("assets/images/guardianpose2.png").convert_alpha()
            
            guardian1_img = pygame.transform.scale(guardian1_img, (self.PLAYER_SIZE, self.PLAYER_SIZE))
            guardian2_img = pygame.transform.scale(guardian2_img, (self.PLAYER_SIZE, self.PLAYER_SIZE))
            
            # Almacenar los frames de idle
            self.player_idle_images = [guardian1_img, guardian2_img]
            
            # Cargar frames de run (3 frames)
            guardian_run1_img = pygame.image.load("assets/images/guardianrun1.png").convert_alpha()
            guardian_run2_img = pygame.image.load("assets/images/guardianrun2.png").convert_alpha()
            guardian_run3_img = pygame.image.load("assets/images/guardianrun3.png").convert_alpha()
            
            guardian_run1_img = pygame.transform.scale(guardian_run1_img, (self.PLAYER_SIZE, self.PLAYER_SIZE))
            guardian_run2_img = pygame.transform.scale(guardian_run2_img, (self.PLAYER_SIZE, self.PLAYER_SIZE))
            guardian_run3_img = pygame.transform.scale(guardian_run3_img, (self.PLAYER_SIZE, self.PLAYER_SIZE))
            
            # Almacenar los frames de run
            self.player_run_images = [guardian_run1_img, guardian_run2_img, guardian_run3_img]
            
        except pygame.error as e:
            print(f"Error al cargar la imagen del jugador: {e}. Usando color sólido.")
            self.player_idle_images = None
            self.player_run_images = None
    
    def actualizar_movimiento(self, keys, entidades_colisionables):
        """Actualiza el movimiento y física del jugador"""
        # Reiniciar velocidad horizontal
        self.velocidad_x = 0
        self.is_moving = False
        
        # Movimiento horizontal
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocidad_x = 6
            self.is_moving = True
            self.facing_right = True
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocidad_x = -6
            self.is_moving = True
            self.facing_right = False
        
        # Aplicar movimiento horizontal
        self.rect.x += self.velocidad_x
        
        # Colisión horizontal
        for entidad in entidades_colisionables:
            if self.rect.colliderect(entidad):
                if self.velocidad_x > 0:
                    self.rect.right = entidad.left
                elif self.velocidad_x < 0:
                    self.rect.left = entidad.right
        
        # Aplicar gravedad
        self.velocidad_y += self.gravedad
        
        # Salto
        if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
            if self.en_suelo:
                self.velocidad_y = self.salto_fuerza
                self.en_suelo = False
        
        # Aplicar movimiento vertical
        self.rect.y += self.velocidad_y
        self.en_suelo = False
        
        # Colisión vertical
        for entidad in entidades_colisionables:
            if self.rect.colliderect(entidad):
                if self.velocidad_y >= 0:
                    self.rect.bottom = entidad.top
                    self.velocidad_y = 0
                    self.en_suelo = True
                else:
                    self.rect.top = entidad.bottom
                    self.velocidad_y = 0
    
    def actualizar_animacion(self):
        """Actualiza la animación del jugador"""
        if self.player_idle_images and self.player_run_images:
            # Determinar el tipo de animación actual
            new_animation_type = "run" if (self.is_moving and self.en_suelo) else "idle"
            
            # Si cambió el tipo de animación, reiniciar el frame index
            if new_animation_type != self.current_animation_type:
                self.current_animation_type = new_animation_type
                self.current_frame_index = 0
                self.animation_timer = 0
            
            # Actualizar animación según el tipo
            self.animation_timer += 1
            if self.animation_timer >= self.ANIMATION_SPEED:
                self.animation_timer = 0
                
                if self.current_animation_type == "run":
                    # Animación de correr (3 frames)
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.player_run_images)
                else:
                    # Animación de idle (2 frames)
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.player_idle_images)
    
    def dibujar(self, pantalla, camara_x):
        """Dibuja al jugador en la pantalla"""
        if self.player_idle_images and self.player_run_images:
            # Determinar qué conjunto de imágenes usar según la animación actual
            if self.current_animation_type == "run" and self.is_moving and self.en_suelo:
                current_images = self.player_run_images
                max_frames = len(self.player_run_images)
            else:
                current_images = self.player_idle_images
                max_frames = len(self.player_idle_images)
            
            # Asegurarse de que el índice esté dentro del rango
            if self.current_frame_index >= max_frames:
                self.current_frame_index = 0
            
            # Obtener la imagen actual
            current_image = current_images[self.current_frame_index]
            
            # Voltear la imagen si está mirando hacia la izquierda
            if not self.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
            
            # Dibujar el sprite
            pantalla.blit(current_image, (self.rect.x - camara_x, self.rect.y))
            
        elif self.player_idle_images:
            # Fallback: Solo tenemos imágenes idle
            current_image = self.player_idle_images[self.current_frame_index % len(self.player_idle_images)]
            if not self.facing_right:
                current_image = pygame.transform.flip(current_image, True, False)
            pantalla.blit(current_image, (self.rect.x - camara_x, self.rect.y))
        else:
            # Fallback: Dibujar el rectángulo rojo si la imagen no se cargó
            pygame.draw.rect(pantalla, (255, 50, 50), 
                           pygame.Rect(self.rect.x - camara_x, self.rect.y, 
                                     self.rect.width, self.rect.height))
    
    def verificar_colision_portal(self, portal_rect):
        """Verifica si el jugador colisiona con el portal"""
        return self.rect.colliderect(portal_rect)
    
    def limitar_movimiento(self, ancho_mundo_maximo):
        """Limita el movimiento del jugador dentro del mundo"""
        self.rect.x = max(0, min(self.rect.x, ancho_mundo_maximo - self.rect.width))
    
    def get_posicion_para_camara(self):
        """Obtiene la posición del jugador para el cálculo de la cámara"""
        return self.rect.x