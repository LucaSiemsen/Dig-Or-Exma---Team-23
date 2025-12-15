from src.button import Button
import pygame




class MainMenu:
    #Hauptmenüklasse, beinhaltet Hintergrund, Butttons Update und Draw Logik
    def __init__(self, screen, bg_scaled, bg_rect, font, titleimg):
        self.screen=screen
        self.clock= pygame.time.Clock() #clock für fps begrenzung
        self.auswahl=None
        self.running=True
        self.bg_scaled=bg_scaled
        self.bg_rect=bg_rect
        self.font=font
        self.buttons=self.create_buttons()

        try:
            title_img=pygame.image.load(
                titleimg
            ).convert_alpha()
            target_width=int(self.buttons["START"].rect.width*1.6)
            scale_factor=target_width/title_img.get_width()
            target_heigt= int(title_img.get_height()*scale_factor)

            title_img=pygame.transform.scale(
                title_img,(target_width, target_heigt)
            )

            self.title_surface= title_img
        except:
            font=pygame.font.SysFont(None,72,bold=True)
            self.title_surface=font.render("DIG OR EXMA",True,(255,255,255))
        
        self.title_rect=self.title_surface.get_rect()
        self.title_rect.centerx=self.buttons["START"].rect.centerx
        self.title_rect.bottom=self.buttons["START"].rect.top -60

        self.cheat_buffer= ""
        self.cheat_code= "ichcheate"
        self.godmode=False
        self.cheat_max_len= len(self.cheat_code)

    def create_buttons(self):
        bg=self.bg_rect
        button_w=200
        button_h=60
        gap=65

        start_x=bg.centerx-button_w//2
        start_y=bg.centery-gap
        
        return{
            "START":Button(start_x,start_y,button_h,button_w,(0,200,0),
                           "START",self.font,(255,255,255)),
            "QUIT":Button(start_x,start_y + gap,button_h,button_w,(200,0,0),
                           "QUIT",self.font,(255,255,255)),
            
        }
        
        
    def update(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.auswahl="QUIT"
                self.running=False
            elif event.type==pygame.KEYDOWN:
                self.handle_cheat_input(event)
        mouse_pos=pygame.mouse.get_pos()
        for name, button in self.buttons.items():
            button.b_groesse_aendern(mouse_pos)

            if button.is_clicked():
                self.auswahl=name
                self.running=False
        
        
    def draw (self):
        #Zeichnet Huntergrund, Buttons, aktualiiert den bildschirm
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg_scaled,self.bg_rect)
        self.screen.blit(self.title_surface,self.title_rect)

        for button in self.buttons.values():
            button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        #Hauptschleife des Menüs läuft solange wie Running=True
        #Gibt am ende die Aktion zurück 
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(60)
        self.running=True
        return {"auswahl": self.auswahl, "godmode":self.godmode}
    
    def handle_cheat_input(self,event):
        if event.unicode.isprintable() and not self.godmode:
            self.cheat_buffer += event.unicode.lower()
            if len(self.cheat_buffer)>self.cheat_max_len:
                self.cheat_buffer=self.cheat_buffer[-self.cheat_max_len:]
            if self.cheat_buffer==self.cheat_code:
                self.godmode=True
                self.cheat_buffer=""
    


 