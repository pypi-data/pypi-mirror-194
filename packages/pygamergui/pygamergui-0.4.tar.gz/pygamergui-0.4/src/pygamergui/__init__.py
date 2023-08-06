#Checking modules
try:
 import pygame
 import rich
except Exception:
    raise Exception("pygame OR Rich not installed please install it first")
#---------------------

#importing needed modules
from rich.console import Console
import pygame
#------------------------

#printing the message
cons=Console()
cons.print("[green]Hello from pygamer [red] Thank for using my module[/red] [/green]")
cons.print("[green]if you like it [red] do support it by suscribing my youtube channel [/red] [/green]")
cons.print("[green]Youtube:->[red]https://www.youtube.com/channel/UCNj9jZBVxRWm7TA5g2K7XtA [/red] [/green]")
#----------------------