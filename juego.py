import pygame, random, math, sys

pygame.init()
ancho, alto = 400, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Flappy Bird")
reloj = pygame.time.Clock()

pajaro_x, pajaro_y, pajaro_radio = 90, alto // 2, 15
velocidad, gravedad, fuerza_salto = 0, 0.5, -8.5
tubos, ancho_tubo, espacio_tubo, vel_tubo = [], 70, 160, 3
ultimo_tubo, intervalo = 0, 1500
puntos, record, suelo = 0, 0, 80
estado = "menu"

celeste = (112, 197, 206)
verde = (84, 186, 50)
marron = (222, 216, 149)
amarillo = (250, 220, 40)
naranja = (240, 130, 30)
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (220, 50, 50)

def texto(txt, tam, x, y, color):
    img = pygame.font.SysFont("arial", tam, bold=True).render(txt, True, color)
    pantalla.blit(img, img.get_rect(center=(x, y)))

def dibujar_pajaro():
    pygame.draw.circle(pantalla, amarillo, (pajaro_x, int(pajaro_y)), pajaro_radio)
    pygame.draw.circle(pantalla, negro, (pajaro_x, int(pajaro_y)), pajaro_radio, 2)
    pygame.draw.circle(pantalla, blanco, (pajaro_x + 7, int(pajaro_y) - 5), 5)
    pygame.draw.circle(pantalla, negro, (pajaro_x + 9, int(pajaro_y) - 5), 2)
    pygame.draw.polygon(pantalla, naranja, [(pajaro_x+12, int(pajaro_y)), (pajaro_x+22, int(pajaro_y)+3), (pajaro_x+12, int(pajaro_y)+7)])

def dibujar_tubo(x, centro):
    arriba = centro - espacio_tubo // 2
    abajo = centro + espacio_tubo // 2
    pygame.draw.rect(pantalla, verde, (x, 0, ancho_tubo, arriba))
    pygame.draw.rect(pantalla, verde, (x, abajo, ancho_tubo, alto - suelo - abajo))

def hay_colision():
    r = pajaro_radio - 3
    p = pygame.Rect(pajaro_x - r, pajaro_y - r, r * 2, r * 2)
    if p.bottom >= alto - suelo or p.top <= 0:
        return True
    for t in tubos:
        arriba = t[1] - espacio_tubo // 2
        abajo = t[1] + espacio_tubo // 2
        if p.colliderect(pygame.Rect(t[0], 0, ancho_tubo, arriba)):
            return True
        if p.colliderect(pygame.Rect(t[0], abajo, ancho_tubo, alto - suelo - abajo)):
            return True
    return False

jugando = True
while jugando:
    tiempo = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
            jugando = False

        saltar = (evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP)) or (evento.type == pygame.MOUSEBUTTONDOWN)
        if saltar:
            if estado == "menu":
                estado, velocidad = "jugando", fuerza_salto
                ultimo_tubo = tiempo - intervalo + 600
            elif estado == "jugando":
                velocidad = fuerza_salto
            elif estado == "muerto":
                pajaro_y, velocidad = alto // 2, fuerza_salto
                tubos, puntos = [], 0
                ultimo_tubo = tiempo - intervalo + 600
                estado = "jugando"

    if estado == "menu":
        pajaro_y = alto // 2 + 8 * math.sin(tiempo / 200)

    elif estado == "jugando":
        velocidad += gravedad
        pajaro_y += velocidad
        if tiempo - ultimo_tubo > intervalo:
            tubos.append([ancho + 20, random.randint(150, alto - suelo - 150), False])
            ultimo_tubo = tiempo
        for t in tubos:
            t[0] -= vel_tubo
            if not t[2] and t[0] + ancho_tubo < pajaro_x:
                t[2] = True
                puntos += 1
        tubos = [t for t in tubos if t[0] + ancho_tubo > 0]
        if hay_colision():
            estado = "muerto"
            if puntos > record:
                record = puntos

    elif estado == "muerto":
        if pajaro_y < alto - suelo - pajaro_radio:
            velocidad += gravedad
            pajaro_y = min(pajaro_y + velocidad, alto - suelo - pajaro_radio)

    pantalla.fill(celeste)
    for t in tubos:
        dibujar_tubo(t[0], t[1])
    pygame.draw.rect(pantalla, marron, (0, alto - suelo, ancho, suelo))
    dibujar_pajaro()

    if estado == "menu":
        texto("FLAPPY BIRD", 44, ancho // 2, 130, amarillo)
        texto("ESPACIO para jugar", 22, ancho // 2, 400, blanco)
        texto("Record: " + str(record), 20, ancho // 2, 460, blanco)
    elif estado == "jugando":
        texto(str(puntos), 54, ancho // 2, 70, blanco)
    elif estado == "muerto":
        texto("GAME OVER", 38, ancho // 2, 200, rojo)
        texto("Puntos: " + str(puntos), 28, ancho // 2, 260, blanco)
        texto("ESPACIO para reintentar", 18, ancho // 2, 340, blanco)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
