#Módulo do monitor do arquivo dynamics.json
from time import sleep, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from . import recarregaJson

#Classe de atuação do watchdog
class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, watchPath) -> None:
        self.watchPath = watchPath

        #Reset do tempo do evento passado
        self.last_modified = 0

    #Função de callback de modificação do arquivo json
    def on_modified(self, event) -> None:

        if not event.is_directory and event.src_path == self.watchPath:

            #Salva o tempo atual em segundos
            tempo_atual = time()

            #Executa o recarregamento apenas se o tempo entre eventos for menor que um segundo
            if tempo_atual - self.last_modified > 1:

                print(f"Modificado com sucesso")
                recarregaJson()
                self.last_modified = tempo_atual

#Classe do observador do watchdog
class Watchdog:
    def __init__(self, handler) -> None:
        self.handler = handler
        self.watchPath = handler.watchPath
        self.observer = Observer()
    
    #Inicialização
    def start(self) -> None:
        self.observer.schedule(self.handler, path = self.handler.watchPath, recursive= False)

        try:
            self.observer.start()

            while True:
                sleep(1)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            print(f'Algo deu errado: {e}')

    #Parada
    def stop(self) -> None:
        self.observer.stop()
        self.observer.join()