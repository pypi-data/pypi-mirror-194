import pygame

#@class fot button---------------
class simple_button():
    """ this is to crete a simple button either with color change OR with no color change """
    def __init__(self,w=70,h=70,color=(0,0,255),color1=(0,255,0),target=None,text=None,fg="white",text_size=40,args=[]):
        self.h=h
        self.w=w
        self.color=color
        self.color1=color1
        self.target=target
        self.text=text
        self.text_size=text_size
        self.fg=fg
        self.args=args
        pygame.font.init()
        self.font = pygame.font.Font("freesansbold.ttf", text_size)
    def show_no_anemi(self,x,y,window,boder_width=0,corner_round_level=0):
        
        #--------for target-----------
        mouse=pygame.mouse.get_pos()
        rect=pygame.Rect(x,y,self.w,self.h)
        if self.target!=None:
            if rect.collidepoint(mouse):
                if window.eve.type == pygame.MOUSEBUTTONDOWN:
                    self.target(self.args)
        #------------------------------

        #---------draw rect-----------------
        pygame.draw.rect(window.scren,self.color,rect,boder_width,corner_round_level)
        #------------------------------------
        
        #-------for text----------------
        if self.text!=None:
            txt=self.font.render(self.text,True,self.fg)
            window.scren.blit(txt,(x+(rect.h/20),rect.midleft[1]-18))
        #--------------------------------
        
    def show_color_change(self,x,y,window,boder_width=0,corner_round_level=0):
        #-------------some variables------------
        color=self.color
        mouse=pygame.mouse.get_pos()
        rect=pygame.Rect(x,y,self.w,self.h)
        #----------------------------------------
        
        #---------for target---------------------
        if self.target!=None:
            if rect.collidepoint(mouse):
                if window.eve.type == pygame.MOUSEBUTTONDOWN:
                    self.target(self.args)
        #---------------------------------------

        #-------------for color change----------
        if rect.collidepoint(mouse):
                if window.eve.type == pygame.MOUSEBUTTONDOWN:
                    color=self.color1
        #---------------------------------------

        #-------draw rect-------------
        pygame.draw.rect(window.scren,color,rect,boder_width,corner_round_level)
        #------------------------------

        #-------for text----------------
        if self.text!=None:
            txt=self.font.render(self.text,True,self.fg)
            window.scren.blit(txt,(x+(rect.h/20),rect.midleft[1]-18))
#--------------------------------

#@class for text------------
class text:
    def __init__(self,text,color='white',size=38):
        self.text=text
        self.color=color
        self.size=size
        pygame.font.init()
        self.font = pygame.font.Font("freesansbold.ttf", self.size)
    def show(self,window,x,y):
        txt_surface=self.font.render(self.text,True,self.color)
        window.scren.blit(txt_surface,(x,y))
#---------------------------

#@class for radio-button-----
class button_radio():
    def __init__(self,radius=10,color='black',target=None):
        self.r=radius
        self.color=color
        self.active=False
    def show(self,window,x,y):
        mouse=pygame.mouse.get_pos()
        pygame.draw.circle(window.scren,self.color,(x,y),self.r,3)
        rect_circle=pygame.Rect(x,y,self.r*2,self.r*2)
        rect_circle.center=(x,y)
        if window.eve.type == pygame.MOUSEBUTTONDOWN:
            if rect_circle.collidepoint(mouse):
                if self.active==False:
                    self.active=True
                else:self.active=False
        if self.active:
            pygame.draw.circle(window.scren,self.color,(x,y),self.r/1.5)
            return True
        else:return False
#----------------------------

#@class for slider-----------
class slider:
    def __init__(self,x,y,w=150,h=5,color='white',color_circle='white',start=1,end=10,radius=10,corner_round=0,text_size=38,t1_align='side',t2_align='up',t3_align='side',show_text=True):
        self.t1=t1_align
        self.t2=t2_align
        self.t3=t3_align
        self.text_show=show_text

        self.x=x
        self.y=y

        self.color=color
        self.cc=color_circle

        self.start=start
        self.end=end

        self.h=h
        self.w=w
        self.r=radius
        self.corner=corner_round

        self.rect=pygame.Rect(self.x,self.y,self.w,self.h)

        self.circleposx=self.rect.centerx
        self.circleposy=self.rect.centery
        
        self.circle_rect=pygame.Rect(self.circleposx,self.circleposy,self.r*2,self.r*2)     
        self.circle_rect.center=[self.circleposx,self.circleposy]

        self.ts=text_size
        self.text1=text(f'{self.start}',size=text_size)
        self.text2=text(f'{self.end//2}',size=text_size)
        self.text3=text(f'{self.end}',size=text_size)       
    
    def show(self,window):
        
        mouse_pressed=False

        if window.eve.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed=True
        if window.eve.type == pygame.MOUSEBUTTONUP and mouse_pressed == True:
            mouse_pressed=False

        self.circle_rect.center=[self.circleposx,self.circleposy]
        
        mouse=pygame.mouse.get_pos()
        pygame.draw.rect(window.scren,self.color,self.rect,0,self.corner)
        pygame.draw.circle(window.scren,self.cc,(self.circleposx,self.circleposy),self.r)
     
        if mouse_pressed==True:
            if self.rect.collidepoint(mouse):
                self.circleposx=mouse[0]
        
        if mouse_pressed==True:
            if self.circle_rect.collidepoint(mouse):
                self.circleposx=mouse[0]
     
        if self.text_show==True:
            self.show_text(window)

        pos=self.circleposx-self.rect.midleft[0]
        return round((pos*self.end)/self.rect.width,2)
    def show_text(self,window):
        # for@start text----------------------
        match self.t1:
            case 'side':
                self.text1.show(window,
                            self.rect.midleft[0]-self.ts+20,
                            self.rect.midleft[1]-20
                            )
            case 'up':
                self.text1.show(window,
                            self.rect.topleft[0]-self.ts+25,
                            self.rect.topleft[1]-self.ts
                            )
            case 'down':
                self.text1.show(window,
                            self.rect.bottomleft[0]-self.ts+25,
                            self.rect.bottomleft[1]+self.ts-25
                            )
            case _:
                raise Exception(f'invalid align command -> {self.t1}. use up, down or side as command')
        # for@mid text---------------------------- 
        match self.t2:
            case 'up':
                self.text2.show(window,
                            self.rect.midtop[0]-self.ts+20,
                            self.rect.midtop[1]-27
                            )
            case 'down':
                self.text2.show(window,
                            self.rect.midbottom[0]-self.ts+20,
                            self.rect.midbottom[1]+self.ts-25
                            )
            case _:
                raise Exception(f'invalid align command -> {self.t2} . use up or down as command')
        # for@last text-------------------------------
        match self.t3:
            case 'side':
                self.text3.show(window,
                            self.rect.midright[0]-self.ts+20,
                            self.rect.midleft[1]-20
                            )
            case 'up':
                self.text3.show(window,
                            self.rect.topright[0]-self.ts+25,
                            self.rect.topleft[1]-self.ts
                            )
            case 'down':
                self.text3.show(window,
                            self.rect.bottomright[0]-self.ts+25,
                            self.rect.bottomleft[1]+self.ts-25
                            )
            case _:
                raise Exception(f'invalid align command -> {self.t3} . use up, down or side as command')
#-----------------------------