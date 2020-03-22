from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, messagebox
from re import findall
from datetime import datetime

class Page(Frame):

    def __init__(self, parent, name):

        Frame.__init__(self, parent)

        note.add(self, text=name)

def save():
    pass

def getRat():
    pass

def refresh():
    pass

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
                return 'Year not in range 1-31~'
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
    date = datetime.strptime(f'{day}/{month}/{year}', '%d/%B/%Y')
    return date

def addDate():
    name, day, month, year, tags, info = getVals()
    if(name!=None):
        date = combDate(day, month, year)
        tags = findall('([a-zA-Z0-9_ ]*),*\s*', tags)
        tags.remove('')     

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
    pass
    # coords=[i.xc for i in points]
    # coords.sort()
    # srats=[i.rat for i in points]
    # sf=1.001**event.delta

    # absolute_difference_function = lambda list_value : abs(list_value - event.x)
    # mid = min(coords, key=absolute_difference_function)
    # print(timeline.itemcget(points[coords.index(mid)], option='text'))
    # difs=[]
    # newCoords=[]
    # for i in coords: difs.append((mid-i)*sf)
    # for i in difs: 
    #     #if (mid-i)>=0 and (mid-i)<=8: 
    #     newCoords.append(mid-i)
    # erats=[(i-10)/580 for i in newCoords]
    # for i in range(len(points)):
    #     #print(points[i])
    #     points[i].xc=newCoords[i]
    #     points[i].rat=erats[i]
    #     timeline.coords(points[i].point, newCoords[i]-4,points[i].y1,newCoords[i]+4,points[i].y2)
    #     timeline.coords(points[i].txt, newCoords[i],points[i].interval)
    #     timeline.coords(points[i].verLine, newCoords[i],points[i].yc,newCoords[i],points[i].yc2)
    
def buildMain():
    c.create_line(0,300,1020,300, fill='black', width=3)
    #c.bind('<MouseWheel>', dozoom)

GREY = '#7f7f7f'
FONT = ('Bahnschrift Light', 18)
months=['January', 'February', 'March', 'April', 'May', 'June',
 'July', 'August', 'September', 'October', 'November', 'December']
days=[i for i in range(1,32)]
years=[i for i in range(1000,2025)]

root = Tk()
root.geometry('1020x600')

note =  ttk.Notebook(root, padding=0)
note.pack(fill='both', expand=True)

main = Page(note, 'Timeline')
sub = Page(note, 'Add Date')
subsub = Page(note, 'sub sub')

backimg = PhotoImage(file='C:\\Users\\3664\\python\\TEST\\AddDateTest.png')

c = Canvas(main, bd=0, highlightthickness=0, relief='flat')
c.pack(fill='both', expand=True)

buildMain()
buildAdd()

t = Label(subsub, text='why')
t.pack()

root.mainloop()
