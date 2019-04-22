##### START MY CODE
from detectPitches2 import recordPitchFromInput
from main import jpg2pitches
import time
import tkinter.filedialog
# from tkthread import tk, TkThread
from tkinter import *


# threading code adapted from https://pythonprogramming.net/threading-tutorial-python/
import threading
from queue import Queue
import time

print_lock = threading.Lock()

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()
        
        # Run the example job with the avail worker in queue (thread)
        exampleJob(worker)
        
        # completed with the job
        q.task_done()

# Create the queue and threader 
q = Queue()

def beats2duration(beats, tempo):
    return beats * 60 / tempo
    
def pitchIsClose(recorded, target):
    tolerance = 30
    return abs(float(recorded) - float(target)) <= tolerance

# colors
RED = "#b80c09"
BLUE = "#0b4f6c"
CYAN = "#01baef"
WHITE = "#fbfbff"
BLACK = "#040f16"
GRAY = "#d3d3d3"
DGRAY = "#afaeae"
LGRAY = "#eaeaea"

# # adapted from https://github.com/serwy/tkthread/blob/master/demo/progress.py
# root = tk.Tk()
# tkt = TkThread(root)  # make the thread-safe callable
# 
# def runThread(func, name=None):
#     threading.Thread(target=func, name=name).start()
# 
# ent_sync = tk.Entry(root)
# ent_sync.pack()
# 
# def pause():
#     # block the main thread from executing
#     ent_sync.insert('end', ' block main thread')
#     ent_sync.update()
#     time.sleep(5)
#     
def threader(q, file):
    q.put(jpg2pitches(file))
# root.after(2500, pause)

def init(data):
    data.buttonWidth = data.width//8
    data.buttonHeight = data.width//16
    data.tempo = 120
    data.mode = "gameMode"
    data.goalPitches = []
    data.loadingText = ""#Click, then wait while we\nconvert your file."
    data.tuneText = "This is tune mode.\nClick play to begin."
    data.backWidth = data.width//8
    data.backHeight = data.height//16
    data.featureSize = data.width//20
    data.widthMargin = data.width//20
    data.tunePause = True
    data.gamePause = True
    data.tuneTimer = 0
    
def loadImages(data):
    bg = "/Users/emma/Documents/15-112/112tp/code/resources/samples/testytesty.gif"
    return bg
    
def mousePressed(event, data):
    if data.mode == "startPage":
        startMousePressed(event, data)
    elif data.mode == "loadingMode":
        loadingMousePressed(event, data)
    elif data.mode == "tuneMode":
        tuneMousePressed(event, data)
    elif data.mode == "gameMode":
        gameMousePressed(event, data)

def keyPressed(event, data):
    pass

def timerFired(data):
    if data.mode == "startPage":
        startTimerFired(data)
    elif data.mode == "loadingMode":
        loadingTimerFired(data)
    elif data.mode == "tuneMode":
        tuneTimerFired(data)
    elif data.mode == "gameMode":
        gameTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "startPage":
        startRedrawAll(canvas, data)
    elif data.mode == "loadingMode":
        loadingRedrawAll(canvas, data)
    elif data.mode == "tuneMode":
        tuneRedrawAll(canvas, data)
    elif data.mode == "gameMode":
        gameRedrawAll(canvas, data)
     
##### START SCREEN MODE #####
def startRedrawAll(canvas, data):
    # title
    canvas.create_rectangle(0, 0, data.width, data.height, fill=CYAN)
    canvas.create_text(data.width//2, data.height//6, text="Violin Hero", font="Arial 30")
    # tune mode
    canvas.create_rectangle(data.width//4 - data.buttonWidth, 
        data.height//2 - data.buttonHeight, data.width//4 + data.buttonWidth, 
        data.height//2 + data.buttonHeight, fill=BLUE)
    canvas.create_text(data.width//4, data.height//2, text="Tune Mode", font="Arial 20")
    # game mode
    canvas.create_rectangle(3*data.width//4 - data.buttonWidth,
    data.height//2 - data.buttonHeight, 3*data.width//4 + data.buttonWidth,
    data.height//2 + data.buttonHeight, fill=RED)
    canvas.create_text(3*data.width//4, data.height//2, text="Game Mode", font="Arial 20")
    
    
def startMousePressed(event, data):
    # tune mode
    if data.width//4 - data.buttonWidth <= event.x <= data.width//4 + data.buttonWidth \
    and data.height//2 - data.buttonHeight <= event.y <= data.height//2 + data.buttonHeight:
        if len(data.goalPitches) < 1:
            data.mode = "loadingMode"
    # game mode
    elif 3*data.width//4 - data.buttonWidth <= event.x <= 3*data.width//4 + data.buttonWidth \
    and data.height//2 - data.buttonHeight <= event.y <= data.height//2 + data.buttonHeight:
        if len(data.goalPitches) < 1:
            data.mode = "loadingMode"
            
def startTimerFired(data):
    pass

##### LOADING SCREEN MODE #####
def loadingRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill=CYAN)
    canvas.create_text(data.width//2, data.height//2, 
        text=data.loadingText, font="Arial 20")
    canvas.create_rectangle(0, 0, data.backWidth, data.backHeight, fill=RED)
    canvas.create_text(data.backWidth//2, data.backHeight//2, text="Back", font="Arial 16")
    canvas.create_rectangle(data.width//2 - data.buttonWidth, data.height//2 - data.buttonHeight, data.width//2 + data.buttonWidth, data.height//2 + data.buttonHeight, fill=BLUE)
    canvas.create_text(data.width//2, data.height//2, text="Select a file", font="Arial 14")
    
def loadingMousePressed(event, data):
    if 0 <= event.x <= data.backWidth and 0 <= event.y <= data.backHeight:
        # back button was pressed
        data.mode = "startPage"
    elif data.width//2 - data.buttonWidth <= event.x <= data.width//2 + data.buttonWidth \
    and data.height//2 - data.buttonHeight <= event.y <= data.height//2 + data.buttonHeight:
        # this line from https://stackoverflow.com/questions/16798937/creating-a-browse-button-with-tkinter
        try:
            # root = Tk()
            file =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            print(file)
            if len(data.goalPitches) < 2:
                # data.goalPitches = jpg2pitches(file)
                # adapted from https://stackoverflow.com/questions/2846653/how-to-use-threading-in-python
                q.put(file)
                t = threading.Thread(target=threader, args=(q, file))
                t.daemon = True
                t.start()
                data.goalPitches = q.get()
                # q.put(0)
                # q.join()
                ##### thread.start -- make file run independently of tkinter -- start new threads for all of them
        except:
            print("Wrong file type. Try again.")
        data.mode = "tuneMode"
    # else: 
    #     if len(data.goalPitches) < 2:
    #         data.goalPitches = \
    #         jpg2pitches("/Users/emma/Documents/15-112/112tp/code/resources/samples/fire.jpg")
    #     data.mode = "tuneMode"
    
def loadingTimerFired(data):
    pass
    
##### TUNE MODE #####
def tuneRedrawAll(canvas, data):
    # image = \
    #     PhotoImage(file="/Users/emma/Documents/15-112/112tp/code/resources/samples/testytesty.gif")
    # canvas.create_image(data.width//2, data.height//2, image=image)
    canvas.create_rectangle(0, 0, data.width, data.height, fill=WHITE)
    canvas.create_text(data.width//2, data.height//2, 
        text = data.tuneText, font="Arial 20")
    # back button
    canvas.create_rectangle(0, 0, data.backWidth, data.backHeight, fill=RED)
    canvas.create_text(data.backWidth//2, data.backHeight//2, text="Back", font="Arial 16")
    # features bar
    canvas.create_rectangle(0, 8.5*data.height//10, data.width, data.height, fill=GRAY)
    # pause/play button
    if data.tunePause:
        # play button
        canvas.create_oval(data.width//2 - data.featureSize, 9.25*data.height//10 - data.featureSize, data.width//2 + data.featureSize, 9.25*data.height//10 + data.featureSize, fill=LGRAY)
        canvas.create_polygon(data.width//2 - data.featureSize//2.5, 9.25*data.height//10 - data.featureSize//2, data.width//2 - data.featureSize//2.5, 9.25*data.height//10 + data.featureSize//2, data.width//2 + data.featureSize//1.5, 9.25*data.height//10, fill=BLACK)
    else:
        # pause button
        canvas.create_oval(data.width//2 - data.featureSize, 9.25*data.height//10 - data.featureSize, data.width//2 + data.featureSize, 9.25*data.height//10 + data.featureSize, fill=LGRAY)
        canvas.create_rectangle(data.width//2 - data.featureSize//2, 9.25*data.height//10 - data.featureSize//2, data.width//2 - data.featureSize//6, 9.25*data.height//10 + data.featureSize//2, fill=BLACK)
        canvas.create_rectangle(data.width//2 + data.featureSize//2, 9.25*data.height//10 - data.featureSize//2, data.width//2 + data.featureSize//6, 9.25*data.height//10 + data.featureSize//2, fill=BLACK)
        
        
def tuneMousePressed(event, data):
    if 0 <= event.x <= data.backWidth and 0 <= event.y <= data.backHeight:
        # back button was pressed
        data.mode = "startPage"
    elif data.width//2 - data.featureSize <= event.x <= data.width//2 + data.featureSize \
    and 9.25*data.height//10 - data.featureSize <= event.y <= 9.25*data.height//10 + data.featureSize:
        data.tunePause = not data.tunePause
                    
def tuneTimerFired(data):
    data.tuneTimer += 1
    if not data.tunePause:
        for pitch in data.goalPitches:
            dur = beats2duration(int(pitch[1]), data.tempo)
            print("dur", dur)
            inPitch = recordPitchFromInput(dur)
            if pitchIsClose(inPitch, pitch[0]):
                print("Nailed it!")
                data.tuneText = "Nailed it!"
            else:
                print("Oof, pretty off there.")
                data.tuneText = "Oof, pretty off there."
                    
                    
##### GAME MODE #####

def gameRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill=BLUE)
    # back button
    canvas.create_rectangle(0, 0, data.backWidth, data.backHeight, fill=RED)
    canvas.create_text(data.backWidth//2, data.backHeight//2, text="Back", font="Arial 16")
    # features bar
    canvas.create_rectangle(0, 8.5*data.height//10, data.width, data.height, fill=GRAY)
    # pause/play button
    if data.gamePause:
        # play button
        canvas.create_oval(data.width//2 - data.featureSize, 9.25*data.height//10 - data.featureSize, data.width//2 + data.featureSize, 9.25*data.height//10 + data.featureSize, fill=LGRAY)
        canvas.create_polygon(data.width//2 - data.featureSize//2.5, 9.25*data.height//10 - data.featureSize//2, data.width//2 - data.featureSize//2.5, 9.25*data.height//10 + data.featureSize//2, data.width//2 + data.featureSize//1.5, 9.25*data.height//10, fill=BLACK)
    else:
        # pause button
        canvas.create_oval(data.width//2 - data.featureSize, 9.25*data.height//10 - data.featureSize, data.width//2 + data.featureSize, 9.25*data.height//10 + data.featureSize, fill=LGRAY)
        canvas.create_rectangle(data.width//2 - data.featureSize//2, 9.25*data.height//10 - data.featureSize//2, data.width//2 - data.featureSize//6, 9.25*data.height//10 + data.featureSize//2, fill=BLACK)
        canvas.create_rectangle(data.width//2 + data.featureSize//2, 9.25*data.height//10 - data.featureSize//2, data.width//2 + data.featureSize//6, 9.25*data.height//10 + data.featureSize//2, fill=BLACK)
    # keys
    for i in range(4):
        canvas.create_rectangle(data.widthMargin + (data.width//4)*i, 7.5*data.height//10, (data.width//4)*(i+1) - data.widthMargin, 8*data.height//10, outline=WHITE, width=data.width//100)
    
def gameMousePressed(event, data):
    if 0 <= event.x <= data.backWidth and 0 <= event.y <= data.backHeight:
        # back button was pressed
        data.mode = "startPage"
    elif data.width//2 - data.featureSize <= event.x <= data.width//2 + data.featureSize \
    and 9.25*data.height//10 - data.featureSize <= event.y <= 9.25*data.height//10 + data.featureSize:
        data.gamePause = not data.gamePause
        
def gameTimerFired(data):
    pass

##### RUN FUNCTION #####

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(650, 650)
##### END MY CODE