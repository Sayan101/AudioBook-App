import pyttsx3
import threading
import PyPDF2
from tkinter import *
from tkinter import ttk
#from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import pygame
from pygame import mixer
from ttkthemes import themed_tk as tk

#function to get a PDF file to read
pdfReader=''
def fetchPDF():

    book=askopenfile(mode="rb" ,filetypes =[('PDF Files', '*.pdf')])
    if book is not None:
        book_selected['text']="Book Selected"
        global pdfReader
        pdfReader=PyPDF2.PdfFileReader(book)
        pages=pdfReader.getNumPages()
        print(pages)
        return pdfReader
    else:
        print("File not selected")



def readPage():

    page_num_str=pageNumInput.get()
    page_num=int(page_num_str)
    pages=pdfReader.getNumPages()

    if page_num in range(1,pages):
        page=pdfReader.getPage(page_num)
        text=page.extractText()
        print(type(text))
        #running the pyttsx3 as a new thread so that the tkinter window does not freze
        #passigntext as an tuple notice the ',' else the string is treated as an iterable and each letter is consiodered
        th=threading.Thread(target=run_pyttsx3, args=(text,))
        th.start()
    else:
        print("Page number does not exist")
        th=threading.Thread(target=run_pyttsx3, args=("Page number does not exist",))
        th.start()

def onWord(name, location, length):
    print ('word', name, location, length)
    if keyboard.is_pressed("esc"):
        engine.stop()

#start utterance
def run_pyttsx3(text):
    engine=pyttsx3.init()
    engine.setProperty('rate', 200)
    #th=threading.Thread(target=engine.connect,args=('started-word',onWord,))
    #th.start()
    engine.connect('started-word', onWord)
    engine.say(text)
    engine.runAndWait()

def savePDFtoMP3():
    pages=pdfReader.getNumPages()
    entire_text=''
    print("Conversion started")
    for i in range(1,pages):
        page=pdfReader.getPage(i)
        text=page.extractText()
        entire_text+=text
    engine=pyttsx3.init()
    #print(entire_text)
    engine.save_to_file(entire_text ,'AudioBook.wav')
    engine.runAndWait()

def listenToEbook():
    mixer.init()
    mixer.music.load('AudioBook.wav')
    mixer.music.play()
def pauseEbook():
    mixer.music.pause()
def stopEbook():
    mixer.music.stop()


# create a tkinter window
root = tk.ThemedTk()
lis=root.get_themes()
print(lis)
# Returns a list of all themes that can be set
root.set_theme("radiance")
root.title("AudioBook Application!")
# Open window having dimension 1000x600
root.geometry('800x500')
nopage=""
# Create a Button
select_book= Button(root, text = 'Select Book',bd = '5',command =lambda:fetchPDF())
#btn2 =Button(root,text='Quit!',bd='5',command=root.destroy)
listen_page =Button(root,text='Listen!',bd='5',command=lambda: readPage())
convert =Button(root,text='Convert!',bd='5',command=lambda: savePDFtoMP3())
#playPhoto = PhotoImage(file='play.png')
play=Button(root,text='play!',bd='5',command=lambda: listenToEbook())
#pausePhoto = PhotoImage(file='pause.png')
pause=Button(root,text='pause!',bd='5',command=lambda: pauseEbook())
#stopPhoto = PhotoImage(file='stop.png')
stop=Button(root,text='stop!',bd='5',command=lambda: stopEbook())
#btn4 =Button(root,text='Play Page',bd='5',command=lambda: submit())

book_selected= Label(root,text='')
book_selected.place(x = 175,y = 50)
enter_page_num= Label(root,text ="Enter the page number you wish to listen to :" ).place(x = 50,y = 100)
convert_label= Label(root,text ="Convert Entire book to Audio:" ).place(x = 50,y = 150)
play_pause_label= Label(root,text ="Play/Pause Audiobook:" ).place(x = 50,y = 200)
pageNumInput= Entry(root,width = 30)


# Set the position of button on the top of window.
#btn.pack(side = 'top')
select_book.place(x=50,y=50)
#btn2.pack(side='bottom')
#btn2.place(x=100,y=100)
listen_page.place(x=600,y=100)
pageNumInput.place(x = 400,y = 100)
convert.place(x=250,y=150)
play.place(x=50,y=250)
pause.place(x=150,y=250)
stop.place(x=250,y=250)
#print(pages)
root.mainloop()
