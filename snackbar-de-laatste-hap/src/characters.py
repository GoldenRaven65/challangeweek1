import random

characters = [
    {
        "name": "Morana Mane",
        "appearance": (
            "Een vrouw van ongeveer 1.80 meter met lang rood haar komt binnen. "
            "Ze bekijkt het menu en vraagt of de keuken nog open is. "
            "In het raam achter haar zie je de toonbank, de lampen en jezelf. "
            "haar spiegelbeeld daarintegen is nergens te bekennen."
        ),
        "anomaly": True
    },
    {
        "name": "Jack Jastan",
        "appearance": (
            "Een man komt binnen met een brede glimlach en doet een dansje voor de kassa. "
            "Zijn schoenen piepen over de vloer. Hij wacht even op je reactie. "
            "'Bruiloft', zegt hij, terwijl hij zijn stropdas losmaakt. "
            "'Hebben jullie nog iets met heel veel kaas?'"
        ),
        "anomaly": False
    },
    {
        "name": "Elisa Elsbeth",
        "appearance": (
            "Een vrouw in een veel te grote regenjas trekt de deur achter zich dicht. "
            "Haar mascara is uitgelopen. Ze kijkt steeds achterom. "
            "Terwijl ze muntjes uit haar zak haalt, telt ze zachtjes mee. "
            "'Doe toch maar eentje. Een kleine.'"
        ),
        "anomaly": False
    },
    {
        "name": "Simon Slik",
        "appearance": (
            "Een man in een keurig pak legt wat muntgeld op de toonbank. "
            "'Een broodje kroket, alsjeblieft.' "
            "Hij glimlacht met gesloten lippen. Je kijkt naar zijn mond wanneer hij verder praat. "
            "'Werk je hier helemaal alleen?' antwoord hij met gesloten lippen."
        ),
        "anomaly": True
    },
    {
        "name": "Mevrouw Vos",
        "appearance": (
            "Een oudere vrouw zet een lege boodschappentas naast haar voeten. "
            "Ze bestelt twee kroketten en kijkt naar het tafeltje bij het raam. "
            "'Daar zaten we altijd op vrijdag.' "
            "Wanneer je vraagt of ze het mee wil nemen, knikt ze. "
            "'Ja. Thuis eet ik die tweede morgen wel op.'"
        ),
        "anomaly": False
    },
    {
        "name": "Verdinand van Veen",
        "appearance": (
            "Een jongen met een fietshelm onder zijn arm vraagt om een milkshake. "
            "Hij leest de smaken boven je hoofd en krabt aan zijn kin. "
            "Je ziet zijn spiegelbeeld hetzelfde doen in het raam. "
            "Dan laat hij zijn hand zakken. In het raam blijft zijn hand nog even bij zijn gezicht."
        ),
        "anomaly": True
    },
    {
        "name": "Ruben Ralin",
        "appearance": (
            "Een man in werkkleding duwt de deur met zijn schouder open. "
            "Er zitten donkere vegen op zijn mouwen en zijn handen trillen. "
            "Hij laat zijn kleingeld vallen en vloekt terwijl hij het opraapt. "
            "'Twaalf uur dozen gesjouwd. Heb je koffie?' "
            "Zijn telefoon gaat. Op het scherm staat 'Mam'. Hij neemt meteen op."
        ),
        "anomaly": False
    },
    {
        "name": "Dina Den Dekker",
        "appearance": (
            "Een vrouw met een gele haarclip bestelt friet zonder zout. "
            "Ze trekt haar portemonnee uit haar jas en laat een pasje vallen. "
            "Zonder te bukken laat ze haar arm langs haar been zakken. "
            "Je ziet haar vingers de vloer bereiken terwijl haar schouders op dezelfde hoogte blijven. "
            "Ze legt het pasje terug en vraagt hoeveel ze moet betalen."
        ),
        "anomaly": True
    }
]

def get_random_character():
    return random.choice(characters)