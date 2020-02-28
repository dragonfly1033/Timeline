from tkinter import *
from tkinter import ttk
import os, json

def do_popup(event):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()

def main():
    root = Tk()
    root.geometry('800x500')
    root.bind("<Button-3>", do_popup)

    root.update()
    width = root.winfo_width()
    height = root.winfo_height()

    popup = Menu(root, tearoff=0)
    popup.add_command(label="Add")
    popup.add_command(label="Help")

    timeline = Canvas(root, bg='light grey', width=width, height=height)
    timeline.grid(row=0, column=0)

    buffer1 = timeline.create_line(10, height//2 + 20, 10, height//2 - 20, fill='black', width='3')
    line = timeline.create_line(10, height//2, width-10, height//2, fill='black', width='3')
    buffer2 = timeline.create_line(width-10, height//2 + 20, width-10, height//2 - 20, fill='black', width='3')

    root.mainloop()


def check_data():
    folder = os.popen('chdir').read().strip('\n')
    if(not os.path.exists(folder+ r'\timelineData.json')):
        print('not')
        with open('timelineData.json', 'w') as f:
            pass
        timelineData = {}
    else:
        print('here')
        with open('timelineData.json', 'r') as f:
            d = f.read()
            timelineData = json.loads(d)
def save():
    with open('timelineData.json', 'w') as f:
        d = json.dumps(timelineData)
        f.write(d)

check_data()
main()
save()

