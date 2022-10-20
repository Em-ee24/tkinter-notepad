import tkinter, detect, darkdetect
from tkinter import ttk

font = "Segoe UI Variable" if detect.windows else "San Fransisco"
mac = True if detect.mac else False

cursor = "pointinghand" if mac else "@Windows_Hand.cur"

dark = darkdetect.isDark()

menu_background = "#202020" if dark else "#f3f3f3"
background = "#272727" if dark else "#f9f9f9"
active_menu_background = "#2d2d2d" if dark else "#eaeaea"
foreground = "white" if dark else "black"