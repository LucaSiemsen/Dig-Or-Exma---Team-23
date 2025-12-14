import pygame as pg

class SoundManager:
    def __init__(self):
        pg.mixer.init()
        #Liste der eigentlichen Songs, die abgespielt werden können
        self.songs = ["music/background_music.mp3", "music/intro.mp3"]
        
        #soundeffekte Laden
        self.hit_sound = pg.mixer.Sound("music/hit_soundeffect.mp3")
        self.footsteps_sound = pg.mixer.Sound("music/footsteps.mp3")
        self.gameover_sound = pg.mixer.Sound("music/gameover.mp3")
        self.ECTS_sound = pg.mixer.Sound("music/ECTS_coin.mp3")
        self.powerup_sound = pg.mixer.Sound("music/powerup.mp3")
        #Packt alle Soundeffekte in eine Liste damit man die Lautstärke zentral steuern kann (kann erweitert werden)
        self.sfx_sounds = [self.hit_sound, self.footsteps_sound, self.gameover_sound, self.ECTS_sound, self.powerup_sound]
        
        # Basislautstärke für Musik und Soundeffekte
        self.base_vol_music = 1.0
        self.base_vol_sfx = 1.0
        self.is_muted = False
        self.is_paused = False


    def play_song(self, index: int):
        pg.mixer.music.load(self.songs[index])
        pg.mixer.music.play(-1) # -1 bedeutet Endlosschleife
        

    def toggle_mute(self) -> None:
        self.is_muted = not self.is_muted
        
        if self.is_muted:
            pg.mixer.music.set_volume(0)
            for s in self.sfx_sounds:
                s.set_volume(0)
        else:
            #Zurück auf die gemerkte Lautstärke setzen
            pg.mixer.music.set_volume(self.base_vol_music)
            for s in self.sfx_sounds:
                s.set_volume(self.base_vol_sfx)

    #Diese Methode wird vom Slider aufgerufen
    def set_music_volume(self, vol: float):
        #Wir speichern den Wert immer, damit wir nach dem Unmuten wissen, wie laut es war
        self.base_vol_music = max(0.0, min(1.0, float(vol)))
        self.base_vol_sfx = self.base_vol_music 
        
        #Nur anwenden, wenn nicht gemuted
        if not self.is_muted:
            pg.mixer.music.set_volume(self.base_vol_music)
            for s in self.sfx_sounds:
                s.set_volume(self.base_vol_sfx)
    
    
    def play_hitsound(self): 
        self.hit_sound.play()
        
    def play_footsteps(self):
        self.footsteps_sound.play()
        
    def game_over_music(self):
        self.gameover_sound.stop()
        self.gameover_sound.play()
        
    def pause_music(self):
        pg.mixer.music.pause()

    def unpause_music(self):
        pg.mixer.music.unpause()
    
    def stop_hitsound(self):
        self.hit_sound.stop()
        
    def play_ects_sound(self):
        self.ECTS_sound.play()
        
    def play_powerup_sound(self):
        self.powerup_sound.play()
    
    def get_music_volume(self):
        return self.base_vol_music