# unidades/unidad3/nivel2.py
import pygame, sys
import random
import os
import importlib

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from general.jugador import Jugador
from general.vidas import SistemaVidas

def nivel2(pantalla, ancho, alto):
    """Unidad 3 - Nivel 2: Regla de Simpson 1/3 (con vida extra y carga a nivel3)"""

    pygame.init()
    reloj = pygame.time.Clock()

    # ---------- Fuentes ----------
    try:
        fuente = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 48)
        fuente_mensaje = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 32)
        fuente_cuerpo = pygame.font.SysFont("Arial", 26)
        fuente_temporizador = pygame.font.Font("assets/fonts/Pieces of Eight.ttf", 36)
    except Exception:
        fuente = pygame.font.SysFont("Arial", 40)
        fuente_mensaje = pygame.font.SysFont("Arial", 30)
        fuente_cuerpo = pygame.font.SysFont("Arial", 26)
        fuente_temporizador = pygame.font.SysFont("Arial", 36)

    # ---------- Fondo ----------
    try:
        fondo = pygame.image.load("assets/images/fondoprueba.jpg").convert()
        fondo = pygame.transform.scale(fondo, (ancho, alto))
    except Exception:
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((135, 206, 235))
    fondo_ancho = fondo.get_width()

    # ---------- Piso ----------
    try:
        piso_img = pygame.image.load("assets/images/piso4.png").convert_alpha()
    except Exception:
        piso_img = None

    # ---------- Mundo ----------
    ALTURA_SUELO = 110
    ANCHO_MUNDO_MAXIMO = 5000
    suelo = pygame.Rect(0, alto - ALTURA_SUELO, ANCHO_MUNDO_MAXIMO, ALTURA_SUELO)

    # ---------- Portal ----------
    try:
        portal_img = pygame.image.load("assets/images/portalsinfondo.png").convert_alpha()
        PORTAL_WIDTH = 270
        PORTAL_HEIGHT = 360
        portal_img = pygame.transform.scale(portal_img, (PORTAL_WIDTH, PORTAL_HEIGHT))
    except Exception:
        portal_img = pygame.Surface((150, 200), pygame.SRCALPHA)
        portal_img.fill((100, 50, 200, 200))

    # Meta posicionada hacia el final del nivel (ajustable)
    meta_x = 3600
    meta = pygame.Rect(meta_x, alto - ALTURA_SUELO - PORTAL_HEIGHT, PORTAL_WIDTH, PORTAL_HEIGHT)

    # ---------- Clases ----------
    class Enemigo:
        def __init__(self, x, y, ancho_e=60, alto_e=60, rango=150, velocidad=2):
            self.rect = pygame.Rect(x, y, ancho_e, alto_e)
            self.color = (170, 40, 40)
            self.rango = rango
            self.velocidad = velocidad
            self.origen_x = x
            self.direccion = 1
            self.cooldown_hit = 0
            self.vivo = True

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

    class ObjetoRojo:
        def __init__(self, x, y, ancho=36, alto=36):
            self.rect = pygame.Rect(x, y, ancho, alto)
            self.color = (255, 0, 0)
            self.cooldown_hit = 0

        def actualizar(self):
            if self.cooldown_hit > 0:
                self.cooldown_hit -= 1

        def dibujar(self, surf, camara_x):
            r = self.rect.move(-camara_x, 0)
            pygame.draw.rect(surf, self.color, r, border_radius=8)
            pygame.draw.circle(surf, (255, 200, 200), r.center, 8)

        def intentar_danar(self, jugador_rect):
            if self.rect.colliderect(jugador_rect) and self.cooldown_hit == 0:
                self.cooldown_hit = 45
                return True
            return False

    # ---------- Generador de obstaculos (reacomodado distinto a nivel1) ----------
    def generar_obstaculos():
        plataformas_local = []
        objetos_local = []
        enemigos_local = []

        # Zona de inicio: plataformas cortas y escalonadas
        plataformas_local.extend([
            pygame.Rect(200, alto - ALTURA_SUELO - 60, 160, 18),
            pygame.Rect(420, alto - ALTURA_SUELO - 110, 120, 18),
            pygame.Rect(620, alto - ALTURA_SUELO - 70, 200, 18),
        ])
        objetos_local.extend([
            ObjetoRojo(480, alto - ALTURA_SUELO - 140),
        ])

        # Zona central: pasarela y huecos con obstáculos
        offset_central = 900
        plataformas_local.extend([
            pygame.Rect(offset_central + 40, alto - ALTURA_SUELO - 140, 260, 18),
            pygame.Rect(offset_central + 380, alto - ALTURA_SUELO - 90, 160, 18),
            pygame.Rect(offset_central + 620, alto - ALTURA_SUELO - 160, 120, 18),
            pygame.Rect(offset_central + 820, alto - ALTURA_SUELO - 110, 140, 18),
        ])
        objetos_local.extend([
            ObjetoRojo(offset_central + 220, alto - ALTURA_SUELO - 40),
            ObjetoRojo(offset_central + 700, alto - ALTURA_SUELO - 40),
        ])
        enemigos_local.append(Enemigo(offset_central + 520, alto - ALTURA_SUELO - 140, rango=200, velocidad=2))

        # Zona final: plataformas pequeñas y combinación enemigo/objetos
        offset_final = 2200
        plataformas_local.extend([
            pygame.Rect(offset_final + 30, alto - ALTURA_SUELO - 100, 140, 18),
            pygame.Rect(offset_final + 220, alto - ALTURA_SUELO - 200, 180, 18),
            pygame.Rect(offset_final + 480, alto - ALTURA_SUELO - 120, 160, 18),
            pygame.Rect(offset_final + 740, alto - ALTURA_SUELO - 90, 120, 18),
        ])
        objetos_local.extend([
            ObjetoRojo(offset_final + 120, alto - ALTURA_SUELO - 40),
            ObjetoRojo(offset_final + 520, alto - ALTURA_SUELO - 40),
            ObjetoRojo(offset_final + 880, alto - ALTURA_SUELO - 40),
        ])
        enemigos_local.append(Enemigo(offset_final + 560, alto - ALTURA_SUELO - 170, rango=160, velocidad=3))

        return plataformas_local, objetos_local, enemigos_local

    plataformas, objetos_rojos, enemigos = generar_obstaculos()
    entidades_colisionables = [suelo] + plataformas

    # ---------- Problemas (Simpson 1/3) ----------
    MENSAJES_ALEATORIOS = [
        {
            "problema_titulo": "PROBLEMA 1:",
            "titulo": "REGLA 1/3 DE SIMPSON",
            "ecuacion": "∫₂³ (1/(1+x²)) dx, n=10",
            "condiciones": ["Calcula usando Simpson 1/3:", "A =", "B =", "H =", "I ="],
            "texto": ["Resuelve la integral y completa:"],
            "inputs": [
                {"label": "A =", "correct_answer": "2", "placeholder": "Límite inferior"},
                {"label": "B =", "correct_answer": "3", "placeholder": "Límite superior"},
                {"label": "H =", "correct_answer": "0.1", "placeholder": "Paso"},
                {"label": "I =", "correct_answer": "0.14189715", "placeholder": "Resultado"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 2:",
            "titulo": "REGLA 1/3 DE SIMPSON",
            "ecuacion": "∫₀¹ (1-x²) dx, n=4",
            "condiciones": ["Calcula usando Simpson 1/3:", "A =", "B =", "H =", "I ="],
            "texto": ["Resuelve la integral y completa:"],
            "inputs": [
                {"label": "A =", "correct_answer": "0", "placeholder": "Límite inferior"},
                {"label": "B =", "correct_answer": "1", "placeholder": "Límite superior"},
                {"label": "H =", "correct_answer": "0.25", "placeholder": "Paso"},
                {"label": "I =", "correct_answer": "0.6666666666", "placeholder": "Resultado"}
            ]
        },
    ]

    # ---------- Jugador y Vidas ----------
    jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
    sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)

    # ---------- Temporizador ----------
    class Temporizador:
        def __init__(self, tiempo_total_minutos=20):
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

    temporizador = Temporizador(10)  # tiempo por problema (ajustable)

    # ---------- Estado ----------
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

    # ---------- Util ----------
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
            except Exception:
                return False
        return True

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

    # ---------- Cargar nivel3 (no cerrar pygame) ----------
    def cargar_nivel3():
        try:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_nivel3 = os.path.join(directorio_actual, "nivel3.py")
            print(f"[nivel2] intentando cargar: {ruta_nivel3}")

            if os.path.exists(ruta_nivel3):
                if directorio_actual not in sys.path:
                    sys.path.append(directorio_actual)
                import nivel3
                importlib.reload(nivel3)
                nivel3.nivel3(pantalla, ancho, alto)
                return True
            else:
                print("[nivel2] nivel3.py no encontrado en unidad3")
                return False
        except Exception as e:
            print(f"[nivel2] Error al cargar nivel3: {e}")
            import traceback
            traceback.print_exc()
            return False

    # ---------- Main loop ----------
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and not (mostrar_mensaje and show_overlay):
                    return

                if mostrar_mensaje:
                    if show_overlay:
                        if e.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            # Si el jugador ganó (check_result True) -> vida + carga nivel3
                            if check_result is True:
                                sistema_vidas.ganar_vida()
                                mostrar_mensaje = False
                                show_overlay = False
                                temporizador.detener()

                                # Mensaje corto en consola y cargar nivel3
                                print("[nivel2] Respuesta correcta - vida extra otorgada. Cargando nivel3...")
                                if cargar_nivel3():
                                    return
                                else:
                                    return

                            elif check_result is False:
                                sistema_vidas.perder_vida()
                                fallos_en_problema_actual += 1
                                if sistema_vidas.get_vidas() <= 0:
                                    # dejar overlay de game over, al ENTER reinicia nivel (manejo abajo)
                                    pass
                                else:
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

                    # edición de inputs
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

        # Si no hay mensaje y las vidas son 0 -> reiniciar
        if not mostrar_mensaje and sistema_vidas.get_vidas() <= 0:
            reiniciar_nivel()
            continue

        # Actualización principal
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
                        jugador.rect.x -= 40
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

            # Entrar al portal -> mostrar problema
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

        # Temporizador durante el overlay de pregunta
        if mostrar_mensaje and not show_overlay and not tiempo_agotado_overlay:
            tiempo_valido = temporizador.actualizar()
            if not tiempo_valido and temporizador.tiempo_agotado():
                sistema_vidas.perder_vida()
                tiempo_agotado_overlay = True
                temporizador.detener()

        # ---------- Dibujado ----------
        offset_x = camara_x % fondo_ancho
        for i in range(-2, (ancho // fondo_ancho) + 3):
            pantalla.blit(fondo, ((i * fondo_ancho) - offset_x, 0))

        COLOR_SUELO = (100, 80, 50)
        COLOR_MADERA_OSCURA = (101, 67, 33)
        COLOR_MADERA_CLARA = (139, 90, 43)

        # Piso
        if piso_img:
            num_tiles = (suelo.width // piso_img.get_width()) + 1
            for i in range(num_tiles):
                pantalla.blit(piso_img, (suelo.x - camara_x + i * piso_img.get_width(), suelo.y))
        else:
            pygame.draw.rect(pantalla, COLOR_SUELO, pygame.Rect(suelo.x - camara_x, suelo.y, suelo.width, suelo.height))

        # Plataformas
        for p in plataformas:
            pygame.draw.rect(pantalla, COLOR_MADERA_CLARA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6)
            pygame.draw.rect(pantalla, COLOR_MADERA_OSCURA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6, width=3)

        # Portal
        pantalla.blit(portal_img, (meta.x - camara_x, meta.y))

        # Enemigos y objetos
        for en in enemigos:
            en.dibujar(pantalla, camara_x)
        for obj in objetos_rojos:
            obj.dibujar(pantalla, camara_x)

        # Jugador
        jugador.dibujar(pantalla, camara_x)

        # HUD
        texto = fuente.render("UNIDAD 3 - NIVEL 2", True, (255, 255, 255))
        pantalla.blit(texto, (20, 20))
        sistema_vidas.dibujar(pantalla, ancho)

        # Overlay del problema
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

            titulo_p = fuente.render(mensaje_data.get("problema_titulo", ""), True, (255, 255, 255))
            pantalla.blit(titulo_p, titulo_p.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_p.get_height() + 8

            titulo_t = fuente_mensaje.render(mensaje_data.get("titulo", ""), True, (0, 255, 255))
            pantalla.blit(titulo_t, titulo_t.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_t.get_height() + 25

            # Mostrar ecuación
            ecuacion_surf = fuente_cuerpo.render(mensaje_data.get("ecuacion", ""), True, (255, 255, 255))
            pantalla.blit(ecuacion_surf, ecuacion_surf.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += ecuacion_surf.get_height() + 25

            left_x = cuadro_contenido.left + 30
            content_width = cuadro_contenido.width - 60

            for cond in mensaje_data.get("condiciones", []):
                cond_surf = fuente_cuerpo.render(cond, True, (220, 220, 220))
                pantalla.blit(cond_surf, (left_x, y_pos))
                y_pos += fuente_cuerpo.get_height() + 8

            y_pos += 12

            for linea in mensaje_data.get("texto", []):
                linea_surf = fuente_cuerpo.render(linea, True, (220, 220, 220))
                pantalla.blit(linea_surf, (left_x, y_pos))
                y_pos += fuente_cuerpo.get_height() + 8

            # Inputs
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

                    pantalla.blit(label_surf, (input_x, input_y + (input_height - label_surf.get_height()) // 2))

                    box_rect = pygame.Rect(input_x + label_surf.get_width() + 20, input_y, field_width, input_height)

                    if active_input_label == label and check_result is None:
                        border_color = (0, 200, 255)
                        border_width = 3
                    elif check_result is False and show_overlay:
                        border_color = (255, 50, 50)
                        border_width = 3
                    elif check_result is True and show_overlay:
                        border_color = (50, 255, 50)
                        border_width = 3
                    else:
                        border_color = (180, 180, 180)
                        border_width = 2

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

                    pantalla.blit(text_surf, (box_rect.x + 10, box_rect.y + (input_height - text_surf.get_height()) // 2))

                    if active_input_label == label and not show_overlay:
                        if (pygame.time.get_ticks() // 500) % 2 == 0:
                            cursor_x = box_rect.x + 10 + text_surf.get_width()
                            cursor = pygame.Rect(cursor_x, box_rect.y + 8, 2, text_surf.get_height())
                            pygame.draw.rect(pantalla, (0, 0, 0), cursor)

                if not show_overlay:
                    hint = fuente_mensaje.render("Presiona ENTER para verificar - TAB para cambiar campo", True, (200, 200, 200))
                    pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx, bottom=cuadro.bottom - 15))
            else:
                hint = fuente_mensaje.render("Presiona ENTER para continuar", True, (200, 200, 200))
                pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx, bottom=cuadro.bottom - 18))

        # Overlay de feedback
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
                mensaje_principal = "¡FELICIDADES! Respuesta correcta - Ganaste 1 Vida"
                mensaje_hint = "Presiona ENTER para continuar"
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

            pantalla.blit(main_text, main_text.get_rect(centerx=fb_cuadro.centerx, centery=fb_cuadro.centery - 20))
            pantalla.blit(hint_text, hint_text.get_rect(centerx=fb_cuadro.centerx, centery=fb_cuadro.centery + 40))

        pygame.display.flip()
        reloj.tick(60)

# Permite ejecutar el nivel de forma independiente
if __name__ == '__main__':
    pygame.init()
    ANCHO, ALTO = 1200, 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("UNIDAD 3 - NIVEL 2 - SIMPSON 1/3")
    nivel2(pantalla, ANCHO, ALTO)
    pygame.quit()
    sys.exit()