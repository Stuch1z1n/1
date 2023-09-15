from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime, timedelta
from kivy.clock import Clock
from plyer import notification

class RegistroDePontoApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10

        self.nome_label = Label(text="Nome:")
        self.nome_entry = TextInput()
        self.registrar_entrada_button = Button(text="Registrar Entrada", on_release=self.registrar_entrada)
        self.registrar_ida_almoço_button = Button(text="Registrar Ida Almoço", on_release=self.registrar_ida_almoço)
        self.registrar_volta_almoço_button = Button(text="Registrar Volta Almoço", on_release=self.registrar_volta_almoço)
        self.registrar_saida_button = Button(text="Registrar Saída", on_release=self.registrar_saida)
        self.registros_text = TextInput(readonly=True, height=400, multiline=True)

        self.add_widget(self.nome_label)
        self.add_widget(self.nome_entry)
        self.add_widget(self.registrar_entrada_button)
        self.add_widget(self.registrar_ida_almoço_button)
        self.add_widget(self.registrar_volta_almoço_button)
        self.add_widget(self.registrar_saida_button)
        self.add_widget(self.registros_text)

        self.hora_entrada = datetime.now().replace(hour=7, minute=0, second=0, microsecond=0)
        self.hora_saida = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
        self.hora_inicio_almoço = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        self.hora_fim_almoço = datetime.now().replace(hour=13, minute=0, second=0, microsecond=0)
        self.horas_trabalhadas = timedelta()

        self.hora_extra_interval = 1  # Intervalo de verificação de hora extra em minutos
        self.hora_extra_threshold = 8 * 60  # Threshold para considerar hora extra em minutos
        self.hora_extra_notified = False  # Para evitar notificar várias vezes

        Clock.schedule_interval(self.verificar_hora_extra, self.hora_extra_interval * 60)

    def registrar_ponto(self, evento):
        nome = self.nome_entry.text
        hora_registro = datetime.now()
        registro = f"{nome} registrou o ponto de {evento} em {hora_registro.strftime('%Y-%m-%d %H:%M:%S')}\n"
        self.registros_text.text += registro

        self.nome_entry.text = ""

    def registrar_entrada(self, instance):
        self.registrar_ponto("Entrada")

    def registrar_ida_almoço(self, instance):
        self.registrar_ponto("Ida Almoço")

    def registrar_volta_almoço(self, instance):
        self.registrar_ponto("Volta Almoço")

    def registrar_saida(self, instance):
        self.registrar_ponto("Saída")

    def verificar_hora_extra(self, dt):
        hora_registro = datetime.now()
        if self.hora_entrada <= hora_registro <= self.hora_saida:
            horas_trabalhadas = hora_registro - self.hora_entrada
            if self.hora_inicio_almoço <= hora_registro <= self.hora_fim_almoço:
                horas_almoco = hora_registro - self.hora_inicio_almoço
                horas_trabalhadas -= horas_almoco

            minutos_trabalhados = horas_trabalhadas.total_seconds() / 60
            if minutos_trabalhados > self.hora_extra_threshold and not self.hora_extra_notified:
                notification_title = "Hora Extra"
                notification_text = "Você está em hora extra!"
                notification.notify(title=notification_title, message=notification_text)
                self.hora_extra_notified = True
            elif minutos_trabalhados <= self.hora_extra_threshold:
                self.hora_extra_notified = False

class PontoApp(App):
    def build(self):
        return RegistroDePontoApp()

if __name__ == "__main__":
    PontoApp().run()
