from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from json import dumps, loads
from os import popen, path

class EventS:
    def __init__(self, eName, day, month, year, eInfo, Tags):
        global timelineData
        self.eName, self.Date = eName, f'{day.zfill(2)}/{month}/{year.zfill(4)}'
        self.eInfo, self.Tags = eInfo, Tags

        timelineData[self.eName] = {'date': self.Date, 'info': self.eInfo, 'tags': self.Tags}

        
def sortData():
    global timelineData
    kl = list(timelineData.keys())
    vl = list(timelineData.values())
    dl = [timelineData[i]['date'] for i in timelineData]
    s = [datetime.strptime(i['date'], '%d/%B/%Y') for i in timelineData.values()]
    s.sort()

    timelineData = {kl[dl.index(i.strftime('%d/%B/%Y'))]: vl[dl.index(i.strftime('%d/%B/%Y'))] for i in s}
    if(len(timelineData) >= 1):
        kl = list(timelineData.keys())
        vl = list(timelineData.values())
        s = [datetime.strptime(i['date'], '%d/%B/%Y') for i in timelineData.values()]
        unwanted = [kl[0], kl[-1]]
        newdict = {i: timelineData[i] for i in timelineData if i not in unwanted}
        for i in unwanted:
            timelineData[i]['rat'] = unwanted.index(i)
        for i in newdict:
            minn = min(s)
            maxx = max(s)
            cur = datetime.strptime(newdict[i]['date'], '%d/%B/%Y')
            num = cur - minn
            den = maxx - minn
            rat = num/den
            timelineData[i]['rat'] = rat

def save():
    sortData()
    with open('timelineData.json', 'w') as f:
        d = dumps(timelineData)
        f.write(d)

def do_popup(event, popup):
    try:
        popup.tk_popup(event.x_root + 40, event.y_root + 10, 0)
    finally:
        popup.grab_release()

def addDate(day, month, year, name, e4, root, timeline, width, height):
    dval = day.get()
    mval = month.get()
    yval = year.get()
    nval = name.get()
    ival = e4.get('1.0', END)
    if(dval == 'Unknown'):
        addRange()
    elif(mval == 'Unknown'):
        addRange()
    else:
        new = EventS(nval, dval, mval, yval, ival, [])
    save()
    refresh(timeline, width, height)

def subAdd(root, timeline, width, height):
    dateR = Tk()
    l0 = Label(dateR, text='Enter Name:   ')
    l1 = Label(dateR, text='Enter Day:   ')
    l2 = Label(dateR, text='Enter Month: ')
    l3 = Label(dateR, text='Enter Year:  ')
    l4 = Label(dateR, text='Enter Info:  ')
    l0.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)
    l4.grid(row=4, column=0)

    e0 = Entry(dateR, width=24)
    e1 = ttk.Combobox(dateR, values=[i for i in range(1, 32)])
    e2 = ttk.Combobox(dateR, values=months)
    e3 = ttk.Combobox(dateR, values=[i for i in range(1, 2021)])
    e4 = Text(dateR, width=50, height=10)
    e0.grid(row=0, column=1)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    e3.grid(row=3, column=1)
    e4.grid(row=4, column=1, padx=25, pady=10)
    b1 = ttk.Button(dateR, text='Add', width=42, command=lambda: addDate(
        e1, e2, e3, e0, e4, root, timeline, width, height))
    b1.grid(row=5, columnspan=2, pady=10)

    dateR.mainloop()

def refresh(timeline, width, height):
    timeline.delete("date")
    for i in timelineData:
        r = timelineData[i]['rat']
        xc = 10 + (r*(width-20))
        y1 = (height//2)-4
        y2 = (height//2)+4
        point = timeline.create_oval(xc-4, y1, xc+4, y2, fill='black', activefill='red', tags=('date'))
        txt = timeline.create_text(xc, y1-25, anchor='w', text=i, angle=90, tags=('date'))

def check_data():
    global timelineData
    folder = popen('chdir').read().strip('\n')
    if(not path.exists(folder+ r'\timelineData.json')):
        with open('timelineData.json', 'w') as f:
            d = dumps({})
            f.write(d)
    else:
        with open('timelineData.json', 'r') as f:
            d = f.read()
            timelineData = loads(d)

def clear(timeline, width, height):
    def subc(timeline, width, height):
        global timelineData
        timelineData = {}
        save()
        refresh(timeline, width, height)
    clearW=Tk()
    ll= Label(clearW, text='Are you sure? ')
    ll.pack()
    bb = ttk.Button(clearW, text='Yes', command=lambda: subc(timeline, width, height))
    bb.pack()
    bl = ttk.Button(clearW, text='no', command=lambda: clearW.destroy())
    bl.pack()
    clearW.mainloop()

def main():
    root = Tk()
    root.geometry('800x500')

    root.update()
    width = root.winfo_width()
    height = root.winfo_height()

    popup = Menu(root, tearoff=0)
    popup.add_command(label="Add Date", command= lambda: subAdd(root, timeline, width, height))
    popup.add_command(label="Add Range")
    popup.add_command(label="Clear", command=lambda: clear(
        timeline, width, height))
    popup.add_command(label="Help")

    timeline = Canvas(root, bg='light grey', width=width, height=height)
    timeline.grid(row=0, column=0)

    buffer1 = timeline.create_line(10, height//2 + 20, 10, height//2 - 20, fill='black', width='3')
    line = timeline.create_line(10, height//2, width-10, height//2, fill='black', width='3')
    buffer2 = timeline.create_line(width-10, height//2 + 20, width-10, height//2 - 20, fill='black', width='3')

    refresh(timeline, width, height)

    root.bind("<Button-3>", lambda x: do_popup(x, popup))
    root.mainloop()


timelineData = {}
months = ['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
check_data()
main()

