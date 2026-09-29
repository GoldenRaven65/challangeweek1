import random
import tkinter as tk
from tkinter import messagebox


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


class OrderKeeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Keeper")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#eef2f5")

        self.score = 0
        self.lives = 3
        self.round_number = 0
        self.character = None
        self.order_shown = False

        self.title = tk.Label(root, text="ORDER KEEPER", font=("Arial", 22, "bold"), bg="#eef2f5", fg="#243447")
        self.title.pack(pady=(22, 4))
        self.info = tk.Label(root, text="", font=("Arial", 11), bg="#eef2f5", fg="#536779")
        self.info.pack()

        self.card = tk.Frame(root, bg="white", highlightbackground="#cbd5df", highlightthickness=1)
        self.card.pack(fill="x", padx=35, pady=20)

        self.round_label = tk.Label(self.card, text="", font=("Arial", 10, "bold"), bg="white", fg="#4d8b83")
        self.round_label.pack(pady=(20, 8))
        self.name_label = tk.Label(self.card, text="", font=("Arial", 24, "bold"), bg="white", fg="#243447")
        self.name_label.pack()
        self.appearance_label = tk.Label(self.card, text="", font=("Arial", 12), wraplength=400, bg="white", fg="#536779")
        self.appearance_label.pack(padx=30, pady=(8, 20))

        self.order_label = tk.Label(self.card, text="Order: nog niet bekeken", font=("Arial", 11, "bold"), bg="white", fg="#c28b32")
        self.order_label.pack(pady=(0, 10))
        self.order_button = tk.Button(self.card, text="Bekijk order", command=self.show_order, width=18, bg="#f4cf7a", fg="#243447", relief="flat", pady=7, cursor="hand2")
        self.order_button.pack(pady=(0, 20))

        self.message = tk.Label(root, text="Bekijk eerst de order.", font=("Arial", 11), bg="#eef2f5", fg="#536779")
        self.message.pack(pady=(0, 12))

        buttons = tk.Frame(root, bg="#eef2f5")
        buttons.pack(fill="x", padx=35)
        self.make_button = tk.Button(buttons, text="Order maken (+5)", command=lambda: self.choose("maken"), state="disabled", bg="#4d8b83", fg="white", relief="flat", pady=10, cursor="hand2")
        self.make_button.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.send_button = tk.Button(buttons, text="Wegsturen (+3)", command=lambda: self.choose("wegsturen"), state="disabled", bg="#c26b62", fg="white", relief="flat", pady=10, cursor="hand2")
        self.send_button.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.next_round()

    def next_round(self):
        self.round_number += 1
        self.character = random.choice(characters)
        self.order_shown = False
        self.round_label.config(text=f"RONDE {self.round_number}")
        self.name_label.config(text=self.character["name"])
        self.appearance_label.config(text=self.character["appearance"])
        self.order_label.config(text="Order: nog niet bekeken", fg="#c28b32")
        self.order_button.config(text="Bekijk order", state="normal")
        self.make_button.config(state="disabled")
        self.send_button.config(state="normal")
        self.message.config(text="Bekijk de order en maak een keuze.", fg="#536779")
        self.update_info()

    def show_order(self):
        self.order_shown = True
        self.order_label.config(text=f"Order: {self.character['order']}", fg="#4d8b83")
        self.order_button.config(text="Order bekeken", state="disabled")
        self.make_button.config(state="normal")

    def choose(self, action):
        if action == "maken":
            points = -10 if self.character["anomaly"] else 5
        else:
            points = 3 if self.character["anomaly"] else -5

        self.score += points
        if points < 0:
            self.lives -= 1
        self.make_button.config(state="disabled")
        self.send_button.config(state="disabled")
        result = "Goed gedaan!" if points > 0 else "Dat was geen goede keuze."
        self.message.config(text=f"{result}  {points:+d} punten", fg="#4d8b83" if points > 0 else "#c26b62")
        self.update_info()
        if self.lives == 0:
            self.root.after(700, self.game_over)
        else:
            self.root.after(700, self.next_round)

    def update_info(self):
        self.info.config(text=f"Score: {self.score:+d}    Levens: {'♥' * self.lives}   Ronde: {self.round_number}")

    def game_over(self):
        messagebox.showinfo("Spel voorbij", f"Je hebt geen levens meer.\nEindscore: {self.score:+d}")
        self.score = 0
        self.lives = 3
        self.round_number = 0
        self.next_round()


if __name__ == "__main__":
    window = tk.Tk()
    OrderKeeper(window)
    window.mainloop()
