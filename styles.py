import detect, darkdetect
import tkinter as tk

# Remove secondary window upon creation.
app = tk.Tk()
app.overrideredirect(1)
app.withdraw()

# Font options.
font = "Segoe UI Variable" if detect.windows else "San Fransisco"
original_font_size = int(tk.Frame().winfo_screenwidth() / 128)
font_size = int(tk.Frame().winfo_screenwidth() / 128)
max_size = int(tk.Frame().winfo_screenwidth() / 64)
min_size = int(tk.Frame().winfo_screenwidth() / 320)

# Check whether mac
mac = True if detect.mac else False

# Compatible cursor
cursor = "pointinghand" if mac else "@Windows_Hand.cur"

# Check dark
dark = darkdetect.isDark()

# Sets colours depending on whether dark or not
menu_background = "#202020" if dark else "#f3f3f3"
background = "#272727" if dark else "#f9f9f9"
active_menu_background = "#2d2d2d" if dark else "#eaeaea"
foreground = "white" if dark else "black"