from tkinter import *
from classes import Person
def mahan(newGuest,hall):
    return hall
def main():
    hall=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    hallButton=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    helperOpen = False
    hall[0][0] = Person(name="mahan",health="healthy",intrest="ai",speaker="no",sensitivity="0")
    
    def mkGuest():
        newGuest = Person(name=newName.get(),health=newHealth.get(),intrest=newInterest.get(),speaker=newSpeaker.get(),sensitivity=newSensitivity.get())
        if (newGuest.health == ("healthy" or "suspect" or "sick")) and (newGuest.intrest == ("math" or "ai" or "art" or "economy")) and (newGuest.speaker == ("yes" or "no")) and (newGuest.sensitivity == ("0" or "1" or "2")):
            hall = mahan(newGuest,hall)
            refresh()
        def refresh():
            ...
    def openhelper(x,y):
        def closehelper():
            helperWindow.destroy()
            helperOpen = False
        if helperOpen == False and hall[x][y] != None:
            helperOpen = True
            helperWindow = Toplevel(mainWindow)
            Label(helperWindow,text=f"name: {hall[x][y].name}").place()
            Label(helperWindow,text=f"health status: {hall[x][y].health}").place()
            Label(helperWindow,text=f"intrest: {hall[x][y].intrest}").place()
            Label(helperWindow,text=f"is speaker: {hall[x][y].speaker}").place()
            Label(helperWindow,text=f"sensitivity: {hall[x][y].sensitivity}").place()
            Button(helperWindow,text="close",command=closehelper)

    mainWindow = Tk()
    margin = 30
    for i in range(10):
        for j in range(10):
            hallButton[i][j] = Button(mainWindow,text=f"{i*10}{j}\nu",command=lambda: openhelper(i,j))#,width=margin,height=margin)
            hallButton[i][j].grid(row=i,column = j)
    hallButton[0][0].config(text="00\nmahan")
    Label(text="enter name: ").grid(row = 10,column=10)
    newName = Entry(mainWindow,font = ('Arial',15))
    newName.grid(row = 10,column=11)
    Label(text="enter health state: (healthy, suspect, sick)").grid(row = 11,column=10)
    newHealth = Entry(mainWindow,font = ('Arial',15))
    newHealth.grid(row = 11,column=11)
    Label(text="enter interest : (math, ai, art, economy)").grid(row = 12,column=10)
    newInterest = Entry(mainWindow,font = ('Arial',15))
    newInterest.grid(row = 12,column=11)
    Label(text="will the guest be speaking? (yes/no)").grid(row = 13,column=10)
    newSpeaker = Entry(mainWindow,font = ('Arial',15))
    newSpeaker.grid(row = 13,column=11)
    Label(text="how sensitive is the guest? (0, 1, 2)").grid(row = 14,column=10)
    newSensitivity = Entry(mainWindow,font = ('Arial',15))
    newSensitivity.grid(row = 14,column=11)
    mknewButton = Button(mainWindow,text='add guest',command=mkGuest)
    mknewButton.grid(row = 15,column=10)
    mainWindow.mainloop()
if __name__ == "__main__":
    main()