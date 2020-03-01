from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from json import dumps, loads
from os import popen, path
from re import findall

class EventS:
    def __init__(self, eName, day, month, year, eInfo, Tags):
        self.eName, self.Date = eName, f'{day.zfill(2)}/{month}/{year.zfill(4)}'
        self.eInfo, self.Tags = eInfo, Tags

        self.info = {'date': self.Date, 'info': self.eInfo, 'tags': self.Tags}

    def draw_point(self, xc, y1, y2, i, timeline):
        self.name = i
        self.xc = xc
        self.y1=y1
        self.y2 = y2
        self.point = timeline.create_oval(xc-4, y1, xc+4, y2, fill='black', activefill='red', tags=('date', str(self.name)))
        timeline.tag_bind(self.name, '<ButtonPress-1>', lambda x: showInfo(x, self.name))

    def draw_txt(self, xc, interval, anchor, i, timeline):
        self.interval = interval
        self.anchor = anchor
        self.txt = timeline.create_text(xc, interval, activefill='red', fill='black', anchor=anchor, text=self.name, angle=90, tags=('date', str(self.name)))
        timeline.tag_bind(self.name, '<ButtonPress-1>', lambda x: showInfo(x, self.name))


def sortData():
    global timelineData
    kl = list(timelineData.keys())
    vl = list(timelineData.values())
    dl = [timelineData[i]['date'] for i in timelineData]
    s = [datetime.strptime(i['date'], '%d/%B/%Y') for i in timelineData.values()]
    s.sort()

    timelineData = {kl[dl.index(i.strftime('%d/%B/%Y'))]: vl[dl.index(i.strftime('%d/%B/%Y'))] for i in s}
    if(len(timelineData) > 0):
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

def addDate(day, month, year, name, e4, root, timeline, width, height, e5):
    global timelineData
    dval = day.get()
    mval = month.get()
    yval = year.get()
    nval = name.get()
    ival = e4.get('1.0', END)
    tags = list(e5.get().split(','))
    if(tags == ['']): tags = []
    if(dval == 'Unknown'):
        addRange()
    elif(mval == 'Unknown'):
        addRange()
    else:
        globals()[nval] = EventS(nval, dval, mval, yval, ival, tags)
    timelineData[nval] = globals()[nval].info
    save()
    refresh(timeline, width, height)

def subAdd(root, timeline, width, height):
    def checkE(e1, e2, e3, e0, e4, root, timeline, width, height, e5):
        if(e1.get()=='00' or e2.get()=='' or e3.get()=='0000' or e0.get()==''):
            pass
        elif(int(e1.get()) not in days or int(e3.get()) not in years or e2.get() not in months):
            pass
        else:
            try:
                int(e0.get())
            except ValueError:
                s = e5.get()
                inter = s.replace(']','').replace('[','').replace(' ,',',').replace(', ',',').split(',')
                if(inter == s):
                    pass
                elif(0 in [len(re.findall('\S', i)) for i in inter] and inter != ['']):
                    pass
                else:
                    addDate(e1, e2, e3, e0, e4, root, timeline, width, height, e5)

    dateR = Tk()
    l0 = Label(dateR, text='Enter Name:        ')
    l1 = Label(dateR, text='Enter Day:         ')
    l2 = Label(dateR, text='Enter Month:       ')
    l3 = Label(dateR, text='Enter Year:        ')
    l4 = Label(dateR, text='Enter Info:        ')
    l5 = Label(dateR, text='Enter Tags (CSV):  ')
    l0.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)
    l4.grid(row=5, column=0)
    l5.grid(row=4, column=0)

    e0 = Entry(dateR, width=24)
    e1 = ttk.Combobox(dateR, values=days)
    e2 = ttk.Combobox(dateR, values=months)
    e3 = ttk.Combobox(dateR, values=years)
    e4 = Text(dateR, width=50, height=10)
    e5 = Entry(dateR, width=24)
    e0.grid(row=0, column=1)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    e3.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e4.grid(row=5, column=1, padx=25, pady=10)
    b1 = ttk.Button(dateR, text='Add', width=42, command=lambda: checkE(e1, e2, e3, e0, e4, root, timeline, width, height, e5))
    b1.grid(row=6, columnspan=2, pady=10)

    dateR.mainloop()

def refresh(timeline, width, height):
    global side, dateObjs
    timeline.delete("date")
    for i in timelineData:
        r = timelineData[i]['rat']
        xc = 10 + (r*(width-20))
        y1 = (height//2)-4
        y2 = (height//2)+4
        if side == True:
            interval = y1-25
            anchor = 'w'
        else:
            interval = y2+25
            anchor = 'e'
        globals()[i].draw_point(xc, y1, y2, i, timeline)
        globals()[i].draw_txt(xc, interval, anchor, i, timeline)
        side = not side
    side = True

def setText(wid, text):
    wid.delete(0, END)
    wid.insert(0, text)

def showInfo(event, tag):
    global curShowName
    canvas = event.widget
    itemID = canvas.find_withtag(tag)[0]
    itemName = canvas.gettags(itemID)[1]
    item = globals()[itemName]
    tags=str(item.Tags).replace('[', '').replace(']','').replace("'",'')
    curShowName = item.eName
    setText(nameShow, item.eName)
    setText(dateShow, item.Date)
    setText(tagsShow, tags)
    setText(infoShow, item.eInfo)

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
    clearW.title('Clear?')
    ll= Label(clearW, text='Are you sure? ')
    ll.pack()
    bb = ttk.Button(clearW, text='Yes', command=lambda: subc(timeline, width, height))
    bb.pack()
    bl = ttk.Button(clearW, text='no', command=lambda: clearW.destroy())
    bl.pack()
    clearW.mainloop()

def main():
    def subsave(timeline, width, height):
        def subs(timeline, width, height):
            global timelineData
            t0=nameShow
            try:
                t1, t2, t3= dateShow.get().split('/')
            except:
                t1, t2, t3 = '','',''
            t4 = infoShow
            t5=tagsShow
            if(t0.get()=='' and t1=='' and t2=='' and t3=='' and t4.get()=='' and t5.get()==''):
                del timelineData[curShowName]
                del globals()[curShowName]
                save()
                refresh(timeline, width, height)
            elif(t1=='00' or t2=='' or t3=='0000' or t0.get()=='' or t1=='' or t3==''):
                pass
            elif(int(t1) not in days or int(t3) not in years or t2 not in months):
                pass
            else:
                try:
                    int(t0.get())
                except ValueError:
                    s = t5.get()
                    inter = s.replace(']','').replace('[','').replace(' ,',',').replace(', ',',').split(',')
                    if(inter == s):
                        pass
                    elif(0 in [len(re.findall('\S', i)) for i in inter] and inter != ['']):
                        pass
                    else:
                        name = nameShow.get()
                        date = dateShow.get()
                        tags = list(tagsShow.get().split(','))
                        if(tags == ['']): tags = []
                        info = infoShow.get()
                        d, m, y= date.split('/')
                        del timelineData[curShowName]
                        del globals()[curShowName]
                        timelineData[name] = {}
                        globals()[name] = EventS(name, d, m, y, info, tags)
                        timelineData[name]['date'] = date
                        timelineData[name]['tags'] = tags
                        timelineData[name]['info'] = info
                        save()
                        refresh(timeline, width, height)
        saveW=Tk()
        saveW.title('Save?')
        ll= Label(saveW, text='Are you sure? ')
        ll.pack()
        bb = ttk.Button(saveW, text='Yes', command=lambda: subs(timeline, width, height))
        bb.pack()
        bl = ttk.Button(saveW, text='no', command=lambda: saveW.destroy())
        bl.pack()
        saveW.mainloop()

    root = Tk()

    root.update()
    width = 800
    height = 500

    for i in timelineData:
        d, m, y = timelineData[i]['date'].split('/')
        globals()[i] = EventS(i, d, m, y, timelineData[i]['info'], timelineData[i]['tags'])

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

    infoBox = Frame(root, width = 800, height = 250, bg='blue')
    infoBox.grid(row=1, column=0)

    
    nameLabel = Label(infoBox, text='Name: ', width = 10, relief='ridge')
    nameLabel.grid(row=0 , column=0)    
    dateLabel = Label(infoBox, text='Date: ', width = 10, relief='ridge')
    dateLabel.grid(row=1 , column=0)    
    tagsLabel = Label(infoBox, text='Tags: ', width = 10, relief='ridge')
    tagsLabel.grid(row=2 , column=0)    
    infoLabel = Label(infoBox, text='Info: ', width = 10, relief='ridge')
    infoLabel.grid(row=3 , column=0)

    globals()['nameShow'] = Entry(infoBox, text='', width = 120, relief='ridge')
    nameShow.grid(row=0 , column=1)    
    globals()['dateShow'] = Entry(infoBox, text='', width = 120, relief='ridge')
    dateShow.grid(row=1 , column=1)    
    globals()['tagsShow'] = Entry(infoBox, text='', width = 120, relief='ridge')
    tagsShow.grid(row=2 , column=1)    
    globals()['infoShow'] = Entry(infoBox, text='', width = 120, relief='ridge')
    infoShow.grid(row=3 , column=1)

    saveBut = ttk.Button(infoBox, text='Save', command= lambda: subsave(timeline, width, height), width=107)
    saveBut.grid(row=4, columnspan=2, sticky='we')

    root.bind("<Button-3>", lambda x: do_popup(x, popup))
    root.mainloop()


timelineData = {}
curShowName = ''
days = ['Unknown'] + [i for i in range(1,32)]
months = ['Unknown','January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
years = [i for i in range(1, 2021)]
side = True
check_data()
main()

