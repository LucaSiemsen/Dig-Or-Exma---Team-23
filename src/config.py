#config.py
# ----------------------------------------------------------
#Hier liegen alle "magischen Zahlen": Grid-Größe, Timer,
#ECTS-Ziel und natürlich die Fragen für die Professoren.


from dataclasses import dataclass
from src.questions import questions as raw_questions_data

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


<<<<<<< HEAD
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
=======
# Wir laden die Fragen dynamisch aus questions.py und wandeln sie
# in Question-Objekte um. Die Zuordnung zum Professor erfolgt
# automatisch anhand des Namens
QUESTIONS_BY_PROF: dict[str, list[Question]] = {}

for q_id, data in raw_questions_data.items():
    prof_name = data["prof_name"]
    # Wir machen aus "Prof. Projekt" einen simplen Schlüssel "projekt"
    prof_key = prof_name.split(" ")[-1].lower().replace(".", "")

    if prof_key not in QUESTIONS_BY_PROF:
        QUESTIONS_BY_PROF[prof_key] = []

    # Richtige Antwort für die Erklärung holen
    correct_idx = data["correct"]
    correct_text = data["answers"][correct_idx]

    # Question-Objekt erstellen
    q_obj = Question(
        text=data["question"],
        answers=data["answers"],
        correct=correct_idx,
        explanation=f"Richtig! '{correct_text}' stimmt."
    )
    
    QUESTIONS_BY_PROF[prof_key].append(q_obj)
>>>>>>> 88e6609f0deb9366e5611ed5c29fa84aef7d2f99



# ----------------------------------------------------------
# AUTOMATISCHE PROFESSOREN-GENERIERUNG
# ----------------------------------------------------------
# Wir erstellen die Liste der Gegner dynamisch basierend auf den
# geladenen Fragen. Die Sprites werden rotierend zugewiesen.

PROFESSORS = []
prof_id_counter = 0

<<<<<<< HEAD
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
=======
# Wir haben aktuell 3 Sprites, die wir abwechselnd nutzen
available_sprites = [
    "assets/sprites/prof_math.png",
    "assets/sprites/prof_oop.png",
    "assets/sprites/prof_net.png"
>>>>>>> 88e6609f0deb9366e5611ed5c29fa84aef7d2f99
]

for prof_key, questions_list in QUESTIONS_BY_PROF.items():
    
    # Den Anzeigenamen holen wir uns aus den Rohdaten
    # Wir suchen den ersten Eintrag in den Rohdaten, der zu diesem Key passt
    display_name = "Unbekannter Prof"
    for v in raw_questions_data.values():
        # Wir bauen den Key genauso nach wie oben beim Import
        k = v["prof_name"].split(" ")[-1].lower().replace(".", "")
        if k == prof_key:
            display_name = v["prof_name"]
            break
    
    # Sprite auswählen (0, 1, 2, 0, 1, 2...)
    sprite_path = available_sprites[prof_id_counter % len(available_sprites)]
    
    prof_entry = {
        "id": prof_id_counter,
        "type": prof_key,
        "name": display_name,
        "sprite": sprite_path,
        "questions": questions_list
    }
    
    PROFESSORS.append(prof_entry)
    prof_id_counter += 1

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


