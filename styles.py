import detect, darkdetect
import tkinter as tk

# Remove secondary window upon creation.
app = tk.Tk()
app.overrideredirect(True)
app.withdraw()

# Font options.
font = "Segoe UI Variable" if detect.windows else "San Fransisco"
originalFontSize = int(tk.Frame().winfo_screenwidth() / 128)
fontSize = int(tk.Frame().winfo_screenwidth() / 128)
maxSize = int(tk.Frame().winfo_screenwidth() / 64)
minSize = int(tk.Frame().winfo_screenwidth() / 320)

# Check whether mac
mac = True if detect.mac else False

# Compatible cursor
cursor = ""
if detect.mac == True:
    cursor = "pointinghand"
elif detect.windows == True:
    cursor = "@Windows_Hand.cur"
else:
    cursor = ""

# Check dark
dark = darkdetect.isDark()

# Sets colours depending on whether dark or not
menuBackground = "#202020" if dark else "#f3f3f3"
background = "#272727" if dark else "#f9f9f9"
activeMenuBackground = "#2d2d2d" if dark else "#eaeaea"
menuCommandBackground = activeMenuBackground
activeMenuCommandBackground = "#383838" if dark else "#f0f0f0"
foreground = "white" if dark else "black"