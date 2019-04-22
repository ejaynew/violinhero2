from tkinter import *
import tkinter
import time
import threading
import random
import queue
from queue import Queue

# code adapted from http://code.activestate.com/recipes/82965/ 
# and https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html


class GuiPart:
    def __init__(self, master, queue, endCommand, color):
        self.queue = queue
        # Set up the GUI
        self.color = "blue"
        
        def init(data):
            data.color="blue"
            data.circles = []
            data.bg = "yellow"
        
        def mousePressed(event, data):
            data.circles.append((event.x, event.y, self.color))
        
        def keyPressed(event, data):
            pass
        
        def timerFired(data):
            data.bg = random.choice(["pink", "white", "orange", "purple"])
        
        def redrawAll(canvas, data):
            canvas.create_rectangle(0, 0, data.width, data.height, fill=data.bg)
            for (x, y, color) in data.circles:
                canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=color)
        
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
        class Struct(object): pass
        data = Struct()
        data.width = 300
        data.height = 300
        data.timerDelay = 100 # milliseconds
        root = Tk()
        root.resizable(width=False, height=False) # prevents resizing window
        init(data)
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0)
        canvas.pack()
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, canvas, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, canvas, data))
        timerFiredWrapper(canvas, data)


    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                print("pre color", self.color)
                self.color = msg
                print("entered")
                print("color", self.color)
                print(msg)
            except:
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication, "blue")

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(random.random() * 0.3)
            msg = random.choice(["blue", "purple", "pink", "black"])
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

root = tkinter.Tk()

client = ThreadedClient(root)
root.mainloop()