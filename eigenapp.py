#ik ga eerst eigen charechters maken
# dan zorgen dat python random een charechter kiest om te laten zien
# op basis van of het goed of fout is het verhaallijn verder uitschrijven
import random
import time
 
charecters = [
    {
        "name": "Morana Mane",
        "appearence": (
            "Een vrouw van ongeveer 1.80 meter met lang rood haar komt binnen. "
            "Ze bekijkt het menu en vraagt of de keuken nog open is. "
            "In het raam achter haar zie je de toonbank, de lampen en jezelf. "
            "haar spiegelbeeld daarintegen is nergens te bekennen."
        ),
        "anomaly": True
    },
    {
        "name": "Jack Jastan",
        "appearence": (
            "Een man komt binnen met een brede glimlach en doet een dansje voor de kassa. "
            "Zijn schoenen piepen over de vloer. Hij wacht even op je reactie. "
            "'Bruiloft', zegt hij, terwijl hij zijn stropdas losmaakt. "
            "'Hebben jullie nog iets met heel veel kaas?'"
        ),
        "anomaly": False
    },
    {
        "name": "Elisa Elsbeth",
        "appearence": (
            "Een vrouw in een veel te grote regenjas trekt de deur achter zich dicht. "
            "Haar mascara is uitgelopen. Ze kijkt steeds achterom. "
            "Terwijl ze muntjes uit haar zak haalt, telt ze zachtjes mee. "
            "'Doe toch maar eentje. Een kleine.'"
        ),
        "anomaly": False
    },
    {
        "name": "Simon Slik",
        "appearence": (
            "Een man in een keurig pak legt wat muntgeld op de toonbank. "
            "'Een broodje kroket, alsjeblieft.' "
            "Hij glimlacht met gesloten lippen. Je kijkt naar zijn mond wanneer hij verder praat. "
            "'Werk je hier helemaal alleen?' antwoord hij met gesloten lippen."
        ),
        "anomaly": True
    },
    {
        "name": "Mevrouw Vos",
        "appearence": (
            "Een oudere vrouw zet een lege boodschappentas naast haar voeten. "
            "Ze bestelt twee kroketten en kijkt naar het tafeltje bij het raam. "
            "'Daar zaten we altijd op vrijdag.' "
            "Wanneer je vraagt of ze het mee wil nemen, knikt ze. "
            "'Ja. Thuis eet ik die tweede morgen wel op.'"
        ),
        "anomaly": False
    },
    {
        "name": "verdinand van Veen",
        "appearence": (
            "Een jongen met een fietshelm onder zijn arm vraagt om een milkshake. "
            "Hij leest de smaken boven je hoofd en krabt aan zijn kin. "
            "Je ziet zijn spiegelbeeld hetzelfde doen in het raam. "
            "Dan laat hij zijn hand zakken. In het raam blijft zijn hand nog even bij zijn gezicht."
        ),
        "anomaly": True
    },
    {
        "name": "Ruben Ralin",
        "appearence": (
            "Een man in werkkleding duwt de deur met zijn schouder open. "
            "Er zitten donkere vegen op zijn mouwen en zijn handen trillen. "
            "Hij laat zijn kleingeld vallen en vloekt terwijl hij het opraapt. "
            "'Twaalf uur dozen gesjouwd. Heb je koffie?' "
            "Zijn telefoon gaat. Op het scherm staat 'Mam'. Hij neemt meteen op."
        ),
        "anomaly": False
    },
    {
        "name": "dina Den Dekker",
        "appearence": (
            "Een vrouw met een gele haarclip bestelt friet zonder zout. "
            "Ze trekt haar portemonnee uit haar jas en laat een pasje vallen. "
            "Zonder te bukken laat ze haar arm langs haar been zakken. "
            "Je ziet haar vingers de vloer bereiken terwijl haar schouders op dezelfde hoogte blijven. "
            "Ze legt het pasje terug en vraagt hoeveel ze moet betalen."
        ),
        "anomaly": True
    }
]
#python heeft nu de charecters opgeslagen  nu ga ik het random maken
charecter = random.choice(charecters)
def typ_tekst(tekst):
    for letter in tekst:
        print(letter, end="", flush=True)
        time.sleep(0.05)
    print()
 
username:str = input("Pick a username ")
typ_tekst("[23:54] — Snackbar De Laatste Hap")
typ_tekst("De frituur sist. Buiten staat niemand, maar het lampje van de deurbel knippert.")
typ_tekst('Collega: "Daar ben je. Je schort ligt achter de kassa."')
typ_tekst('Jij: "Zou jij niet blijven tot twee?"')
typ_tekst("Ze trekt haar jas aan... binnenstebuiten. Ze laat hem zo.")
typ_tekst("Ja. Sorry. Ik moet echt naar huis")
typ_tekst("[23:55] Collega: “De vriezer is aangevuld. De kassa telt vanzelf. \n\
En de achterdeur moet op slot blijven.”")
typ_tekst("Jij: “Oké. Verder nog iets?”")
typ_tekst("Ze kijkt langs je heen, naar het raam.")
time.sleep(1)
typ_tekst("Collega: “Er komen hier ’s nachts soms vreemde klanten.")
typ_tekst("Jij: “Vreemd als in dronken?”")
typ_tekst("Collega: “Kijk goed voordat je iemand helpt. Naar hun gezicht. Hoe ze bewegen. Het raam achter ze.”")
typ_tekst("Jij: “Waarom het raam?”")
typ_tekst("ze stopt met schrijven.")
typ_tekst("Collega: “Daar kun je soms iets zien wat je aan de balie mist.”")
typ_tekst("[23:58] Ze loopt gehaast naar de uitgang")
typ_tekst('jij: "Wacht! en als er iets niet klopt?"')
typ_tekst(f'"dan bedien je ze niet {username}"')
typ_tekst('jij: "Is dit een grap?!?"')
typ_tekst('Collega "dat dacht ik mijn eerste nacht ook"')
typ_tekst("De deur valt dicht voordat je kunt antwoorden.")
typ_tekst("je bekijkt de kassabon:")
typ_tekst("Je dienst eindigt om 06:00. Als ik terugkom... Ik heb mijn eten al gehad")
time.sleep(2)
def behandel_klant(charecter):
    while True:
        keuze = input("Wil je deze klant bedienen? (ja/nee) ")
        if keuze == "ja":
            if charecter["anomaly"] == True:
                typ_tekst("De glimlach van de klant wordt onnatuurlijk breed.")
                typ_tekst("Voordat je achteruit kunt stappen, grijpt het monster je.")
                typ_tekst("Je wordt opgegeten. Je nachtdienst is voorbij.")
                break
            else:
                typ_tekst("Je helpt de klant. Die vertrekt tevreden.")
                break
        elif keuze == "nee":
            if charecter["anomaly"] == True:
                typ_tekst("De klant staart je aan. Even beweegt niemand.")
                typ_tekst("Dan verdwijnt de glimlach en loopt het monster langzaam naar buiten.")
                typ_tekst("Je hebt het monster geweigerd. Voorlopig ben je veilig.")
                break
            else:
                typ_tekst("de klant spuugt in je gezicht en loopt vervolgens woedend de snackbar uit")
                break
        else:
            typ_tekst("Vul ja of nee in.")
# ik wil later hier toevoegen dan de speler de intro kan skippen en direct kan spelen maar weet nog niet hoe
typ_tekst("[00:00] — Nachtdienst begonnen")
typ_tekst("Je legt de bon naast de kassa.")
typ_tekst("Dan gaat de deurbel.")
typ_tekst(charecter["name"])
typ_tekst(charecter["appearence"])
behandel_klant(charecter)
 
deur_keuze = input("Doe je de achterdeur open? (ja/nee): ")
while True:
    if deur_keuze == "ja":
        typ_tekst("Je draait het slot om.")
        typ_tekst("De deur wordt tegen je aan geduwd.")
        typ_tekst("Buiten staat iets met de stem van je collega.")
        break
 
    elif deur_keuze == "nee":
        typ_tekst("Je blijft achter de toonbank staan.")
        typ_tekst('De stem vraagt: "Je laat me toch niet buiten staan?"')
        time.sleep(2)
        typ_tekst("Je antwoordt niet. Uiteindelijk stopt het kloppen.")
        break
    else:
        typ_tekst("Vul ja of nee in.")
        break
 