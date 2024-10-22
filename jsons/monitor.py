from time import sleep
from json import load
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database import carregaJson

class MonitorJSON(FileSystemEventHandler):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == "./dynamics.json":
            with open('dynamics.json', 'r') as file:
                self.recarregaJson()
    
    def recarregaJson(self):
        with open('dynamics.json', 'r') as file:
            dados = load(file)
            self.callback(dados)

def obs_init(callback):

    caminho = "."
    observer = Observer()
    handler = MonitorJSON(callback)
    observer.schedule(handler, path= caminho, recursive= False)
    observer.start()

    try:
        while True:
            sleep(1)
    except Exception:
        observer.stop()
    observer.join()