import ctypes
import time
import os
from threading import Thread
from PIL import ImageGrab
from datetime import datetime

class WindowMonitor:
    def __init__(self, callback, screenshot_dir):
        """
        :param callback: Función a llamar cuando cambia la ventana.
        :param screenshot_dir: Directorio donde guardar capturas.
        """
        self.callback = callback
        self.screenshot_dir = screenshot_dir
        self.is_running = False
        self.last_window = "None"
        
        # Cargar librerías de usuario de Windows
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

    def start(self):
        self.is_running = True
        self.thread = Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        print("[WindowMonitor] Iniciado.")

    def stop(self):
        self.is_running = False
        print("[WindowMonitor] Detenido.")

    def _get_active_window_title(self):
        hwnd = self.user32.GetForegroundWindow()
        length = self.user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        self.user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    def _take_screenshot(self, window_title):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Limpiamos el nombre del archivo de caracteres inválidos
            safe_title = "".join([c for c in window_title if c.isalnum() or c in (' ', '-', '_')]).strip()[:30]
            filename = f"screenshot_{timestamp}_{safe_title}.png"
            path = os.path.join(self.screenshot_dir, filename)
            
            screenshot = ImageGrab.grab()
            # Redimensionar si es necesario para ahorrar espacio (opcional, aquí guardamos original)
            screenshot.save(path, optimize=True, quality=50)
            return path
        except Exception as e:
            print(f"Error tomando captura: {e}")
            return None

    def _monitor_loop(self):
        while self.is_running:
            try:
                current_window = self._get_active_window_title()
                if current_window != self.last_window and current_window.strip() != "":
                    self.last_window = current_window
                    
                    # Notificar cambio
                    message = f"\n[WINDOW CHANGED: {current_window} - {datetime.now()}]\n"
                    self.callback(message)
                    
                    # Tomar screenshot (opcional: solo si no es vacío)
                    self._take_screenshot(current_window)
                    
            except Exception as e:
                print(f"Error en WindowMonitor: {e}")
            
            time.sleep(1) # Revisar cada segundo
