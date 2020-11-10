'''
Current Objective: Add a Replay quote functionality
'''

import sqlite3 
from gtts import gTTS 
import os 
from tkinter import *

#    #    # Database Information #    #    #
#####
# Table : Quotes
# -> content
# -> author
#####

def createTable():
    # Create a Database or Connect to One -> Create Cursor
    conn = sqlite3.connect('quoteMe.db')
    c = conn.cursor()

    # Creates Table if it is not already there
    try:
        c.execute("""CREATE TABLE Quotes (   
        content text,
        author text
        )""")
    except sqlite3.OperationalError as er:
        pass
        

    
    #Commit Changes -> Close DB
    conn.commit()
    conn.close()

#    #    # Text to Speech Functionality #    #    #
def txt2speech(text_to_read):
    language = 'en'
    myMP3 = gTTS(text=text_to_read, lang=language, slow=False) 
    myMP3.save("quote.mp3") 

def pull_quote():
    #Create a Database or Connect to One -> Create Cursor
    conn = sqlite3.connect('quoteMe.db')
    c = conn.cursor()

    list_to_read = c.execute("SELECT * FROM Quotes ORDER BY RANDOM() LIMIT 1")    
    format_to_read = c.fetchall()
    global quote_to_read
    quote_to_read = str(format_to_read[0][0])

    #Commit Changes -> Close Database
    conn.commit()
    conn.close()

#    #    # GUI Element Functionalities #    #    #
def playQuote():
    pull_quote()
    txt2speech(quote_to_read)
    os.system("mpg123 quote.mp3")  # Plays Audio
    print(quote_to_read)

def replayQuote():
    os.system("mpg123 quote.mp3")

def submitQuote():
    #Create a Database or Connect to One -> Create Cursor
    conn = sqlite3.connect('quoteMe.db')
    c = conn.cursor()
    
    #Insert Into Table
    c.execute(""" INSERT INTO Quotes Values (:content, :author)
    """,
    {
        'content' : contentEntry.get(),
        'author' : authorEntry.get()
    }
    )

    #Commit Changes -> Close Database
    conn.commit()
    conn.close()
    
    contentEntry.delete(0, END)
    authorEntry.delete(0, END)

def addQuote():
    # Create new window
    global addNew
    addNew = Tk()
    addNew.geometry("350x100")
    addNew.configure(background = 'light blue')
    addNew.title("Add a new Quote")

    # Labels : Creates and Attaches to Window
    contentEntry_label = Label(addNew, text="Paste in the quote")
    contentEntry_label.grid(row=0,column=0)
    authorEntry_label = Label(addNew, text="Type in the author")
    authorEntry_label.grid(row=1,column=0)

    # Entry Boxes
    global contentEntry
    global authorEntry
    contentEntry = Entry(addNew, width=30)
    contentEntry.grid(row=0,column=1)
    authorEntry = Entry(addNew, width=30)
    authorEntry.grid(row=1,column=1)

    # Buttons
    submit_quote_btn = Button(addNew, text="Submit Quote",command=submitQuote, bg="green")
    submit_quote_btn.grid(row=4,column=0,columnspan=2, pady=10, padx=10, ipadx=100)

#    #    # GUI Information #    #    #
def guiDriver():
    # General Root Window Information
    root = Tk()
    root.geometry("300x75")
    root.configure(background = 'light blue')
    root.title("quoteMe")

    # Play Quote Button
    quote_me_up = Button(root, text="Give me a Quote!", command=playQuote, bg="blue")
    quote_me_up.pack()

    # Replay Quote Button
    replay_quote = Button(root, text="Replay Quote!", command=replayQuote, bg="yellow")
    replay_quote.pack()

    # Add Quote Button
    add_a_quote = Button(root, text="Add a new Quote!", command=addQuote, bg="orange")
    add_a_quote.pack()

    # Runs root window
    root.mainloop()    

#    #    # Testing #    #    #
createTable()
guiDriver()
