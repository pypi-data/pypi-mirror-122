# -*- coding=utf-8 -*-

from tkinter import *
import __init__ as tkex
import blackboard
import system
import timer
import tix as tktix
import tix.filedialog as tixfile
import turtledrawer as tdraw
import os

def _clear():
    try:
        for root, dirs, files in os.walk('__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('__pycache__')
    except OSError:
        pass
    try:
        for root, dirs, files in os.walk('tix/__pycache__', topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
        os.rmdir('tix/__pycache__')
    except OSError:
        pass
    try:
        os.remove('word bank.dat')
    except OSError:
        pass
    return True

def _test_tkextension():
    tkex.askvalue()
    tkex.askitem()
    tkex.askanswer()
    tkex.controlboard()
    tkex.singlechoices()
    tkex.answersheet()
    tk = Tk()
    tkex.create(tk)
    tk.destroy()
    _clear()
    return True

def _test_blackboard():
    return _test_tix_blackboard()

def _test_system():
    system.opensource('tkextension')
    system.opensource('blackboard')
    system.opensource('test')
    system.opensource('timer')
    system.opensource('tix')
    system.opensource('tix.filedialog')
    system.opensource('turtledrawer')
    _clear()
    return True

def _test_timer():
    return _test_tix_timer()

def _test_tix():
    tk = Tk()
    tk.title('_test_tix')
    # Tkinter
    tktix.AskValue(tk)
    tktix.AskItem(tk)
    tktix.AskAnswer(tk)
    v = IntVar()
    tktix.ControlBoard(tk)
    tktix.SingleChoices(tk)
    tktix.AnswerSheet(tk)
    _clear()
    return True

def _test_tix_blackboard():
    tk = Tk()
    tk.title('_test_tix_blackboard')
    # Tkinter
    x = tk.winfo_screenwidth()
    y = tk.winfo_screenheight()
    blackboard.BlackBoard(tk, width=x - 100, height=y - 250).place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor='center')
    tk.mainloop()
    _clear()
    return True

def _test_tix_filedialog():
    tk = Tk()
    tk.title('_test_tix_filedialog')
    # Tkinter
    tixfile.FileTree(tk)
    _clear()
    return True

def _test_tix_timer():
    tk = Tk()
    tk.title('_test_tix_timer')
    # Tkinter
    timer.Timer(tk, 'timer', 1)
    timer.Timer(tk, 'down count', 1)
    timer.Timer(tk, 'alarm clock', 1)
    _clear()
    return True

def _test_turtledrawer():
    a = tdraw.Draw()
    a.create_triangle(1)
    a.create_rectangle(1, 1)
    a.create_pentagon(1)
    a.create_polygon(6, 1)
    a.create_pg(3, 3)
    a.create_pg1(3, 3)
    a.create_koch(1)
    a.create_koch_snowflake(1)
    _clear()
    return True

def _test(module='all'):
    if module == 'all':
        return (
            _test_tkextension(),
            _test_system(),
            _test_tix(),
            _test_tix_blackboard(),
            _test_tix_filedialog(),
            _test_tix_timer(),
            _test_turtledrawer()
            )
    elif module == 'tkextension':
        return _test_tkextension()
    elif module == 'blackboard':
        return _test_blackboard()
    elif module == 'system':
        return _test_system()
    elif module == 'timer':
        return _test_timer()
    elif module == 'tix':
        return _test_tix()
    elif module == 'tix.blackboard':
        return _test_tix_blackboard()
    elif module == 'tix.filedialog':
        return _test_tix_filedialog()
    elif module == 'tix.timer':
        return _test_tix_timer()
    elif module == 'turtledrawer':
        return _test_turtledrawer()

_clear()
