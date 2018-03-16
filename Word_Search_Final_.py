# -*- coding: utf-8 -*-
import itertools
from random import randint,choice
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
        
        self.label1 = Label(master,text="Enter the Words (put a '-' between every word) ")
        #self.label1.place(x=10,y=10,width=250,height=20)
        self.label1.grid(column=0,sticky=W)
        
        self.entry1 = Entry(master)
        #self.entry1.place(x=270,y=10,width=100,height=20)
        self.entry1.grid(row=0,column=1)
        
        self.label2 = Label(master,text="Enter the Size :")
        #self.label2.place(x=10,y=40,width=100,height=20)
        self.label2.grid(row=1,column=0,sticky=W)
        
        self.entry2 = Entry(master)
        #self.entry2.place(x=270,y=40,width=100,height=20)
        self.entry2.grid(row=1,column=1)
        
        self.label3 = Label(master,text="Difficulty :(Easy or Difficult)")
        #self.label3.place(x=10,y=70,width=100,height=20)
        self.label3.grid(row=2,column=0,sticky=W)
        
        self.entry3 = Entry(master)
        #self.entry3.place(x=270,y=70,width=100,height=20)
        self.entry3.grid(row=2,column=1)
        
        self.button = Button(master,text="Generate",command=self.getText)
        #self.button.place(x=320,y=70,width=50,height=20)
        self.button.grid(row=3,columnspan=2)

    def random_letter(self): #This function generates a random letter to fill the spots that doesn't contain the words.
        r = randint(0,25) #This generates a random number between 0 and 25.
        return chr(ord("A")+r) #I use that number to randomly choose a letter from the alphabet.

    def fit_possible(self,L,X,Y,l,dX,dY): #This function tests if the given word 'l' can fill the position starting from the index(X,Y)and going in the direction that implies dX,dY. 
        if X+dX*len(l) >len(L) or X+dX*len(l) < 0 or Y+dY*len(l) >len(L)or Y+dY*len(l) < 0 :            
            return False
        for i in range(len(l)) :
            if L[X+dX*i][Y+dY*i] != "*"and L[X+dX*i][Y+dY*i] != l[i] :  #If the given position isn't blank or contains a different letter then we can't put the word in that position.
                return False
        return True

    def getText(self):
        W = self.entry1.get() #this variable takes the string containg the words.
        D = self.entry3.get() #this variable takes the difficulty given.
        val = self.entry2.get()
        
        if D == "" or W == "" or val == "":
            tkinter.messagebox.showerror("Error","All inputs are required")
            return None
        
        if D.lower() != "easy" and D!="difficult" : #Display an error if there is a mistake in writing the difficulty.
            tkinter.messagebox.showerror("Error","Choose the difficulty")
            return None
        try:
            val = int(self.entry2.get())
        except ValueError: #Display an error if the size entered isn't an integer.
            tkinter.messagebox.showerror("Error","The size should be an integer")
            return None
        
        n = int(self.entry2.get()) #This variable takes the size of the grid.
        W = W.split("-") #Transforrm the string into a list of words.
        W = [word.upper()
             for word in W]  #Making sure that the words are all upper case.
        L=[["*" for k in range(n)]
                   for i in range(n)] #inittiate with a blank grid.
        LL=[] #This list record the steps made by the program.
        i=0
        while i<len(W) :
            LL.append(L) #whenever L changes append it to LL to later backtrack our steps.
            fit = False 
            P = [[h for h in range(len(L))]
                    for j in range(2)]
            com = list(itertools.product(*P)) #this is a list of the positions on the grid.
            while (not fit) and com != [] : #This loop ends when the word fits or that we test all the position and noone checked.
                X,Y = choice(com) #I choose a random position on the grid.
                com.remove((X,Y)) #Then i remove it so i don't run it twice.
                if D.lower() == "easy" : #If the user choose the easy difficulty the words are filled either vertically or horizontally.
                    R = [[0,1],[0,1]]
                    comR = list(itertools.product(*R))
                    comR.remove((0,0))
                    comR.remove((1,1))
                if D.lower() == "difficult" : #If the user choose difficult the words are filled either vertically or horizontally or diagonaly
                    R = [[-1,0,1],[-1,0,1]]
                    comR = list(itertools.product(*R))
                    comR.remove((0,0))
                while comR !=[] and not fit : #here we try the directions based on the difficulty chosen by the user.
                    dX,dY = choice(comR)
                    comR.remove((dX,dY))
                    fit =  self.fit_possible(L,X,Y,W[i],dX,dY)
                    #print(str(fit)+W[i])
            if com==[] and not fit: #If the word doesn't fit in any position we backtrack our step and chenge the position of the previous word.
                i-=1
                if i<0 or LL[-1]==L: #If we reached the first word and it didn't fit then we can't generate the grid.
                    tkinter.messagebox.showerror("Error","Try less words or a bigger size")
                    return None
                L = LL[i]
                LL = LL[:-1]
                continue
            for k in range(len(W[i])): #If the word fits we fill in the given position and direction.
                L[X+dX*k][Y+dY*k] = W[i][k]
            i+=1
        for i in range(len(L)) : # After filling all the words we fill the blanks with random letters.
            for k in range(len(L[i])) :
                if L[i][k] == "*":
                    L[i][k]=self.random_letter()
        for i in range(n): #I use the labels to display the grid.
            for k in range(n) :
                label = Label(self.master,text=L[i][k])
                label["width"] = 3
                label.grid(row=i+5,column=k+3,sticky="w")
        label0 = Label(self.master,text="The list of words :") #here i show the list of words chosen.
        label0.grid(row=4,column=0)
        for i in range(len(W)):
            label = Label(self.master,text=W[i])
            label["width"] = 10
            label.grid(row=i+5,column=0)



if __name__ == "__main__":
    root = Tk() #here i added the labels and the entries shown in the interface initially.
    app = GUI(master=root)
    app.mainloop()