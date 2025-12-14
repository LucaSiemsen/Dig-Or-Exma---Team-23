import pygame
import sys
hover_aenderung=5  # globale Hover-Vergrößerung (Pixelanzahl um die der Button wächst)


class Button:
        #Repräsentiert einen einfachen UI-Button mit Hover- und Klickfunktion.
    def __init__(self,x,y,hoehe_orginal,breite_orginal,buttonfarbe,text,schriftart,schriftfarbe):
         
       # Initialisiert einen Button.

        #:param x: Ausgangsposition X (oben links)
        #:param y: Ausgangsposition Y (oben links)
        #:param hoehe_orginal: Ausgangshöhe des Buttons
        #:param breite_orginal: Ausgangsbreite des Buttons
        #:param buttonfarbe: RGB-Farbe des Buttons
        #:param schriftart: Font-Objekt (optional, aktuell nicht genutzt)
        #:param schriftfarbe: RGB-Farbe für Text (optiona)

        self.x_orginal= x   # Speichert die fixe Originalposition X
        self.y_orginal= y    # Speichert die fixe Originalposition Y
        self.hoehe_orginal=hoehe_orginal    # Ausgangshöhe des Buttons
        self.breite_orginal=breite_orginal   # Ausgangsbreite des Buttons

        self.buttonfarbe=buttonfarbe #Button Farbe
        self.text=text   
        self.schriftart=schriftart      #Font (ungenutzt)
        self.schriftfarbe=schriftfarbe  #Textfarbe (ungenutzt)
        self.rect=pygame.Rect(x,y,self.breite_orginal,self.hoehe_orginal) 
        # Das Rechteck, das Position und Größe repräsentiert (wird dynamisch verändert)


    def draw (self,screen):
        #zeichnet den Button auf den Screen
        #parameter screen: das pygame-fenster
        pygame.draw.rect(screen,self.buttonfarbe,self.rect)  # zeichnet das Rechteck
        if self.text and self.schriftart:
            text_surface=self.schriftart.render(
                self.text, True, self.schriftfarbe
            )
            text_rect= text_surface.get_rect(
                center=self.rect.center
            )
            screen.blit(text_surface, text_rect)


    def b_groesse_aendern (self,mausposition):
        #Passt die Buttongröße an, wenn der Mauszeiger darüber ist (Hover-Effekt).
        #Mauspositon: Aktuelle Mausposition als Tupel
        mausposition=pygame.mouse.get_pos() #holt aktuelle Mausposition
        if self.rect.collidepoint(mausposition):
            #Button befindet sich unter der Maus =größer zeichnen
            neue_breite = self.breite_orginal+hover_aenderung
            neue_hoehe=self.hoehe_orginal+hover_aenderung

            verschiebung_x=hover_aenderung//2 #zentriert verschiebung x
            verschiebung_y=hover_aenderung//2 #zentriert verschiebung y
            
            #neue größe setzen
            self.rect.width=neue_breite
            self.rect.height=neue_hoehe
            #button wächst zur mitte hin position korriegieren
            self.rect.x=self.x_orginal-verschiebung_x
            self.rect.y=self.y_orginal-verschiebung_y

        else:
            #Maus ist nicht über dem Button = orginalposition wiederherstellen
            self.rect.width=self.breite_orginal
            self.rect.height=self.hoehe_orginal
            self.rect.x=self.x_orginal
            self.rect.y=self.y_orginal


    def is_clicked (self):
        #prüft ob der Button mit der linken Maustaste angeklickt wurde.
        #return true wenn geklickt wurde sonst False
        mausposition=pygame.mouse.get_pos() #aktuelle Position
        mausklick=pygame.mouse.get_pressed()    #aktueller Status der Maustaste

        if  self.rect.collidepoint(mausposition) and mausklick[0]:
            return True
        else:
           return False

            