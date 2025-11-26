# 🎓 Dig Or Exma – Team 23

**Fortgeschrittene Programmierung – HAW-Kiel (Wintersemester 2025)**  
Projektarbeit von **Team 23**  
👨‍💻 Luca Siemsen (939491) · Aaron Lehrke (937367) · Corinna Filipp (946691) · Dimitri Homutov (935939)

---

## 🕹️ Spielidee

In *Dig Or Exma* steuerst du einen Studenten, der sich durchs Semester „durchgräbt“.  
Während der BAföG-Timer unaufhaltsam tickt, musst du ECTS-Punkte sammeln,  
Klausuren überstehen und Professoren ausweichen – sonst droht die Exmatrikulation. 😅  

Das Spielkonzept ist bewusst humorvoll, basiert aber auf objektorientiertem Design mit  
Klassen wie `Student`, `Level`, `Block`, `Enemy`, `Dozent`, `Klausur` und PowerUps  
(`Pizza`, `EnergyDrink`, `Party`, `ChatGPT` usw.).  

---

## ⚙️ Technische Umsetzung

Das Spiel ist mit **Python 3.11+** und **Pygame** umgesetzt.  
Die Struktur folgt einem modularen Aufbau:

Fortgeschrittene-Programmierung/
│
├── src/
│ ├── main.py
│ ├── game.py
│ ├── student.py
│ ├── enemy.py
│ ├── level.py
│ ├── block.py
│ ├── entity.py
│ ├── powerups.py
│ └── collectibles.py
│
├── assets/
│ ├── sprites/ ← Platz für Grafiken
│ └── sounds/ ← Platz für Soundeffekte
│
├── requirements.txt
└── README.md


---

## 🎮 Steuerung

| Taste | Aktion |
|-------|--------|
| **↑ ↓ ← →** | Bewegung um ein Feld (gräbt automatisch) |
| **G** | Graben an aktueller Position |
| **ESC / Fenster schließen** | Spiel beenden |

---

## 🧩 Ziele & Spielmechanik

- **ECTS sammeln:** 2 ECTS = Level bestanden  
- **Timer:** BAföG-Zeit tickt stetig runter  
- **Gegner:** Dozent & Klausur – Berührung führt zu Game Over  
- **PowerUps (geplant):** Pizza (Rettung), Party (Buff/Debuff), ChatGPT (Klausurhilfe)  

---

## 💡 Ausführen (lokal)

1. Projekt klonen:
   ```bash
   git clone https://github.com/LucaSiemsen/Fortgeschrittene-Programmierung.git
   cd Fortgeschrittene-Programmierung

## Virtuelle Umgebung erstellen & aktivieren:
python -m venv venv
.\venv\Scripts\activate

## Abhängigkeiten installieren:
pip install -r requirements.txt

## Spiel starten:
python -m src.main

## 📚 Hinweise

Dieses Projekt entstand im Rahmen des Moduls Fortgeschrittene Programmierung.

Ziel war es, objektorientierte Konzepte praktisch anzuwenden.

Der aktuelle Stand entspricht dem Design-Konzept und ist lauffähig als Prototyp.

Erweiterungen (z. B. PowerUps, Level-System, Animationen) sind geplant.

## 🏁 Fazit

Ein Student, zwei ECTS, drei Tastenanschläge – und das Semester ist (fast) gerettet.
Oder um es in Pythons Worten zu sagen:


if semester.over():
    print("Game Over")
else:
    print("Level geschafft 🎓")


