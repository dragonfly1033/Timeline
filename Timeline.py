from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import os, json

class Event:
    def __init__(self, eName, Date, eInfo, Tags):
        self.eName, self.Date, self.eInfo, self.Tags = eName, Date, eInfo, Tags
        timelineData[self.eName] = {'date':self.Date, 'info':self.eInfo, 'tags':self.Tags}


def do_popup(event, popup):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()

def addDate():
    dateR = Tk()
    l1 = Label(dateR, text='Enter Day:   ')
    l2 = Label(dateR, text='Enter Month: ')
    l3 = Label(dateR, text='Enter Year:  ')
    l1.grid(row=0, column=0)
    l2.grid(row=1, column=0)
    l3.grid(row=2, column=0)
    day = StringVar()
    month = StringVar()
    year = StringVar()
    e1 = Combobox(dateR, values=[i for i in range(1,32)])
    e2 = Combobox(dateR, values=['January', 'February', 'March', 'April', 'May', 'June',
                                    'July', 'August', 'September', 'October', 'November', 'December'])
    e3 = Combobox(dateR, values=[i for i in range(-100, 2021)])
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)

    dateR.mainloop()


def main():
    root = Tk()
    root.geometry('800x500')

    root.update()
    width = root.winfo_width()
    height = root.winfo_height()

    popup = Menu(root, tearoff=0)
    popup.add_command(label="Add Date", command= lambda: addDate())
    popup.add_command(label="Add Range")
    popup.add_command(label="Help")

    timeline = Canvas(root, bg='light grey', width=width, height=height)
    timeline.grid(row=0, column=0)

    buffer1 = timeline.create_line(10, height//2 + 20, 10, height//2 - 20, fill='black', width='3')
    line = timeline.create_line(10, height//2, width-10, height//2, fill='black', width='3')
    buffer2 = timeline.create_line(width-10, height//2 + 20, width-10, height//2 - 20, fill='black', width='3')

    root.bind("<Button-3>", lambda x: do_popup(x, popup))
    root.mainloop()


def check_data():
    folder = os.popen('chdir').read().strip('\n')
    if(not os.path.exists(folder+ r'\timelineData.json')):
        with open('timelineData.json', 'w') as f:
            pass
    else:
        with open('timelineData.json', 'r') as f:
            d = f.read()
            timelineData = json.loads(d)
def save():
    with open('timelineData.json', 'w') as f:
        d = json.dumps(timelineData)
        f.write(d)


timelineData = {}

check_data()
main()
save()

