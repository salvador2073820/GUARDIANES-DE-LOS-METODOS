import pygame, sys
import random
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from general.jugador import Jugador
from general.vidas import SistemaVidas

def nivel3(pantalla, ancho, alto):

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
        fuente_encabezado = pygame.font.SysFont("Arial", 20) 

    
    try:
        fondo = pygame.image.load("assets/images/fondonivel1.png").convert()
        fondo = pygame.transform.scale(fondo, (ancho, alto))
    except pygame.error:
        fondo = pygame.Surface((ancho, alto))
        fondo.fill((135, 206, 235))
    fondo_ancho = fondo.get_width()

    
    try:
        piso_img = pygame.image.load("assets/images/piso3.jpg").convert_alpha()
    except pygame.error:
        piso_img = None

    
    ALTURA_SUELO = 110
    ANCHO_MUNDO_MAXIMO = 5000

    
    suelo = pygame.Rect(0, alto - ALTURA_SUELO, ANCHO_MUNDO_MAXIMO, ALTURA_SUELO)
    plataformas = [
        pygame.Rect(200, alto - ALTURA_SUELO - 80, 180, 20),
        pygame.Rect(520, alto - ALTURA_SUELO - 140, 140, 20),
        pygame.Rect(900, alto - ALTURA_SUELO - 220, 220, 20),
        pygame.Rect(1300, alto - ALTURA_SUELO - 100, 120, 20),
        pygame.Rect(1700, alto - ALTURA_SUELO - 260, 180, 20),
        pygame.Rect(1000, alto - ALTURA_SUELO - 60, 90, 20),
        pygame.Rect(1450, alto - ALTURA_SUELO - 200, 110, 20),
    ]
    entidades_colisionables = [suelo] + plataformas

    try:
        portal_img = pygame.image.load("assets/images/portalsinfondo.png").convert_alpha()
        PORTAL_WIDTH = 270
        PORTAL_HEIGHT = 360
        portal_img = pygame.transform.scale(portal_img, (PORTAL_WIDTH, PORTAL_HEIGHT))
    except pygame.error:
        portal_img = pygame.Surface((150, 200), pygame.SRCALPHA)
        portal_img.fill((100, 50, 200, 200))

    meta = pygame.Rect(2400, alto - ALTURA_SUELO - PORTAL_HEIGHT, PORTAL_WIDTH, PORTAL_HEIGHT)

    MENSAJES_ALEATORIOS = [
        {
            "problema_titulo": "PROBLEMA 1",
            "titulo": "NEWTON HACIA ATRÁS",
            "tabla": [
                (2.2, 2.54),
                (2.5, 2.82),
                (2.8, 3.21)
            ],
            "texto": [
                "Obtener g(x) para x = 2.4"
            ],
            "inputs": [
                {"label": "s =", "correct_answer": "-1.333333333"},
                {"label": "g(x) =", "correct_answer": "2.714444444"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 2",
            "titulo": "NEWTON HACIA ATRÁS",
            "tabla": [
                (2.0, 0.40),
                (2.5, 0.50),
                (3.0, 0.60)
            ],
            "texto": [
                "Obtener g(x) para x = 2.9"
            ],
            "inputs": [
                {"label": "s =", "correct_answer": "-0.2"},
                {"label": "g(x) =", "correct_answer": "0.58"}
            ]
        },
        {
            "problema_titulo": "PROBLEMA 3",
            "titulo": "NEWTON HACIA ATRÁS",
            "tabla": [
                (5.0, 1.61),
                (6.0, 1.79),
                (7.0, 1.95),
                (8.0, 2.08)
            ],
            "texto": [
                "Obtener g(x) para x = 8"
            ],
            "inputs": [
                {"label": "s =", "correct_answer": "0"},
                {"label": "g(x) =", "correct_answer": "2.08"}
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

    # Cámara
    camara_x = 0

    # Estado de la interfaz/inputs
    mostrar_mensaje = False
    mensaje_data = None
    input_texts = {}
    active_input_label = None
    check_result = None
    show_overlay = False
    vidas_restantes_despues_error = 0
    tiempo_agotado_overlay = False

    # Contador de fallos para el PROBLEMA ACTUAL: si llega a 3 -> reiniciar nivel
    fallos_en_problema_actual = 0

    # Variables para almacenar las posiciones de los inputs
    input_rects = {}

    def check_answers(data, inputs):
        TOLERANCE = 1e-6
        for spec in data.get("inputs", []):
            label = spec["label"]
            correct = spec["correct_answer"]
            player = inputs.get(label, "").strip()
            if not player:
                return False
            try:
                if abs(float(player) - float(correct)) > TOLERANCE:
                    return False
            except ValueError:
                if player.lower() != correct.lower():
                    return False
            except:
                return False
        return True

    # Función para reiniciar estado del nivel (volvemos a estado inicial del nivel)
    def reiniciar_nivel():
        nonlocal jugador, sistema_vidas, temporizador, camara_x
        nonlocal mostrar_mensaje, mensaje_data, input_texts, active_input_label
        nonlocal check_result, show_overlay, vidas_restantes_despues_error, tiempo_agotado_overlay
        nonlocal fallos_en_problema_actual, input_rects

        # Reinstanciar jugador y vidas
        jugador = Jugador(100, alto - ALTURA_SUELO - 140, ancho, alto)
        sistema_vidas = SistemaVidas(max_vidas=5, vidas_iniciales=3)
        temporizador.reiniciar()
        camara_x = 0

        # Reset UI
        mostrar_mensaje = False
        mensaje_data = None
        input_texts = {}
        active_input_label = None
        check_result = None
        show_overlay = False
        vidas_restantes_despues_error = 0
        tiempo_agotado_overlay = False
        fallos_en_problema_actual = 0
        input_rects = {}

    
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
                            # Si el jugador agotó vidas tras error y no quedan vidas -> salir
                            if check_result is False and vidas_restantes_despues_error <= 0:
                                return

                            if check_result is True:
                                # RESPUESTA CORRECTA: Ganar 1 vida y avanzar al NIVEL 4
                                sistema_vidas.ganar_vida()
                                mostrar_mensaje = False
                                show_overlay = False
                                temporizador.detener()

                                # === PANTALLA DE TRANSICIÓN AL NIVEL 4 ===
                                pantalla.fill((0, 0, 0))  # Fondo negro
                                
                                # Mostrar mensaje de transición
                                mensaje_transicion = fuente.render("¡NIVEL 3 COMPLETADO!", True, (255, 255, 255))
                                mensaje_continuar = fuente_mensaje.render("Cargando nivel 4...", True, (200, 200, 200))
                                
                                pantalla.blit(mensaje_transicion, mensaje_transicion.get_rect(center=(ancho//2, alto//2 - 50)))
                                pantalla.blit(mensaje_continuar, mensaje_continuar.get_rect(center=(ancho//2, alto//2 + 50)))
                                pygame.display.flip()
                                
                                # Pequeña pausa para mostrar el mensaje
                                pygame.time.delay(2000)

                                # TRANSICIÓN AL NIVEL 4
                                try:
                                    from unidades.unidad1.nivel4 import nivel4
                                    # Llamada a nivel4: aquí se realiza la transferencia al siguiente nivel.
                                    nivel4(pantalla, ancho, alto)
                                    return  # Salir del nivel 3 después de completar nivel 4
                                except Exception as ex:
                                    print("Error al cargar Nivel 4:", ex)
                                    return  # Salir si no se puede cargar el nivel 4

                            elif check_result is False:
                                # RESPUESTA INCORRECTA: perder vida y permitir reintento
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
                                    # Reiniciar nivel después de 3 fallos
                                    reiniciar_nivel()
                            continue

                    # Si se está respondiendo (inputs)
                    if mensaje_data and mensaje_data.get("inputs"):
                        if e.unicode.isdigit() or e.unicode in ".-":
                            if active_input_label and len(input_texts[active_input_label]) < 40:
                                input_texts[active_input_label] += e.unicode
                        elif e.key == pygame.K_BACKSPACE:
                            if active_input_label:
                                input_texts[active_input_label] = input_texts[active_input_label][:-1]
                        elif e.key in (pygame.K_TAB, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                            # Navegación entre inputs con TAB, flechas arriba/abajo y derecha/izquierda
                            labels = [i['label'] for i in mensaje_data["inputs"]]
                            if active_input_label in labels:
                                i = labels.index(active_input_label)
                                if e.key in (pygame.K_TAB, pygame.K_DOWN, pygame.K_RIGHT):
                                    active_input_label = labels[(i + 1) % len(labels)]
                                else:  # K_UP o K_LEFT
                                    active_input_label = labels[(i - 1) % len(labels)]
                        elif e.key in (pygame.K_RETURN, pygame.K_SPACE):
                            check_result = check_answers(mensaje_data, input_texts)
                            if check_result is False:
                                vidas_restantes_despues_error = sistema_vidas.get_vidas_restantes_despues_error()
                            show_overlay = True
                            temporizador.detener()
                    else:
                        if e.key in (pygame.K_RETURN, pygame.K_SPACE):
                            mostrar_mensaje = False
                            temporizador.detener()
                    continue

            if e.type == pygame.MOUSEBUTTONDOWN and mostrar_mensaje and mensaje_data and mensaje_data.get("inputs") and not show_overlay:
                mouse_x, mouse_y = e.pos
                
                # Verificar si se hizo click en alguno de los inputs
                for label, rect in input_rects.items():
                    if rect.collidepoint(mouse_x, mouse_y):
                        active_input_label = label
                        break

        if not mostrar_mensaje:
            keys = pygame.key.get_pressed()
            jugador.actualizar_movimiento(keys, entidades_colisionables)
            jugador.actualizar_animacion()
            jugador.limitar_movimiento(ANCHO_MUNDO_MAXIMO)
            camara_x = max(0, jugador.get_posicion_para_camara() - ancho // 2)

            
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
                # Mueve al jugador para que no colisione repetidamente con el portal
                jugador.rect.right = meta.left - 5
                # Resetear contador de fallos para este nuevo problema
                fallos_en_problema_actual = 0
                # Limpiar rectángulos de inputs
                input_rects = {}

        if mostrar_mensaje and not show_overlay and not tiempo_agotado_overlay:
            tiempo_valido = temporizador.actualizar()
            if not tiempo_valido and temporizador.tiempo_agotado():
                # Tiempo agotado: el jugador pierde 1 vida y aparece overlay
                sistema_vidas.perder_vida()
                tiempo_agotado_overlay = True
                temporizador.detener()

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

        # Plataformas (diferente disposición visual)
        for p in plataformas:
            pygame.draw.rect(pantalla, COLOR_MADERA_CLARA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=5)
            pygame.draw.rect(pantalla, COLOR_MADERA_OSCURA, pygame.Rect(p.x - camara_x, p.y, p.width, p.height), border_radius=5, width=3)

        # Portal
        pantalla.blit(portal_img, (meta.x - camara_x, meta.y))

        # Jugador
        jugador.dibujar(pantalla, camara_x)

        # Título
        texto = fuente.render("NIVEL 3", True, (255, 255, 255))
        pantalla.blit(texto, (20, 20))

        # Vidas
        sistema_vidas.dibujar(pantalla, ancho)

        # Si se muestra mensaje (problema)
        if mostrar_mensaje and mensaje_data:
            # Temporizador en pantalla (si no hay overlay y no se agotó)
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

            # Fondo semitransparente
            s = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            pantalla.blit(s, (0, 0))

            cuadro_ancho = ancho * 0.85
            cuadro_alto = alto * 0.75
            cuadro_x = (ancho - cuadro_ancho) // 2
            cuadro_y = (alto - cuadro_alto) // 2
            cuadro = pygame.Rect(cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto)

            pygame.draw.rect(pantalla, (200, 200, 200), cuadro, border_radius=15)
            cuadro_contenido = cuadro.inflate(-30, -30)
            pygame.draw.rect(pantalla, (50, 50, 50), cuadro_contenido, border_radius=10)

            y_pos = cuadro_contenido.top + 20

            titulo_p = fuente.render(mensaje_data["problema_titulo"], True, (255, 255, 255))
            pantalla.blit(titulo_p, titulo_p.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_p.get_height() + 10

            titulo_t = fuente_mensaje.render(mensaje_data["titulo"], True, (0, 255, 255))
            pantalla.blit(titulo_t, titulo_t.get_rect(centerx=cuadro.centerx, top=y_pos))
            y_pos += titulo_t.get_height() + 20

            # Mostrar enunciado
            line_height = fuente_cuerpo.get_height() + 5
            for linea in mensaje_data.get("texto", []):
                linea_surf = fuente_cuerpo.render(linea, True, (255, 255, 255))
                pantalla.blit(linea_surf, linea_surf.get_rect(centerx=cuadro.centerx, top=y_pos))
                y_pos += line_height

            y_pos += 10  # Espacio adicional antes de la tabla

            # Mostrar tabla de datos si existe
            if mensaje_data.get("tabla"):
                tabla_datos = mensaje_data["tabla"]
                
                # Configuración de la tabla
                tabla_width = 400
                fila_height = 40
                tabla_x = cuadro_contenido.centerx - tabla_width // 2
                tabla_y = y_pos
                tabla_height = (len(tabla_datos) + 1) * fila_height + 10

                # Fondo de la tabla
                pygame.draw.rect(pantalla, (40, 40, 40), (tabla_x, tabla_y, tabla_width, tabla_height), border_radius=8)
                pygame.draw.rect(pantalla, (200, 200, 200), (tabla_x, tabla_y, tabla_width, tabla_height), 2, border_radius=8)

                # Encabezados de la tabla
                encabezado_y = tabla_y + 8
                encabezado_xi = fuente_cuerpo.render("Xi", True, (255, 255, 255))
                encabezado_yi = fuente_cuerpo.render("Yi", True, (255, 255, 255))
                
                # Centrar encabezados en sus columnas
                col_xi_center = tabla_x + tabla_width * 0.25
                col_yi_center = tabla_x + tabla_width * 0.75
                
                pantalla.blit(encabezado_xi, (col_xi_center - encabezado_xi.get_width() // 2, encabezado_y))
                pantalla.blit(encabezado_yi, (col_yi_center - encabezado_yi.get_width() // 2, encabezado_y))

                # Línea horizontal debajo del encabezado
                pygame.draw.line(pantalla, (200, 200, 200), 
                                (tabla_x + 10, encabezado_y + encabezado_xi.get_height() + 5),
                                (tabla_x + tabla_width - 10, encabezado_y + encabezado_xi.get_height() + 5), 2)

                # Línea vertical separadora
                separador_x = tabla_x + tabla_width // 2
                pygame.draw.line(pantalla, (180, 180, 180), 
                                (separador_x, tabla_y + 10),
                                (separador_x, tabla_y + tabla_height - 10), 2)

                # Dibujar filas con datos
                fila_y = tabla_y + fila_height + 5
                for i, (xi, yi) in enumerate(tabla_datos):
                    # Renderizar valores
                    xi_text = fuente_cuerpo.render(f"{xi}", True, (255, 255, 255))
                    yi_text = fuente_cuerpo.render(f"{yi}", True, (255, 255, 255))
                    
                    # Centrar valores en sus columnas
                    pantalla.blit(xi_text, (col_xi_center - xi_text.get_width() // 2, fila_y))
                    pantalla.blit(yi_text, (col_yi_center - yi_text.get_width() // 2, fila_y))
                    
                    # Línea horizontal entre filas
                    if i < len(tabla_datos) - 1:
                        pygame.draw.line(pantalla, (150, 150, 150),
                                        (tabla_x + 10, fila_y + fila_height - 5),
                                        (tabla_x + tabla_width - 10, fila_y + fila_height - 5), 1)
                    
                    fila_y += fila_height

                y_pos = tabla_y + tabla_height + 20

            # Inputs para respuestas
            if mensaje_data.get("inputs"):
                input_y_start = y_pos
                input_height = 40
                field_width = 300

                # Limpiar rectángulos anteriores
                input_rects = {}

                for i, spec in enumerate(mensaje_data["inputs"]):
                    label = spec["label"]

                    label_surf = fuente_cuerpo.render(label, True, (255, 255, 255))
                    total_width = label_surf.get_width() + 10 + field_width
                    input_x = cuadro.centerx - total_width // 2
                    input_y = input_y_start + i * 50

                    pantalla.blit(
                        label_surf,
                        (input_x, input_y + (input_height - label_surf.get_height()) // 2)
                    )

                    box_rect = pygame.Rect(
                        input_x + label_surf.get_width() + 10,
                        input_y,
                        field_width,
                        input_height
                    )

                    # Guardar el rectángulo para detección de clicks
                    input_rects[label] = box_rect

                    if active_input_label == label and check_result is None:
                        border_color = (0, 255, 255)
                    elif check_result is False and show_overlay:
                        border_color = (255, 0, 0)
                    elif check_result is True and show_overlay:
                        border_color = (0, 255, 0)
                    else:
                        border_color = (255, 255, 255)

                    pygame.draw.rect(pantalla, border_color, box_rect, border_radius=5, width=3)
                    pygame.draw.rect(pantalla, (255, 255, 255), box_rect.inflate(-3, -3), border_radius=5)

                    text_surf = fuente_cuerpo.render(input_texts.get(label, ""), True, (0, 0, 0))
                    pantalla.blit(text_surf, (box_rect.x + 5, box_rect.y + 7))

                    if active_input_label == label and not show_overlay:
                        if (pygame.time.get_ticks() // 500) % 2 == 0:
                            cursor = pygame.Rect(
                                box_rect.x + 5 + text_surf.get_width(),
                                box_rect.y + 7,
                                2,
                                text_surf.get_height()
                            )
                            pygame.draw.rect(pantalla, (0, 0, 0), cursor)

                if not show_overlay:
                    hint = fuente_mensaje.render("Presiona ENTER para verificar", True, (200, 200, 200))
                    pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx, bottom=cuadro.bottom - 15))
                    
                    # Instrucciones de navegación
                    navegacion = fuente_cuerpo.render("Usa TAB, flechas o haz click para cambiar entre campos", True, (180, 180, 180))
                    pantalla.blit(navegacion, navegacion.get_rect(centerx=cuadro.centerx, bottom=cuadro.bottom - 45))
            else:
                hint = fuente_mensaje.render("Presiona ENTER para continuar", True, (200, 200, 200))
                pantalla.blit(hint, hint.get_rect(centerx=cuadro.centerx, bottom=cuadro.bottom - 15))

        # Overlay (tiempo agotado / éxito / fallo) 
        if mostrar_mensaje and (show_overlay or tiempo_agotado_overlay):
            s_overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            s_overlay.fill((0, 0, 0, 100))
            pantalla.blit(s_overlay, (0, 0))

            fb_ancho = ancho * 0.6
            fb_alto = 200
            fb_x = (ancho - fb_ancho) // 2
            fb_y = (alto - fb_alto) // 2 - 100
            fb_cuadro = pygame.Rect(fb_x, fb_y, fb_ancho, fb_alto)

            if tiempo_agotado_overlay:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡TIEMPO AGOTADO! Perdiste 1 Vida"
                if sistema_vidas.get_vidas() > 0:
                    mensaje_hint = "Presiona ENTER para volver a intentar"
                else:
                    mensaje_hint = "Presiona ENTER o ESC para Salir del Nivel"
            elif check_result is True:
                color_fondo = (50, 200, 50)
                color_texto = (255, 255, 255)
                mensaje_principal = "¡FELICIDADES! Respuesta correcta"
                mensaje_hint = "Presiona ENTER para continuar"
            else:
                color_fondo = (200, 50, 50)
                color_texto = (255, 255, 255)
                if fallos_en_problema_actual >= 3:
                    mensaje_principal = "¡REINICIANDO NIVEL! Fallaste 3 veces"
                    mensaje_hint = "..."
                elif vidas_restantes_despues_error <= 0:
                    mensaje_principal = "¡GAME OVER! Vidas Agotadas"
                    mensaje_hint = "Presiona ENTER o ESC para Salir del Nivel"
                else:
                    mensaje_principal = f"¡INCORRECTO! Perdiste 1 Vida ({sistema_vidas.get_vidas()} restantes)"
                    mensaje_hint = "Presiona ENTER para volver a intentar"

            pygame.draw.rect(pantalla, (255, 255, 255), fb_cuadro, border_radius=15)
            pygame.draw.rect(pantalla, color_fondo, fb_cuadro.inflate(-5, -5), border_radius=10)

            main_text = fuente.render(mensaje_principal, True, color_texto)
            hint_text = fuente_mensaje.render(mensaje_hint, True, color_texto)

            pantalla.blit(main_text, main_text.get_rect(centerx=fb_cuadro.centerx, centery=fb_cuadro.centery - 20))
            pantalla.blit(hint_text, hint_text.get_rect(centerx=fb_cuadro.centerx, centery=fb_cuadro.centery + 40))

        pygame.display.flip()
        reloj.tick(60)

# Permitir ejecución directa para pruebas
if __name__ == '__main__':
    pygame.init()
    ANCHO, ALTO = 1200, 800
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("NIVEL 3")
    nivel3(pantalla, ANCHO, ALTO)
    pygame.quit()
    sys.exit()