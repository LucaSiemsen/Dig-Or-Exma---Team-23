#config.py
# ----------------------------------------------------------
#Hier liegen alle "magischen Zahlen": Grid-Größe, Timer,
#ECTS-Ziel und natürlich die Fragen für die Professoren.


from dataclasses import dataclass

#Spielfeld-Konfiguration 
#Das Verhältnis Muss! 5:3 sein
GRID_COLS = 15        #wie viele Kacheln breit
GRID_ROWS = 9        #wie viele Kacheln hoch

#Abstand zum Bildschirmrand (in Kacheln), damit alles zentriert ist
GRID_MARGIN_X_TILES = 2
GRID_MARGIN_Y_TILES = 2

#BAföG-Timer (pro Level)
BAFOEG_TIME_SECONDS = 60.0

#Wie viele ECTS brauche ich, um das Level zu bestehen?
REQUIRED_ECTS = 5

WHITE = (255, 255, 255)



@dataclass #wir benutzen Dataclass, um uns Schreibarbeit zu sparen und den Code übersichtlicher zu machen
class Question:
    text: str
    answers: list[str]   #Liste mit Antwortmöglichkeiten
    correct: int         #Index in der answers-Liste (0, 1, 2, ...)
    explanation: str     #Erklärung, die nach der Antwort angezeigt wird


#Fragen nach Professor-Typ sortiert.
#Die type-Strings ("math", "oop", "net") benutzen wir auch in PROFESSORS
QUESTIONS_BY_PROF: dict[str, list[Question]] = {
    "math": [
        Question(
            text="Wofür steht das große O in der O-Notation?",
            answers=[
                "Obergrenze des Laufzeitwachstums",
                "Optimale Laufzeit",
                "Oszillierende Laufzeit",
            ],
            correct=0,
            explanation="Big-O beschreibt die asymptotische Obergrenze des Wachstumsverhaltens.",
        ),
        Question(
            text="Was ist 2^10?",
            answers=["512", "1024", "2048"],
            correct=1,
            explanation="2^10 = 1024, deshalb sind so viele Größen in der Informatik Vielfache von 1024.",
        ),
    ],
    "oop": [
        Question(
            text="Welche Aussage beschreibt Kapselung (Encapsulation) am besten?",
            answers=[
                "Mehrere Klassen in einer Datei speichern",
                "Innere Details verstecken und nur ein Interface anbieten",
                "Code in möglichst viele Funktionen aufteilen",
            ],
            correct=1,
            explanation="Kapselung versteckt Implementierungsdetails hinter einer klaren Schnittstelle.",
        ),
        Question(
            text="Was ist in OOP eine Klasse?",
            answers=[
                "Eine einzelne Variable",
                "Ein Objekt zur Laufzeit",
                "Eine Blaupause für Objekte",
            ],
            correct=2,
            explanation="Eine Klasse ist eine Art Bauplan für Objekte (Instanzen).",
        ),
    ],
    "net": [
        Question(
            text="Welches Protokoll wird typischerweise für Webseiten verwendet?",
            answers=["HTTP", "FTP", "SMTP"],
            correct=0,
            explanation="HTTP (oder HTTPS) ist die Basis für den Austausch von Webseiten.",
        ),
        Question(
            text="Was ist ein Port in der Netzwerktechnik?",
            answers=[
                "Ein physisches LAN-Kabel",
                "Eine logische Endpunktnummer für Verbindungen",
                "Die Geschwindigkeit einer Verbindung",
            ],
            correct=1,
            explanation="Ein Port identifiziert einen logischen Endpunkt auf einem Rechner (z.B. 80 für HTTP).",
        ),
    ],
}



# Professoren-Konfiguration (wird vom Level geladen)
# Jeder Prof hat:
#   - id:        nur zur Not, falls man später gezielt auswählen will
#   - type:      Schlüssel für QUESTIONS_BY_PROF (muss passen!)
#   - name:      Anzeige im HUD / bei Fragen
#   - sprite:    Pfad zu deinem PNG im assets/sprites Ordner


PROFESSORS = [
    {
        "id": 0,
        "type": "math",                            #muss zu QUESTIONS_BY_PROF["math"] passen
        "name": "Prof. Ada (Mathe)",
        "sprite": "assets/sprites/prof_math.png",
        "questions": QUESTIONS_BY_PROF["math"],
    },
    {
        "id": 1,
        "type": "oop",                             #muss zu QUESTIONS_BY_PROF["oop"] passen
        "name": "Prof. Byte (OOP)",
        "sprite": "assets/sprites/prof_oop.png",
        "questions": QUESTIONS_BY_PROF["oop"],
    },
    {
        "id": 2,
        "type": "net",                             #muss zu QUESTIONS_BY_PROF["net"] passen
        "name": "Prof. Quantum (Netzwerke)",
        "sprite": "assets/sprites/prof_net.png",
        "questions": QUESTIONS_BY_PROF["net"],
    },
]

LEVELS = [
    # Level 1: 2 Professoren frei, 2 ECTS, 1 Pizza
    {"ects": 2, "pizzas": 1, "prof_count": 2, "guard_mode": False},

    # Level 2: 2 Professoren, einer “bewacht” ein ECTS, 2 ECTS, 2 Pizzen
    {"ects": 2, "pizzas": 2, "prof_count": 2, "guard_mode": True},

    # Level 3 (später): 3 ECTS nahe Ecken, Radius-Logik
    {"ects": 3, "pizzas": 3, "prof_count": 3, "guard_mode": False},

    # Level 4 (später): 3 ECTS, 2 nahe beieinander, mehr Pizzen
    {"ects": 3, "pizzas": 4, "prof_count": 3, "guard_mode": False},
]
