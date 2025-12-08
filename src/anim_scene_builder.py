#die fertigen animationen sind als spritesheet hinterlegt jeweils das passende beim objektaufruf übergeben
import pygame

class Animator_Scenes:
    def __init__(self,x,y,sheetliste,speed,schleife):
        self.x=x
        self.y=y
        self.sheetliste=sheetliste
        self.sheetliste_count=len(sheetliste)
        self.speed=speed
        self.schleife=schleife 
        self.aktiv=False
        self.frame_index=0
        self.last_update=pygame.time.get_ticks()

    def load_from_spritesheet(self, sheet_path, frame_width, frame_height):#funktion von gpt "schreibe mir ne funktion in ner klasse die spritesheets aus pixel lädt damit ich nicht jedes bild einzeln laden muss"
    # Keine Transparenz → convert() statt convert_alpha()
           
        sheet = pygame.image.load(sheet_path).convert()

        sheet_width = sheet.get_width()
        self.sheetliste = []  # alte Frames überschreiben

        # Anzahl Frames = Breite / Framebreite
        self.sheetliste_count = sheet_width // frame_width

        for i in range(self.sheetliste_count):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            self.sheetliste.append(frame)



    def start (self):
        self.aktiv=True
        self.frame_index=0
        self.last_update=pygame.time.get_ticks()

    def update(self):
        if self.aktiv==False: #die logik müsste auch funktionieren? not ist mir zu gefährlich
            return
        now=pygame.time.get_ticks()
        
        if now - self.last_update>= self.speed:
            self.last_update=now
            self.frame_index+=1

        if self.frame_index>= self.sheetliste_count:
            if self.schleife:
                self.frame_index=0
            else:#chatgpt generiert 
             # Animation stoppt sauber nach letztem Frame
                self.frame_index = self.sheetliste_count - 1
                self.aktiv = False            

    def draw (self,screen):
        screen.blit(self.sheetliste[self.frame_index],(self.x,self.y))
    


    
