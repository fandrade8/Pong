import random
import sys
import pygame
from pygame.locals import *
from settings import Settings


def draw_paddle(paddle, screen):
    settings = Settings()

    if paddle.bottom > settings.window_height - settings.line_thickness:
        paddle.bottom = settings.window_height - settings.line_thickness

    elif paddle.top < settings.line_thickness:
        paddle.top = settings.line_thickness

    pygame.draw.rect(screen, settings.wht, paddle)


def draw_ball(ball, screen):
    settings = Settings()

    pygame.draw.rect(screen, settings.wht, ball)


def arena(screen):
    settings = Settings()

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, settings.wht,
                     ((0, 0), (settings.window_width, settings.window_height)),
                     settings.line_thickness * 2)
    pygame.draw.line(screen, settings.wht, ((settings.window_width / 2), 0),
                     ((settings.window_width / 2), settings.window_height),
                     (settings.line_thickness // 4))


def ball_movement(ball, ball_dir_x, ball_dir_y):
    ball.x += ball_dir_x
    ball.y += ball_dir_y
    return ball


def edge_collision(ball, ball_dir_x, ball_dir_y):
    settings = Settings()

    if ball.top == settings.line_thickness or ball.bottom == (settings.window_height - settings.line_thickness):
        ball_dir_y = ball_dir_y * -1
    if ball.left == settings.line_thickness or ball.right == (settings.window_width - settings.line_thickness):
        ball_dir_x = ball_dir_x * -1
    return ball_dir_x, ball_dir_y


def ai(ball, ball_dir_x, paddle2):
    st = Settings()

    if ball_dir_x == -1:
        if paddle2.centery < (st.window_height/2):
            paddle2.y += 1
        elif paddle2.centery > (st.window_height/2):
            paddle2.y -= 1

    elif ball_dir_x == 1:
        if paddle2.centery < ball.y:
            paddle2.y += 1
        else:
            paddle2.y -= 1

    return paddle2


def ball_collision(ball, paddle1, paddle2, ball_dir_x):
    if ball_dir_x == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ball_dir_x == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1


def get_score(paddle1, ball, score, ball_dir_x):
    st = Settings()

    if ball.left == st.line_thickness:
        return 0

    elif ball_dir_x == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score

    elif ball.right == st.window_width - st.line_thickness:
        score += 5

    else:
        return score


def display_score(score, screen):
    st = Settings()

    resultSurf = BASICFONT.render("Score = %s" % score, True, st.wht)
    result_Rect = resultSurf.get_rect()
    result_Rect.topleft = (st.window_width - 150, 25)
    screen.blit(resultSurf, result_Rect)


def main():
    pygame.init()
    settings = Settings()
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    pygame.display.set_caption("Pong")

    ball_x = settings.window_width / 2 - settings.line_thickness / 2
    ball_y = settings.window_height / 2 - settings.line_thickness / 2
    p1_pos = (settings.window_height - settings.paddle_size) / 2
    p2_pos = (settings.window_height - settings.paddle_size) / 2
    score = 0

    paddle1 = pygame.Rect(settings.paddle_offset, p1_pos, settings.line_thickness, settings.paddle_size)
    paddle2 = pygame.Rect(settings.window_width - settings.paddle_offset - settings.line_thickness, p2_pos,
                          settings.line_thickness, settings.paddle_size)
    ball = pygame.Rect(ball_x, ball_y, settings.line_thickness, settings.line_thickness)

    ball_dir_x = -1
    ball_dir_y = -1

    arena(screen)
    draw_paddle(paddle1, screen)
    draw_paddle(paddle2, screen)
    draw_ball(ball, screen)

    pygame.mouse.set_visible(0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                paddle1.y = mouse_y

        arena(screen)
        draw_paddle(paddle1, screen)
        draw_paddle(paddle2, screen)
        draw_ball(ball, screen)

        ball = ball_movement(ball, ball_dir_x, ball_dir_y)
        ball_dir_x, ball_dir_y = edge_collision(ball, ball_dir_x, ball_dir_y)
        score = get_score(paddle1, ball, score, ball_dir_x)
        ball_dir_x = ball_dir_x * ball_collision(ball, paddle1, paddle2, ball_dir_x)
        paddle2 = ai(ball, ball_dir_x, paddle2)

        display_score(score, screen)

        pygame.display.update()
        fps_clock.tick(settings.FPS)


if __name__ == "__main__":
    main()

