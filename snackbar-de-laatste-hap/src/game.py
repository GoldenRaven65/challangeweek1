import random
import pygame

from characters import characters


class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)
        self.username = ""

        self.characters = self.load_characters()
        self.current_character = random.choice(self.characters)
        self.message = "Wil je deze klant bedienen? Typ ja of nee en druk op Enter."
        self.visible_appearance = ""
        self.visible_message = ""
        self.typing_speed = 35
        self.typing_timer = 0
        self.answer = ""
        self.finished = False
        self.customers_completed = 0
        self.current_hour = 0
        self.work_finished = False
        self.cutscene_lines = []
        self.cutscene_index = 0
        self.cutscene_visible = ""
        self.cutscene_timer = 0

        self.start_typing(self.current_character["appearance"], self.message)

    def start_typing(self, appearance, message):
        self.current_character["display_appearance"] = appearance
        self.message = message
        self.visible_appearance = ""
        self.visible_message = ""
        self.typing_timer = 0

    def update_typing(self):
        if self.typing_timer < self.typing_speed:
            self.typing_timer += 1000 / self.settings.FPS
            return

        self.typing_timer = 0
        if len(self.visible_appearance) < len(self.current_character["display_appearance"]):
            next_index = len(self.visible_appearance) + 1
            self.visible_appearance = self.current_character["display_appearance"][:next_index]
        elif len(self.visible_message) < len(self.message):
            next_index = len(self.visible_message) + 1
            self.visible_message = self.message[:next_index]

    def start_cutscene(self):
        self.work_finished = True
        self.cutscene_lines = [
            f"[06:00] — Je dienst zit erop, {self.username or 'medewerker'}.",
            "De laatste klant is vertrokken. De snackbar wordt eindelijk stil.",
            "Je kijkt nog een keer naar het raam. Deze keer beweegt je spiegelbeeld precies met je mee.",
            "Buiten begint de ochtend. Je doet het licht uit en draait de deur op slot.",
            "De voordeurbel klinkt nog één keer... hoewel niemand buiten staat.",
            "EINDE VAN DE NACHTDIENST",
        ]
        self.cutscene_index = 0
        self.cutscene_visible = ""
        self.cutscene_timer = 0

    def update_cutscene(self):
        if self.cutscene_index >= len(self.cutscene_lines):
            return

        if self.cutscene_timer < self.typing_speed:
            self.cutscene_timer += 1000 / self.settings.FPS
            return

        self.cutscene_timer = 0
        line = self.cutscene_lines[self.cutscene_index]
        next_index = len(self.cutscene_visible) + 1
        self.cutscene_visible = line[:next_index]

    def load_characters(self):
        return characters

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.work_finished:
            if event.key not in (pygame.K_RETURN, pygame.K_SPACE):
                return

            if self.cutscene_index >= len(self.cutscene_lines):
                return

            line = self.cutscene_lines[self.cutscene_index]
            if len(self.cutscene_visible) < len(line):
                self.cutscene_visible = line
                return

            self.cutscene_index += 1
            self.cutscene_visible = (
                line if self.cutscene_index >= len(self.cutscene_lines) else ""
            )
            self.cutscene_timer = 0
            return

        if event.key == pygame.K_SPACE and self.finished:
            self.current_character = random.choice(self.characters)
            self.message = "Wil je deze klant bedienen? Typ ja of nee en druk op Enter."
            self.answer = ""
            self.start_typing(self.current_character["appearance"], self.message)
            self.finished = False
            return

        if self.finished:
            return

        if event.key == pygame.K_BACKSPACE:
            self.answer = self.answer[:-1]
            return

        if event.key == pygame.K_RETURN:
            choice = self.answer.strip().lower()
            if choice in ("ja", "j", "yes", "y"):
                self.answer = ""
                self.choose_answer(True)
            elif choice in ("nee", "n", "no"):
                self.answer = ""
                self.choose_answer(False)
            return

        if event.unicode.isalpha() and len(self.answer) < 3:
            self.answer += event.unicode.lower()

    def choose_answer(self, serves_customer):
        if serves_customer:
            if self.current_character["anomaly"]:
                self.message = "Je hebt het monster bediend. Je bent opgegeten."
            else:
                self.message = "Je helpt de klant. Die vertrekt tevreden."
            self.finished = True
        else:
            if self.current_character["anomaly"]:
                self.message = "Je weigert het monster. Voorlopig ben je veilig."
            else:
                self.message = "De klant wordt boos en loopt weg."
            self.finished = True

        self.customers_completed += 1
        if self.customers_completed % 3 == 0:
            self.current_hour += 1

        if self.current_hour >= 6:
            self.start_cutscene()
            return

        self.visible_message = ""
        self.typing_timer = 0

    def update(self):
        self.clock.tick(self.settings.FPS)
        if self.work_finished:
            self.update_cutscene()
        else:
            self.update_typing()

    def draw_wrapped_text(self, text, x, y, width, font):
        words = text.split()
        line = ""
        line_height = font.get_height()

        for word in words:
            test_line = f"{line} {word}".strip()
            if font.size(test_line)[0] > width:
                surface = font.render(line, True, self.settings.TEXT_COLOR)
                self.screen.blit(surface, (x, y))
                y += line_height + 8
                line = word
            else:
                line = test_line

        if line:
            surface = font.render(line, True, self.settings.TEXT_COLOR)
            self.screen.blit(surface, (x, y))

        return y + line_height

    def draw(self):
        self.screen.fill(self.settings.BACKGROUND_COLOR)

        if self.work_finished:
            self.draw_cutscene()
            return

        title = self.font.render(
            f"[{self.current_hour:02d}:00] — Nachtdienst",
            True,
            self.settings.ACCENT_COLOR,
        )
        self.screen.blit(title, (40, 35))

        y = 110
        name = self.font.render(
            self.current_character["name"],
            True,
            self.settings.TEXT_COLOR,
        )
        self.screen.blit(name, (40, y))
        y += 55

        y = self.draw_wrapped_text(
            self.visible_appearance,
            40,
            y,
            self.settings.WIDTH - 80,
            self.small_font,
        )

        y += 45
        self.draw_wrapped_text(
            self.visible_message,
            40,
            y,
            self.settings.WIDTH - 80,
            self.small_font,
        )

        if self.finished:
            instruction = "Druk op SPATIE om een nieuwe klant te kiezen."
            color = self.settings.ACCENT_COLOR
        else:
            instruction = f"Typ ja of nee en druk op Enter: {self.answer}"
            color = self.settings.TEXT_COLOR

        bottom = self.small_font.render(instruction, True, color)
        self.screen.blit(bottom, (40, self.settings.HEIGHT - 55))

    def draw_cutscene(self):
        title = self.font.render(
            "[06:00] — Dienst beëindigd",
            True,
            self.settings.ACCENT_COLOR,
        )
        self.screen.blit(title, (40, 35))

        self.draw_wrapped_text(
            self.cutscene_visible,
            40,
            150,
            self.settings.WIDTH - 80,
            self.small_font,
        )

        if self.cutscene_index < len(self.cutscene_lines):
            line = self.cutscene_lines[self.cutscene_index]
            if len(self.cutscene_visible) == len(line):
                instruction = "Druk op Enter om verder te gaan"
                bottom = self.small_font.render(instruction, True, self.settings.ACCENT_COLOR)
                self.screen.blit(bottom, (40, self.settings.HEIGHT - 55))