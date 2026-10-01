import sys
import pygame

from game import Game
from scenes import IntroScene
from settings import Settings


def main():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Snackbar De Laatste Hap")

    game = Game(screen, settings)
    username = ""
    intro = None
    showing_username = True
    showing_intro = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if showing_username and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN and username.strip():
                    game.username = username.strip()
                    intro = IntroScene(game)
                    showing_username = False
                    showing_intro = True
                elif event.unicode.isprintable() and len(username) < 20:
                    username += event.unicode
            elif showing_intro:
                intro.handle_event(event)
            else:
                game.handle_event(event)

        if showing_username:
            screen.fill(settings.BACKGROUND_COLOR)
            title = game.font.render("Welkom bij Snackbar De Laatste Hap", True, settings.ACCENT_COLOR)
            prompt = game.small_font.render("Vul je username in en druk op Enter:", True, settings.TEXT_COLOR)
            name = game.font.render(username, True, settings.TEXT_COLOR)
            screen.blit(title, (40, 170))
            screen.blit(prompt, (40, 250))
            screen.blit(name, (40, 290))
        elif showing_intro:
            intro.update()
            intro.draw()
            if intro.finished:
                showing_intro = False
        else:
            game.update()
            game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()