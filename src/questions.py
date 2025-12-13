# ============================================================
# questions.py – Alle Professorfragen
# Dient als "Datenbank" für alle Quiz-Inhalte.
# Verwendung eines Dictionarys ermöglicht schnellen Zugriff über die ID.

# Author/Verantwortlich: Aaron Lehrke (937367)

# ============================================================



questions = {
    # --- Projektmanagement & Organisation ---
    1: {
        "prof_name": "Prof. Projekt",
        "question": "Was gehört zum 'Magischen Dreieck' im Projektmanagement?",
        "answers": [
            "Kosten, Zeit, Qualität",      # Index 0 (Korrekt)
            "Spaß, Freizeit, Gehalt",      # Index 1
            "Hardware, Software, Maus",    # Index 2
            "Kaffee, Pizza, Mate"          # Index 3
        ],
        "correct": 0 # "Kosten, Zeit, Qualität" steht an 1. Stelle (Index 0)
    },
    2: {
        "prof_name": "Dr. Plan",
        "question": "Was ist ein 'Meilenstein' in einem Projekt?",
        "answers": [
            "Ein Stein am Wegesrand",      # Index 0
            "Ein wichtiges Zwischenziel",  # Index 1 (Korrekt)
            "Eine Maßeinheit",             # Index 2
            "Ein Programmierfehler"        # Index 3
        ],
        "correct": 1 # "Ein wichtiges Zwischenziel" steht an 2. Stelle (Index 1)
    },
    3: {
        "prof_name": "Dr. Prozesse",
        "question": "Welche Versionsnummer ist der aktuellste Standard für BPMN?",
        "answers": ["1.0", "3.0", "2.0", "2.5"],
        "correct": 2 # "2.0" steht an 3. Stelle (Index 2)
    },
    4: {
        "prof_name": "Dr. Change",
        "question": "Wie viele Stufen hat das Change Management Modell nach Kotter?",
        "answers": ["5", "6", "7", "8"],
        "correct": 3 # "8" steht an 4. Stelle (Index 3)
    },

    # --- IT-Management ---
    5: {
        "prof_name": "Prof. Boss",
        "question": "Wofür steht die Abkürzung CIO?",
        "answers": [
            "Chief Information Officer",   # Index 0 (Korrekt)
            "Computer Input Output",       # Index 1
            "Chief Internet Operator",     # Index 2
            "Central Intelligence Office"  # Index 3
        ],
        "correct": 0
    },
    6: {
        "prof_name": "Prof. Stakeholder",
        "question": "Wer ist ein 'Stakeholder'?",
        "answers": [
            "Jemand, der das Steak hält",  # Index 0
            "Der Programmierer",           # Index 1
            "Eine Interessengruppe",       # Index 2 (Korrekt)
            "Der Server-Admin"             # Index 3
        ],
        "correct": 2
    },
    7: {
        "prof_name": "Dr. Strategie",
        "question": "Was bedeutet 'Outsourcing'?",
        "answers": [
            "Drucken von Dokumenten",      # Index 0
            "Auslagerung von Aufgaben",    # Index 1 (Korrekt)
            "Kauf neuer Hardware",         # Index 2
            "Einstellen neuer Mitarbeiter" # Index 3
        ],
        "correct": 1
    },
    8: {
        "prof_name": "Prof. Service",
        "question": "Was ist ein SLA?",
        "answers": [
            "Ein Salat",                   # Index 0
            "Service Level Agreement",     # Index 1 (Korrekt)
            "Super Large Array",           # Index 2
            "System Local Access"          # Index 3
        ],
        "correct": 1
    },
    9: {
        "prof_name": "Prof. ITIL",
        "question": "Was ist ITIL?",
        "answers": [
            "Ein Intel-Prozessor",         # Index 0
            "Eine Programmiersprache",     # Index 1
            "Best Practices für IT-Services", # Index 2 (Korrekt)
            "Ein neues iPhone"             # Index 3
        ],
        "correct": 2
    },
    10: {
        "prof_name": "Dr. Start",
        "question": "Wie nennt man das erste Treffen in einem Projekt?",
        "answers": [
            "Kick-off",                    # Index 0 (Korrekt)
            "Sit-in",                      # Index 1
            "Stand-up",                    # Index 2
            "Hang-out"                     # Index 3
        ],
        "correct": 0
    },

# --- Datenbankysteme  ---
    11: {
        "prof_name": "Prof. Data",
        "question": "Wofür steht SQL?",
        "answers": [
            "Structured Question List",    # Index 0
            "Simple Query Language",       # Index 1
            "Structured Query Language",   # Index 2 (Korrekt)
            "Standard Query Loop"          # Index 3
        ],
        "correct": 2 # Verweist auf "Structured Query Language"
    },
    12: {
        "prof_name": "Prof. Data",
        "question": "Was identifiziert einen Datensatz eindeutig?",
        "answers": [
            "Fremdschlüssel",              # Index 0
            "Primärschlüssel",             # Index 1 (Korrekt)
            "Sekundärschlüssel",           # Index 2
            "Haustürschlüssel"             # Index 3
        ],
        "correct": 1 # Verweist auf "Primärschlüssel"
    },
    13: {
        "prof_name": "Dr. ERP",
        "question": "Welcher Hersteller ist bekannt für ERP-Systeme?",
        "answers": [
            "SAP",                         # Index 0 (Korrekt)
            "Nintendo",                    # Index 1
            "Spotify",                     # Index 2
            "Netflix"                      # Index 3
        ],
        "correct": 0 # Verweist auf "SAP"
    },
    14: {
        "prof_name": "Klausur",
        "question": "Was vermeidet man durch Normalisierung?",
        "answers": [
            "Redundanz",                   # Index 0 (Korrekt)
            "Speicherplatz",               # Index 1
            "Datenschutz",                 # Index 2
            "Performance"                  # Index 3
        ],
        "correct": 0 # Verweist auf "Doppelte Datenhaltung"
    },
    15: {
        "prof_name": "Klausur",
        "question": "Was ist CSV?",
        "answers": [
            "Ein Video",                   # Index 0
            "Textformat für Tabellen",     # Index 1 (Korrekt)
            "Ein Bild",                    # Index 2
            "Eine App"                     # Index 3
        ],
        "correct": 1 # Verweist auf "Textformat für Tabellen" (Comma Separated Values)
    },

    # --- Prozessmanagement (BPM) ---
    16: {
        "prof_name": "Klausur",
        "question": "Was ist eine EPK?",
        "answers": [
            "Eine Krankheit",              # Index 0
            "Ereignisgesteuerte Prozesskette", # Index 1 (Korrekt)
            "Ein Einkaufspreis",           # Index 2
            "Ein Projektkürzel"            # Index 3
        ],
        "correct": 1
    },
    17: {
        "prof_name": "Prof. Swimlane",
        "question": "Was zeigt eine 'Swimlane' in einem BPMN-Diagramm an?",
        "answers": [
            "Die Wassertiefe",             # Index 0
            "Die Zuständigkeit (Wer?)",    # Index 1 (Korrekt)
            "Die Dauer",                   # Index 2
            "Die Kosten"                   # Index 3
        ],
        "correct": 1
    },
    18: {
        "prof_name": "Dr. Prozess",
        "question": "Was stellt ein Rechteck mit abegrundeten Ecken in BPMN dar?",
        "answers": [
            "Ereignis (Event)",                     # Index 0 
            "Aktivität (Task)",                     # Index 1 (Korrekt)
            "Entscheidung (Gateway)",               # Index 2
            "Kommentar"                             # Index 3
        ],
        "correct": 1
    },
    19: {
        "prof_name": "Dr. Value",
        "question": "Von wem stammt die 'Wertschöpfungskette'?",
        "answers": ["Michael Porter", "Bill Gates", "Elon Musk", "Steve Jobs"],
        "correct": 0
    },
    20: {
        "prof_name": "Prof. Cloud",
        "question": "Was ist SaaS?",
        "answers": ["Software as a Service", "System as a Server", "Storage as a Stick", "Sold as a Service"],
        "correct": 0
    },

    # --- Moderne Methoden & Frameworks (Agil usw.) ---
    21: {
        "prof_name": "Dr. Agile",
        "question": "Welche Methode ist 'agil'?",
        "answers": [
            "Wasserfall",                  # Index 0
            "Scrum",                       # Index 1 (Korrekt)
            "V-Modell",                    # Index 2
            "Beton-Modell"                 # Index 3
        ],
        "correct": 1 # Verweist auf "Scrum"
    },
    22: {
        "prof_name": "Dr. Scrum",
        "question": "Wie nennt man den 'Chef' im Scrum?",
        "answers": [
            "Projektleiter",               # Index 0
            "Product Owner",               # Index 1 (Korrekt)
            "Scrum King",                  # Index 2
            "Team Lead"                    # Index 3
        ],
        "correct": 1 # Verweist auf "Product Owner"
    },
    23: {
        "prof_name": "Dr. Sprint",
        "question": "Wie nennt man einen Arbeitszyklus in Scrum?",
        "answers": [
            "Sprint",                      # Index 0 (Korrekt)
            "Marathon",                    # Index 1
            "Jogging",                     # Index 2
            "Walk"                         # Index 3
        ],
        "correct": 0 # Verweist auf "Sprint"
    },
    24: {
        "prof_name": "Prof. Goal",
        "question": "Wofür steht das 'S' in SMART-Zielen?",
        "answers": [
            "Schnell",                     # Index 0
            "Spezifisch",                  # Index 1 (Korrekt)
            "Super",                       # Index 2
            "Spontan"                      # Index 3
        ],
        "correct": 1 # Verweist auf "Spezifisch"
    },
    25: {
        "prof_name": "Prof. Kanban",
        "question": "Woher kommt Kanban ursprünglich?",
        "answers": [
            "Toyota (Automobil)",          # Index 0 (Korrekt)
            "Apple (IT)",                  # Index 1
            "McDonalds (Food)",            # Index 2
            "NASA (Raumfahrt)"             # Index 3
        ],
        "correct": 0 # Verweist auf "Toyota (Automobil)"
    },

    # --- ABWL ---
    26: {
        "prof_name": "Prof. Biz",
        "question": "Was bedeutet B2B?",
        "answers": [
            "Business to Business",        # Index 0 (Korrekt)
            "Back to Business",            # Index 1
            "Business to Buyer",           # Index 2
            "Best to Buy"                  # Index 3
        ],
        "correct": 0 # Verweist auf "Business to Business"
    },
    27: {
        "prof_name": "Prof. Biz",
        "question": "Was ist ein ERP-System?",
        "answers": [
            "Ein Spiel",                   # Index 0
            "Enterprise Resource Planning", # Index 1 (Korrekt)
            "Electronic Repair Program",   # Index 2
            "Easy Run Process"             # Index 3
        ],
        "correct": 1 # Verweist auf "Enterprise Resource Planning"
    },
    28: {
        "prof_name": "Dr. Prozess",
        "question": "Wie wird ein 'Start-Event' in BPMN dargestellt?",
        "answers": [
            "Dicker Kreis",                # Index 0
            "Dünner Kreis",                # Index 1 (Korrekt)
            "Rechteck",                    # Index 2
            "Raute"                        # Index 3
        ],
        "correct": 1 # Verweist auf "Dünner Kreis" (Dicker Kreis ist meist End-Event)
    },
    29: {
        "prof_name": "Dr. Prozess",
        "question": "Wofür steht die Raute in einem Flussdiagramm?",
        "answers": [
            "Start/Ende",                  # Index 0
            "Prozessschritt",              # Index 1
            "Entscheidung",                # Index 2 (Korrekt)
            "Dokument"                     # Index 3
        ],
        "correct": 2 # Verweist auf "Entscheidung" (Verzweigung)
    },
    30: {
        "prof_name": "Prof. Markt",
        "question": "Was ist CRM?",
        "answers": [
            "Computer Room Management",         # Index 0
            "Customer Relationship Management", # Index 1 (Korrekt)
            "Central Risk Management",          # Index 2
            "Cold Room Marketing"               # Index 3
        ],
        "correct": 1 # Verweist auf "Customer Relationship Management"
    },

    # --- IT-Sicherheit & -Recht ---
    31: {
        "prof_name": "Dr. Safe",
        "question": "Was ist 'Phishing'?",
        "answers": [
            "Angeln gehen",                # Index 0
            "Passwort-Klau per Fake-Mail", # Index 1 (Korrekt)
            "Ein Computervirus",           # Index 2
            "Daten löschen"                # Index 3
        ],
        "correct": 1 # Verweist auf den Passwort-Diebstahl
    },
    32: {
        "prof_name": "Dr. Legal",
        "question": "Was regelt die DSGVO?",
        "answers": [
            "Straßenverkehr",              # Index 0
            "Datenschutz",                 # Index 1 (Korrekt)
            "Gehälter",                    # Index 2
            "Urlaubstage"                  # Index 3
        ],
        "correct": 1 # Verweist auf "Datenschutz"
    },
    33: {
        "prof_name": "Prof. Hacker",
        "question": "Welches Passwort ist am sichersten?",
        "answers": [
            "123456",                      # Index 0 (Unsicher)
            "password",                    # Index 1 (Unsicher)
            "P@ssw0rd!23",                 # Index 2 (Korrekt, da Sonderzeichen & Zahlen)
            "user123"                      # Index 3 (Unsicher)
        ],
        "correct": 2 # Verweist auf das komplexe Passwort
    },
    34: {
        "prof_name": "Dr. Backup",
        "question": "Warum macht man ein Backup?",
        "answers": [
            "Zum Spaß",                    # Index 0
            "Datensicherung",              # Index 1 (Korrekt)
            "Speicher verbrauchen",        # Index 2
            "PC verlangsamen"              # Index 3
        ],
        "correct": 1 # Verweist auf "Datensicherung"
    },
    35: {
        "prof_name": "Prof. Compliance",
        "question": "Was bedeutet Compliance?",
        "answers": [
            "Regeltreue",                  # Index 0 (Korrekt)
            "Computerwissen",              # Index 1
            "Kompliziertheit",             # Index 2
            "Beschwerde"                   # Index 3
        ],
        "correct": 0 # Verweist auf "Regeltreue" (Einhaltung von Regeln)
    },

    # --- Zufällige Basics ---
    36: {
        "prof_name": "Prof. Basic",
        "question": "Was ist Open Source?",
        "answers": [
            "Teure Software",              # Index 0
            "Quellcode ist öffentlich",    # Index 1 (Korrekt)
            "Software ohne Code",          # Index 2
            "Ein Virus"                    # Index 3
        ],
        "correct": 1 # Verweist auf "Quellcode ist öffentlich"
    },
    37: {
        "prof_name": "Dr. Plan",
        "question": "Was zeigt ein Gantt-Diagramm?",
        "answers": [
            "Geldfluss",                   # Index 0
            "Zeitlicher Projektablauf",    # Index 1 (Korrekt)
            "Netzwerkstruktur",            # Index 2
            "Datenbankmodell"              # Index 3
        ],
        "correct": 1 # Verweist auf die Zeitplanung (Balkendiagramm)
    },
    38: {
        "prof_name": "Prof. Supply",
        "question": "Was ist SCM?",
        "answers": [
            "Supply Chain Management",     # Index 0 (Korrekt)
            "Source Code Manager",         # Index 1
            "System Core Module",          # Index 2
            "Super Cool Man"               # Index 3
        ],
        "correct": 0 # Verweist auf die Lieferkette
    },
    39: {
        "prof_name": "Dr. Zip",
        "question": "Was macht man beim 'Zippen'?",
        "answers": [
            "Löschen",                     # Index 0
            "Kopieren",                    # Index 1
            "Komprimieren",                # Index 2 (Korrekt)
            "Drucken"                      # Index 3
        ],
        "correct": 2 # Verweist auf Komprimierung (Platz sparen)
    },
    40: {
        "prof_name": "Prof. Algo",
        "question": "Was ist ein Algorithmus?",
        "answers": [
            "Ein Rhythmus",                # Index 0
            "Eine Handlungsvorschrift",    # Index 1 (Korrekt)
            "Ein Computerteil",            # Index 2
            "Eine Programmiersprache"      # Index 3
        ],
        "correct": 1 # Verweist auf die Problemlösungs-Vorschrift
    },

    # --- Bachelor-Endlevel ---
    41: {
        "prof_name": "Prof. Final",
        "question": "Was bedeutet 'www'?",
        "answers": [
            "World Wide Web",              # Index 0 (Korrekt)
            "Wer Wo Was",                  # Index 1
            "World Web Wide",              # Index 2
            "Wide World Web"               # Index 3
        ],
        "correct": 0 # Verweist auf "World Wide Web"
    },
    42: {
        "prof_name": "Dr. Mail",
        "question": "Was ist Spam?",
        "answers": [
            "Wichtige Post",               # Index 0
            "Unerwünschte Mails",          # Index 1 (Korrekt)
            "Ein Virenprogramm",           # Index 2
            "Eine Firewall"                # Index 3
        ],
        "correct": 1 # Verweist auf unerwünschte Nachrichten
    },
    43: {
        "prof_name": "Prof. Office",
        "question": "Welche Software nutzt man für Präsentationen?",
        "answers": [
            "Excel",                       # Index 0
            "Word",                        # Index 1
            "PowerPoint",                  # Index 2 (Korrekt)
            "Outlook"                      # Index 3
        ],
        "correct": 2 # Verweist auf "PowerPoint"
    },
    44: {
        "prof_name": "Dr. Browser",
        "question": "Was ist Firefox?",
        "answers": [
            "Ein Spiel",                   # Index 0
            "Ein Webbrowser",              # Index 1 (Korrekt)
            "Ein Virus",                   # Index 2
            "Ein Textprogramm"             # Index 3
        ],
        "correct": 1 # Verweist auf den Browser
    },
    45: {
        "prof_name": "Prof. Key",
        "question": "Tastenkombination für Kopieren?",
        "answers": [
            "Strg + V",                    # Index 0
            "Strg + C",                    # Index 1 (Korrekt)
            "Strg + X",                    # Index 2
            "Strg + P"                     # Index 3
        ],
        "correct": 1 # Verweist auf Copy (C)
    },
    46: {
        "prof_name": "Prof. Key",
        "question": "Tastenkombination für Einfügen?",
        "answers": [
            "Strg + V",                    # Index 0 (Korrekt)
            "Strg + C",                    # Index 1
            "Strg + Z",                    # Index 2
            "Strg + A"                     # Index 3
        ],
        "correct": 0 # Verweist auf STRG + V (Index 0)
    },
    47: {
        "prof_name": "Dr. Search",
        "question": "Was ist Google?",
        "answers": [
            "Ein Browser",                 # Index 0
            "Eine Suchmaschine",           # Index 1 (Korrekt)
            "Ein Betriebssystem",          # Index 2
            "Ein PC-Hersteller"            # Index 3
        ],
        "correct": 1 # Verweist auf die Suchmaschine (Primärfunktion)
    },
    48: {
        "prof_name": "Prof. App",
        "question": "Was ist Android?",
        "answers": [
            "Ein Roboter",                 # Index 0
            "Ein mobiles Betriebssystem",  # Index 1 (Korrekt)
            "Eine App",                    # Index 2
            "Ein Handyhersteller"          # Index 3
        ],
        "correct": 1 # Verweist auf das OS
    },
    49: {
        "prof_name": "Dr. Social",
        "question": "Was ist LinkedIn?",
        "answers": [
            "Ein Spiel",                   # Index 0
            "Ein Berufsnetzwerk",          # Index 1 (Korrekt)
            "Ein Videoportal",             # Index 2
            "Ein Musikdienst"              # Index 3
        ],
        "correct": 1 # Verweist auf das Business-Netzwerk
    },
    50: {
        "prof_name": "Prof. Bachelor",
        "question": "Was steht am Ende des Studiums?",
        "answers": [
            "Die Rente",                   # Index 0
            "Die Bachelorarbeit",          # Index 1 (Korrekt)
            "Die Einschulung",             # Index 2
            "Das Abitur"                   # Index 3
        ],
        "correct": 1 # Der krönende Abschluss!
    }
}
