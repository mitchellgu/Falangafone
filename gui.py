#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import Frame, Button, Style


class LeapMusic(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def initUI(self):

        self.parent.title("LeapMusic")
        self.pack(fill=BOTH, expand=1)

        #playButton = Button(self, text="Play",
        #    command=)
        #pauseButton = Button(self, text="Pause",
        #    command=)
        playButton = Button(self, text="Play")
        pauseButton = Button(self, text="Pause")
        heightLabel = Label(self, text="Height: ")
        volumeLabel = Label(self, text="Volume: ")
        distanceLabel = Label(self, text="Distance Between Hands: ")
        speedLabel= Label(self, text="Music Speed: ")
        playButton.pack(side = BOTTOM, fill=X,padx=10)
        pauseButton.pack(side = BOTTOM, fill=X,padx=10)
        heightLabel.pack(padx=5, pady=10, side=LEFT)
        volumeLabel.pack(padx=5, pady=10, side=LEFT)
        distanceLabel.pack(padx=5, pady=10, side=LEFT)
        speedLabel.pack(padx=5, pady=10, side=LEFT)



def main():

    root = Tk()
    root.geometry("500x500")
    app = LeapMusic(root)
    root.mainloop()


if __name__ == '__main__':
    main()
