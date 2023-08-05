import tkinter as tk
from datetime import datetime as dt
from tkinter import font as tkfont
from tkinter import ttk

from .event_management import EventFactory
from .window import Window

window = Window.create()
EventFactory.create(window)
window.run()
exit()

topmost: bool = False


def execute():
    global topmost
    topmost = not topmost
    root.attributes('-topmost', topmost)


root = tk.Tk()
root.title('tkinter application')
root.geometry('300x100')
root.overrideredirect(False)

menu = tk.Menu(root, tearoff=0)


def fuga():
    global now_time
    global now_date
    now = dt.now()
    hoge = time_label['textvariable']
    hoge.set(now.strftime('%H:%M:%S'))
    now_date.set(now.strftime('%Y/%m/%d %a'))
    menu.entryconfigure(0, label='fuga')


menu.add_command(label="hoge", command=fuga)
root.bind('<Button-3>', lambda e: menu.post(e.x_root, e.y_root))

font_time = tkfont.Font(family="M+ 1mn", size=34, weight='bold')
font_date = tkfont.Font(family="M+ 1mn", size=12)

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH)

# button_display = ttk.Button(frame, text='Window作成', command=display)
now = dt.now()
now_time = tk.StringVar(frame)
now_time.set(now.strftime('%H:%M:%S'))
now_date = tk.StringVar(frame)
now_date.set(now.strftime('%Y/%m/%d %a'))

time_label = ttk.Label(frame,
                       textvariable=now_time,
                       anchor='center',
                       font=font_time)
print(id(time_label['textvariable']), id(now_time))
date_label = ttk.Label(frame,
                       textvariable=now_date,
                       anchor='center',
                       font=font_date)
time_label.pack(fill=tk.BOTH, expand=True, pady=(5, 0), padx=10)
date_label.pack(fill=tk.BOTH, expand=True, pady=(0, 5), padx=10)

# button_display.pack()

root.mainloop()
