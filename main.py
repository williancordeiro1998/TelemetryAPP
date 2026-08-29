import json
import logging
import threading
import time
import urllib.request
import os

# Importações do Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class TelemetryAgent:
    def __init__(self, endpoint: str, interval: int = 10, log_callback=None):
        self.endpoint = endpoint
        self.interval = interval
        self.stop_event = threading.Event()
        self.log_callback = log_callback  # Usado para enviar mensagens para a tela do app

    def _log_ui(self, message):
        logging.info(message)
        if self.log_callback:
            # Clock.schedule_once garante que a UI seja atualizada na thread principal
            Clock.schedule_once(lambda dt: self.log_callback(message))

    def collect(self) -> dict:
        # Coleta de dados segura para Android e Desktop
        telemetry_data = {
            "platform": platform,  # Retorna 'android', 'win', 'linux', etc.
            "timestamp": time.time(),
        }

        if platform == 'android':
            # Tenta pegar informações reais do hardware no Android via PyJNIus
            try:
                from jnius import autoclass
                Build = autoclass('android.os.Build')
                telemetry_data["device_model"] = Build.MODEL
                telemetry_data["manufacturer"] = Build.MANUFACTURER
                telemetry_data["android_version"] = Build.VERSION.RELEASE
            except Exception as e:
                telemetry_data["device_model"] = "Android Genérico"
        else:
            import platform as py_platform
            telemetry_data["device_model"] = py_platform.node()
            telemetry_data["system"] = py_platform.system()

        return telemetry_data

    def send(self, telemetry: dict) -> bool:
        payload = json.dumps(telemetry).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AndroidTelemetryAgent/1.0",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                success = 200 <= response.status < 300
            if success:
                self._log_ui("Telemetria enviada com sucesso!")
            else:
                self._log_ui(f"Erro no Servidor: HTTP {response.status}")
            return success
        except Exception as exc:
            self._log_ui(f"Falha de rede: {exc}")
            return False

    def run(self):
        self._log_ui("Agente iniciado em 2º plano.")
        while not self.stop_event.is_set():
            telemetry = self.collect()
            self.send(telemetry)
            self.stop_event.wait(self.interval)
        self._log_ui("Agente encerrado.")

    def stop(self):
        self._log_ui("Parando agente...")
        self.stop_event.set()


class TelemetryApp(App):
    def build(self):
        # Configuração da Interface (UI)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.status_label = Label(text="Agente Parado", halign="center", font_size='18sp')
        self.layout.add_widget(self.status_label)

        self.btn_start = Button(text="Iniciar Telemetria", size_hint=(1, 0.2), background_color=(0, 1, 0, 1))
        self.btn_start.bind(on_press=self.start_agent)
        self.layout.add_widget(self.btn_start)

        self.btn_stop = Button(text="Parar Telemetria", size_hint=(1, 0.2), background_color=(1, 0, 0, 1))
        self.btn_stop.bind(on_press=self.stop_agent)
        self.layout.add_widget(self.btn_stop)

        self.agent = None
        self.agent_thread = None

        return self.layout

    def update_status(self, message):
        self.status_label.text = message

    def start_agent(self, instance):
        if self.agent_thread and self.agent_thread.is_alive():
            return  # Já está rodando

        # Endpoint de teste. Troque para o seu servidor real.
        endpoint = "https://httpbin.org/post"

        self.agent = TelemetryAgent(endpoint, interval=10, log_callback=self.update_status)
        self.agent_thread = threading.Thread(target=self.agent.run, daemon=True)
        self.agent_thread.start()

    def stop_agent(self, instance):
        if self.agent:
            self.agent.stop()

    def on_stop(self):
        # Garante que a thread seja fechada quando o app for fechado
        if self.agent:
            self.agent.stop()


if __name__ == '__main__':
    TelemetryApp().run()