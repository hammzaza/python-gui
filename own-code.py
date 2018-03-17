# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox
class GUI(Frame):
    def __init__(self, master=None):    # constructor
        super().__init__(master)
        # create/initialize user interface data
        self.master = master
        self.master.geometry("640x480")
        self.master['width'] = 640
        self.master['height'] = 480
        self.master['padx'] = 10
        self.master['pady'] = 10
        self.master['bg'] = '#cecece'
        self.master.title('Word Search Puzzle')
        #gui created ^

        self.label1 = Label(master,text="Enter the Words (put a '-' between every word) ")

        self.label1.grid(column=0,sticky=W)

        self.entry1 = Entry(master)

        self.entry1.grid(row=0,column=1) #input to insert words like john-james etc which are to be displayed in the list.

        self.label2 = Label(master,text="Enter the Size :")

        self.label2.grid(row=1,column=0,sticky=W)

        self.entry2 = Entry(master)

        self.entry2.grid(row=1,column=1)

        self.label3 = Label(master,text="Difficulty :(Easy or Difficult)")

        self.label3.grid(row=2,column=0,sticky=W)

        self.entry3 = Entry(master) #input for getting difficulty.

        self.entry3.grid(row=2,column=1)

        self.button = Button(master,command=self.generateevent,text="Generate")

        self.button.grid(row=3,columnspan=2)

        # creates labels with 3 inputs. ^
    def generateevent(self):
        try:
            val = int(self.entry2.get())
        except ValueError:  #Display an error if the size entered isn't an integer.
            tkinter.messagebox.showerror("Error", "The size should be an integer")
            return None
        words = self.entry1.get()
        words = words.split("-")
        maxlength = self.getmaxlength(words)
        size = int(self.entry2.get())

        if size < maxlength:
            tkinter.messagebox.showerror("Error", "The size should be greater than the length of the words")
            return None

        difficulty = self.entry3.get()

        if (difficulty != 'easy') and (difficulty !='difficult'):
            tkinter.messagebox.showerror("Error", "Please enter the correct difficulty")
            return None
        if difficulty =='easy':
            self.easydifficulty(words,maxlength)
        #errors handled^^


    def getmaxlength(self,words):
        maxlength = 0
        for word in words:
            if maxlength <= len(word):
                maxlength = len(word)
        return maxlength
    def easydifficulty(self,words,maxlength):
        gridd = [[' ' for x in range(maxlength +1)] for y in range(maxlength+1)]
        
        # for i in range(0,maxlength+1):
        #     for j in range(0,maxlength+1):
        #         Label(text=gridd[i][j], width=3).grid(row=i+10,column=j+10)


if __name__ == "__main__":
    root = Tk()
    app = GUI(master=root)
    app.mainloop()