import random
from pathlib import Path

import pygame

from characters import CHARACTERS, Character


YES_ANSWERS = {"ja", "j", "yes", "y"}
NO_ANSWERS = {"nee", "n", "no"}


class Game:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 26)
        self.username = ""
        self.background = self.load_background()

        self.characters = CHARACTERS
        self.remaining_characters = list(self.characters)
        self.current_character = self.take_next_character()
        self.message = "Wil je deze klant bedienen? Typ ja of nee en druk op Enter."
        self.visible_appearance = ""
        self.visible_message = ""
        self.typing_speed = self.settings.TYPING_SPEED
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
        self.night_event_active = False
        self.night_event_lines = []
        self.night_event_index = 0
        self.night_event_visible = ""
        self.night_event_timer = 0
        self.night_event_waiting_choice = False
        self.night_event_answer = ""
        self.night_event_choice_completed = False

        self.start_typing(self.current_character.appearance, self.message)

    def load_background(self):
        image_path = (
            Path(__file__).resolve().parent.parent
            / "exec-4ab69568-c07e-47c0-92c5-956f14df3e1d.png"
        )
        try:
            image = pygame.image.load(image_path).convert()
            return pygame.transform.smoothscale(
                image,
                (self.settings.WIDTH, self.settings.HEIGHT),
            )
        except (FileNotFoundError, pygame.error):
            return None

    def draw_background(self):
        self.screen.fill(self.settings.BACKGROUND_COLOR)
        if self.background is None:
            return

        self.screen.blit(self.background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        self.screen.blit(overlay, (0, 0))

    def start_typing(self, appearance, message):
        self.display_appearance = appearance
        self.message = message
        self.visible_appearance = ""
        self.visible_message = ""
        self.typing_timer = 0

    def update_typing(self):
        if self.typing_timer < self.typing_speed:
            self.typing_timer += 1000 / self.settings.FPS
            return

        self.typing_timer = 0
        if len(self.visible_appearance) < len(self.display_appearance):
            next_index = len(self.visible_appearance) + 1
            self.visible_appearance = self.display_appearance[:next_index]
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

    def start_night_event(self):
        self.night_event_active = True
        self.night_event_lines = [
            "Je telefoon trilt. Je collega belt.",
            '“Luister. Ik ben mijn telefoon vergeten. Maar als iemand—”',
            "Drie harde klappen tegen de achterdeur.",
            'Achter de deur: “Doe open! Ik ben het!”',
            'Door de telefoon fluistert diezelfde stem: “Niet opendoen.”',
            "De deurklink gaat langzaam omlaag.",
        ]
        self.night_event_index = 0
        self.night_event_visible = ""
        self.night_event_timer = 0
        self.night_event_waiting_choice = False
        self.night_event_answer = ""
        self.night_event_choice_completed = False

    def update_night_event(self):
        if self.night_event_waiting_choice:
            return

        if self.night_event_index >= len(self.night_event_lines):
            self.night_event_waiting_choice = True
            return

        if self.night_event_timer < self.typing_speed:
            self.night_event_timer += 1000 / self.settings.FPS
            return

        self.night_event_timer = 0
        line = self.night_event_lines[self.night_event_index]
        next_index = len(self.night_event_visible) + 1
        self.night_event_visible = line[:next_index]

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

    def take_next_character(self) -> Character:
        character_index = random.randrange(len(self.remaining_characters))
        return self.remaining_characters.pop(character_index)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.night_event_active:
            self.handle_night_event(event)
            return

        if self.work_finished:
            if event.key == pygame.K_ESCAPE:
                self.cutscene_index = len(self.cutscene_lines)
                self.cutscene_visible = ""
                return

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
            if not self.remaining_characters:
                return

            self.current_character = self.take_next_character()
            self.message = "Wil je deze klant bedienen? Typ ja of nee en druk op Enter."
            self.answer = ""
            self.start_typing(self.current_character.appearance, self.message)
            self.finished = False
            return

        if self.finished:
            return

        if event.key == pygame.K_BACKSPACE:
            self.answer = self.answer[:-1]
            return

        if event.key == pygame.K_RETURN:
            choice = self.answer.strip().lower()
            if choice in YES_ANSWERS:
                self.answer = ""
                self.choose_answer(True)
            elif choice in NO_ANSWERS:
                self.answer = ""
                self.choose_answer(False)
            return

        if event.unicode.isalpha() and len(self.answer) < 3:
            self.answer += event.unicode.lower()

    def handle_night_event(self, event):
        if self.night_event_waiting_choice:
            if event.key == pygame.K_BACKSPACE:
                self.night_event_answer = self.night_event_answer[:-1]
            elif event.key == pygame.K_RETURN:
                choice = self.night_event_answer.strip().lower()
                if choice in YES_ANSWERS:
                    self.finish_night_event(
                        [
                            "Je draait het slot om. Je collega glipt naar binnen en gooit de deur dicht.",
                            "“Waarom deed je open?! De deur moet op slot blijven!!!”",
                            "Dan ziet ze je telefoon.",
                            "“Met wie bel je?”",
                            "De verbinding wordt verbroken.",
                        ]
                    )
                elif choice in NO_ANSWERS:
                    self.finish_night_event(
                        [
                            "Je hoort een sleutel in het slot. Je collega stapt binnen.",
                            "“Goed zo. Jij overleeft het wel,” lacht ze.",
                            "Ze pakt haar telefoon van onder de toonbank.",
                            "Jouw telefoon ligt nog tegen je oor. Je hoort iemand ademhalen.",
                            "“Hup, weer aan het werk.”",
                        ]
                    )
            elif event.unicode.isalpha() and len(self.night_event_answer) < 3:
                self.night_event_answer += event.unicode.lower()
            return

        if event.key not in (pygame.K_RETURN, pygame.K_SPACE):
            return

        line = self.night_event_lines[self.night_event_index]
        if len(self.night_event_visible) < len(line):
            self.night_event_visible = line
            return

        self.night_event_index += 1
        self.night_event_visible = ""
        self.night_event_timer = 0
        if self.night_event_index >= len(self.night_event_lines):
            if self.night_event_choice_completed:
                self.night_event_active = False
                self.finished = True
            else:
                self.night_event_waiting_choice = True

    def finish_night_event(self, lines):
        self.night_event_lines.extend(lines)
        self.night_event_answer = ""
        self.night_event_choice_completed = True
        self.night_event_waiting_choice = False
        self.night_event_index = len(self.night_event_lines) - len(lines)
        self.night_event_visible = ""
        self.night_event_timer = 0

    def choose_answer(self, serves_customer):
        if serves_customer:
            if self.current_character.anomaly:
                self.message = "Je hebt het monster bediend. Je bent opgegeten."
            else:
                self.message = "Je helpt de klant. Die vertrekt tevreden."
            self.finished = True
        else:
            if self.current_character.anomaly:
                self.message = "Je weigert het monster. Voorlopig ben je veilig."
            else:
                self.message = "De klant wordt boos en loopt weg."
            self.finished = True

        self.customers_completed += 1
        if self.customers_completed == 1:
            self.start_night_event()
            return

        self.current_hour = min(
            6,
            self.customers_completed * 6 // len(self.characters),
        )

        if not self.remaining_characters:
            self.current_hour = 6
            self.start_cutscene()
            return

        self.visible_message = ""
        self.typing_timer = 0

    def update(self):
        self.clock.tick(self.settings.FPS)
        if self.work_finished:
            self.update_cutscene()
        elif self.night_event_active:
            self.update_night_event()
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
        self.draw_background()

        if self.work_finished:
            self.draw_cutscene()
            return

        if self.night_event_active:
            self.draw_night_event()
            return

        title = self.font.render(
            f"[{self.current_hour:02d}:00] — Nachtdienst",
            True,
            self.settings.ACCENT_COLOR,
        )
        self.screen.blit(title, (40, 35))

        y = 110
        name = self.font.render(
            self.current_character.name,
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

    def draw_night_event(self):
        title = self.font.render(
            "[00:00] — Achterdeur",
            True,
            self.settings.ACCENT_COLOR,
        )
        self.screen.blit(title, (40, 35))

        self.draw_wrapped_text(
            self.night_event_visible,
            40,
            120,
            self.settings.WIDTH - 80,
            self.small_font,
        )

        if self.night_event_waiting_choice:
            instruction = (
                f"Doe je de achterdeur open? (ja/nee): {self.night_event_answer}"
            )
            bottom = self.small_font.render(instruction, True, self.settings.TEXT_COLOR)
            self.screen.blit(bottom, (40, self.settings.HEIGHT - 55))
        elif self.night_event_index < len(self.night_event_lines):
            line = self.night_event_lines[self.night_event_index]
            if len(self.night_event_visible) == len(line):
                instruction = "Druk op Enter om verder te gaan"
                bottom = self.small_font.render(
                    instruction,
                    True,
                    self.settings.ACCENT_COLOR,
                )
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