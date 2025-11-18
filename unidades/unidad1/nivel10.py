import pygame, sys
import random
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from general.jugador import Jugador
from general.vidas import SistemaVidas

def nivel10(pantalla, ancho, alto):

    pygame.init()
    reloj = pygame.time.Clock()


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


    try:
        fondo = pygame.image.load("assets/images/fondonivel1.png").convert()
        fondo = pygame.transform.scale(fondo, (ancho, alto))
    except:
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((120, 160, 250))
    fondo_ancho = fondo.get_width()

    try:
        piso_img = pygame.image.load("assets/images/piso3.jpg").convert_alpha()
    except:
        piso_img = None

    ALTURA_SUELO = 110
    ANCHO_MUNDO_MAXIMO = 5200

    suelo = pygame.Rect(0, alto - ALTURA_SUELO, ANCHO_MUNDO_MAXIMO, ALTURA_SUELO)


    plataformas = [
        pygame.Rect(180, alto - ALTURA_SUELO - 160, 240, 25),
        pygame.Rect(620, alto - ALTURA_SUELO - 90, 200, 25),
        pygame.Rect(1050, alto - ALTURA_SUELO - 240, 240, 25),
        pygame.Rect(1500, alto - ALTURA_SUELO - 100, 200, 25),
        pygame.Rect(1900, alto - ALTURA_SUELO - 210, 250, 25),
        pygame.Rect(2300, alto - ALTURA_SUELO - 140, 230, 25),
        pygame.Rect(2700, alto - ALTURA_SUELO - 260, 260, 25),
        pygame.Rect(3100, alto - ALTURA_SUELO - 120, 200, 25),
        pygame.Rect(3450, alto - ALTURA_SUELO - 160, 260, 25),
        pygame.Rect(3800, alto - ALTURA_SUELO - 80, 200, 25),
    ]
    entidades_colisionables = [suelo] + plataformas


    try:
        portal_img = pygame.image.load("assets/images/portalsinfondo.png").convert_alpha()
        PORTAL_WIDTH = 270
        PORTAL_HEIGHT = 360
        portal_img = pygame.transform.scale(portal_img, (PORTAL_WIDTH, PORTAL_HEIGHT))
    except:
        portal_img = pygame.Surface((200, 260), pygame.SRCALPHA)
        portal_img.fill((90, 50, 190, 180))

    meta = pygame.Rect(3400, alto - ALTURA_SUELO - PORTAL_HEIGHT, PORTAL_WIDTH, PORTAL_HEIGHT)


    class ObjetoRojo:
        def __init__(self, x, y, w=40, h=40):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = (255, 0, 0)
            self.cooldown_hit = 0

        def actualizar(self):
            if self.cooldown_hit > 0:
                self.cooldown_hit -= 1

        def dibujar(self, surf, camara_x):
            r = self.rect.move(-camara_x, 0)
            pygame.draw.rect(surf, self.color, r, border_radius=6)
            pygame.draw.circle(surf, (255, 180, 180), r.center, 10)

        def intentar_danar(self, jugador_rect):
            if self.rect.colliderect(jugador_rect) and self.cooldown_hit == 0:
                self.cooldown_hit = 60
                return True
            return False

    objetos_rojos = [
        ObjetoRojo(520, alto - ALTURA_SUELO - 120),
        ObjetoRojo(1150, alto - ALTURA_SUELO - 260),
        ObjetoRojo(1750, alto - ALTURA_SUELO - 100),
        ObjetoRojo(2550, alto - ALTURA_SUELO - 220),
        ObjetoRojo(3000, alto - ALTURA_SUELO - 100),
    ]

    class Enemigo:
        def __init__(self, x, y, rango=140, velocidad=2):
            self.rect = pygame.Rect(x, y, 60, 60)
            self.color = (190, 40, 40)
            self.origen_x = x
            self.rango = rango
            self.velocidad = velocidad
            self.direccion = 1
            self.cooldown_hit = 0

        def actualizar(self):
            self.rect.x += self.velocidad * self.direccion
            if abs(self.rect.x - self.origen_x) >= self.rango:
                self.direccion *= -1

            if self.cooldown_hit > 0:
                self.cooldown_hit -= 1

        def dibujar(self, surf, camara_x):
            pygame.draw.rect(surf, self.color, self.rect.move(-camara_x, 0))

        def intentar_danar(self, jugador_rect):
            if self.rect.colliderect(jugador_rect) and self.cooldown_hit == 0:
                self.cooldown_hit = 60
                return True
            return False

    enemigos = [
        Enemigo(800, alto - ALTURA_SUELO - 60, rango=210, velocidad=3),
        Enemigo(1800, alto - ALTURA_SUELO - 150, rango=160, velocidad=2),
        Enemigo(2800, alto - ALTURA_SUELO - 60, rango=240, velocidad=3),
    ]

    MENSAJES_ALEATORIOS = [
        {
            "problema_titulo": "PROBLEMA 1",
            "titulo": "MÉTODO FALSA POSICIÓN",
            "texto": [
                "Usando el método de Falsa Posición para",
                "f(x)=e^4x - 7",
                "Contesta lo siguiente:"
            ],
            "inputs": [
                {"label": "Margen de error en  la 12va iteración =", "correct_answer": "0.0042136787", "placeholder": "Respuesta"},
                {"label": "Valor de a cuando i=10", "correct_answer": "0.457640879", "placeholder": "Respuesta"},
                {"label": "Valor de f(a) cuando i=14", "correct_answer": "-0.192744668", "placeholder": "Respuesta"},
                {"label": "Valor de x cuando margen de error = 0.001", "correct_answer": "0.483066368", "placeholder": "Respuesta"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 2",
            "titulo": "MÉTODO FALSA POSICIÓN",
            "texto": [
                "Usando el método de Falsa Posición para",
                "f(x)=2x^2 - 6x - 2",
                "Contesta lo siguiente:"
            ],
            "inputs": [
               {"label": "Margen de error en  la 3ra iteración =", "correct_answer": "0.548472075", "placeholder": "Respuesta"},
                {"label": "Valor de a cuando i=5", "correct_answer": "-0.297959183", "placeholder": "Respuesta"},
                {"label": "Valor de f(a) cuando i=2", "correct_answer": "-0.375", "placeholder": "Respuesta"},
                {"label": "Valor de x cuando margen de error = 0.001", "correct_answer": "-0.302735106", "placeholder": "Respuesta"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 3",
            "titulo": "MÉTODO FALSA POSICIÓN",
            "texto": [
                "Usando el método de Falsa Posición para",
                "f(x)=e^7x - 3/4x",
                "Contesta lo siguiente:"
            ],
            "inputs": [
               {"label": "Margen de error en  la 5ta iteración =", "correct_answer": "0.0000105776864", "placeholder": "Respuesta"},
                {"label": "Valor de a cuando i=2", "correct_answer": "5", "placeholder": "Respuesta"},
                {"label": "Valor de f(a) cuando i=3", "correct_answer": "3.381860134", "placeholder": "Respuesta"},
                {"label": "Valor de x cuando margen de error = 0.001", "correct_answer": "5.54138125", "placeholder": "Respuesta"}
            ]
        }
    ]


    jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
    sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)

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

    temporizador = Temporizador(20)

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

    def reiniciar_nivel():
        nonlocal jugador, sistema_vidas, temporizador, camara_x
        nonlocal mostrar_mensaje, mensaje_data, input_texts, active_input_label
        nonlocal check_result, show_overlay, vidas_restantes_despues_error, tiempo_agotado_overlay
        nonlocal fallos_en_problema_actual

        jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
        sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)
        temporizador.reiniciar()
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

                            if check_result is False and sistema_vidas.get_vidas() <= 0:
                                reiniciar_nivel()
                                continue

                            if tiempo_agotado_overlay and sistema_vidas.get_vidas() <= 0:
                                reiniciar_nivel()
                                continue

                            if check_result is True:
                                sistema_vidas.ganar_vida()
                                mostrar_mensaje = False
                                show_overlay = False
                                temporizador.detener()
                                try:
                                    from unidades.unidad1.nivel11 import nivel11
                                    nivel11(pantalla, ancho, alto)
                                    return
                                except Exception as ex:
                                    print("Error al cargar Nivel 11:", ex)

                            elif check_result is False:
                                sistema_vidas.perder_vida()
                                fallos_en_problema_actual += 1
                                check_result = None
                                input_texts = {i["label"]: "" for i in mensaje_data.get("inputs", [])}
                                if mensaje_data.get("inputs"):
                                    active_input_label = mensaje_data["inputs"][0]["label"]
                                show_overlay = False
                                temporizador.reiniciar()
                                temporizador.iniciar()

                                if fallos_en_problema_actual >= 3:
                                    reiniciar_nivel()
                            elif tiempo_agotado_overlay:
                                tiempo_agotado_overlay = False
                                mostrar_mensaje = False
                                temporizador.reiniciar()
                                temporizador.iniciar()
                            continue

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
                                idx = labels.index(active_input_label)
                                if e.key in (pygame.K_TAB, pygame.K_DOWN):
                                    active_input_label = labels[(idx + 1) % len(labels)]
                                else:
                                    active_input_label = labels[(idx - 1) % len(labels)]
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

                start_y = cuadro_contenido.centery + 30

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

        if not mostrar_mensaje:
            if sistema_vidas.get_vidas() <= 0:
                reiniciar_nivel()
                continue

            keys = pygame.key.get_pressed()
            jugador.actualizar_movimiento(keys, entidades_colisionables)
            jugador.actualizar_animacion()
            jugador.limitar_movimiento(ANCHO_MUNDO_MAXIMO)
            camara_x = max(0, jugador.get_posicion_para_camara() - ancho // 2)

            for en in enemigos:
                en.actualizar()
                if en.intentar_danar(jugador.rect):
                    sistema_vidas.perder_vida()
                    jugador.rect.x -= 50

            for obj in objetos_rojos:
                obj.actualizar()
                if obj.intentar_danar(jugador.rect):
                    sistema_vidas.perder_vida()
                    jugador.rect.x -= 30

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

        if mostrar_mensaje and not show_overlay and not tiempo_agotado_overlay:
            if not temporizador.actualizar():
                sistema_vidas.perder_vida()
                tiempo_agotado_overlay = True
                temporizador.detener()


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
            pygame.draw.rect(pantalla, COLOR_MADERA_CLARA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6)
            pygame.draw.rect(pantalla, COLOR_MADERA_OSCURA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=6, width=3)

        pantalla.blit(portal_img, (meta.x - camara_x, meta.y))

        for en in enemigos:
            en.dibujar(pantalla, camara_x)

        for obj in objetos_rojos:
            obj.dibujar(pantalla, camara_x)

        jugador.dibujar(pantalla, camara_x)

        texto = fuente.render("NIVEL 10 - MÉTODO FALSA POSICIÓN", True, (255, 255, 255))
        pantalla.blit(texto, (20, 20))
        sistema_vidas.dibujar(pantalla, ancho)


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
                fondo_tiempo = pygame.Surface(
                    (tiempo_surface.get_width() + 20, tiempo_surface.get_height() + 10), pygame.SRCALPHA)
                fondo_tiempo.fill((0, 0, 0, 150))
                pantalla.blit(fondo_tiempo, (tiempo_rect.x - 10, tiempo_rect.y - 5))
                pantalla.blit(tiempo_surface, tiempo_rect)

            # Fondo semitransparente
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
            right_x = cuadro_contenido.centerx + 20

            # Texto
            for linea in mensaje_data.get("texto", []):
                linea_surf = fuente_cuerpo.render(linea, True, (220, 220, 220))
                pantalla.blit(linea_surf, (left_x, y_pos))
                y_pos += fuente_cuerpo.get_height() + 8

            y_pos += 20

            # Tabla
            tabla = mensaje_data.get("tabla", [])
            if tabla:
                tabla_width = 300
                tabla_x = right_x
                tabla_y = cuadro_contenido.top + 120
                fila_h = 40

                pygame.draw.rect(pantalla, (60, 60, 100), (tabla_x, tabla_y, tabla_width, fila_h), border_radius=8)

                encabezados = tabla[0]
                for j, header in enumerate(encabezados):
                    header_surf = fuente_cuerpo.render(str(header), True, (255, 255, 255))
                    x_pos = tabla_x + 20 + j * (tabla_width // len(encabezados))
                    pantalla.blit(header_surf,
                                   (x_pos, tabla_y + (fila_h - header_surf.get_height()) // 2))

                # Filas
                for i, fila in enumerate(tabla[1:], 1):
                    fila_y = tabla_y + i * fila_h
                    pygame.draw.rect(pantalla,
                                     (40 + 10 * (i % 2), 40, 40),
                                     (tabla_x, fila_y, tabla_width, fila_h))
                    for j, valor in enumerate(fila):
                        valor_surf = fuente_cuerpo.render(str(valor), True, (255, 255, 255))
                        x_pos = tabla_x + 20 + j * (tabla_width // len(fila))
                        pantalla.blit(valor_surf,
                                       (x_pos, fila_y + (fila_h - valor_surf.get_height()) // 2))

                tabla_h = len(tabla) * fila_h
                pygame.draw.rect(pantalla, (200, 200, 200),
                                 (tabla_x, tabla_y, tabla_width, tabla_h), 2, border_radius=8)

            # Inputs
            if mensaje_data.get("inputs"):
                input_height = 46
                field_width = 350
                spacing = 20

                start_y = cuadro_contenido.centery + 20

                for i, spec in enumerate(mensaje_data["inputs"]):
                    label = spec["label"]
                    placeholder = spec.get("placeholder", "")

                    label_surf = fuente_cuerpo.render(label, True, (255, 255, 255))
                    total_width = label_surf.get_width() + 20 + field_width
                    input_x = cuadro_contenido.centerx - total_width // 2
                    input_y = start_y + i * (input_height + spacing)

                    pantalla.blit(label_surf,
                                  (input_x, input_y + (input_height - label_surf.get_height()) // 2))

                    box_rect = pygame.Rect(
                        input_x + label_surf.get_width() + 20,
                        input_y, field_width, input_height)

                    # Color del borde
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

                    pygame.draw.rect(pantalla, (240, 240, 240),
                                     box_rect, border_radius=8)
                    pygame.draw.rect(pantalla, border_color,
                                     box_rect, border_width, border_radius=8)

                    text_to_show = input_texts.get(label, "")
                    if not text_to_show and active_input_label != label:
                        text_to_show = placeholder
                        color_texto = (150, 150, 150)
                    else:
                        color_texto = (0, 0, 0)

                    text_surf = fuente_cuerpo.render(text_to_show, True, color_texto)

                    if text_surf.get_width() > field_width - 20:
                        t = text_to_show
                        while fuente_cuerpo.render(t + "...", True, color_texto).get_width() > field_width - 20 and len(t) > 1:
                            t = t[:-1]
                        text_surf = fuente_cuerpo.render(t + "...", True, color_texto)

                    pantalla.blit(text_surf,
                                   (box_rect.x + 10,
                                    box_rect.y + (input_height - text_surf.get_height()) // 2))

                    # Cursor
                    if active_input_label == label and not show_overlay:
                        if (pygame.time.get_ticks() // 500) % 2 == 0:
                            cursor_x = box_rect.x + 10 + text_surf.get_width()
                            cursor = pygame.Rect(
                                cursor_x, box_rect.y + 8, 2, text_surf.get_height())
                            pygame.draw.rect(pantalla, (0, 0, 0), cursor)

                if not show_overlay:
                    hint = fuente_mensaje.render(
                        "Presiona ENTER para verificar - TAB para cambiar campo",
                        True, (200, 200, 200))
                    pantalla.blit(hint,
                                  hint.get_rect(centerx=cuadro.centerx,
                                                bottom=cuadro.bottom - 15))

        if mostrar_mensaje and (show_overlay or tiempo_agotado_overlay):
            s_overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            s_overlay.fill((0, 0, 0, 100))
            pantalla.blit(s_overlay, (0, 0))

            fb_ancho = ancho * 0.6
            fb_alto = 200
            fb_x = (ancho - fb_ancho) // 2
            fb_y = (alto - fb_alto) // 2 - 80

            fb = pygame.Rect(fb_x, fb_y, fb_ancho, fb_alto)

            if tiempo_agotado_overlay:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡TIEMPO AGOTADO! Perdiste 1 Vida"
                mensaje_hint = "ENTER para intentar de nuevo" if sistema_vidas.get_vidas() > 0 else "ENTER para reiniciar nivel"
            elif check_result is True:
                color_fondo = (50, 200, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡CORRECTO!"
                mensaje_hint = "ENTER para avanzar al Nivel 11"
            else:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                if fallos_en_problema_actual >= 3:
                    mensaje_principal = "3 ERRORES → REINICIO"
                    mensaje_hint = "ENTER para continuar"
                elif sistema_vidas.get_vidas() <= 0:
                    mensaje_principal = "¡GAME OVER!"
                    mensaje_hint = "ENTER para reiniciar nivel"
                else:
                    mensaje_principal = f"¡INCORRECTO! Te quedan {sistema_vidas.get_vidas()} vidas"
                    mensaje_hint = "ENTER para intentar de nuevo"

            pygame.draw.rect(pantalla, (255, 255, 255), fb, border_radius=15)
            pygame.draw.rect(pantalla, color_fondo, fb.inflate(-6, -6), border_radius=10)

            main_text = fuente.render(mensaje_principal, True, color_texto)
            hint_text = fuente_mensaje.render(mensaje_hint, True, color_texto)

            pantalla.blit(main_text,
                          main_text.get_rect(centerx=fb.centerx, centery=fb.centery - 20))
            pantalla.blit(hint_text,
                          hint_text.get_rect(centerx=fb.centerx, centery=fb.centery + 40))

        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    pygame.init()
    ANCHO, ALTO = 1200, 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("NIVEL 10 - MÉTODO FALSA POSICIÓN")
    nivel10(pantalla, ANCHO, ALTO)
    pygame.quit()
    sys.exit()
