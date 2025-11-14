import pygame
import os

class SistemaVidas:
    def __init__(self, max_vidas=5, vidas_iniciales=3):
        self.vidas = vidas_iniciales
        self.MAX_VIDAS = max_vidas
        self.corazon_img = self._cargar_imagen_corazon()
        
    def _cargar_imagen_corazon(self):
        """Carga la imagen del corazón para las vidas"""
        try:
            corazon_img = pygame.image.load("assets/images/corazon.png").convert_alpha()
            corazon_img = pygame.transform.scale(corazon_img, (50, 50))
            return corazon_img
        except pygame.error:
            print("Error al cargar la imagen de corazón. Usando un color de reemplazo.")
            corazon_img = pygame.Surface((50, 50), pygame.SRCALPHA)
            corazon_img.fill((255, 0, 0, 200))
            return corazon_img
    
    def perder_vida(self):
        """Resta una vida y devuelve True si aún hay vidas"""
        self.vidas = max(0, self.vidas - 1)
        return self.vidas > 0
    
    def ganar_vida(self):
        """Añade una vida hasta el máximo"""
        self.vidas = min(self.MAX_VIDAS, self.vidas + 1)
    
    def reiniciar(self, vidas_iniciales=3):
        """Reinicia las vidas al valor inicial"""
        self.vidas = vidas_iniciales
    
    def dibujar(self, pantalla, ancho):
        """Dibuja las vidas en la pantalla"""
        heart_width = self.corazon_img.get_width()
        heart_spacing = 5
        start_x = ancho - 20 - heart_width
        heart_y = 20

        for i in range(self.vidas):
            heart_x = start_x - (i * (heart_width + heart_spacing))
            pantalla.blit(self.corazon_img, (heart_x, heart_y))
    
    def get_vidas(self):
        """Devuelve el número actual de vidas"""
        return self.vidas
    
    def get_vidas_restantes_despues_error(self):
        """Devuelve las vidas que quedarían después de un error"""
        return max(0, self.vidas - 1)