import asyncio
import json
import tkinter as tk
from tkinter import ttk
import os

entry_width = 25

def configurate(name: str, settings: dict[str, tuple[float, float]], **kwargs) -> dict[str, any]:
    win =  tk.Tk()
    win.geometry(f"{600}x{entry_width * (len(settings) + 2)}")
    win.title(name)

    filename = f"./saves/{name}_config.json"
    if os.path.isfile(filename):
        file = json.loads(open(filename, 'r').read())
    else:
        file = None

    entries = {}
    for row, (setting, minmax) in enumerate(settings.items()):
        label = ttk.Label(win, text=setting)
        label.grid(column=0, row=row)
        entry = ttk.Entry(win, width=50)
        if file != None and setting in file.keys():
            entry.insert(0, file[setting])
        entry.grid(column=1, row=row)
        entries[setting] = entry

    launcher = ttk.Button(win, text="Сохранить и запустить симуляцию")
    launcher.grid(column=0, row=len(entries), columnspan=2)

    error = ttk.Label(win, foreground="#f00")
    error.grid(column=0, row=len(entries) + 1, columnspan=2)
    
    get_result = lambda: dict([(setting, float(entry.get())) for setting, entry in entries.items()])

    launching = False
    def launch():
        for setting, entry in entries.items():
            try:
                bounds = settings[setting]
                if float(entry.get()) < bounds[0] or bounds[1] < float(entry.get()):
                    error.config(text=f"Значение `{setting}` должно быть в диапозоне [{bounds[0]},{bounds[1]}]")
                    return
            except ValueError:
                error.config(text=f"Значение `{setting}` должно быть числом")
                return
        
        open(filename, 'w').write(json.dumps(get_result()))

        nonlocal launching
        launching = True
    launcher.config(command=launch)

    if kwargs.get("quick_mode", False):
        launch()

    while not launching and len(win.children):
        win.update()
    
    if len(win.children):
        result = get_result()
        win.destroy()
        return result
    else:
        return {}

if __name__ == "__main__":
    print(configurate("test", {"number a" : (0, 100), "number b" : (-10, 10)}))