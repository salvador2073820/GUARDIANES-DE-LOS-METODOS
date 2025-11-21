# unidades/unidad4/nivel5.py
import pygame, sys
import random
import os
import importlib

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from general.jugador import Jugador
from general.vidas import SistemaVidas


def nivel5(pantalla, ancho, alto):
    """Nivel 5 del Mundo 4 - Runge-Kutta 3er Orden"""

    pygame.init()
    reloj = pygame.time.Clock()

    # ---------- Fuentes ----------
    try:
        fuente = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 48)
        fuente_mensaje = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 32)
        fuente_cuerpo = pygame.font.SysFont("Arial", 26)
        fuente_temporizador = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 36)
    except FileNotFoundError:
        fuente = pygame.font.SysFont("Arial", 40)
        fuente_mensaje = pygame.font.SysFont("Arial", 29)
        fuente_cuerpo = pygame.font.SysFont("Arial", 26)
        fuente_temporizador = pygame.font.SysFont("Arial", 36)

    # ---------- Fondo ----------
    try:
        fondo = pygame.image.load("assets/images/fondoprueba2.jpg").convert()
        fondo = pygame.transform.scale(fondo, (ancho, alto))
    except pygame.error:
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((135, 206, 235))
    fondo_ancho = fondo.get_width()

    try:
        piso_img = pygame.image.load("assets/images/piso2.png").convert_alpha()
    except pygame.error:
        piso_img = None

    # ---------- Mundo ----------
    ALTURA_SUELO = 110
    ANCHO_MUNDO_MAXIMO = 5200
    suelo = pygame.Rect(0, alto - ALTURA_SUELO, ANCHO_MUNDO_MAXIMO, ALTURA_SUELO)

    # ---------- Portal ----------
    try:
        portal_img = pygame.image.load("assets/images/portalsinfondo.png").convert_alpha()
        PORTAL_WIDTH = 270
        PORTAL_HEIGHT = 360
        portal_img = pygame.transform.scale(portal_img, (PORTAL_WIDTH, PORTAL_HEIGHT))
    except pygame.error:
        portal_img = pygame.Surface((150, 200), pygame.SRCALPHA)
        portal_img.fill((100, 50, 200, 200))

    meta_x = 4350
    meta = pygame.Rect(meta_x, alto - ALTURA_SUELO - PORTAL_HEIGHT, PORTAL_WIDTH, PORTAL_HEIGHT)

    # ---------- Clases de Obstáculos ----------
    class ObjetoRojo:
        def __init__(self, x, y, ancho=40, alto=40):
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.color = (255, 0, 0)
            self.cooldown_hit = 0

        def actualizar(self):
            if self.cooldown_hit > 0:
                self.cooldown_hit -= 1

        def dibujar(self, surf, camara_x):
            r = self.rect.move(-camara_x, 0)
            pygame.draw.rect(surf, self.color, r, border_radius=8)
            pygame.draw.circle(surf, (255, 200, 200), r.center, 10)

        def intentar_danar(self, jugador_rect):
            if self.rect.colliderect(jugador_rect) and self.cooldown_hit == 0:
                self.cooldown_hit = 60
                return True
            return False

    class Enemigo:
        def __init__(self, x, y, ancho_e=60, alto_e=60, rango=120, velocidad=2):
            self.rect = pygame.Rect(x, y, ancho_e, alto_e)
            self.color = (180, 40, 40)
            self.rango = rango
            self.velocidad = velocidad
            self.origen_x = x
            self.direccion = 1
            self.vivo = True
            self.cooldown_hit = 0

        def actualizar(self):
            if not self.vivo:
                return
            self.rect.x += self.velocidad * self.direccion
            if abs(self.rect.x - self.origen_x) >= self.rango:
                self.direccion *= -1
            if self.cooldown_hit > 0:
                self.cooldown_hit -= 1

        def dibujar(self, surf, camara_x):
            r = self.rect.move(-camara_x, 0)
            pygame.draw.rect(surf, self.color, r, border_radius=6)

        def intentar_danar(self, jugador_rect):
            if self.vivo and self.rect.colliderect(jugador_rect) and self.cooldown_hit == 0:
                self.cooldown_hit = 60
                return True
            return False

 # ---------- Obstáculos personalizados para Nivel 5 (RK 3er Orden) ----------
    def generar_obstaculos():

        plataformas_local = []
        objetos_local = []
        enemigos_local = []

            # ==========================
            #       ZONA INICIO
            # ==========================
        inicio_offset = 120

        plataformas_local.extend([
            pygame.Rect(inicio_offset + 40, alto - ALTURA_SUELO - 90, 200, 20),
            pygame.Rect(inicio_offset + 360, alto - ALTURA_SUELO - 160, 220, 20),
            pygame.Rect(inicio_offset + 720, alto - ALTURA_SUELO - 120, 190, 20),
            pygame.Rect(inicio_offset + 1050, alto - ALTURA_SUELO - 80, 170, 20),
       ])

        objetos_local.extend([
            ObjetoRojo(inicio_offset + 280, alto - ALTURA_SUELO - 40),
            ObjetoRojo(inicio_offset + 860, alto - ALTURA_SUELO - 40),
        ])

        enemigos_local.append(
            Enemigo(inicio_offset + 600, alto - ALTURA_SUELO - 150, rango=110, velocidad=2)
        )

            # ==========================
            #       ZONA MEDIA
            #  Plataformas en zig-zag
            # ==========================
        medio_offset = 1750

        plataformas_local.extend([
            pygame.Rect(medio_offset + 50, alto - ALTURA_SUELO - 130, 250, 20),
            pygame.Rect(medio_offset + 420, alto - ALTURA_SUELO - 210, 240, 20),
            pygame.Rect(medio_offset + 760, alto - ALTURA_SUELO - 150, 260, 20),
            pygame.Rect(medio_offset + 1120, alto - ALTURA_SUELO - 230, 250, 20),
            pygame.Rect(medio_offset + 1470, alto - ALTURA_SUELO - 180, 260, 20),
        ])

        objetos_local.extend([
            ObjetoRojo(medio_offset + 230, alto - ALTURA_SUELO - 40),
            ObjetoRojo(medio_offset + 690, alto - ALTURA_SUELO - 40),
            ObjetoRojo(medio_offset + 1280, alto - ALTURA_SUELO - 40),
        ])

        enemigos_local.extend([
            Enemigo(medio_offset + 350, alto - ALTURA_SUELO - 210, rango=140, velocidad=3),
            Enemigo(medio_offset + 1000, alto - ALTURA_SUELO - 230, rango=170, velocidad=2),
            Enemigo(medio_offset + 1420, alto - ALTURA_SUELO - 200, rango=140, velocidad=3),
        ])

            # ==========================
            #       ZONA FINAL
            #   Plataforma ascendente
            # ==========================
        final_offset = 3200

        plataformas_local.extend([
            pygame.Rect(final_offset + 60, alto - ALTURA_SUELO - 150, 240, 20),
            pygame.Rect(final_offset + 430, alto - ALTURA_SUELO - 200, 230, 20),
            pygame.Rect(final_offset + 780, alto - ALTURA_SUELO - 280, 240, 20),
            pygame.Rect(final_offset + 1140, alto - ALTURA_SUELO - 210, 270, 20),
            pygame.Rect(final_offset + 1500, alto - ALTURA_SUELO - 170, 240, 20),
        ])

        objetos_local.extend([
            ObjetoRojo(final_offset + 260, alto - ALTURA_SUELO - 40),
            ObjetoRojo(final_offset + 620, alto - ALTURA_SUELO - 40),
            ObjetoRojo(final_offset + 1010, alto - ALTURA_SUELO - 40),
        ])

        enemigos_local.append(
            Enemigo(final_offset + 1100, alto - ALTURA_SUELO - 260, rango=90, velocidad=5)
        )

        return plataformas_local, objetos_local, enemigos_local

    plataformas, objetos_rojos, enemigos = generar_obstaculos()
    entidades_colisionables = [suelo] + plataformas

    # ---------- Problemas ----------
    MENSAJES_ALEATORIOS = [
        {
            "problema_titulo": "PROBLEMA 1",
            "titulo": "RUNGE-KUTTA 3er ORDEN",
            "ecuacion": "y' = (2yt + 1)/ y^2",
           "condiciones": ["y0 = 1, h = 0.25"],
            "texto": ["Calcula y1, y2 usando el método de Runge-Kutta 3er orden."],
            "inputs": [
                {"label": "k3 para y1 =", "correct_answer": "0.257939981", "placeholder": "Respuesta"},
                {"label": "y1 =", "correct_answer": "1.211723276", "placeholder": "Respuesta"},
                {"label": "k2 para y2=", "correct_answer": "0.2765423608", "placeholder": "Respuesta"},
                {"label": "y2 =", "correct_answer": "1.488327488", "placeholder": "Respuesta"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 2",
            "titulo": "RUNGE-KUTTA 3er ORDEN",
            "ecuacion": "y' - 5yt + 1 = 0",
           "condiciones": ["y0 = 2, h = 0.2"],
            "texto": ["Calcula y1, y2 usando el método de Runge-Kutta 3er orden."],
            "inputs": [
                {"label": "k1 para y1 =", "correct_answer": "-0.2", "placeholder": "Respuesta"},
                {"label": "y1 =", "correct_answer": "1.999333333", "placeholder": "Respuesta"},
                {"label": "k3 para y2=", "correct_answer": "0.8636106665", "placeholder": "Respuesta"},
                {"label": "y2 =", "correct_answer": "2.463099555", "placeholder": "Respuesta"}
            ]
        }
    ]

       # ---------- Jugador, vidas, temporizador ----------
    jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
    sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)

    class Temporizador:
        def __init__(self, tiempo_total_minutos=40):
            self.tiempo_total_segundos = tiempo_total_minutos * 60
            self.tiempo_restante = self.tiempo_total_segundos
            self.activo = False
            self.tiempo_inicio = None

        def iniciar(self):
            self.activo = True
            self.tiempo_inicio = pygame.time.get_ticks()

        def detener(self):
            self.activo = False

        def reiniciar(self):
            self.tiempo_restante = self.tiempo_total_segundos
            self.activo = False
            self.tiempo_inicio = None

        def actualizar(self):
            if self.activo and self.tiempo_inicio is not None:
                tiempo_transcurrido = (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
                self.tiempo_restante = max(0, self.tiempo_total_segundos - tiempo_transcurrido)
                return self.tiempo_restante > 0
            return True

        def obtener_tiempo_formateado(self):
            minutos = self.tiempo_restante // 60
            segundos = self.tiempo_restante % 60
            return f"{minutos:02d}:{segundos:02d}"

        def tiempo_agotado(self):
            return self.tiempo_restante <= 0

    temporizador = Temporizador(40)

    camara_x = 0
    mostrar_mensaje = False
    mensaje_data = None
    input_texts = {}
    active_input_label = None
    check_result = None
    show_overlay = False
    vidas_restantes_despues_error = 0
    tiempo_agotado_overlay = False
    fallos_en_problema_actual = 0

    # ---------- Validación de respuestas ----------
    def check_answers(data, inputs):
        TOLERANCE = 1e-6
        for spec in data.get("inputs", []):
            label = spec["label"]
            correct = spec["correct_answer"]
            player = inputs.get(label, "").strip()
            if not player:
                return False
            try:
                player_clean = player.replace(',', '.')
                correct_clean = correct.replace(',', '.')
                if abs(float(player_clean) - float(correct_clean)) > TOLERANCE:
                    return False
            except ValueError:
                if player.lower() != correct.lower():
                    return False
            except:
                return False
        return True

    # ---------- Reiniciar nivel ----------
    def reiniciar_nivel():
        nonlocal jugador, sistema_vidas, temporizador, camara_x
        nonlocal mostrar_mensaje, mensaje_data, input_texts, active_input_label
        nonlocal check_result, show_overlay, vidas_restantes_despues_error, tiempo_agotado_overlay
        nonlocal fallos_en_problema_actual, plataformas, objetos_rojos, enemigos, entidades_colisionables

        jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
        sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)
        temporizador.reiniciar()
        camara_x = 0

        plataformas, objetos_rojos, enemigos = generar_obstaculos()
        entidades_colisionables = [suelo] + plataformas

        mostrar_mensaje = False
        mensaje_data = None
        input_texts = {}
        active_input_label = None
        check_result = None
        show_overlay = False
        vidas_restantes_despues_error = 0
        tiempo_agotado_overlay = False
        fallos_en_problema_actual = 0

    # ---------- Cargar Nivel 6 ----------
    def cargar_nivel6():
        try:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_nivel6 = os.path.join(directorio_actual, "nivel6.py")
            print(f"[nivel5] intentando cargar: {ruta_nivel6}")

            if os.path.exists(ruta_nivel6):
                if directorio_actual not in sys.path:
                    sys.path.append(directorio_actual)

                import nivel6
                importlib.reload(nivel6)

                nivel6.nivel6(pantalla, ancho, alto)
                return True
            else:
                print(f"[nivel5] nivel6.py no encontrado en: {directorio_actual}")
                return False
        except Exception as e:
            print(f"[nivel5] Error al cargar nivel6: {e}")
            import traceback
            traceback.print_exc()
            return False

    # ===================== BUCLE PRINCIPAL =====================
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and not (mostrar_mensaje and show_overlay):
                    return

                if mostrar_mensaje:
                    # ---------- Overlay de resultado ----------
                    if show_overlay:
                        if e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            if sistema_vidas.get_vidas() <= 0:
                                reiniciar_nivel()
                                continue

                            if tiempo_agotado_overlay:
                                if sistema_vidas.get_vidas() <= 0:
                                    reiniciar_nivel()
                                else:
                                    tiempo_agotado_overlay = False
                                    show_overlay = False
                                    input_texts = {i["label"]: "" for i in mensaje_data.get("inputs", [])}
                                    if mensaje_data.get("inputs"):
                                        active_input_label = mensaje_data["inputs"][0]["label"]
                                    temporizador.reiniciar()
                                    temporizador.iniciar()
                                continue

                            if check_result is True:
                                sistema_vidas.ganar_vida()
                                mostrar_mensaje = False
                                show_overlay = False
                                temporizador.detener()
                                print("[nivel5] ¡Respuesta correcta! Ganaste 1 vida. Cargando nivel 6...")
                                if cargar_nivel6():
                                    return
                                else:
                                    print("[nivel5] No se pudo cargar nivel6.py")
                                    return

                            elif check_result is False:
                                sistema_vidas.perder_vida()
                                fallos_en_problema_actual += 1

                                if sistema_vidas.get_vidas() > 0:
                                    check_result = None
                                    input_texts = {i["label"]: "" for i in mensaje_data.get("inputs", [])}
                                    if mensaje_data.get("inputs"):
                                        active_input_label = mensaje_data["inputs"][0]["label"]
                                    show_overlay = False
                                    temporizador.reiniciar()
                                    temporizador.iniciar()

                                if fallos_en_problema_actual >= 3:
                                    reiniciar_nivel()
                            continue

                    # ---------- Entrada en los inputs ----------
                    if mensaje_data and mensaje_data.get("inputs"):
                        if e.unicode.isdigit() or e.unicode in ".-,":
                            if active_input_label and len(input_texts[active_input_label]) < 40:
                                input_texts[active_input_label] += e.unicode
                        elif e.key == pygame.K_BACKSPACE:
                            if active_input_label:
                                input_texts[active_input_label] = input_texts[active_input_label][:-1]
                        elif e.key in (pygame.K_TAB, pygame.K_UP, pygame.K_DOWN):
                            labels = [i['label'] for i in mensaje_data["inputs"]]
                            if active_input_label in labels:
                                i = labels.index(active_input_label)
                                if e.key in (pygame.K_TAB, pygame.K_DOWN):
                                    active_input_label = labels[(i + 1) % len(labels)]
                                else:
                                    active_input_label = labels[(i - 1) % len(labels)]
                        elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                            check_result = check_answers(mensaje_data, input_texts)
                            if check_result is False:
                                vidas_restantes_despues_error = sistema_vidas.get_vidas()
                            show_overlay = True
                            temporizador.detener()
                    else:
                        if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                            mostrar_mensaje = False
                            temporizador.detener()
                    continue

            # ---------- Click en cajas de texto ----------
            if e.type == pygame.MOUSEBUTTONDOWN and mostrar_mensaje and mensaje_data and mensaje_data.get("inputs") and not show_overlay:
                mouse_x, mouse_y = e.pos
                cuadro_ancho = min(ancho * 0.95, 1000)
                cuadro_alto = min(alto * 0.85, 700)
                cuadro_x = (ancho - cuadro_ancho) // 2
                cuadro_y = (alto - cuadro_alto) // 2
                cuadro = pygame.Rect(cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto)
                cuadro_contenido = cuadro.inflate(-36, -36)

                input_height = 46
                field_width = 350
                spacing = 15
                total_inputs_height = len(mensaje_data["inputs"]) * (input_height + spacing) - spacing
                start_y = cuadro_contenido.bottom - total_inputs_height - 40

                for i, spec in enumerate(mensaje_data["inputs"]):
                    label = spec["label"]
                    label_surf = fuente_cuerpo.render(label, True, (255, 255, 255))
                    total_width = label_surf.get_width() + 20 + field_width
                    input_x = cuadro_contenido.centerx - total_width // 2
                    input_y = start_y + i * (input_height + spacing)
                    box_rect = pygame.Rect(input_x + label_surf.get_width() + 20, input_y, field_width, input_height)

                    if box_rect.collidepoint(mouse_x, mouse_y):
                        active_input_label = label
                        break

        # ---------- Reinicio si no hay vidas ----------
        if not mostrar_mensaje and sistema_vidas.get_vidas() <= 0:
            reiniciar_nivel()
            continue

        # ---------- Lógica del juego cuando no hay mensaje ----------
        if not mostrar_mensaje:
            keys = pygame.key.get_pressed()
            jugador.actualizar_movimiento(keys, entidades_colisionables)
            jugador.actualizar_animacion()
            jugador.limitar_movimiento(ANCHO_MUNDO_MAXIMO)
            camara_x = max(0, jugador.get_posicion_para_camara() - ancho // 2)

            for en in enemigos:
                en.actualizar()
                if en.intentar_danar(jugador.rect):
                    sistema_vidas.perder_vida()
                    try:
                        jugador.rect.x -= 50
                    except:
                        pass

            for obj in objetos_rojos:
                obj.actualizar()
                if obj.intentar_danar(jugador.rect):
                    sistema_vidas.perder_vida()
                    try:
                        jugador.rect.x -= 30
                    except:
                        pass

            if jugador.verificar_colision_portal(meta):
                mensaje_data = random.choice(MENSAJES_ALEATORIOS)
                input_texts = {i["label"]: "" for i in mensaje_data.get("inputs", [])}
                if mensaje_data.get("inputs"):
                    active_input_label = mensaje_data["inputs"][0]["label"]
                else:
                    active_input_label = None
                check_result = None
                show_overlay = False
                mostrar_mensaje = True
                tiempo_agotado_overlay = False
                temporizador.reiniciar()
                temporizador.iniciar()
                jugador.rect.right = meta.left - 5
                fallos_en_problema_actual = 0

        # ---------- Temporizador del mensaje ----------
        if mostrar_mensaje and not show_overlay and not tiempo_agotado_overlay:
            tiempo_valido = temporizador.actualizar()
            if not tiempo_valido and temporizador.tiempo_agotado():
                sistema_vidas.perder_vida()
                tiempo_agotado_overlay = True
                temporizador.detener()

        # ---------- Dibujado del mundo ----------
        offset_x = camara_x % fondo_ancho
        for i in range(-2, (ancho // fondo_ancho) + 3):
            pantalla.blit(fondo, ((i * fondo_ancho) - offset_x, 0))

        COLOR_SUELO = (100, 80, 50)
        COLOR_MADERA_OSCURA = (101, 67, 33)
        COLOR_MADERA_CLARA = (139, 90, 43)

        if piso_img:
            num_tiles = (suelo.width // piso_img.get_width()) + 1
            for i in range(num_tiles):
                pantalla.blit(piso_img, (suelo.x - camara_x + i * piso_img.get_width(), suelo.y))
        else:
            pygame.draw.rect(pantalla, COLOR_SUELO, pygame.Rect(suelo.x - camara_x, suelo.y, suelo.width, suelo.height))

        for p in plataformas:
            pygame.draw.rect(pantalla, COLOR_MADERA_CLARA,
                             pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6)
            pygame.draw.rect(pantalla, COLOR_MADERA_OSCURA,
                             pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6, width=3)

        pantalla.blit(portal_img, (meta.x - camara_x, meta.y))

        for en in enemigos:
            en.dibujar(pantalla, camara_x)
        for obj in objetos_rojos:
            obj.dibujar(pantalla, camara_x)

        jugador.dibujar(pantalla, camara_x)

        # ---------- HUD ----------
        texto = fuente.render("MUNDO 4 - NIVEL 5 - RUNGE-KUTTA 3er ORDEN", True, (255, 255, 255))
        pantalla.blit(texto, (20, 20))
        sistema_vidas.dibujar(pantalla, ancho)

        # ---------- Ventana de problema ----------
        if mostrar_mensaje and mensaje_data:
            if not show_overlay and not tiempo_agotado_overlay:
                tiempo_texto = temporizador.obtener_tiempo_formateado()
                if temporizador.tiempo_restante <= 300:
                    color_tiempo = (255, 0, 0)
                elif temporizador.tiempo_restante <= 600:
                    color_tiempo = (255, 165, 0)
                else:
                    color_tiempo = (255, 255, 255)
                tiempo_surface = fuente_temporizador.render(tiempo_texto, True, color_tiempo)
                tiempo_rect = tiempo_surface.get_rect(center=(ancho // 2, 50))
                fondo_tiempo = pygame.Surface((tiempo_surface.get_width() + 20, tiempo_surface.get_height() + 10), pygame.SRCALPHA)
                fondo_tiempo.fill((0, 0, 0, 150))
                pantalla.blit(fondo_tiempo, (tiempo_rect.x - 10, tiempo_rect.y - 5))
                pantalla.blit(tiempo_surface, tiempo_rect)

            s = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            pantalla.blit(s, (0, 0))

            cuadro_ancho = min(ancho * 0.95, 1000)
            cuadro_alto = min(alto * 0.85, 700)
            cuadro_x = (ancho - cuadro_ancho) // 2
            cuadro_y = (alto - cuadro_alto) // 2
            cuadro = pygame.Rect(cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto)

            pygame.draw.rect(pantalla, (220, 220, 220), cuadro, border_radius=16)
            cuadro_contenido = cuadro.inflate(-36, -36)
            pygame.draw.rect(pantalla, (28, 28, 28), cuadro_contenido, border_radius=12)

            y_pos = cuadro_contenido.top + 18

            titulo_p = fuente.render(mensaje_data["problema_titulo"], True, (255, 255, 255))
            pantalla.blit(titulo_p, titulo_p.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_p.get_height() + 8

            titulo_t = fuente_mensaje.render(mensaje_data["titulo"], True, (0, 255, 255))
            pantalla.blit(titulo_t, titulo_t.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_t.get_height() + 25

            left_x = cuadro_contenido.left + 30

            ecuacion_surf = fuente_cuerpo.render(mensaje_data["ecuacion"], True, (220, 220, 255))
            pantalla.blit(ecuacion_surf, (left_x, y_pos))
            y_pos += fuente_cuerpo.get_height() + 15

            for cond in mensaje_data.get("condiciones", []):
                cond_surf = fuente_cuerpo.render(cond, True, (220, 220, 220))
                pantalla.blit(cond_surf, (left_x, y_pos))
                y_pos += fuente_cuerpo.get_height() + 8

            y_pos += 15
            for linea in mensaje_data.get("texto", []):
                linea_surf = fuente_cuerpo.render(linea, True, (220, 220, 220))
                pantalla.blit(linea_surf, (left_x, y_pos))
                y_pos += fuente_cuerpo.get_height() + 8

            if mensaje_data.get("inputs"):
                input_height = 46
                field_width = 350
                spacing = 15
                total_inputs_height = len(mensaje_data["inputs"]) * (input_height + spacing) - spacing
                start_y = cuadro_contenido.bottom - total_inputs_height - 40

                for i, spec in enumerate(mensaje_data["inputs"]):
                    label = spec["label"]
                    placeholder = spec.get("placeholder", "")

                    label_surf = fuente_cuerpo.render(label, True, (255, 255, 255))
                    total_width = label_surf.get_width() + 20 + field_width
                    input_x = cuadro_contenido.centerx - total_width // 2
                    input_y = start_y + i * (input_height + spacing)

                    pantalla.blit(label_surf, (input_x,
                                               input_y + (input_height - label_surf.get_height()) // 2))

                    box_rect = pygame.Rect(input_x + label_surf.get_width() + 20, input_y,
                                           field_width, input_height)

                    if active_input_label == label and check_result is None:
                        border_color = (0, 200, 255); border_width = 3
                    elif check_result is False and show_overlay:
                        border_color = (255, 50, 50); border_width = 3
                    elif check_result is True and show_overlay:
                        border_color = (50, 255, 50); border_width = 3
                    else:
                        border_color = (180, 180, 180); border_width = 2

                    pygame.draw.rect(pantalla, (240, 240, 240), box_rect, border_radius=8)
                    pygame.draw.rect(pantalla, border_color, box_rect, border_width, border_radius=8)

                    text_to_show = input_texts.get(label, "")
                    if not text_to_show and active_input_label != label:
                        text_to_show = placeholder
                        color_texto = (150, 150, 150)
                    else:
                        color_texto = (0, 0, 0)

                    text_surf = fuente_cuerpo.render(text_to_show, True, color_texto)
                    if text_surf.get_width() > field_width - 20:
                        temp_text = text_to_show
                        while fuente_cuerpo.render(temp_text + "...", True, color_texto).get_width() > field_width - 20 and len(temp_text) > 1:
                            temp_text = temp_text[:-1]
                        text_surf = fuente_cuerpo.render(temp_text + "...", True, color_texto)

                    pantalla.blit(text_surf, (box_rect.x + 10,
                                              box_rect.y + (input_height - text_surf.get_height()) // 2))

                    if active_input_label == label and not show_overlay:
                        if (pygame.time.get_ticks() // 500) % 2 == 0:
                            cursor_x = box_rect.x + 10 + text_surf.get_width()
                            cursor = pygame.Rect(cursor_x, box_rect.y + 8, 2, text_surf.get_height())
                            pygame.draw.rect(pantalla, (0, 0, 0), cursor)

                if not show_overlay:
                    hint = fuente_mensaje.render(
                        "Presiona ENTER para verificar - TAB para cambiar campo",
                        True, (200, 200, 200))
                    pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx,
                                                      bottom=cuadro.bottom - 15))
            else:
                hint = fuente_mensaje.render("Presiona ENTER para continuar",
                                             True, (200, 200, 200))
                pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx,
                                                  bottom=cuadro.bottom - 18))

        # ---------- Overlay de resultado ----------
        if mostrar_mensaje and (show_overlay or tiempo_agotado_overlay):
            s_overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            s_overlay.fill((0, 0, 0, 100))
            pantalla.blit(s_overlay, (0, 0))

            fb_ancho = ancho * 0.6
            fb_alto = 200
            fb_x = (ancho - fb_ancho) // 2
            fb_y = (alto - fb_alto) // 2 - 80
            fb_cuadro = pygame.Rect(fb_x, fb_y, fb_ancho, fb_alto)

            if tiempo_agotado_overlay:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡TIEMPO AGOTADO! Perdiste 1 Vida"
                if sistema_vidas.get_vidas() > 0:
                    mensaje_hint = "Presiona ENTER para volver a intentar"
                else:
                    mensaje_hint = "Presiona ENTER para REINICIAR NIVEL"
            elif check_result is True:
                color_fondo = (50, 200, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡FELICIDADES! Respuesta correcta"
                mensaje_hint = "Presiona ENTER para continuar al NIVEL 6"
            else:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                if fallos_en_problema_actual >= 3:
                    mensaje_principal = "¡REINICIANDO NIVEL! Fallaste 3 veces"
                    mensaje_hint = "Presiona ENTER para continuar"
                elif sistema_vidas.get_vidas() <= 0:
                    mensaje_principal = "¡GAME OVER! Vidas Agotadas"
                    mensaje_hint = "Presiona ENTER para REINICIAR NIVEL"
                else:
                    mensaje_principal = f"¡INCORRECTO! Perdiste 1 Vida ({sistema_vidas.get_vidas()} restantes)"
                    mensaje_hint = "Presiona ENTER para volver a intentar"

            pygame.draw.rect(pantalla, (255, 255, 255), fb_cuadro, border_radius=15)
            pygame.draw.rect(pantalla, color_fondo, fb_cuadro.inflate(-6, -6), border_radius=10)

            main_text = fuente.render(mensaje_principal, True, color_texto)
            hint_text = fuente_mensaje.render(mensaje_hint, True, color_texto)

            pantalla.blit(main_text, main_text.get_rect(centerx=fb_cuadro.centerx,
                                                        centery=fb_cuadro.centery - 20))
            pantalla.blit(hint_text, hint_text.get_rect(centerx=fb_cuadro.centerx,
                                                        centery=fb_cuadro.centery + 40))

        pygame.display.flip()
        reloj.tick(60)


if __name__ == '__main__':
    pygame.init()
    ANCHO, ALTO = 1200, 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("MUNDO 4 - NIVEL 5 - RUNGE-KUTTA 3er ORDEN")
    nivel5(pantalla, ANCHO, ALTO)
    pygame.quit()
    sys.exit()