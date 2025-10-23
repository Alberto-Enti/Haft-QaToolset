from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import tkinter as tk
import os

LOG_PATH = r"C:\ProgramasQA\LogDisplay\log.txt" #rutaLogs

class LogHandler(FileSystemEventHandler):
    def __init__(self, label):
        self.label = label
        self.last_pos = 0

    def on_modified(self, event):
        if event.src_path.endswith("log.txt") or "log.txt" in event.src_path:
            try:
                with open(LOG_PATH, "r", encoding="utf-8") as f:
                    f.seek(self.last_pos)
                    new_lines = f.readlines()
                    self.last_pos = f.tell()
                if new_lines:
                    self.label.config(text=new_lines[-1].strip())
            except FileNotFoundError:
                self.last_pos = 0


root = tk.Tk()
root.title("Unity Log Viewer")
root.geometry("500x80")
root.configure(bg="#222")

label = tk.Label(root, text="Esperando log...", fg="#ff00ee", bg="#22ff00", font=("Consolas", 22))
label.pack(fill="both", expand=True)

event_handler = LogHandler(label)
observer = Observer()
observer.schedule(event_handler, path=os.path.dirname(LOG_PATH), recursive=False)

try:
    observer.start()
except Exception as e:
    print("Error iniciando observer:", e)

try:
    root.mainloop()
finally:
    observer.stop()
    observer.join()

