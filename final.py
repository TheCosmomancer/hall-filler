from tkinter import *
class Person :
    def __init__ (self,name,health,intrest,speaker,mobility):
        self.name = name
        self.health = health #healthy, suspect, sick
        self.intrest = intrest #math, AI, art, economy
        self.speaker = speaker #True, False
        self.mobility = mobility #0, 1, 2
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
    maxes = [item for item in scores if item[2] == max[2]]
    if len(maxes) > 1:
        for item in maxes:
            #check if sick and near edges
            if newGuest.health != "healthy":
                if not (3<item[1]<6):
                    item[2] -= 2
                if  item[0] > 5:
                    item[2] -=2
            else:
                if item[0] < 6:
                    item[2] -=1
            #check if not speaker and in speaker seats
            if newGuest.speaker != "yes":
                print(1)
                if item[0] == 9 or item[1] == 0 or item[1] == 9:
                    print(2)
                    item[2] -= 5
            # check if not disabled and in disabled seats
            if newGuest.mobility == "0":
                if item[1] == 0 or item[1] == 9:
                    item[2] -= 5
        max = maxes[0]
        for i in range(1,len(maxes)):
            if maxes[i][2] > max[2]:
                max = maxes[i]
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
        auth = int(guest.mobility)
        if guest.speaker == "yes" and guest.mobility == "0":
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
    if y != 0 and y != 9:
        score -= 5*int(guest.mobility)
    return score
    
                         
def main():
    hall=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    hallButton=[[None,None,None,None,None,None,None,None,None,None] for x in range(10)]
    helperOpen = [False]

    def mkGuest(hall):
        newGuest = Person(name=newName.get(),health=newHealth.get(),intrest=newInterest.get(),speaker=newSpeaker.get(),mobility=newmobility.get())
        if newGuest.health == "healthy" or newGuest.health == "suspect" or newGuest.health == "sick":
            if newGuest.intrest == "math" or newGuest.intrest == "ai" or newGuest.intrest == "art" or newGuest.intrest == "economy":
                if newGuest.speaker == "yes" or newGuest.speaker == "no":
                    if newGuest.mobility == "0" or newGuest.mobility == "1" or newGuest.mobility == "2":
                        hall,x,y = mahan(newGuest,hall)
                        hallButton[x][y].config(text=f"{x*10}{y}\n{newGuest.name}")
    def openhelper(x,y,helperOpen):
        def closehelper():
            helperWindow.destroy()
            helperOpen[0] = False
        if helperOpen[0] == False and hall[x][y] != None:
            helperOpen[0] = True
            helperWindow = Toplevel(mainWindow)
            Label(helperWindow,text=f"name: {hall[x][y].name}").pack()
            Label(helperWindow,text=f"health status: {hall[x][y].health}").pack()
            Label(helperWindow,text=f"intrest: {hall[x][y].intrest}").pack()
            Label(helperWindow,text=f"is speaker: {hall[x][y].speaker}").pack()
            Label(helperWindow,text=f"mobility: {hall[x][y].mobility}").pack()
            Button(helperWindow,text="close",command=closehelper).pack()

    mainWindow = Tk()
    for i in range(10):
        for j in range(10):
            hallButton[i][j] = Button(mainWindow,text=f"{i*10}{j}\nempty",command=lambda i=i,j=j: openhelper(i,j,helperOpen))
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
    Label(text='does the guest use a wheelchair or a cane to walk?\n("0" for none, "1" for cane, "2" for wheelchair)').grid(row = 14,column=10)
    newmobility = Entry(mainWindow,font = ('Arial',15))
    newmobility.grid(row = 14,column=11)
    mknewButton = Button(mainWindow,text='add guest',command=lambda:mkGuest(hall))
    mknewButton.grid(row = 15,column=10)
    mainWindow.mainloop()
if __name__ == "__main__":
    main()