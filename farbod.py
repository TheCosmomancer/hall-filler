from tkinter import *
class Person :
    def __init__ (self,name,health,intrest,speaker,sensitivity):
        self.name = name
        self.health = health #healthy, suspect, sick
        self.intrest = intrest #math, AI, art, economy
        self.speaker = speaker #True, False
        self.sensitivity = sensitivity #0, 1, 2
def mahan(newGuest,hall):
    scores = []
    for i in range(10):
        for j in range(10):
            if hall[i][j] == None:
                scores.append([i,j,score_seat(hall,newGuest,i,j)])
    max = scores[0]
    for i in range(1,len(scores)):
        if scores[i][2] > max[2]:
            max = scores[i]
    hall[max[0]][max[1]] = newGuest
    return hall,max[0],max[1]
def score_seat(hall,guest,x,y):
    #healthcheck
    score = 0
    if guest.health !="healthy":
        for i in range(-2,3):
            temp = abs(i)
            for j in range(temp-2,3-temp):
                try:
                    if hall[x+i][y+j].health == "healthy":
                        score-=1
                except:
                    pass
        for i in range(-3,4):
            temp = abs(i)
            for j in range(temp-3,4-temp):
                try:
                    if hall[x+i][y+j].speaker == "yes":
                        score-=1
                except:
                    pass
    else:
        auth = int(guest.sensitivity)
        if guest.speaker == "yes" and guest.sensitivity == "0":
            auth += 1
        for i in range(-(2+auth),3+auth):
            temp = abs(i)
            for j in range(temp-(2+auth),3+auth-temp):
                try:
                    if hall[x+i][y+j].health != "healthy":
                        score-=1
                except:
                    pass
    #intrest check
    for i in [-1,1]:
        try:
            if hall[x+i][y].intrest == guest.intrest:
                score+=1
        except:
            pass
        try:
            if hall[x][y+i].intrest == guest.intrest:
                score+=1
        except:
            pass
    #speaker check
    if guest.speaker == "yes":
        if x != 9 and y != 0 and y != 9:
            score -= 5
    #mobilty check
    if y != 0 and y != 0:
        score -= 5*int(guest.sensitivity)
    return score
    
                         
def main():
    hall=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    hallButton=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    helperOpen = False

    def mkGuest(hall):
        newGuest = Person(name=newName.get(),health=newHealth.get(),intrest=newInterest.get(),speaker=newSpeaker.get(),sensitivity=newSensitivity.get())
        if newGuest.health == "healthy" or newGuest.health == "suspect" or newGuest.health == "sick":
            if newGuest.intrest == "math" or newGuest.intrest == "ai" or newGuest.intrest == "art" or newGuest.intrest == "economy":
                if newGuest.speaker == "yes" or newGuest.speaker == "no":
                    if newGuest.sensitivity == "0" or newGuest.sensitivity == "1" or newGuest.sensitivity == "2":
                        hall,x,y = mahan(newGuest,hall)
                        hallButton[x][y].config(text=f"{x*10}{y}\n{newGuest.name}")
    def openhelper(x,y,helperOpen):
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
    for i in range(10):
        for j in range(10):
            hallButton[i][j] = Button(mainWindow,text=f"{i*10}{j}\nu",command=lambda i=i,j=j: openhelper(i,j,helperOpen))
            hallButton[i][j].grid(row=i,column = j)
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
    mknewButton = Button(mainWindow,text='add guest',command=lambda:mkGuest(hall))
    mknewButton.grid(row = 15,column=10)
    mainWindow.mainloop()
if __name__ == "__main__":
    main()