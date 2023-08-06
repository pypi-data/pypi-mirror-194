from pygamergui import window
from pygamergui import tools
import pygamergui
from rich import print,inspect

def b1test(args):
    t1.text="use"
def b2test(args):
    t1.text="hello"


b1=tools.simple_button(target=b1test,
                  text='use',
                  fg='white',
                  w=75,
                  h=50,
                  color=(0,175,250),
                  args=[1]
                  )

b2=tools.simple_button(target=b2test,
                  fg='white',
                  text="hello",
                  w=100,
                  h=50,
                  color=(0,175,250)
                  )

t1=tools.text("what to use??")

r1=tools.button_radio(radius=30,color='cyan')

s1=tools.slider(300,
                550,
                h=10,
                corner_round=10,
                color='purple',
                t1_align='side',
                text_size=20,
                )

def update():
    b1.show_no_anemi(200,400,window=windowm,corner_round_level=10)
    b2.show_color_change(300,400,window=windowm,corner_round_level=10)

    t1.show(windowm,175,175)

    r1.show(windowm,300,300)

    a=s1.show(windowm)
windowm=window.app(title='test',bgcolor=(40,40,40),target=update,update_rate=10)
windowm.run()