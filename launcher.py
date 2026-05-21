import subprocess
import os
import webbrowser
import time
import sys
import tkinter
import tkinter.messagebox



#folder = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
exe_path = os.path.abspath(sys.executable)
folder = os.path.dirname(exe_path)
 
app_path = os.path.join(folder, "app.py")
tkinter.messagebox.showinfo("Debug", f"exe: {exe_path}\nfolder: {folder}\napp: {app_path}")
subprocess.Popen(["streamlit", "run", app_path, "--server.headless", "true"])

time.sleep(3)

webbrowser.open("http://localhost:8501")


