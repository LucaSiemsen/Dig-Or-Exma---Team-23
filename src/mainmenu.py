from button import Button
import pygame


button1=Button()
button2=Button()
buttons=[button1,button2]
"nur zum klar machen wie ich s mir denke mir ist bewusst das ich oben button paaramenter übergeben muss."
class MainMenu:
    #Hauptmenüklasse, beinhaltet Hintergrund, Butttons Update und Draw Logik
    def __init__(self, screen, bild, buttons):
        #initialisiere das menü
        #parameter screen das pygame fenster
        #parameter bild das geladene hintergrundbild
        #parameter butttons liste von buttonobjekten
        self.screen=screen  #referenz auf fenster
        self.bild=bild      #Hintergrundbild nicht gescaled
        self.buttons=buttons    #liste aller button im Menü
        self.clock= pygame.time.Clock() #clock für fps begrenzung
        self.bild=pygame.transform.scale(self.bild, self.screen.get_size())
        self.auswahl=None #speichert welcher button geklickt wurde
        self.running=True   #Menülauf-Flag
        
    def update(self):
        #verarbeitet events, mausbewegung, buttonhover und klicks
        events=pygame.event.get() #alle aktuellen events holen
        for event in events:
            if event.type==pygame.QUIT: #fenster schließen
                self.running=False
                self.auswahl="QUIT" #kann der gameloop auswerten
        mausposition=pygame.mouse.get_pos() #mausposition für Hover
        mausklick=pygame.mouse.get_pressed()    #Maustastenstatus

        for button in self.buttons:
            button.b_groesse_aendern(mausposition)  #Hovereffekt updaten

            #Prüfen ob Button geklickt wurde
            if button.is_clicked():
                #Aktion wird nur gespeichert
                #Button führt nichts aus
                self.auswahl="platzhalter für den button der dann angesprochen werden soll."
                self.running=False #Menüschleife beenden
        
    def draw (self):
        #Zeichnet Huntergrund, Buttons, aktualiiert den bildschirm
        self.screen.fill((0,0,0))
        self.screen.blit(self.bild,(0,0) )
        pygame.display.flip()

    def run(self):
        #Hauptschleife des Menüs läuft solange wie Running=True
        #Gibt am ende die Aktion zurück 
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(60)
        return self.auswahl
    


    #----andere version hauptmenu nur nutzen wenn dem mauszeiger ein kleines spritebild folgen soll

    button1=Button()
button2=Button()
buttons=[button1,button2]
"nur zum klar machen wie ich s mir denke mir ist bewusst das ich oben button paaramenter übergeben muss."
class MainMenu:
    #Hauptmenüklasse, beinhaltet Hintergrund, Butttons Update und Draw Logik
    def __init__(self, screen, bild, buttons):
        #initialisiere das menü
        #parameter screen das pygame fenster
        #parameter bild das geladene hintergrundbild
        #parameter butttons liste von buttonobjekten
        self.screen=screen  #referenz auf fenster
        self.bild=bild      #Hintergrundbild nicht gescaled
        self.buttons=buttons    #liste aller button im Menü
        self.clock= pygame.time.Clock() #clock für fps begrenzung
        self.bild=pygame.transform.scale(self.bild, self.screen.get_size())
        self.auswahl=None #speichert welcher button geklickt wurde
        self.running=True   #Menülauf-Flag
        
    def update(self):
        #verarbeitet events, mausbewegung, buttonhover und klicks
        events=pygame.event.get() #alle aktuellen events holen
        for event in events:
            self.curser.stalk()
            if event.type==pygame.QUIT: #fenster schließen
                self.running=False
                self.auswahl="QUIT" #kann der gameloop auswerten
        mausposition=pygame.mouse.get_pos() #mausposition für Hover
        mausklick=pygame.mouse.get_pressed()    #Maustastenstatus

        for button in self.buttons:
            button.b_groesse_aendern(mausposition)  #Hovereffekt updaten

            #Prüfen ob Button geklickt wurde
            if button.is_clicked():
                #Aktion wird nur gespeichert
                #Button führt nichts aus
                self.auswahl="platzhalter für den button der dann angesprochen werden soll."
                self.running=False #Menüschleife beenden
        
    def draw (self):
        #Zeichnet Huntergrund, Buttons, aktualiiert den bildschirm
        self.screen.fill((0,0,0))
        self.screen.blit(self.bild,(0,0) )
        self.cursor.draw((0,0))
        pygame.display.flip()

    def run(self):
        #Hauptschleife des Menüs läuft solange wie Running=True
        #Gibt am ende die Aktion zurück 
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(60)
        return self.auswahl


            