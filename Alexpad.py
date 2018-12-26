import tkinter as tk

from tkinter import filedialog

import os


from tkinter import messagebox



class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Untitled - AlexPad")

        self.mainFrame = MainFrame(self)
        self.mainFrame.pack(fill="both", expand=True)

        self.mainFrame.text.focus_set()
        self.protocol("WM_DELETE_WINDOW", lambda : self.save_before_leave(self.destroy))

    def save_before_leave(self, callback, *args):

        textBuffer = self.mainFrame.text.get('1.0', 'end-1c')

        
        if self.mainFrame.curFilePath:
           
            if self.mainFrame.curFileCont != textBuffer:
                response = messagebox.askyesnocancel("AlexPad - Unsaved File", "Do you want to save before leaving?")
                
                if response:
                    self.mainFrame.save_file()
                    callback()
              
                elif response is False:
                    callback()

            else:
                callback()

        else:
            
            if textBuffer:
                response = messagebox.askyesnocancel("AlexPad - Unsaved File", "Do you want to save before leaving?")
               
                if response:
                    self.mainFrame.save_as_file()
                    callback()
               
                elif response is False:
                    callback()
            else:
                callback()
      
        return "break"
        



class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

       
        self.menu = MainMenu(master)
        master.config(menu=self.menu)

       
        self.curFilePath = ''

       
        self.curFileCont = ''

        self.text = tk.Text(self, wrap="none")
      
        self.text.config(bg='#FFFFFF',fg='#000000', selectbackground='#FF8000')
        self.text.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.scroll_bar_config()
        self.menu_command_config()
        self.key_binds_config()


  
    def scroll_bar_config(self):

        self.scrollY = AutoScrollbar(self, orient="vertical", command=self.text.yview)
        self.scrollY.grid(row=0, column=1, sticky="nsew")
        self.text['yscrollcommand'] = self.scrollY.set

        self.scrollX = AutoScrollbar(self, orient="horizontal", command=self.text.xview)
        self.scrollX.grid(row=1, column=0, sticky="nsew")
        self.text['xscrollcommand'] = self.scrollX.set

    def menu_command_config(self):
        #New
        self.menu.file.entryconfig(0, command=lambda : self.master.save_before_leave(self.new_file))
        #Open...
        self.menu.file.entryconfig(1, command=lambda : self.master.save_before_leave(self.open_file))
        #Save
        self.menu.file.entryconfig(2, command=self.save_file)
        #Save as
        self.menu.file.entryconfig(3, command=self.save_as_file)

        #Cut
        self.menu.edit.entryconfig(0, command=self.cut)
        #Copy
        self.menu.edit.entryconfig(1, command=self.copy)
        #Paste
        self.menu.edit.entryconfig(2, command=self.paste)
        #Delete
        self.menu.edit.entryconfig(3, command=self.delete)

    def key_binds_config(self):
        self.text.bind('<Control-n>', lambda event : self.master.save_before_leave(self.new_file))
        self.text.bind('<Control-N>', lambda event : self.master.save_before_leave(self.new_file))
        self.text.bind('<Control-o>', lambda event : self.master.save_before_leave(self.open_file))
        self.text.bind('<Control-O>', lambda event : self.master.save_before_leave(self.open_file))
        self.text.bind('<Control-s>', self.save_file)
        self.text.bind('<Control-S>', self.save_file)
        self.text.bind('<Control-Shift-s>', self.save_as_file)
        self.text.bind('<Control-Shift-S>', self.save_as_file)

    def new_file(self, *args):
        self.text.delete("1.0", "end")
        self.curFilePath = ''
        self.curFileCont = ''

      
        self.master.title("Untitled - AlexPad")


    def open_file(self, *args):

       
        filePath = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),("All files", "*.*")))

        
        if filePath:
            try:
                
                with open(filePath, encoding="UTF-8") as f:
                    self.text.delete("1.0", "end")
                    self.curFileCont = f.read()
                    self.text.insert("1.0", self.curFileCont)
            
            except UnicodeDecodeError:
               
                with open(filePath, encoding="ANSI") as f:
                    self.text.delete("1.0", "end")
                    self.curFileCont = f.read()
                    self.text.insert("1.0", self.curFileCont)

            
            self.master.title(os.path.basename(f.name) + " - AlexPad")

            
            self.curFilePath = filePath

    def save_file(self, *args):
       
        if self.curFilePath:
            try:
               
                with open(self.curFilePath, 'w', encoding="UTF-8") as f:
                    self.curFileCont = self.text.get('1.0', 'end-1c')
                    f.write(self.curFileCont)
            
            except UnicodeDecodeError:
               
                with open(self.curFilePath, 'w', encoding="ANSI") as f:
                    self.curFileCont = self.text.get('1.0', 'end-1c')
                    f.write(self.curFileCont)

            
            self.master.title(os.path.basename(f.name) + " - AlexPad")

        else:
            self.save_as_file()

    def save_as_file(self, *args):
        self.curFilePath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"),("All files", "*.*")))
        
        if self.curFilePath:
            self.save_file()


    def cut(self):
       
        if self.text.tag_ranges(tk.SEL):
            self.text.clipboard_clear()
            
            self.text.clipboard_append(self.text.get(tk.SEL_FIRST, tk. SEL_LAST))
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)

    def copy(self):
        
        if self.text.tag_ranges(tk.SEL):
            self.text.clipboard_clear()
           
            self.text.clipboard_append(self.text.get(tk.SEL_FIRST, tk. SEL_LAST))

    def paste(self):
      
        if self.text.tag_ranges(tk.SEL):
           
            selFirstIndex = self.text.index(tk.SEL_FIRST)
            
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)
           
            self.text.insert(selFirstIndex, self.text.clipboard_get())

        else:
            self.text.insert(tk.INSERT, self.text.clipboard_get())

    def delete(self):
       
        if self.text.tag_ranges(tk.SEL):
            self.text.delete(tk.SEL_FIRST, tk. SEL_LAST)
    



class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.master = master

        
        self.file = FileMenu(self)
        self.add_cascade(label="File", menu=self.file)

        self.edit = EditMenu(self)
        self.add_cascade(label="Edit", menu=self.edit)



class FileMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)
        self.master = master

        self.add_command(label="New                Ctrl + N")
        self.add_command(label="Open...          Ctrl + O")
        self.add_command(label="Save               Ctrl + S")
        self.add_command(label="Save As...      Ctrl + Shift + S")


        
        self.add_separator()
        
        self.add_command(label="Exit                 Alt + F4", command=lambda : master.master.save_before_leave(self.master.master.destroy))



class EditMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, tearoff=0)

        self.add_command(label="Cut              Ctrl + X")
        self.add_command(label="Copy           Ctrl + C")
        self.add_command(label="Paste          Ctrl + V")
        self.add_command(label="Delete         Delete")



class AutoScrollbar(tk.Scrollbar):
   
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)


def test():
    with open(__file__, "rU") as f:
        root.mainFrame.text.insert("1.0", f.read())


if __name__ == "__main__":
    root = MainWindow()
    #test()
    root.mainloop()