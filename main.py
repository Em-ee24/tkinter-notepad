import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as filedialog
import styles, detect
from stack import Stack, CustomNode

class Notepad:

    def __init__(self, *args, **kwargs):
        width = int(tk.Frame().winfo_screenwidth() / 2)
        height = int(tk.Frame().winfo_screenheight() / 2)

        # Where the file is located. Used as the title of the window.
        self.__fileName = ""

        # Whether the file is saved or not.
        self.__saved = False

        # Copied text stored in this variable
        self.__copiedText = ""

        # Creates undo and redo stacks.
        self.__clearStacks()

        # Root window configs
        self.__root = kwargs['window']
        self.__root.geometry(str(width) + "x" + str(height) + "+0+0")
        self.__root.title("Untitled")
        self.__root.iconbitmap("pen.ico")
        self.__root.grid_rowconfigure(1, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__root.protocol("WM_DELETE_WINDOW", self.__exitProcess)
        self.__root.config()

        if detect.windows:

            # Creates a menu frame at the top of the app window.
            self.__menuFrame = tk.Frame(self.__root, background=styles.menu_background)
            self.__menuFrame.grid(row=0, column=0, sticky='news')

            # Create the dropdown heading for the file options.
            self.__fileMenu = tk.Menubutton(self.__menuFrame, text="File", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor)
            self.__fileMenu.grid(row=0, column=0, padx=5)
            self.__fileOptions = tk.Menu(self.__fileMenu , tearoff=0, background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground)
            self.__fileMenu.config(menu=self.__fileOptions)

            # Create the dropdown heading for the edit options.
            self.__editMenu = tk.Menubutton(self.__menuFrame, text="Edit", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground,  )
            self.__editMenu.grid(row=0, column=1, padx=5)
            self.__editOptions = tk.Menu(self.__editMenu, tearoff=0, background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground)
            self.__editMenu.config(menu=self.__editOptions)

            # Create the dropdown heading for the help options.
            self.__helpMenu = tk.Menubutton(self.__menuFrame, text="Help", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor)
            self.__helpMenu.grid(row=0, column=2, padx=5)
            self.__helpOptions = tk.Menu(self.__helpMenu, tearoff=0, background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground)
            self.__helpMenu.config(menu=self.__helpOptions)

        else:

            self.__menuBar = tk.Menu(self.__root)

            # Create the three menu dropdown headings.
            self.__fileOptions = tk.Menu(self.__menuBar, tearoff=0)
            self.__editOptions = tk.Menu(self.__menuBar, tearoff=0)
            self.__helpOptions = tk.Menu(self.__menuBar, tearoff=0)

            # Add the heading labels and options menu to the menu headings.
            self.__menuBar.add_cascade(label="File", menu=self.__fileOptions)
            self.__menuBar.add_cascade(label="Edit", menu=self.__editOptions)
            self.__menuBar.add_cascade(label="Help", menu=self.__helpOptions)

            # Add the menu bar to the window.
            self.__root.config(menu=self.__menuBar)

        # Set of options regarding the file.
        self.__fileOptions.add_command(label="Open File", command=self.__loadFile, accelerator="Command-O" if styles.mac else "Ctrl+O")
        self.__fileOptions.add_command(label="Save", command=self.__saveFile, accelerator="Command-S" if styles.mac else "Ctrl+S")
        self.__fileOptions.add_command(label="Exit", command=self.__exitProcess, accelerator="Command-W" if styles.mac else "Ctrl+W")

        # Set of options regarding text operations.
        self.__editOptions.add_command(label="Copy", command=self.__copySelected, accelerator="Command-C" if styles.mac else "Ctrl+C")
        self.__editOptions.add_command(label="Paste", command=self.__pasteSelected, accelerator="Command-V" if styles.mac else "Ctrl+V")
        self.__editOptions.add_command(label="Undo", command=self.__undo, accelerator="Command-Z" if styles.mac else "Ctrl+Z")
        self.__editOptions.add_command(label="Redo", command=self.__redo, accelerator="Command-Shift+Z" if styles.mac else "Ctrl+Shift+Z")
        self.__editOptions.add_command(label="Start Fresh", command=self.__emptyFile)

        # Set of options regarding app help.
        self.__helpOptions.add_command(label="About Notepad", command=self.__displayAbout)

        # Extra window configs and key bindings.
        self.__root.bind("<Control-o>", func=self.__loadFile)
        self.__root.bind("<Command-o>", func=self.__loadFile)
        self.__root.bind("<Control-w>", func=self.__exitProcess)
        self.__root.bind("<Command-w>", func=self.__exitProcess)
        self.__root.bind("<Control-s>", func=self.__saveFile)
        self.__root.bind("<Command-s>", func=self.__saveFile)
        self.__root.bind("<Control-c>", func=self.__copySelected)
        self.__root.bind("<Command-c>", func=self.__copySelected)
        self.__root.bind("<Control-z>", func=self.__undo)
        self.__root.bind("<Command-z>", func=self.__undo)
        self.__root.bind("<Control-Z>", func=self.__redo)
        self.__root.bind("<Command-Z>", func=self.__redo)
        self.__root.bind("<KeyPress>", func=lambda event: self.__setSaved(saved=False))
        self.__root.bind("<space>", func=self.__addUndoStep)
        self.__root.bind("<Return>", func=self.__addUndoStep)
        self.__root.bind("<BackSpace>", func=self.__addUndoStep)

        # Create the area where the text is typed.
        self.__textArea = tk.Text(self.__root, font=(styles.font, 11), borderwidth=0, background=styles.background, foreground=styles.foreground)
        self.__textArea.grid(row=1, column=0, sticky='news')
        self.__textArea.focus()

        # Create thes crollbar for the text area so that overflowing text can be shown.
        self.__textScrollBar = tk.Scrollbar(self.__textArea)
        self.__textScrollBar.config(command=self.__textArea.yview)
        self.__textScrollBar.pack(side="right", fill="y")
        self.__textArea.config(yscrollcommand=self.__textScrollBar.set)

    # Can be used to create or clear the undo/redo stacks.
    def __clearStacks(self):
        self.__undoStack = Stack()
        self.__redoStack = Stack()
        return

    # Changes the "saved" attribute used when exiting the program.
    def __setSaved(self, saved, event=None):
        self.__saved = saved
        return

    # Updates window title to the directory of the file.
    def __updateTitle(self):
        self.__root.title(str(self.__fileName)) if self.__fileName != "" else None
        return

    # Loads text file from user's computer.
    def __loadFile(self, event=None):

        # Gets the directory of the file.
        self.__fileName = filedialog.askopenfilename(
            defaultextension='*.txt',
            filetypes=[
                ("Text Documents", "*.txt"),
                ("All Files", "*.*"),
            ]
        )

        # Check to make sure they havent cancelled file open.
        if self.__fileName != "":
            self.__updateTitle()

            file = open(self.__fileName, "r")
            contents = file.read()
            file.close()

            self.__textArea.insert("1.0", contents)
            self.__setSaved(True)
            self.__clearStacks()
        else:
            mb.showerror(title="Open Error", message="Failed to open file. Please try again.")

        return

    # Updates the file location.
    def __updateSaveFileLocation(self):

        # Gets the directory of the file.
        self.__fileName = filedialog.asksaveasfilename(
            initialfile="Untitled.txt",
            defaultextension=".txt",
            filetypes=[
                ("Text Documents", "*.txt"),
                ("All Files", "*.*"),
            ]
        )

        # Check to make sure they havent cancelled file save.
        if self.__fileName != "":
            self.__updateTitle()
        return

    # Checks to see where to save the file before saving. If empty (user cancelled saving) then the program will display a message withot saving.
    def __saveFile(self, event=None):

        if self.__fileName == "":
            self.__updateSaveFileLocation()

        # Check file location again to make sure they haven't cancelled. If they have then display a message to them.
        if self.__fileName != "":
            file = open(self.__fileName, "w")
            file.write(self.__textArea.get('1.0', 'end'))
            file.close()
            self.__setSaved(True)
        else:
            mb.showerror(title="Save Error", message="Your file hasn't been saved. Please try again.")

        return

    # Asks and saves the file upon user request and before closing the app.
    # If its saved then the exit the program without asking.
    # If it's not saved then the user is asked whether they want the file saved or not.
    def __exitProcess(self, event=None):

        exit = False

        if self.__saved:
            exit = True
        elif mb.askyesno(title="Save File", message="Would you like to save this file?"):
            self.__saveFile()
            if self.__saved:
                exit = True
        else:
            exit = True

        if exit:
            self.__destroy()
        
        return

    # Copies selected text.    
    def __copySelected(self, event=None):
        self.__copiedText = self.__textArea.selection_get()
        return

    # Pastes copied text.
    def __pasteSelected(self):
        self.__addUndoStep()
        self.__textArea.insert('insert', self.__copiedText)
        return

    # Clears text within the file upon user request and clears the undo and redo stacks.
    def __emptyFile(self):

        if mb.askyesno(title="Empty Notepad Warning", message="WARNING: This action is not reversible. Are you sure you want to continue?", icon="warning"):
            self.__textArea.delete('1.0', 'end')

        self.__clearStacks()
        return

    # Adds a node to the undo stack.
    def __addUndoStep(self, event=None):
        node = self.__createNode(self.__textArea.get("1.0", "end").strip(), self.__textArea.index("insert"))
        self.__undoStack.push(node)
        return

    # Adds a node to the redo stack.
    def __addRedoStep(self):
        node = self.__createNode(self.__textArea.get("1.0", "end").strip(), self.__textArea.index("insert"))
        self.__redoStack.push(node)
        return

    # Cretes a node by storing the text and cursorPosition of the text area.
    def __createNode(self, text, cursorPosition):
        node = CustomNode()
        node.text = text
        node.cursorPosition = cursorPosition
        return node

    # Adds text to the redo stack and then undoes all characters up to one space. Done by replacing all the text within the file.
    def __undo(self, event=None):

        # Save text area state if user wants to redo after undo.
        self.__addRedoStep()

        # Get last saved state from undoStack.
        node = self.__undoStack.pop()
        self.__textArea.delete("1.0", "end")

        if node != None:
            self.__textArea.insert("1.0", node.text)
            self.__textArea.mark_set("insert", node.cursorPosition)
        
        return

    # Adds the text that was undone from the __undo method. 
    def __redo(self, event=None):

        # Save text area state if user wants to undo after redo.
        self.__addUndoStep()

        # Gets last saved state from redoStack.
        node = self.__redoStack.pop()

        if node != None:
            self.__textArea.delete("1.0", "end")
            self.__textArea.insert("1.0", node.text)
            self.__textArea.mark_set("insert", node.cursorPosition)
        
        return

    # Displays information about the app.
    def __displayAbout(self):

        mb.showinfo(
            title="About Notepad",
            message="Version: 1.0\nAuthor: Mostafa El-Shoubaky"
        )

    # Exits the app.
    def __destroy(self):
        self.__root.destroy()

    # Starts the app.
    def start(self):
        self.__root.mainloop()

if __name__ == "__main__":
    n = Notepad(window=tk.Tk())
    n.start()