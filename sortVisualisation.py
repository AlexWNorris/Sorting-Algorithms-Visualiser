from glob import glob
from os import remove
from tokenize import Name
import pygame
from sys import exit
from random import shuffle
from time import sleep
pygame.init()
#visual constants
baseFont = pygame.font.Font(None, 32)
white=255,255,255
black=0,0,0
green=0,255,0
red=255,0,0

#screen 
Sdims=Swidth,Shight=1000,500
screen=pygame.display.set_mode(Sdims)

#user input box
IBW,IBH=200,25
inputBoxRect=pygame.Rect(0.5*(Swidth-IBW),Shight*0.9,IBW,IBH)
IBactive=False
userInput=''
#sorting toggles
bubbleSortRect=pygame.Rect(0.5*(Swidth-IBW)-IBW-5,Shight*0.9,IBW,IBH)
mergSortRect=pygame.Rect(0.5*(Swidth-IBW)+IBW+5,Shight*0.9,IBW,IBH)
bogoSortRect=pygame.Rect(0.5*(Swidth-IBW)+2*(IBW+5),Shight*0.9,IBW,IBH)


#sortables
data=[]
def createBars(UI):
    global data,Swidth,Shight
    data=[]
    try:
        numBars=int(UI)
        for i in range(numBars):
            dataPoint=0.9*((i+1)/numBars)
            data.append(dataPoint)
    except ValueError:
        pass
    shuffle(data)
    drawBars()
    
#redering data bars

def drawBars():
    global data
    numBars=len(data)
    screen.fill(black)
    for i in range(numBars):
        barWidth=Swidth/numBars
        barHeight=Shight*0.9*data[i]    
        rect=pygame.Rect(barWidth*i,(Shight*0.9)-barHeight,barWidth,barHeight)
        pygame.draw.rect(screen,white,rect)
    pygame.display.flip()

def colourBar(index,colour):
    global data
    numBars=len(data)
    barWidth=Swidth/numBars
    barHeight=Shight*0.9*data[index]
    rect=pygame.Rect(barWidth*index,(Shight*0.9)-barHeight,barWidth,barHeight)
    pygame.draw.rect(screen,colour,rect)
    pygame.display.flip()

def checkBars():
    global data,green
    for i in range(len(data)):
        try:
            if data[i]<data[i+1]:
                colourBar(i,green)
                sleep(1.25/len(data))
            else:
                colourBar(i,red)
                break
        except IndexError:
            colourBar(len(data)-1,green)

#sorting algorithms
def bubbleSort():
    global data
    numBars=len(data)
    sorted=False
    while not sorted:
        sorted=True
        try:
            for i in range(len(data)):
                if data[i]>data[i+1]:
                    sorted=False
                    temp=data[i+1]
                    data[i+1]=data[i]
                    data[i]=temp
                drawBars()
        except IndexError:
            pass
            
def mergeSort(Clist):
    global data
    Llist=[]
    Rlist=[]
    middle=int(len(Clist)/2)
    if len(Clist)>1:
        Llist=Clist[:middle]
        Rlist=Clist[middle:]
        Llist=mergeSort(Llist)
        Rlist=mergeSort(Rlist)
        return merge(Llist,Rlist)
    else:
        return Clist

def merge(listA,listB):
    global data
    output=[]
    start=data.index(listA[0])
    while len(listA)>0 or len(listB)>0:
        try:
            if listA[0]<listB[0]:
                output.append(listA[0])
                listA.pop(0)
            else:
                output.append(listB[0])
                listB.pop(0)
        except IndexError:
            if len(listA)==0:
                output+=listB
                listB=[]
            if len(listB)==0:
                output+=listA
                listA=[]
    dataout=len(output)
    for i in range(len(output)):
        data[start+i]=output[i]
    drawBars()
    if len(data)>=100:
        sleep(5/len(data))
    return output


def bogoSort():
    global data
    sorted=False
    while not sorted:
        sorted=True
        shuffle(data)
        drawBars()
        try:
            for i in range(len(data)):
                if data[i]>data[i+1]:
                    sorted=False            
        except IndexError:
            pass
    




#game loop
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: 
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bubbleSortRect.collidepoint(event.pos):
                sleep(0.5)
                bubbleSort()
                checkBars()
            if mergSortRect.collidepoint(event.pos):
                sleep(0.5)
                mergeSort(data)
                checkBars()
            if bogoSortRect.collidepoint(event.pos):
                sleep(0.5)
                bogoSort()
                checkBars()
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_BACKSPACE:
                userInput=userInput[:-1]
            elif event.key==pygame.K_RETURN:
                createBars(userInput)
                userInput=''
            else:
                userInput+=event.unicode 
    
    #render input box
    inputBox=pygame.draw.rect(screen,white,inputBoxRect)
    textSurface=baseFont.render(userInput,True,black)
    screen.blit(textSurface,(inputBoxRect.x+5,inputBoxRect.y+5))
    #render bubble sort toggle
    bubbleSortToggle=pygame.draw.rect(screen,white,bubbleSortRect)
    bubbleSortButtonText=baseFont.render("bubble sort",True,black)
    screen.blit(bubbleSortButtonText,(bubbleSortRect.x+5,bubbleSortRect.y+5))
    #render merg sort toggle
    bubbleSortToggle=pygame.draw.rect(screen,white,mergSortRect)
    mergSortButtonText=baseFont.render("merg sort",True,black)
    screen.blit(mergSortButtonText,(mergSortRect.x+5,mergSortRect.y+5))
    #render bogo sort toggle
    bogoSortToggle=pygame.draw.rect(screen,white,bogoSortRect)
    bogoSortButtonText=baseFont.render("bogo sort",True,black)
    screen.blit(bogoSortButtonText,(bogoSortRect.x+5,bogoSortRect.y+5))
    pygame.display.flip()