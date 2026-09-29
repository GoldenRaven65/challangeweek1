import os
import random
import math
import struct
import tempfile
import tkinter as tk
import wave
from tkinter import messagebox

try:
    import winsound
except ImportError:
    winsound = None


# Lijst met personages en hun bijbehorende bestellingen.
# Elk personage heeft een beschrijving, een vlag voor afwijkend gedrag en een order.
characters = [
    {"name": "Mira Vale", "appearance": "Kort zwart haar en een blauwe jas met vreemde symbolen", "anomaly": True, "order": "Een frikandel speciaal zonder frikandel, maar wel met drie staafjes mayo."},
    {"name": "Jonas Reed", "appearance": "Lang en breedgeschouderd, met een bruine baard en één grote handschoen", "anomaly": False, "order": "Een grote friet met mayo en een kroket."},
    {"name": "Elara Finch", "appearance": "Krullend rood haar, een ronde bril en een opgelapte jas", "anomaly": True, "order": "Een kapsalon, maar alle lagen moeten naast elkaar in aparte bakjes liggen."},
    {"name": "Theo Marsh", "appearance": "Een gele regenjas, drie verschillende sokken en een papieren hoed", "anomaly": True, "order": "Een kaassouffle gevuld met friet en een klein parapluutje."},
    {"name": "Sana Okafor", "appearance": "Donker gevlochten haar, een rafelige sjaal en een zilveren ketting", "anomaly": False, "order": "Een broodje kipburger met sla en knoflooksaus."},
    {"name": "Bram Hollow", "appearance": "Grote lichaamsbouw, kaal hoofd, een wenkbrauw met litteken en een oud harnas", "anomaly": False, "order": "Een dubbele cheeseburger met een kleine friet."},
    {"name": "Lydia Snow", "appearance": "Wit haar, felblauwe ogen en een gerepareerde paarse jurk", "anomaly": True, "order": "Een ijsje dat warm moet zijn, met mosterd als topping."},
    {"name": "Kai Mercer", "appearance": "Slordig blond haar, versleten sneakers en een rugzak vol kaarten", "anomaly": False, "order": "Een mexicano met pindasaus en een blikje cola."},
    {"name": "Nora Bell", "appearance": "Warme glimlach, met bloem bestoven haar en een schort vol sleutels", "anomaly": True, "order": "Een patatje oorlog zonder patat, graag in een schoenendoos."},
    {"name": "Orin Glass", "appearance": "Zilverkleurig haar, smalle ogen en een zwarte mantel met verschroeide randen", "anomaly": True, "order": "Een milkshake met frietsaus, extra heet, en zonder beker."},
    {"name": "Pia Wren", "appearance": "Groen bobkapsel, veel te grote laarzen en een jas vol speldjes", "anomaly": False, "order": "Een berenhap met pindasaus en een kleine cola."},
    {"name": "Daan Voss", "appearance": "Netjes donker haar, een ronde hoed en een notitieboek vol schetsen", "anomaly": False, "order": "Een portie friet met ketchup en een kipcorn."},
    {"name": "Iris Crowe", "appearance": "Lange zilveren vlecht, verschillende oorbellen en een fluwelen jas", "anomaly": True, "order": "Een frikandel die eerst drie rondjes om de snackbar moet lopen."},
    {"name": "Milo Hart", "appearance": "Sproeten, een gestreepte trui en felrode koptelefoon", "anomaly": False, "order": "Een cheeseburger zonder kaas en een medium friet."},
    {"name": "Fenna Rook", "appearance": "Zijkant van het hoofd kaalgeschoren, gele sjaal en laarzen met sterren", "anomaly": True, "order": "Een softijsje met augurken, maar alleen de schaduw ervan."},
    {"name": "Ravi Stone", "appearance": "Krullend zwart haar, leren handschoenen en een rugzak vol snacks", "anomaly": False, "order": "Een broodje mexicano met curry en uitjes."},
    {"name": "June Alder", "appearance": "Lichtblauw haar, een lange jas en een zakhorloge", "anomaly": True, "order": "Een portie friet die achteruit gebakken en bevroren geserveerd wordt."},
    {"name": "Sven Pike", "appearance": "Stekelig bruin haar, een sportshirt en één neon veter", "anomaly": False, "order": "Een bamischijf met chilisaus en een blikje sinas."},
    {"name": "Mae Rowan", "appearance": "Warme bruine krullen, een bril met stervormige glazen en een rode regenjas", "anomaly": True, "order": "Een hamburger zonder broodje, vlees of groente, maar wel met extra kaas."},
    {"name": "Tobias Quill", "appearance": "Lang en dun, met een witte sjaal en met inkt bevlekte vingers", "anomaly": False, "order": "Een grote friet speciaal en een kaassouffle."},
]


def create_audio_file(path, duration, sample_rate, sample_function):
    """Create a small mono WAV file from a sample-producing function."""
    sample_count = int(duration * sample_rate)
    with wave.open(path, "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(sample_rate)
        samples = (
            struct.pack("<h", int(max(-1, min(1, sample_function(index / sample_rate))) * 32767))
            for index in range(sample_count)
        )
        audio_file.writeframes(b"".join(samples))


def create_audio_assets():
    """Build the ambient loop and jumpscare sound in the system temp folder."""
    if winsound is None:
        return None, None

    audio_folder = os.path.join(tempfile.gettempdir(), "order_keeper_audio")
    os.makedirs(audio_folder, exist_ok=True)
    music_path = os.path.join(audio_folder, "creepy_music_v3.wav")
    jumpscare_path = os.path.join(audio_folder, "jumpscare_v2.wav")
    sample_rate = 22050

    if not os.path.exists(music_path):
        def ambient_sample(time):
            fade = min(1, 0.25 + time / 1.5, (12 - time) / 1.5)
            drone = 0.16 * math.sin(2 * math.pi * 110 * time)
            melody = 0.22 * math.sin(2 * math.pi * 220 * time)
            melody += 0.16 * math.sin(2 * math.pi * 330 * time)
            melody += 0.12 * math.sin(2 * math.pi * 440 * time)
            pulse = 0.12 * math.sin(2 * math.pi * 2.2 * time) * math.sin(2 * math.pi * 165 * time)
            return max(0, fade) * (drone + melody + pulse)

        create_audio_file(music_path, 12, sample_rate, ambient_sample)

    if not os.path.exists(jumpscare_path):
        def jumpscare_sample(time):
            if time < 0.08:
                return 0
            progress = (time - 0.08) / 0.72
            envelope = min(1, progress * 18) * max(0, 1 - progress)
            frequency = 180 + 900 * progress
            tone = math.sin(2 * math.pi * frequency * time)
            noise = random.uniform(-1, 1)
            return envelope * (0.7 * tone + 0.3 * noise)

        create_audio_file(jumpscare_path, 0.8, sample_rate, jumpscare_sample)

    return music_path, jumpscare_path


# Hoofdklasse van het spel: beheert de spelstatus, User interface en logica.
class OrderKeeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Keeper")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#120d14")
        self.original_geometry = "1280x720"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.music_path, self.jumpscare_path = create_audio_assets()

        self.score = 0
        self.lives = 3
        self.round_number = 0
        self.character = None
        self.order_shown = False

        self.title = tk.Label(root, text="ORDER KEEPER", font=("Arial", 22, "bold"), bg="#120d14", fg="#e8d5c0")
        self.title.pack(pady=(22, 4))
        self.info = tk.Label(root, text="", font=("Arial", 11), bg="#120d14", fg="#c8a28d")
        self.info.pack()

        self.card = tk.Frame(root, bg="#1c141a", highlightbackground="#4d2c35", highlightthickness=2)
        self.card.pack(fill="x", padx=35, pady=20)

        self.round_label = tk.Label(self.card, text="", font=("Arial", 10, "bold"), bg="#1c141a", fg="#d98675")
        self.round_label.pack(pady=(20, 8))
        self.name_label = tk.Label(self.card, text="", font=("Arial", 24, "bold"), bg="#1c141a", fg="#f0e4d8")
        self.name_label.pack()
        self.appearance_label = tk.Label(self.card, text="", font=("Arial", 12), wraplength=400, bg="#1c141a", fg="#d4b7ab")
        self.appearance_label.pack(padx=30, pady=(8, 20))

        self.order_label = tk.Label(self.card, text="Order: nog niet bekeken", font=("Arial", 11, "bold"), bg="#1c141a", fg="#d9a84f")
        self.order_label.pack(pady=(0, 10))
        self.order_button = tk.Button(self.card, text="Bekijk order", command=self.show_order, width=18, bg="#7a4a3a", fg="#f8ead9", relief="flat", pady=7, cursor="hand2")
        self.order_button.pack(pady=(0, 20))

        self.message = tk.Label(root, text="Bekijk eerst de order.", font=("Arial", 11), bg="#120d14", fg="#d7c5b3")
        self.message.pack(pady=(0, 12))

        self.popup_image = None
        self.popup_label = tk.Label(root, bg="#120d14")
        self.popup_label.place_forget()
        self.load_life_loss_image()
        self.start_music()

        buttons = tk.Frame(root, bg="#120d14")
        buttons.pack(fill="x", padx=35)
        self.make_button = tk.Button(buttons, text="Order maken (+5)", command=lambda: self.choose("maken"), state="disabled", bg="#3a4f4c", fg="#f4efe6", relief="flat", pady=10, cursor="hand2")
        self.make_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.send_button = tk.Button(buttons, text="Wegsturen (+3)", command=lambda: self.choose("wegsturen"), state="disabled", bg="#5c2d2c", fg="#f9eee8", relief="flat", pady=10, cursor="hand2")
        self.send_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.next_round()

    # Start een nieuwe ronde met een willekeurig personage en reset de visuele status.
    def next_round(self):
        self.round_number += 1
        self.character = random.choice(characters)
        self.order_shown = False
        self.round_label.config(text=f"RONDE {self.round_number}")
        self.name_label.config(text=self.character["name"])
        self.appearance_label.config(text=self.character["appearance"])
        self.order_label.config(text="Order: nog niet bekeken", fg="#d9a84f")
        self.order_button.config(text="Bekijk order", state="normal", bg="#7a4a3a", fg="#f8ead9")
        self.make_button.config(state="disabled", bg="#3a4f4c", fg="#f4efe6")
        self.send_button.config(state="normal", bg="#5c2d2c", fg="#f9eee8")
        self.message.config(text="Bekijk de order en maak een keuze.", fg="#d7c5b3")
        self.update_info()

    def show_order(self):
        self.order_shown = True
        self.order_label.config(text=f"Order: {self.character['order']}", fg="#b3d2b1")
        self.order_button.config(text="Order bekeken", state="disabled", bg="#5d473f", fg="#f5eadb")
        self.make_button.config(state="normal", bg="#4b6f61", fg="#f2efe8")

    # Controleert de keuze van de speler en bepaalt punten, levens en feedback.
    def choose(self, action):
        if action == "maken":
            points = -10 if self.character["anomaly"] else 5
        else:
            points = 3 if self.character["anomaly"] else -5

        self.score += points
        if points < 0:
            self.lives -= 1
            self.lose_life_effect()
        self.make_button.config(state="disabled")
        self.send_button.config(state="disabled")
        result = "Goed gedaan!" if points > 0 else "Dat was geen goede keuze."
        self.message.config(text=f"{result}  {points:+d} punten", fg="#b9d7c1" if points > 0 else "#e89b80")
        self.update_info()
        if self.lives == 0:
            self.root.after(700, self.game_over)
        else:
            self.root.after(700, self.next_round)

    def update_info(self):
        self.info.config(text=f"Score: {self.score:+d}    Levens: {'♥' * self.lives}   Ronde: {self.round_number}")

    def load_life_loss_image(self):
        image_path = os.path.join(os.path.dirname(__file__), "image.png")
        if not os.path.exists(image_path):
            return
        try:
            self.popup_image = tk.PhotoImage(file=image_path)
            self.popup_label.config(image=self.popup_image)
            self.popup_label.image = self.popup_image
        except tk.TclError:
            self.popup_image = None

    def show_life_loss_image(self):
        if self.popup_image is None:
            return
        self.popup_label.place(relx=0.5, rely=0.5, anchor="center")
        self.popup_label.lift()
        self.root.after(500, self.hide_life_loss_image)

    def hide_life_loss_image(self):
        self.popup_label.place_forget()

    def lose_life_effect(self):
        self.play_jumpscare()
        self.root.configure(bg="#2d1018")
        self.message.config(fg="#f0a39b")
        self.show_life_loss_image()
        self.animate_shake(0)
        self.root.after(180, lambda: self.root.configure(bg="#120d14"))

    def start_music(self):
        if winsound is not None and self.music_path is not None:
            winsound.PlaySound(self.music_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    def play_jumpscare(self):
        if winsound is None or self.jumpscare_path is None:
            self.root.bell()
            return
        winsound.PlaySound(self.jumpscare_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        self.root.after(900, self.start_music)

    def animate_shake(self, step):
        if step >= 4:
            self.root.geometry(self.original_geometry)
            return
        offset = 4 if step % 2 == 0 else -4
        self.root.geometry(f"1280x720{offset:+d}{offset:+d}")
        self.root.after(35, lambda: self.animate_shake(step + 1))

    def close(self):
        if winsound is not None:
            winsound.PlaySound(None, winsound.SND_PURGE)
        self.root.destroy()

    def game_over(self):
        messagebox.showinfo("Spel voorbij", f"Je hebt geen levens meer.\nEindscore: {self.score:+d}")
        self.score = 0
        self.lives = 3
        self.round_number = 0
        self.next_round()


# Start het spel wanneer het bestand rechtstreeks wordt uitgevoerd.
if __name__ == "__main__":
    window = tk.Tk()
    OrderKeeper(window)
    window.mainloop()
