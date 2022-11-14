from tkinter import Tk
from utils.constants.constant import BGIMG, WIDTH, HEIGHT, TITLE
from App import App

client = Tk()
client.title(TITLE)
client.configure(background=BGIMG)
client.geometry(f"{WIDTH}x{HEIGHT}")
app = App(client)
app.initializeUI()
client.mainloop()