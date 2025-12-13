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



# ----------------------------------------------------------
# AUTOMATISCHE PROFESSOREN-GENERIERUNG
# ----------------------------------------------------------
# Wir erstellen die Liste der Gegner dynamisch basierend auf den
# geladenen Fragen. Die Sprites werden rotierend zugewiesen.

    PROFESSORS = []
    prof_id_counter = 0
# Wir haben aktuell 3 Sprites, die wir abwechselnd nutzen 
    available_sprites = [ "assets/sprites/prof_math.png", "assets/sprites/prof_oop.png", "assets/sprites/prof_net.png" ]
    for prof_key, questions_list in QUESTIONS_BY_PROF.items():
        display_name = ...
        sprite_path = available_sprites[prof_id_counter % len(available_sprites)]

        prof_entry = {
            "id": prof_id_counter,
            "type": prof_key,
            "name": display_name,
            "sprite": sprite_path,
            "questions": questions_list
        }

        # Klausur special
        if prof_key == "klausur":
            prof_entry["sprite"] = "assets/sprites/Prüfung.png"
            prof_entry["hp"] = 3

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


