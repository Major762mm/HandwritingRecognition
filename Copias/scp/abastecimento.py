import pyautogui
import keyboard
from botcity.core import DesktopBot
import time

class Bot(DesktopBot):
    def __init__(self):
        super().__init__()
        # Dicionário associando motoristas às placas
        self.motoristas_placas = {
            1: ("Fernando", "RLN2B33"),
            2: ("Jonael", "RYQ0D17"),
            3: ("Paulo", "RLO4A72"),
            4: ("Rosinaldo", "RLO4B02"),
            5: ("Marcos", "RYP9I37"),
            6: ("Algaraz", "RYR1F75"),
            7: ("Wellington", "RAC6149"),
            8: ("Elkesan", "RLN1J73"),
            9: ("Marcio", "RAG9808"),
            10: ("Jean", "RDU6A81"),
            11: ("Douglas", "RLG2G29"),
            12: ("Fabiano", "RLN2C73"),
            13: ("SIDNEY", "RYR0D88"),
            14: ("GILSONEI", "RDV3D52"),
            15: ("GABER", "RYQ0A97"),
            16: ("JOAO B", "RLG2G29"),
            17: ("CARLINHO", "QJC7023"),
            18: ("DAVID", "RYQ0A97"),
            19: ("FABIANO", "RLN2C73"),
            20: ("GEDIEL", "RYW7I96"),
            21: ("MATHEUS", "RDU6B21"),
            22: ("RICARDO", "RYP9J47"),
            23: ("JONAS B", "RLB1A78"),
            24: ("RAFAEL", "RCB1A78"),
            25: ("RODRIGO", "RLM1I22"),
            26: ("JOSIMAR", "BDR7D72"),
            27: ("JEFERSON", "QJC7023"),
            28: ("LUCENIR", "RLB1A78"),
            #29: ("DAVID", "RYQ0A97"),
            #30: ("DAVID", "RYQ0A97"),
            #31: ("DAVID", "RYQ0A97"),
            #32: ("DAVID", "RYQ0A97"),
            #33: ("DAVID", "RYQ0A97"),
            #34: ("DAVID", "RYQ0A97"),
            #35: ("DAVID", "RYQ0A97"),
            #36: ("DAVID", "RYQ0A97"),
            #37: ("DAVID", "RYQ0A97"),
            #38: ("DAVID", "RYQ0A97"),
            #39: ("DAVID", "RYQ0A97"),
            #40: ("DAVID", "RYQ0A97"),
            #41: ("DAVID", "RYQ0A97"),
            # Adicione outros motoristas e placas aqui
        }

    def action(self, execution=None):
        while True:
            self.click_at(607, 1062)
            self.wait(1) # Checklist antes de iniciar a iteração
            self.click_at(607, 1062)
            motorista_selecionado = self.selecionar_motorista_por_numero()
            if not motorista_selecionado:
                print("Nenhum motorista válido selecionado. Encerrando o loop.")
                break

            motorista, placa = motorista_selecionado
            print(f"Motorista selecionado: {motorista}, Placa: {placa}")

            print("Iniciando nova iteração do loop.")
            self.wait(2000)

            # Primeiro clique e tab
            self.click_at(595, 255)
            print("Clique realizado na posição (595, 255).")
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada.")

            # Espera pela tecla Enter na primeira etapa
            self.aguardar_tecla_enter("Etapa 1")

            # Pressiona tab e aguarda novamente a tecla Enter
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada novamente.")
            self.wait(0.5)

            # Pressiona a seta para baixo 6 vezes
            for i in range(6):
                pyautogui.press('down')
                self.wait(1)
                print(f"Tecla 'Down' pressionada {i+1} vez(es).")

            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'Down'.")
            self.wait(2)

            # Digitar Placa com base no número selecionado
            self.click_at(729, 391)
            self.wait(3)
            pyautogui.write(placa)
            print(f"Placa {placa} digitada para o motorista {motorista}.")
            self.aguardar_tecla_enter("Etapa 2")
            keyboard.press_and_release('tab')

            # Litros
            self.aguardar_digitar("Litros")
            self.aguardar_tecla_enter("Etapa 3")
            print("Esperando após digitar os litros.")
            self.wait(2)

            # Odômetro         
            keyboard.press_and_release('tab')  
            self.aguardar_digitar("Odômetro")
            self.aguardar_tecla_enter("Etapa 4")
            keyboard.press_and_release('tab')
            keyboard.press_and_release('tab')
            self.wait(3)

            # Operador
            keyboard.press_and_release('down')
            self.wait(4)

            # Salva
            self.click_at(324, 615)
            self.moveTo(319, 646)
            self.wait(2)
            time.sleep(4)
            # Novo cadastro
            #self.aguardar_tecla_enter("Etapa 5")
            self.click_at(258, 688)
            self.wait(2)

    def selecionar_motorista_por_numero(self):
        while True:
            print("Selecione o número do motorista na lista abaixo:")
            for numero, (motorista, placa) in self.motoristas_placas.items():
                print(f"{numero}: {motorista} (Placa: {placa})")
            try:
                numero = int(input("Digite o número correspondente: ").strip())
                if numero in self.motoristas_placas:
                    return self.motoristas_placas[numero]
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def aguardar_tecla_enter(self, etapa):
        print(f"Aguardando a tecla Insert ({etapa})...")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'enter':
                print(f"Tecla Insert pressionada ({etapa}).")
                break
            self.wait(0.1)

    def aguardar_digitar(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        while True:
            if keyboard.read_event().name.isnumeric():
                print(f"Texto inserido no campo {campo}.")
                break
            self.wait(0.1)

if __name__ == "__main__":
    Bot.main()
