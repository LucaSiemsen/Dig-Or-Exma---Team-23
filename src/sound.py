import pygame as pg

class SoundManager:
    def __init__(self):
        pg.mixer.init()
        self.music_path = "music/background_music.wav"
        
        #soundeffekte Laden
        self.hit_sound = pg.mixer.Sound("music/hit_soundeffect.wav")
        
        #Packt alle Soundeffekte in eine Liste damit man die Lautstärke zentral steuern kann (kann erweitert werden)
        self.sfx_sounds = [self.hit_sound]
        
        # Basislautstärke für Musik und Soundeffekte
        self.base_vol_music = 0.3  
        self.base_vol_sfx = 1.0
        
        #
        self.is_muted = False

        #Wendet aktuelle Mute-Einstellung auf alle Sounds an.
    def _apply_volumes(self) -> None:
        if self.is_muted:
            factor = 0.0 #Wenn Mute an ist -> Faktor ist 0 (alles wird stumm)
        else:
            factor = 1.0 #Wenn Mute aus ist -> Faktor ist 1 (alles bleibt normal)
        pg.mixer.music.set_volume(self.base_vol_music * factor)
        
        for s in self.sfx_sounds: # geht jedes Element in der Liste von unseren Soundeffekten durch, wenn der sound 0.3 zb ist, wird er mit dem Faktor multipliziert 0.3 Lautstärke * 0 (also unser Mute Faktor) = 0, heißt der sound wird stumm geschaltet
            s.set_volume(self.base_vol_sfx * factor)
            
        #Setzt die Musiklautstärke auf einen Wert zwischen 0.0 und 1.0
    def set_music_volume(self, vol: float) -> None:
        """0.0 .. 1.0"""
        self.base_vol_music = max(0.0, min(1.0, float(vol)))
        self._apply_volumes()
        
        #Spielt den Hitsound ab
    def play_hitsound(self) -> None: 
        self.hit_sound.play()
        
        #Startet die Hintergrundmusik
    def start_music(self) -> None:
        pg.mixer.music.load(self.music_path)
        pg.mixer.music.play(-1)
        self._apply_volumes() # -1 bedeutet Endlosschleife
        
        #Schaltet Stummschaltung ein/aus
    def toggle_mute(self) -> None:
        self.is_muted = not self.is_muted
        self._apply_volumes()
    
    #Pausiert die Hintergrundmusik
    def pause_music(self) -> None:
        pg.mixer.music.pause()
    #Setzt die Hintergrundmusik fort
    def unpause_music(self) -> None:
        pg.mixer.music.unpause()
    
    def stop_hitsound(self) -> None:
        self.hit_sound.stop()  # stoppt alle laufenden Instanzen dieses Sounds

    
        # Methode für den Slider, um die aktuelle Musiklautstärke zu bekommen
    def get_music_volume(self) -> float:
        return float(self.base_vol_music)
        
        


