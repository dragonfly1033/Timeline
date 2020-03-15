from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from json import dumps, loads
from os import popen, path
from re import findall
import TimelineConst
#t0, t1, t2, t3, t4, t5  ==== name, day, month, year, info, tags

class ToggledFrame(Frame):

    def __init__(self, parent, gr, gc, text="", *args, **options):
        #Frame.__init__(self, parent, *args, **options)
        self.frame = Frame(parent, *args, **options)
        #self.frame.pack_propagate(0)
        self.frame.grid(row=gr, column=gc)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = Frame(self.frame, *args, **options)
        self.title_frame.pack(fill="x", expand=1)

        Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=19, text='         +         ', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self.frame, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='         -         ')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='         +         ')

class EventS:
    def __init__(self, name, day, month, year, info, tags):
        self.name, self.Date = name, f'{day.zfill(2)}/{month}/{year.zfill(4)}'
        self.info, self.tags = info, tags

        self.infoD = {'date': self.Date, 'info': self.info, 'tags': self.tags}

    def draw_point(self, xc, y1, y2, i):
        self.name = i
        self.xc = xc
        self.y1=y1
        self.y2 = y2
        self.point = timeline.create_oval(xc-4, y1, xc+4, y2, fill='black', activefill='red', tags=('date', str(self.name)))
        timeline.tag_bind(self.name, '<ButtonPress-1>', lambda x: showInfo(x, self.name))

    def draw_txt(self, xc, interval, anchor, i):
        self.interval = interval
        self.anchor = anchor
        self.txt = timeline.create_text(xc, interval, activefill='red', fill='black', anchor=anchor, text=self.name, angle=90, tags=('date', str(self.name)))
        timeline.tag_bind(self.name, '<ButtonPress-1>', lambda x: showInfo(x, self.name))

    def draw_verLine(self, xc, yc, yc2, i):
        self.yc = yc
        self.yc2 = yc2
        self.verLine = timeline.create_line(xc, yc, xc, yc2, fill='black', activefill='red', width=3, tags=('date', str(self.name)))
        timeline.tag_bind(self.name, '<ButtonPress-1>', lambda x: showInfo(x, self.name))
    
    def getRat(self, rat):
        self.rat = rat


def setText(wid, text):
    wid.delete('1.0', END)
    wid.insert('1.0', text)

def do_popup(event, popup):
    try:
        popup.tk_popup(event.x_root + 40, event.y_root + 10, 0)
    finally:
        popup.grab_release()

def getRatio():
    global timelineData
    if(len(timelineData) > 0):
        kl = list(timelineData.keys())
        vl = list(timelineData.values())
        s = [datetime.strptime(i['date'], '%d/%B/%Y') for i in timelineData.values()]
        unwanted = [kl[0], kl[-1]]
        newdict = {i: timelineData[i] for i in timelineData if i not in unwanted}
        for i in unwanted:
            timelineData[i]['rat'] = unwanted.index(i)
            globals()[i].getRat(unwanted.index(i))
        for i in newdict:
            minn = min(s)
            maxx = max(s)
            cur = datetime.strptime(newdict[i]['date'], '%d/%B/%Y')
            num = cur - minn
            den = maxx - minn
            rat = num/den
            timelineData[i]['rat'] = rat
            globals()[i].getRat(rat)

def sortData():
    global timelineData
    kl = list(timelineData.keys())
    vl = list(timelineData.values())
    dl = [timelineData[i]['date'] for i in timelineData]
    for i in timelineData.values(): print(f":{i['date']}:")#, datetime.strptime(i['date'], '%d/%B/%Y'))
    s = [datetime.strptime(i['date'], '%d/%B/%Y') for i in timelineData.values()]
    s.sort()

    timelineData = {kl[dl.index(i.strftime('%d/%B/%Y'))]: vl[dl.index(i.strftime('%d/%B/%Y'))] for i in s}
    getRatio()


def save():
    sortData()
    with open('timelineData.json', 'w') as f:
        d = dumps(timelineData)
        f.write(d)

def validate(t0, t1, t2, t3, t4, t5):

    typefail=False
    try:
        int(t1)
        int(t3)
    except:
        typefail = True
    if(typefail):
        pass
    elif(t1=='00' or t2=='' or t3=='0000' or t0=='' or t1=='' or t3==''):
        pass
    elif(int(t1) not in TimelineConst.DAYS or int(t3) not in TimelineConst.YEARS or t2 not in TimelineConst.MONTHS):
        pass
    else:
        try:
            int(t0)
        except ValueError:
            s = str(t5)
            inter = s.replace(']','').replace('[','').replace(' ,',',').replace(', ',',').replace('\n','').split(',')
            if(inter == s):
                pass
            elif(0 in [len(re.findall('\S', i)) for i in inter] and inter != ['']):
                pass
            else:
                return True
    return False

def manSave():
    global timelineData
    t0=nameShow
    try:
        t1, t2, t3= dateShow.get('1.0', END).replace('\n','').split('/')
    except:
        t1, t2, t3 = '','',''
    t4 = infoShow
    t5=tagsShow
    if(t0.get('1.0', END)=='' and t1=='' and t2=='' and t3=='' and t4.get('1.0', END)=='' and t5.get('1.0', END)==''):
        del timelineData[TimelineConst.curShowName]
        del globals()[TimelineConst.curShowName]
        save()
        refresh()
    elif(validate(t0.get('1.0', END), t1, t2, t3, t4.get('1.0', END), list(t5.get('1.0', END).split(',')))):
        name = nameShow.get('1.0', END)
        date = dateShow.get('1.0', END).replace('\n','')
        tags = list(tagsShow.get('1.0',END).replace('\n','').split(','))
        if(tags == ['']): tags = []
        info = infoShow.get('1.0', END)
        d, m, y= date.split('/')
        del timelineData[TimelineConst.curShowName]
        del globals()[TimelineConst.curShowName]
        timelineData[name] = {}
        globals()[name] = EventS(name, d, m, y, info, tags)
        timelineData[name]['date'] = date
        timelineData[name]['tags'] = tags
        timelineData[name]['info'] = info
        TimelineConst.curShowName = name
        save()
        refresh()

def confirm(cfunc, *args):
    saveW=Tk()
    saveW.title('Confirm')
    ll= Label(saveW, text='Are you sure? ')
    ll.pack()
    bb = ttk.Button(saveW, text='Yes', command=lambda: cfunc(*args))
    bb.pack()
    bl = ttk.Button(saveW, text='no', command=lambda: saveW.destroy())
    bl.pack()
    saveW.mainloop()

def refresh():
    timeline.delete("date")
    for i in timelineData:
        r = timelineData[i]['rat']
        xc = 10 + (r*(width-20))
        y1 = (height//2)-4
        y2 = (height//2)+4
        ly1 = (height//2)
        if TimelineConst.SIDE == True:
            interval = y1-25
            anchor = 'w'
            ly2 = (height//2)-TimelineConst.verLineHeight
        else:
            interval = y2+25
            anchor = 'e'
            ly2 = (height//2)+TimelineConst.verLineHeight
        globals()[i].draw_point(xc, y1, y2, i)
        globals()[i].draw_txt(xc, interval, anchor, i)
        globals()[i].draw_verLine(xc, ly1, ly2, i)
        TimelineConst.SIDE = not TimelineConst.SIDE
    TimelineConst.SIDE = True

def addRange():
    pass

def addFunc(name, day, month, year, info, tags):
    global timelineData
    name = name.get()
    day = day.get()
    month = month.get()
    year = year.get()
    info = info.get('1.0', END)
    tags = list(tags.get().split(','))
    if(tags == ['']): tags = []
    if(day == 'Unknown'):
        addRange()
    elif(month == 'Unknown'):
        addRange()
    else:
        globals()[name] = EventS(name, day, month, year, info, tags)
    timelineData[name] = globals()[name].infoD
    save()
    refresh()   


def addGUI():
    def ifValid(t0, t1, t2, t3, t4, t5):
        if(validate(t0.get(), t1.get(), t2.get(), t3.get(), t4.get('1.0', END), list(t5.get().split(',')))):
            addFunc(t0, t1, t2, t3, t4, t5)
    dateR = Tk()
    l0 = Label(dateR, text='Enter Name:        ')
    l1 = Label(dateR, text='Enter Day:         ')
    l2 = Label(dateR, text='Enter Month:       ')
    l3 = Label(dateR, text='Enter Year:        ')
    l4 = Label(dateR, text='Enter Info:        ')
    l5 = Label(dateR, text='Enter tags (CSV):  ')
    l0.grid(row=0, column=0)
    l1.grid(row=1, column=0)
    l2.grid(row=2, column=0)
    l3.grid(row=3, column=0)
    l4.grid(row=5, column=0)
    l5.grid(row=4, column=0)

    e0 = Entry(dateR, width=24)
    e1 = ttk.Combobox(dateR, values=TimelineConst.DAYS)
    e2 = ttk.Combobox(dateR, values=TimelineConst.MONTHS)
    e3 = ttk.Combobox(dateR, values=TimelineConst.YEARS)
    e4 = Text(dateR, width=50, height=10)
    e5 = Entry(dateR, width=24)
    e0.grid(row=0, column=1)
    e1.grid(row=1, column=1)
    e2.grid(row=2, column=1)
    e3.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e4.grid(row=5, column=1, padx=25, pady=10)
    b1 = ttk.Button(dateR, text='Add', width=42, command=lambda: ifValid(e0, e1, e2, e3, e4, e5))
    b1.grid(row=6, columnspan=2, pady=10)

    dateR.mainloop()  

def showInfo(event, tag):
    canvas = event.widget
    itemID = canvas.find_withtag(tag)[0]
    itemName = canvas.gettags(itemID)[1]
    item = globals()[itemName]
    tags=str(item.tags).replace('[', '').replace(']','').replace("'",'')
    TimelineConst.curShowName = item.name
    setText(nameShow, item.name)
    setText(dateShow, item.Date)
    setText(tagsShow, tags)
    setText(infoShow, item.info)

def clear():
    global timelineData
    timelineData = {}
    save()
    refresh()

#INIT DATA:::::::::::::::::::::::::::
timelineData = {}
points=[]
#CHECK JSON ::::::::::::::::::::::::::::
folder = popen('chdir').read().strip('\n')
if(not path.exists(folder+ r'\timelineData.json')):
    with open('timelineData.json', 'w') as f:
        d = dumps({})
        f.write(d)
else:
    with open('timelineData.json', 'r') as f:
        d = f.read()
        timelineData = loads(d)

# MAIN GUI:::::::::::::::::::::::::
root = Tk()

root.update()
width = 1040
height = 500

for i in timelineData:
    d, m, y = timelineData[i]['date'].split('/')
    globals()[i] = EventS(i, d, m, y, timelineData[i]['info'], timelineData[i]['tags'])
    points.append(globals()[i])

popup = Menu(root, tearoff=0)
popup.add_command(label="Add Date", command= lambda: addGUI())
popup.add_command(label="Add Range")
popup.add_command(label="Clear", command=lambda: confirm(clear))
popup.add_command(label="Help")

def dozoom(event):

    coords=[i.xc for i in points]
    coords.sort()
    srats=[i.rat for i in points]
    sf=1.001**event.delta

    absolute_difference_function = lambda list_value : abs(list_value - event.x)
    mid = min(coords, key=absolute_difference_function)
    print(timeline.itemcget(points[coords.index(mid)], option='text'))
    difs=[]
    newCoords=[]
    for i in coords: difs.append((mid-i)*sf)
    for i in difs: 
        #if (mid-i)>=0 and (mid-i)<=8: 
        newCoords.append(mid-i)
    erats=[(i-10)/580 for i in newCoords]
    for i in range(len(points)):
        #print(points[i])
        points[i].xc=newCoords[i]
        points[i].rat=erats[i]
        timeline.coords(points[i].point, newCoords[i]-4,points[i].y1,newCoords[i]+4,points[i].y2)
        timeline.coords(points[i].txt, newCoords[i],points[i].interval)
        timeline.coords(points[i].verLine, newCoords[i],points[i].yc,newCoords[i],points[i].yc2)
        

def scroll_start(event):
    timeline.scan_mark(event.x, event.y)
def scroll(event):
    timeline.scan_dragto(event.x, event.y, gain=1)

timeline = Canvas(root, bg='light grey', width=width, height=height)
timeline.grid(row=0, column=0)
timeline.bind('<MouseWheel>', dozoom)
timeline.bind('<ButtonPress-1>', scroll_start)
timeline.bind('<B1-Motion>', scroll)

buffer1 = timeline.create_line(10, height//2 + 20, 10, height//2 - 20, fill='black', width='3')
line = timeline.create_line(10, height//2, width-10, height//2, fill='black', width='3')
buffer2 = timeline.create_line(width-10, height//2 + 20, width-10, height//2 - 20, fill='black', width='3')

getRatio()
refresh()

infoBox = Frame(root, width = 800, height = 250, bg='blue')
infoBox.grid(row=1, column=0)


nameLabel = Label(infoBox, text='Name: ', width = 10, relief='ridge')
nameLabel.grid(row=0 , column=0)    
dateLabel = Label(infoBox, text='Date: ', width = 10, relief='ridge')
dateLabel.grid(row=1 , column=0)    
tagsLabel = Label(infoBox, text='tags: ', width = 10, relief='ridge')
tagsLabel.grid(row=2 , column=0)    
infoLabel = Label(infoBox, text='Info: ', width = 10, relief='ridge')
infoLabel.grid(row=3 , column=0)

nameShow = Text(infoBox, width = 120, relief='ridge', height=1)
nameShow.grid(row=0 , column=1, pady=1, padx=1)    
dateShow = Text(infoBox, width = 120, relief='ridge', height=1)
dateShow.grid(row=1 , column=1, pady=1, padx=1)    
tagsShow = Text(infoBox, width = 120, relief='ridge', height=1)
tagsShow.grid(row=2 , column=1, pady=1, padx=1)    
info_collapse = ToggledFrame(infoBox, 3, 1, text=' '*153+'Info'+' '*120, width=962, height=16)
#info_collapse.grid(row=3 , column=1)
infoShow = Text(info_collapse.sub_frame, width = 120, relief='ridge', height=10)
infoShow.grid(row=3 , column=1)

saveBut = ttk.Button(infoBox, text='Save', command= lambda: confirm(manSave), width=107)
saveBut.grid(row=4, columnspan=2, sticky='we')

root.bind("<Button-3>", lambda x: do_popup(x, popup))
root.mainloop()