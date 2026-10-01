import pygame
import pygame

class Scene:
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def draw(self):
        pass

class IntroScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 30)
        self.texts = [
            "[23:54] — Snackbar De Laatste Hap",
            "De frituur sist. Buiten staat niemand, maar het lampje van de deurbel knippert.",
            'Collega: "Daar ben je. Je schort ligt achter de kassa."',
            'Jij: "Zou jij niet blijven tot twee?"',
            "Ze trekt haar jas aan... binnenstebuiten. Ze laat hem zo.",
            "Ja. Sorry. Ik moet echt naar huis",
            "[23:55] Collega: “De vriezer is aangevuld. De kassa telt vanzelf. \n\
            En de achterdeur moet op slot blijven.”",
            "Jij: “Oké. Verder nog iets?”",
            "Ze kijkt langs je heen, naar het raam.",
            "Collega: “Er komen hier ’s nachts soms vreemde klanten.",
            "Jij: “Vreemd als in dronken?”",
            "Collega: “Kijk goed voordat je iemand helpt. Naar hun gezicht. Hoe ze bewegen. Het raam achter ze.”",
            "Jij: “Waarom het raam?”",
            "ze stopt met schrijven.",
            "Collega: “Daar kun je soms iets zien wat je aan de balie mist.”",
            "[23:58] Ze loopt gehaast naar de uitgang",
            'jij: "Wacht! en als er iets niet klopt?"',
            f'"dan bedien je ze niet {getattr(self.game, "username", "collega")}"',
            'jij: "Is dit een grap?!?"',
            'Collega "dat dacht ik mijn eerste nacht ook"',
            "De deur valt dicht voordat je kunt antwoorden.",
            "je bekijkt de kassabon:",
            "Je dienst eindigt om 06:00. Als ik terugkom... Ik heb mijn eten al gehad"  
        ]
        self.current_text_index = 0
        self.visible_text = ""
        self.typing_timer = 0
        self.typing_speed = self.game.typing_speed
        self.finished = False

    def update(self):
        if self.finished or self.current_text_index >= len(self.texts):
            return

        if self.typing_timer < self.typing_speed:
            self.typing_timer += 1000 / self.game.settings.FPS
            return

        self.typing_timer = 0
        next_index = len(self.visible_text) + 1
        self.visible_text = self.texts[self.current_text_index][:next_index]

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key not in (pygame.K_RETURN, pygame.K_SPACE):
            return

        if len(self.visible_text) < len(self.texts[self.current_text_index]):
            self.visible_text = self.texts[self.current_text_index]
            return

        self.current_text_index += 1
        if self.current_text_index >= len(self.texts):
            self.finished = True
            return

        self.visible_text = ""
        self.typing_timer = 0

    def draw_wrapped_text(self, text, x, y, width):
        words = text.split()
        line = ""
        line_height = self.font.get_height()

        for word in words:
            test_line = f"{line} {word}".strip()
            if self.font.size(test_line)[0] > width:
                surface = self.font.render(line, True, (255, 255, 255))
                self.game.screen.blit(surface, (x, y))
                y += line_height + 8
                line = word
            else:
                line = test_line

        if line:
            surface = self.font.render(line, True, (255, 255, 255))
            self.game.screen.blit(surface, (x, y))

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        if self.finished:
            return

        self.draw_wrapped_text(
            self.visible_text,
            40,
            80,
            self.game.settings.WIDTH - 80,
        )

        if len(self.visible_text) == len(self.texts[self.current_text_index]):
            instruction = "Druk op Enter om verder te gaan"
            instruction_surface = self.font.render(instruction, True, (180, 70, 70))
            self.game.screen.blit(
                instruction_surface,
                (40, self.game.settings.HEIGHT - 60),
            )

class CharacterInteractionScene(Scene):
    def __init__(self, game, character):
        super().__init__(game)
        self.character = character

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        character_text = f"{self.character['name']}: {self.character['appearence']}"
        text_surface = self.game.font.render(character_text, True, (255, 255, 255))
        self.game.screen.blit(text_surface, (20, 20))

class SceneManager:
    def __init__(self, game):
        self.game = game
        self.scenes = {
            "intro": IntroScene(game),
            "character_interaction": None
        }
        self.current_scene = "intro"

    def change_scene(self, scene_name, character=None):
        if scene_name == "character_interaction":
            self.scenes[scene_name] = CharacterInteractionScene(self.game, character)
        self.current_scene = scene_name

    def update(self):
        self.scenes[self.current_scene].update()

    def handle_event(self, event):
        scene = self.scenes[self.current_scene]
        if hasattr(scene, "handle_event"):
            scene.handle_event(event)

    def draw(self):
        self.scenes[self.current_scene].draw()