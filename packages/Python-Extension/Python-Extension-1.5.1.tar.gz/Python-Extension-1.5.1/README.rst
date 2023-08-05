Brief Introduction of Python-Extension

Python-Extension is an extension of Python.


What's New In Python-Extension 1.5
  Python-Extension
    1.Module requirements removed ( python-docx 0.8 and above )
  Pyextension
    Pyextension
      1.New function pyextension.clear() to clear the cache ( consistent with function test._clear() )
    Mathematics
      1.Removed version requirements ( Python 3.10 and above )
    Test
      1.Now can delete the cache 'word bank.dat' using test._clear()
    Unicode
      1.New module Unicode
      2.Function search(thing)
        If thing is a string type, return the unicode number of it
        If thing is a int type, return the corresponding character of it
      3.Function table(items, cols, add_numbers=False)
        Returns a UTF-8 / ASCII table with cols columns
        If the parameter add_numbers is true,
        the corresponding encoding sequence number will be added before the encoding character
      4.Function listcode(items, add_numbers=False)
        Returns a UTF-8 / ASCII list
        If the parameter add_numbers is true,
        the corresponding encoding sequence number will be added before the encoding character
    Word Bank
      1.Added new Word Bank Data
      2.New function word_bank.uninstall(location), word_bank.get()
    Word
      1.Removed module Word
  
  Tkextension
    Tkextension
      1.All dialog windows are now created using the components of the tkextension.tix library
    Blackboard
      1.Now it belongs to the tkextension.tix library(tkextension.tix.blackboard), but it can still be imported using 'import tkextension.blackboard'
      2.Now can choose sqrite that draw when click right-button
    Timer
      1.Now it belongs to the tkextension.tix library(tkextension.tix.timer), but it can still be imported using 'import tkextension.timer'


Pyextension

Pyextension includes main modules
(about function, open source function, computer information function, quick document processing),
mathematical function processing module, password encryption module,
unicode module and English Thesaurus module.


Tkextension

Tkextense includes dialog window, tix widget,
quick generation of Tkinter object,
tix module, tix.blackboard module,
tix.filedialog module, tix.timer module
open source module,
and turtle graphics drawing module