from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, messagebox
from re import findall
from datetime import datetime
from os import popen, path
from json import dumps, loads


class Page(Frame):

    def __init__(self, parent, name):

        Frame.__init__(self, parent)

        note.add(self, text=name)


class Date:
    def __init__(self, name, day, month, year, tags, info):
        self.name = name
        self.day = day
        self.month = month
        self.year = year
        self.tags = tags
        self.info = info
        self.date = f'{day}/{month}/{year}'
        self.dump = {'day':self.day, 'month':self.month, 'year':self.year, 'tags':self.tags, 'info':self.info}

    def __repr__(self):
        print(f'Date({self.name}, {self.date}, {self.tags}, {self.info})')


    def verLine(self, x, y2, canvas):
        self.x=x
        self.verLine_y2 = y2
        canvas.create_line(self.x, 300, self.x, self.verLine_y2, fill=GREY, width=2)

    def text(self, x, y1, canvas):
        self.x = x
        self.text_y1 = y1
        canvas.create_text(self.x, self.text_y1, text=self.name, fill=GREY, angle=90, anchor='w')


def save():
    global dates
    with open('dates.json', 'w') as f:
        d = dumps(dates)
        f.write(d)

def clear():
    global dates
    with open('dates.json', 'w') as f:
        d = dumps({})
        f.write(d)

def getRat():
    global dates
    for i in dates:
        curD = combDate(dates[i]['day'], dates[i]['month'], dates[i]['year'])
        minD = combDate('01','January','1000')
        maxD = combDate('31','December','2024')
        num = curD-minD
        den = maxD-minD
        rat = num/den
        dates[i]['rat'] = rat
    save()

def validate(name, day, month, year, tags, info, dayU, monthU):
    def doName(name):
        if(name=='Name'):
            return 'No Name~'
        elif(len(name)==0):
            return 'No Name~'
        else:
            return ''
    def doDay(day):
        if(day=='Day'):
            return 'No Day~'
        elif(dayU):
            return 'Day=Unknown~'
        elif(len(day)==0):
            return 'No Day~'
        elif(len(day)!=2):
            return 'Day not 2-digit~'
        else:
            try:
                int(day)
            except:
                return 'Day not number~'
            if(int(day) not in days):
                return 'Day not in range 1-31~'
            return ''
    def doMonth(Month):
        if(Month=='Month'):
            return 'No Month~'
        elif(monthU):
            return 'Month=Unknown~'
        else:
            return ''
    def doYear(Year):
        if(Year=='Year'):
            return 'No Year~'
        elif(len(Year)!=4):
            return 'Year not 4-digit number~'
        else:
            try:
                int(Year)
            except:
                return 'Year not number~'
            if(int(Year) not in years):
                return 'Year not in range 1000-2024~'
            return ''    
    def doTags(Tags):
        if(Tags=='Tags'):
            return 'Tags=NA~'
        else:
            return ''
    def doInfo(Info):
        if(Info=='Info'):
            return 'Info=NA~'
        else:
            return ''
    out=''
    out += doName(name)
    out += doDay(day)
    out += doMonth(month)
    out += doYear(year)
    out += doTags(tags)
    out += doInfo(info)
    return out

def getVals():
    name = nameE.get()
    day = dayE.get()
    month = months[round(monthE.get())]
    year = yearE.get()
    tags = tagsE.get()
    info = infoE.get('1.0',END)
    dayU = r1.get()
    monthU = r2.get()
    out = validate(name, day, month, year, tags, info, dayU, monthU)
    if('Day=Unknown~' in out):
        out = out.replace('Day=Unknown~','')
        day = 'Unknown'
    if('Month=Unknown~' in out):
        out = out.replace('Month=Unknown~','')
        month = 'Unknown'
    if('Tags=NA~' in out):
        out = out.replace('Tags=NA~','')
        tags=''
    if('Info=NA~' in out):
        out = out.replace('Info=NA~','')
        info=''
    if(len(out)==0):
        return name, day, month, year, tags, info
    else:
        l = out.split('~')
        ou='Problems:\n'
        for i in l:
            ou += f'{i}\n' 
        messagebox.showinfo('Error', ou)
        return None, None, None, None, None, None

def combDate(day, month, year):
    try:
        date = datetime.strptime(f'{day}/{month}/{year}', '%d/%B/%Y')
        return date
    except ValueError as e:
        messagebox.showwarning('Warning', e)

def addDate():
    global dates
    name, day, month, year, tags, info = getVals()
    if(name!=None):
        if(day!='Unknown' and month!='Unknown'):
            date = combDate(day, month, year)
            if(date != None):
                tags = findall('([a-zA-Z0-9_ ]*),*\s*', tags)
                tags.remove('')     
                new = Date(name, day, month, year, tags, info)
                dates[name] = new.dump
                getRat()
                save()
                buildMain()
        else:
            if(day=='Unknown'):
                startDay = '01'
            if(month=='Unknown'):
                startMonth = 'January'

def buildAdd():
    global r1, r2, nameE, dayE, monthE, yearE, tagsE, infoE
    def showSlider():
        val = monthE.get()
        ind = round(val)
        mon = months[ind]
        nx = (val/11)*500
        if(val<6):
            an = 'sw'
        elif(val>5):
            an = 'se'
        showval.place_configure(x=nx)
        showval.configure(text=mon)
        showval.place_configure(anchor=an)
    def tempclear(wid):
        if(wid not in es):
            wid.delete(0,END)
            es.append(wid)
            
    es=[]

    subback = Label(sub, image=backimg, bg='white')
    subback.image = backimg
    subback.pack(fill='both', expand=True)

    nameE = Entry(subback, width=42, font=FONT, relief='flat', bg='white', fg=GREY, takefocus=False)
    nameE.place(x=90,y=140)
    nameE.insert(0,'Name')
    nameE.bind('<FocusIn>', lambda x: tempclear(nameE))

    dayE = Entry(subback, width=37, font=FONT, relief='flat', bg='white', fg=GREY, takefocus=False)
    dayE.place(x=90,y=211)
    dayE.insert(0,'Day')
    dayE.bind('<FocusIn>', lambda x: tempclear(dayE))
    scaleframe = Frame(subback, bg='white', width=500, height=75)
    scaleframe.place(x=80, y=283)
    #scaleframe.place(x=80, y=305)
    V = IntVar()
    scaleStyle = ttk.Style()
    scaleStyle.configure('Horizontal.TScale', background='white')
    monthE = ttk.Scale(scaleframe, orient=HORIZONTAL, from_=0, to=11, value=1,
     variable=V, length=500, command=lambda x: showSlider(), style='Horizontal.TScale', takefocus=False)
    monthE.place(x=0,y=28)
    showval = Label(scaleframe, text='January', bg='white', font=FONT, fg=GREY)
    showval.place(x=0,y=28, anchor='sw')

    yearE = Entry(subback, width=42, font=FONT, relief='flat', bg='white', fg=GREY, takefocus=False)
    yearE.place(x=90,y=354)
    yearE.insert(0,'Year')
    yearE.bind('<FocusIn>', lambda x: tempclear(yearE))

    tagsE = Entry(subback, width=42, font=FONT, relief='flat', bg='white', fg=GREY, takefocus=False)
    tagsE.place(x=88,y=422)
    tagsE.insert(0,'Tags')
    tagsE.bind('<FocusIn>', lambda x: tempclear(tagsE))

    infoE = scrolledtext.ScrolledText(subback, width=16, height=9, 
    font=('Bahnschrift Light', 18), relief='flat', bg='white', fg=GREY, takefocus=False)
    infoE.place(x=702, y=182)

    CSt = ttk.Style()
    CSt.configure('TCheckbutton', background='white')
    CSt.configure('TCheckbutton', foreground=GREY)
    r1 = BooleanVar()
    dayC = ttk.Checkbutton(subback, variable=r1, takefocus=0)
    dayC.place(x=638, y=242, anchor='e')

    r2 = BooleanVar()
    monthC = ttk.Checkbutton(subback, variable=r2, takefocus=0)
    monthC.place(x=638, y=314, anchor='e')

    saveB = Button(subback, text='Save', font=('Bahnschrift Light', 13), relief='flat', bg='white', 
    bd=0, highlightthickness=0, width=24, height=1, fg=GREY, takefocus=False, command=lambda: addDate())
    saveB.place(x=702, y=477)

def dozoom(event):
    global dates
    print(dates)
    xs=[dates[i]['rat']*1016 for i in dates]
    difs=[]
    c = min(xs, key=lambda list_value : abs(list_value - event.x))
    sf = 1.001**event.delta
    for i in range(len(xs)):
        if(xs[i]!=c):
            d = xs[i] - c
            d*=sf
            d+=c
            difs.append(d)
        else:
            difs.append(c)
    ind=0
    for i in dates:
        dates[i]['rat'] = difs[ind]/1016
        ind+=1
    save()
    buildMain()
        
def buildMain():
    c.delete('all')
    c.create_line(0,300,1020,300, fill=GREY, width=3)
    for i in dates:
        day = dates[i]['day']
        month = dates[i]['month']
        year = dates[i]['year']
        tags = dates[i]['tags']
        info = dates[i]['info']
        rat = dates[i]['rat']
        x = rat*1016
        y2 = 300 - 25
        D = Date(i, day, month, year, tags, info)
        D.verLine(x, y2, c)
        D.text(x, y2-10, c)

def getDates():
    global dates
    folder = popen('chdir').read().strip('\n')
    if(not path.exists(folder+ r'\dates.json')):
        with open('dates.json', 'w') as f:
            d = dumps({})
            f.write(d)
    else:
        with open('dates.json', 'r') as f:
            d = f.read()
            dates = loads(d)

GREY = '#7f7f7f'
FONT = ('Bahnschrift Light', 18)
months=['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
days=[i for i in range(1,32)]
years=[i for i in range(1000,2025)]
dates={}
getDates()
getRat()

root = Tk()
root.geometry('1020x600')
root.bind('<Delete>', lambda x: clear())

note =  ttk.Notebook(root, padding=0)
note.pack(fill='both', expand=True)

main = Page(note, 'Timeline')
sub = Page(note, 'Add Date')
subsub = Page(note, 'sub sub')

backimg = PhotoImage(file='C:\\Users\\3664\\python\\TEST\\AddDateTest.png')

c = Canvas(main, bd=0, highlightthickness=0, relief='flat')
c.pack(fill='both', expand=True)
c.bind('<MouseWheel>', dozoom)

buildMain()
buildAdd()

t = Label(subsub, text='why')
t.pack()

root.mainloop()

#print(dates)