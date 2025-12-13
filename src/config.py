#config.py
# ----------------------------------------------------------
#Hier liegen alle "magischen Zahlen": Grid-Größe, Timer,
#ECTS-Ziel und natürlich die Fragen für die Professoren.


from dataclasses import dataclass

#Spielfeld-Konfiguration 

GRID_COLS = 10          #wie viele Kacheln breit
GRID_ROWS = 10          #wie viele Kacheln hoch

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
"K": [
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
    {
        "id": 3,
        "type": "K",                             #muss zu QUESTIONS_BY_PROF["K"] passen
        "name": "Klausur",
        "sprite": "assets/sprites/Prüfung 1.png",
        "questions": QUESTIONS_BY_PROF["K"],
        "hp" :3 #Klausur hat 3 Fragen
    },
]

LEVELS = [
    # Semester 1
    {"ects": 2, "powerups_total": 1, "prof_count": 2, "guard_mode": False, "hard_prof": False},
    # Semester 2
    {"ects": 2, "powerups_total": 1, "prof_count": 2, "guard_mode": True,  "hard_prof": False},
    # Semester 3
    {"ects": 3, "powerups_total": 2, "prof_count": 3, "guard_mode": False, "hard_prof": True},
    # Semester 4
    {"ects": 3, "powerups_total": 2, "prof_count": 3, "guard_mode": True,  "hard_prof": True},
    # Semester 5
    {"ects": 4, "powerups_total": 3, "prof_count": 4, "guard_mode": False, "hard_prof": True},
    # Semester 6
    {"ects": 4, "powerups_total": 3, "prof_count": 4, "guard_mode": True,  "hard_prof": True},
    # Semester 7
    {"ects": 5, "powerups_total": 4, "prof_count": 5, "guard_mode": True,  "hard_prof": True},
]


