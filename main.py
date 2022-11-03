import tkinter as tk
import tkinter.messagebox as mb
import tkinter.filedialog as filedialog
import styles, detect
from modified_simpledialog import askinteger
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

        if detect.windows:

            # Creates a menu frame at the top of the app window.
            self.__menuFrame = tk.Frame(self.__root, background=styles.menu_background)
            self.__menuFrame.grid(row=0, column=0, sticky='news')

            # Create the dropdown heading for the file options.
            self.__fileMenu = tk.Menubutton(self.__menuFrame, text="File", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor, borderwidth=0)
            self.__fileMenu.grid(row=0, column=0, padx=5, pady=2)
            self.__fileOptions = tk.Menu(self.__fileMenu , tearoff=0, background=styles.menu_command_background, foreground=styles.foreground, activebackground=styles.active_menu_command_background, activeforeground=styles.foreground)
            self.__fileMenu.config(menu=self.__fileOptions)

            # Create the dropdown heading for the edit options.
            self.__editMenu = tk.Menubutton(self.__menuFrame, text="Edit", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor, borderwidth=0)
            self.__editMenu.grid(row=0, column=1, padx=5, pady=2)
            self.__editOptions = tk.Menu(self.__editMenu, tearoff=0, background=styles.menu_command_background, foreground=styles.foreground, activebackground=styles.active_menu_command_background, activeforeground=styles.foreground)
            self.__editMenu.config(menu=self.__editOptions)

            # Create the dropdown heading for the view options.
            self.__viewMenu = tk.Menubutton(self.__menuFrame, text="View", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor, borderwidth=0)
            self.__viewMenu.grid(row=0, column=2, padx=5, pady=2)
            self.__viewOptions = tk.Menu(self.__viewMenu, tearoff=0, background=styles.menu_command_background, foreground=styles.foreground, activebackground=styles.active_menu_command_background, activeforeground=styles.foreground)
            self.__viewMenu.config(menu=self.__viewOptions)

            # Create the dropdown heading for the help options.
            self.__helpMenu = tk.Menubutton(self.__menuFrame, text="Help", background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor, borderwidth=0)
            self.__helpMenu.grid(row=0, column=3, padx=5, pady=2)
            self.__helpOptions = tk.Menu(self.__helpMenu, tearoff=0, background=styles.menu_command_background, foreground=styles.foreground, activebackground=styles.active_menu_command_background, activeforeground=styles.foreground)
            self.__helpMenu.config(menu=self.__helpOptions)

        else:

            self.__menuBar = tk.Menu(self.__root)

            # Create the three menu dropdown headings.
            self.__fileOptions = tk.Menu(self.__menuBar, tearoff=0)
            self.__editOptions = tk.Menu(self.__menuBar, tearoff=0)
            self.__viewOptions = tk.Menu(self.__menuBar, tearoff=0)
            self.__helpOptions = tk.Menu(self.__menuBar, tearoff=0)

            # Add the heading labels and options menu to the menu headings.
            self.__menuBar.add_cascade(label="File", menu=self.__fileOptions)
            self.__menuBar.add_cascade(label="Edit", menu=self.__editOptions)
            self.__menuBar.add_cascade(label="View", menu=self.__viewOptions)
            self.__menuBar.add_cascade(label="Help", menu=self.__helpOptions)

            # Add the menu bar to the window.
            self.__root.config(menu=self.__menuBar)

        # Set of options regarding the file.
        self.__fileOptions.add_command(label="Open File", command=self.__loadFile, accelerator="Command-O" if styles.mac else "Ctrl+O")
        self.__fileOptions.add_separator()
        self.__fileOptions.add_command(label="Save", command=self.__saveFile, accelerator="Command-S" if styles.mac else "Ctrl+S")
        self.__fileOptions.add_command(label="Save As", command=self.__updateSaveFileLocation, accelerator="Command-Shift-S" if styles.mac else "Ctrl+Shift+S")
        self.__fileOptions.add_separator()
        self.__fileOptions.add_command(label="Exit", command=self.__exitProcess, accelerator="Command-W" if styles.mac else "Ctrl+W")

        # Set of options regarding text operations.
        self.__editOptions.add_command(label="Undo", command=self.__undo, accelerator="Command-Z" if styles.mac else "Ctrl+Z")
        self.__editOptions.add_command(label="Redo", command=self.__redo, accelerator="Command-Shift+Z" if styles.mac else "Ctrl+Shift+Z")
        self.__editOptions.add_separator()
        self.__editOptions.add_command(label="Copy", command=self.__copySelected, accelerator="Command-C" if styles.mac else "Ctrl+C")
        self.__editOptions.add_command(label="Paste", command=self.__pasteSelected, accelerator="Command-V" if styles.mac else "Ctrl+V")
        self.__editOptions.add_separator()
        self.__editOptions.add_command(label="Select All", command=self.__selectAll, accelerator="Command-A" if styles.mac else "Ctrl+A")
        self.__editOptions.add_command(label="Go To", command=self.__goToLine, accelerator="Command-G" if styles.mac else "Ctrl+G")
        self.__editOptions.add_separator()
        self.__editOptions.add_command(label="Start Fresh", command=self.__emptyFile)

        # Set of options regarding text view.
        self.__zoomOptions = tk.Menu(self.__viewOptions, tearoff=0, background=styles.menu_background, foreground=styles.foreground, activebackground=styles.active_menu_background, activeforeground=styles.foreground, cursor=styles.cursor)
        self.__zoomOptions.add_command(label="Zoom In", command=lambda: self.__zoomChange(1), accelerator="Command-+" if styles.mac else "Ctrl+Plus")
        self.__zoomOptions.add_command(label="Zoom Out", command=lambda: self.__zoomChange(-1), accelerator="Command--" if styles.mac else "Ctrl+Minus")
        self.__zoomOptions.add_command(label="Original Zoom", command=self.__originalZoom)
        self.__viewOptions.add_cascade(label="Zoom", menu=self.__zoomOptions)

        # Set of options regarding app help.
        self.__helpOptions.add_command(label="About Notepad", command=self.__displayAbout)

        # Extra window configs and key bindings.
        self.__root.bind("<Control-o>", func=self.__loadFile)
        self.__root.bind("<Command-o>", func=self.__loadFile)
        self.__root.bind("<Control-w>", func=self.__exitProcess)
        self.__root.bind("<Command-w>", func=self.__exitProcess)
        self.__root.bind("<Control-s>", func=self.__saveFile)
        self.__root.bind("<Command-s>", func=self.__saveFile)
        self.__root.bind("<Control-S>", func=self.__updateSaveFileLocation)
        self.__root.bind("<Command-S>", func=self.__updateSaveFileLocation)
        self.__root.bind("<Control-a>", func=self.__selectAll)
        self.__root.bind("<Command-a>", func=self.__selectAll)
        self.__root.bind("<Control-c>", func=self.__copySelected)
        self.__root.bind("<Command-c>", func=self.__copySelected)
        self.__root.bind("<Control-z>", func=self.__undo)
        self.__root.bind("<Command-z>", func=self.__undo)
        self.__root.bind("<Control-Z>", func=self.__redo)
        self.__root.bind("<Command-Z>", func=self.__redo)
        self.__root.bind("<Control-g>", func=self.__goToLine)
        self.__root.bind("<Command-g>", func=self.__goToLine)
        self.__root.bind("<Control-=>", func=lambda event: self.__zoomChange(1))
        self.__root.bind("<Command-=>", func=lambda event: self.__zoomChange(1))
        self.__root.bind("<Control-minus>", func=lambda event: self.__zoomChange(-1))
        self.__root.bind("<Command-minus>", func=lambda event: self.__zoomChange(-1))
        self.__root.bind("<KeyPress>", func=self.__updateCursorPositionDisplay)
        self.__root.bind("<space>", func=self.__addUndoStep)
        self.__root.bind("<Return>", func=self.__addUndoStep)
        self.__root.bind("<BackSpace>", func=self.__addUndoStep)
        self.__root.bind("<Control-BackSpace>", func=self.__removeWord)
        self.__root.bind("<Option-BackSpace>", func=self.__removeWord)
        self.__root.bind("<Alt-BackSpace>", func=self.__removeLine)
        self.__root.bind("<Command-BackSpace>", func=self.__removeLine)

        # Create the area where the text is typed.
        self.__textArea = tk.Text(self.__root, font=(styles.font, styles.font_size), borderwidth=0, background=styles.background, foreground=styles.foreground, insertbackground=styles.foreground, highlightthickness=0)
        self.__textArea.grid(row=1, column=0, sticky='news')
        self.__textArea.focus()

        # Create thes crollbar for the text area so that overflowing text can be shown.
        self.__textScrollBar = tk.Scrollbar(self.__textArea)
        self.__textScrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__textScrollBar.set)

        self.__infoFrame = tk.Frame(self.__root, background=styles.menu_background)
        self.__infoFrame.grid(row=2, column=0, sticky='news')

        self.__cursorPositionDisplay = tk.Label(self.__infoFrame, background=styles.menu_background, foreground=styles.foreground)
        self.__cursorPositionDisplay.grid(row=0, column=0, padx=5, pady=2)
        self.__updateCursorPositionDisplay()

        self.__infoFrameSeparator = tk.Label(self.__infoFrame, text="|", background=styles.menu_background, foreground=styles.foreground)
        self.__infoFrameSeparator.grid(row=0, column=1, padx=10, pady=2)

        self.__fontSizeDisplay = tk.Label(self.__infoFrame, background=styles.menu_background, foreground=styles.foreground)
        self.__fontSizeDisplay.grid(row=0, column=2, padx=5, pady=2)
        self.__updateFontSizeDisplay()

    # Adds a node to the redo stack.
    def __addRedoStep(self):
        node = self.__createNode(self.__textArea.get("1.0", "end").strip(), self.__textArea.index("insert"))
        self.__redoStack.push(node)
        return

    # Adds a node to the undo stack.
    def __addUndoStep(self, event=None):
        node = self.__createNode(self.__textArea.get("1.0", "end").strip(), self.__textArea.index("insert"))
        self.__undoStack.push(node)
        self.__updateCursorPositionDisplay()
        return

    # Can be used to create or clear the undo/redo stacks.
    def __clearStacks(self):
        self.__undoStack = Stack()
        self.__redoStack = Stack()
        return

    # Copies selected text.    
    def __copySelected(self, event=None):
        self.__copiedText = self.__textArea.selection_get()
        return

    # Cretes a node by storing the text and cursorPosition of the text area.
    def __createNode(self, text, cursorPosition):
        node = CustomNode()
        node.text = text
        node.cursorPosition = cursorPosition
        return node

    # Exits the app.
    def __destroy(self):
        self.__root.destroy()
        styles.app.destroy()

    # Displays information about the app.
    def __displayAbout(self):

        mb.showinfo(
            title="About Notepad",
            message="Version: 1.0\nAuthor: Mostafa El-Shoubaky"
        )

    # Clears text within the file upon user request and clears the undo and redo stacks while updating the cursor information display.
    def __emptyFile(self):

        if mb.askyesno(title="Empty Notepad Warning", message="WARNING: This action is not reversible. Are you sure you want to continue?", icon="warning"):
            self.__textArea.delete('1.0', 'end')

        self.__clearStacks()
        self.__updateCursorPositionDisplay()

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

    # Moves the cursor to the specified line number.
    def __goToLine(self, event=None):
        number_of_lines = int(self.__textArea.index("end").split(".")[0]) - 1
        line_asked = askinteger("Go To Line Number", "Enter the line you would like to go to:", bg=styles.background, fg=styles.foreground, minvalue=1, maxvalue=number_of_lines)

        if number_of_lines != None:
            self.__textArea.mark_set("insert", str(line_asked) + ".0")

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

    # Returns the font size to the original
    def __originalZoom(self):
        styles.font_size = styles.original_font_size
        self.__zoomChange(0)
        self.__updateFontSizeDisplay()
        return

    # Pastes copied text.
    def __pasteSelected(self):
        self.__addUndoStep()
        self.__textArea.insert('insert', self.__copiedText)
        self.__updateCursorPositionDisplay()
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
            self.__setSaved(False)
            self.__updateCursorPositionDisplay()
        
        return

    # Removes a line of text from the text area.
    def __removeLine(self, event=None):
        current_position = self.__textArea.index("insert")
        line, column = current_position.split(".")

        if current_position == "1.0":
            return

        self.__addUndoStep()
        self.__textArea.delete(str(line) + ".0", current_position)
        self.__updateCursorPositionDisplay()
        
        return

    # Removes a set of characters between the current position of the cursor and (a space or a newline).
    def __removeWord(self, event=None):

        # Gets the current posiiton and makes new variables for the line and column.
        current_position = self.__textArea.index("insert")
        line, column = current_position.split(".")

        # Returns from the procedure if the cursor is right at the start.
        if current_position == "1.0":
            return

        # Add undo step to undo if error is made.
        self.__addUndoStep()

        done = False

        # Goes back one letter every round of while loop and checks if character is a space. If the start of the line is reached, whole line is deleted.
        while (not done):
            new_posiiton = str(line) + "." + str(int(column) - 1)
            character = self.__textArea.get(new_posiiton, str(line) + "." + str(column))

            if int(column) == 0:
                self.__textArea.delete(str(line) + ".0", current_position)
                done = True
            elif character == " ":
                self.__textArea.delete(new_posiiton, current_position)
                done = True
            else:
                column = str(int(column) - 1)

        self.__updateCursorPositionDisplay()
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

    # Selects all text within the text area. The returned string "break" stops default functioanlity of Ctrl+A / Cmd+A.
    def __selectAll(self, event=None):
        self.__textArea.tag_add("sel", "1.0", "end")
        return

    # Changes the "saved" attribute used when exiting the program.
    def __setSaved(self, saved, event=None):
        self.__saved = saved
        return

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
            self.__setSaved(False)
            self.__updateCursorPositionDisplay()
        
        return

    # Updates the label that states the line number and column that the cursor is on.
    def __updateCursorPositionDisplay(self, event=None):
        line, column = self.__textArea.index("insert").split(".")
        self.__cursorPositionDisplay.config(text="Ln " + str(line) + ", Col " + str(int(column) + 1))
        return

    # Updates the displayed font size.
    def __updateFontSizeDisplay(self, event=None):
        self.__fontSizeDisplay.config(text="Font Size: " + str(styles.font_size))
        return

    # Updates the file location.
    def __updateSaveFileLocation(self, event=None):

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

    # Updates window title to the directory of the file.
    def __updateTitle(self):
        self.__root.title(str(self.__fileName)) if self.__fileName != "" else None
        return

    # Changes font size.
    def __zoomChange(self, change_by, event=None):
        bigger_than_max = styles.font_size + change_by >= styles.max_size
        smaller_than_min = styles.font_size + change_by <= styles.min_size

        if not (bigger_than_max or smaller_than_min):
            styles.font_size += change_by
        
        self.__textArea.config(font=(styles.font, styles.font_size))
        self.__updateFontSizeDisplay()
        return

    # Starts the app.
    def start(self):
        self.__root.mainloop()

if __name__ == "__main__":
    n = Notepad(window=tk.Tk())
    n.start()