#Erstellung eines Timers für das BAföG-System

class BafoegTimer:
    #Startmethode, die festlegt, wie lange der Timer läuft
    def __init__(self, duration_seconds: float):
        self.duration = duration_seconds  #Gesamtzeit des Timers
        self.time_left = duration_seconds #Aktuell verbleibende Zeit

    #verbleibende Zeit wird auf die ursprüngliche Dauer zurückgesetzt
    def reset(self):
        self.time_left = self.duration 
        
    #Methode, die die Zeit verringert
    def update(self, dt: float):
        self.time_left = max(0.0, self.time_left - dt)
        #dt = vergangene Zeit seit letztem Frame.
        #0.0 ist die Zeit, die minimal verbleiben kann (Timer läuft nicht ins Negative)

    #Überprüfung, ob die Zeit abgelaufen ist
    @property
    def is_over(self):
        return self.time_left <= 0.0