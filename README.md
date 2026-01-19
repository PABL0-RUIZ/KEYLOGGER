#  Keylogger Educativo en Python

Este proyecto es un **Keylogger Educativo** desarrollado en Python. Ha sido diseñado con una arquitectura modular para facilitar su comprensión, mantenimiento y expansión.

> **Nota:** Este software ha sido creado exclusivamente con fines educativos y de aprendizaje sobre ciberseguridad. El uso de keyloggers sin consentimiento en ordenadores ajenos es ilegal.

## Características

1.  **Monitorización de Teclado**: Captura pulsaciones de teclas en tiempo real.
2.  **Monitorización de Ventanas**: Detecta cambios en la ventana activa y registra el título.
3.  **Capturas de Pantalla**: Toma un screenshot automáticamente cada vez que el usuario cambia de ventana.
4.  **Almacenamiento Versátil**:
    *   **Local**: Guarda logs en `logs/log.txt`.
    *   **Email**: Envía reportes periódicos por correo electrónico.
    *   **FTP**: Capacidad para subir logs a un servidor remoto.

## Estructura del Proyecto

El código está organizado en módulos (`modules/`) para separar responsabilidades:

*   `main.py`: Punto de entrada. Coordina los hilos y la ejecución principal.
*   `modules/key_monitor.py`: Gestiona la captura de teclas usando la librería `pynput`.
*   `modules/window_monitor.py`: Interactúa con la API de Windows (`ctypes`) para detectar la ventana activa.
*   `modules/storage_manager.py`: Encapsula la lógica de guardado local, envío de correos y FTP.

## Instalación y Uso

1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuración**:
    Edita el archivo `config.json` para configurar el envío de correos (opcional):
    ```json
    "email": {
        "sender": "tu_email@gmail.com",
        "password": "tu_app_password",
        ...
    }
    ```

3.  **Ejecutar**:
    ```bash
    python main.py
    ```

4.  **Ver Resultados**:
    *   Los textos se guardan en `logs/log.txt`.
    *   Las capturas se guardan en `logs/screenshots/`.
