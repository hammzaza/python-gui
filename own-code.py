# -*- coding: utf-8 -*-
from random import randint
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
        self.label3 = Label(master, text="Show Solution or Not? Y or N")
        self.label3.grid(row=3, column=0, sticky=W)

        self.entry4 = Entry(master)  #input for getting difficulty.

        self.entry4.grid(row=3, column=1)

        self.button = Button(master,command=self.generateevent,text="Generate")

        self.button.grid(row=4, columnspan=2)


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
        gridd = [['*' for x in range(size)] for y in range(size)]
        if (difficulty != 'easy') and (difficulty !='difficult'):
            tkinter.messagebox.showerror("Error", "Please enter the correct difficulty")
            return None

        elif difficulty =='easy':
            gridd = self.easydifficulty(words,size,gridd)
        elif difficulty =='difficult':
            gridd = self.harddifficulty(words,size,gridd)
        choice = self.entry4.get();
        if choice== 'Y' :
            self.showresults(gridd,size)
        else:
            self.showgrid(gridd,size)
    def showgrid(self,gridd,size):
        for i in range(0, size):
            for j in range(0, size):
                r = randint(0, 25)
                if (gridd[i][j] == '*'):
                    Label(
                        text=chr(ord("A") + r), width=3).grid(row=i + 5, column=j + 5, sticky=W, pady=5, padx=5)
                else:
                    Label(
                        text=gridd[i][j].upper(), width=3).grid(row=i + 5, column=j + 5, sticky=W, pady=5, padx=5)

    def showresults(self,gridd,size):
        for i in range(0, size):
            for j in range(0, size):
                r = randint(0, 25)
                if (gridd[i][j] == '*'):
                    Label(
                        text=chr(ord("A") + r), width=3).grid(row=i + 5, column=j + 5, sticky=W, pady=5, padx=5)
                else:
                    Label(text=gridd[i][j].upper(), width=3,bg="yellow").grid(row=i + 5, column=j + 5, sticky=W, pady=5, padx=5)

    def getmaxlength(self,words):
        maxlength = len(words[0])
        for word in words:
            if maxlength <= len(word):
                maxlength = len(word)
        return maxlength

    def getrandom(self,max):
        if max == 0:
            return 0
        return randint(0,(max-1))
    def easydifficulty(self,words,size,gridd):

        x = 0
        while(x < len(words)):
            rand = randint(1, 3)
            #print(range(0,size-len(word)))
            if rand == 1:
                #horizontally
                randrow = self.getrandom(size)
                randcol = self.getrandom(size-len(words[x]))
                if(self.checkforrow(randrow,randcol,gridd,len(words[x]))):
                    gridd = self.savewordrow(randrow,randcol,gridd,words[x],size)
                    x=x+1
            else:
                #vertically
                randrow = self.getrandom(size - len(words[x]))
                randcol = self.getrandom(size)
                if (self.checkforcol(randrow, randcol, gridd, len(words[x]))):
                    gridd = self.savewordcol(randrow, randcol, gridd,words[x], size)
                    x=x+1
        return gridd

    def harddifficulty(self, words, size,gridd):
        gridd = [['*' for x in range(size)] for y in range(size)]
        x = 0
        while (x < len(words)):
            rand = randint(1,3);
            if rand == 1:
                #horizontal
                randrow = self.getrandom(size)
                randcol = self.getrandom(size - len(words[x]))
                if (self.checkforrow(randrow, randcol, gridd, len(words[x]))):
                    gridd = self.savewordrow(randrow, randcol, gridd, words[x],size)
                    x = x + 1
            elif rand == 2:
                #vertical
                randrow = self.getrandom(size - len(words[x]))
                randcol = self.getrandom(size)
                if (self.checkforcol(randrow, randcol, gridd, len(words[x]))):
                    gridd = self.savewordcol(randrow, randcol, gridd, words[x],size)
                    x = x + 1
            else:
                #diagnal
                randrow = self.getrandom(size - len(words[x]))
                randcol = self.getrandom(size - len(words[x]))
                if (self.checkfordiagnal(randrow, randcol, gridd, len(words[x]))):
                    gridd = self.saveworddiag(randrow, randcol, gridd, words[x],size)
                    x = x + 1
        return gridd

    def checkfordiagnal(self,row,col,gridd,size):
        check=True
        for i in range(0,size):
            if gridd[row+i][col+i] != '*':
                check= False
        return check
    def saveworddiag(self,row,col,grid,word,size):
        x=0
        while(x < len(word)):
            grid[row+x][col+x] = word[x]
            x=x+1
        return grid
    def checkforrow(self,row,col,gridd,size):
        check=True
        for i in range(0,size):
            if gridd[row][col+i] != '*':
                check = False
                break
        return check
    def checkforcol(self, row, col, gridd, size):
        check=True
        for i in range(0,size):
            if gridd[row+i][col] != '*':
                check= False
                break
        return check
    def savewordrow(self,row,col,grid,word,size):
        x=0
        while(x < len(word)):
            grid[row][col+x] = word[x]
            x=x+1
        return grid
    def savewordcol(self,row,col,grid,word,size):
        x=0
        while(x < len(word)):
            grid[row+x][col] = word[x]
            x=x+1
        return grid
if __name__ == "__main__":
    root = Tk()
    app = GUI(master=root)
    app.mainloop()