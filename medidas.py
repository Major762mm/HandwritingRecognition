import os
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification
import time
import threading


class Bot(DesktopBot):
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
        
        self.perguntas_categoria_veiculo = {
            1: "Caminhao",
            2: "Carreta",
            3: "Fiorino",
            4: "Moto",
            5: "Sprinter"
        }

        self.perguntas_modelo = {
            1: "FORD CARGO 11-19",
            2: "FORD / CARGO 15-19",
            3: "FORD / CARGO 17-23",
            4: "FORD/CARGO 816",
            5: "M.BENZ/ ACCELO 1016 CE",
            6: "M.BENZ/ACCELO 1017 CE",
            7: "M.BENZ/ACCELO 815",
            8: "VOLKS 8-150",
            9: "VOLKS 8-160",
            10: "VOLVO/VM 260 6X2R",
            11: "VOLVO/VM 270 6X2R",
            12: "VW/11.180 DRC 4X2",
            13: "VW/24.280 CRM 6x2",
            14: "VW/DELIVERY 11.180"
        }
        

        self.medidas = {
            ("Caminhao", "M.BENZ/ACCELO 1017 CE", "2024"): (220, 220, 620, 1000, 6, 4000, 24, 5000, 30),
            #
            ("Caminhao", "M.BENZ/ACCELO 1016 CE", "2022"): (220, 220, 620, 1000, 6, 4000, 24, 5000, 30),
            ("Caminhao", "M.BENZ/ACCELO 1016 CE", "2023"): (220, 220, 620, 1000, 6, 4000, 24, 5000, 30),
            ("Caminhao", "M.BENZ/ACCELO 1016 CE", "2024"): (220, 220, 620, 1000, 6, 4000, 24, 5000, 30),
            #
            ("Caminhao", "VW/11.180 DRC 4X2", "2024"): (220, 220, 620, 1000, 6, 4000, 24, 5000, 30),
            
            #
            
            # Adicione outras combinações de categoria, modelo e ano conforme necessário
        }

        self.frotas = None
        
    def obter_medidas(self, categoria, modelo, ano):
    # Retorna as medidas para a combinação específica de categoria, modelo e ano
        return self.medidas.get((categoria, modelo, ano), None)
            
    
    def perguntas_input(self):
        self.click_at(1387, 174)
        self.click_at(605, 1062)
        print("Informe uma frota: ")
        self.frotas = int(input("Digite um numero: "))
        self.click_at(592, 139)
        self.paste(self.frotas)
        time.sleep(0.25)
        self.click_at(665, 164)
        self.click_at(665, 164)
        time.sleep(1)
        self.click_at(605, 1062)
        
        # Categoria
        print("Selecione a categoria do veículo:")
        for key, value in self.perguntas_categoria_veiculo.items():
            print(f"{key}: {value}")
        categoria_selecionada = int(input("Digite o número da categoria: "))

        print("\nSelecione o modelo do veículo:")
        for key, value in self.perguntas_modelo.items():
            print(f"{key}: {value}")
        modelo_selecionado = int(input("Digite o número do modelo: "))

        ano = input("\nDigite o ano do veículo (2022, 2023, 2024): ")

        categoria = self.perguntas_categoria_veiculo.get(categoria_selecionada)
        modelo = self.perguntas_modelo.get(modelo_selecionado)

        medidas = self.medidas.get((categoria, modelo, ano))
        if medidas:
            print(f"\nAs medidas para {categoria}: {modelo} de {ano} são {medidas[0]}, {medidas[1]}, {medidas[2]}.")
            self.colar_medidas(medidas)
        else:
            print("\nCombinação de categoria, modelo e ano não encontrada.")

    def colar_medidas(self, medidas):
    # Locais para cada medida (altura, largura, profundidade, Peso CS, Vol. Cs, Peso CF, Vol. CF, Peso Total, Volume Total)
        
        self.click_at(939, 174)
        
        locais = {
            "modelo": (779, 287),
            "altura": (978, 562),  
            "largura": (1082, 561),  
            "profundidade": (1191, 559),
            "Peso CS": (877, 504),
            "Vol. Cs": (972, 503),
            "Peso CF": (541, 556),
            "Vol. CF": (646, 559),
            "Peso Total": (758, 558),
            "Volume Total": (865, 558)
        }

    # Colando cada medida em seu respectivo campo
        for i, (campo, coordenadas) in enumerate(locais.items()):
            if i < len(medidas):  # Verifica se existe uma medida disponível para o campo atual
                self.double_click_at(*coordenadas)
                self.paste(str(medidas[i]))  # Colar a medida
                print(f"Medida {medidas[i]} colada em {campo} nas coordenadas {coordenadas}")
            else:
                print(f"Medida para {campo} não foi fornecida.")
        self.finalizar()
            
            
    def double_click_at(self, x, y):
        """Realiza um clique duplo em uma posição específica."""
        self.click_at(x, y)
        self.wait(0.05)  # Pequeno intervalo entre os cliques
        self.click_at(x, y)        

    def finalizar(self):
        print("Finalizando...")
        self.click_at(1292, 854)
        self.click_at(1387, 174)
        print("Finalizado!")
        
    def iniciar_monitoramento_teclas(self):
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()

    def monitorar_teclas(self):
        """Função para monitorar as teclas 'Q' e 'ESC' em paralelo."""
        while True:
            if keyboard.is_pressed('q'):
                start_time = time.time()
                while keyboard.is_pressed('q'):
                    if time.time() - start_time >= 3:
                        print("Tecla 'Q' pressionada por 3 segundos. Reiniciando o script...")
                        self.notificar("Reiniciando", "Tecla 'Q' pressionada por 3 segundos")
                        return

            if keyboard.is_pressed('esc'):
                start_time = time.time()
                while keyboard.is_pressed('esc'):
                    if time.time() - start_time >= 2:
                        self.click_at(1447, 204)
                        print("Tecla 'ESC' pressionada por 5 segundos. Encerrando o script...")
                        self.notificar("Encerrando", "Tecla 'ESC' pressionada por 2 segundos")
                        os._exit(0)

            time.sleep(0.1)

    def aguardar_tecla_insert(self, etapa):
        print(f"Aguardando a tecla Insert ({etapa})...")
        self.notificar("Aguardando", f"A tecla Insert ({etapa})")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'insert':
                print(f"Tecla Insert pressionada ({etapa}).")
                self.notificar("Tecla Insert pressionada", etapa)
                break
            self.wait(0.1)

    def aguardar_digitar(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            if keyboard.read_event().name.isnumeric():
                print(f"Texto inserido no campo {campo}.")
                self.notificar("Texto inserido", campo)
                break
            self.wait(0.1)

    def aguardar_digitar_texto(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and (event.name.isalnum() or event.name in ['space', 'enter', 'backspace', 'tab', 'shift']):
                print(f"Texto inserido no campo {campo}.")
                self.notificar("Texto inserido", campo)
                break
            self.wait(0.1)

    def notificar(self, titulo, mensagem):
            notification.notify(
                title=titulo,
                message=mensagem,
                timeout=2
            )


if __name__ == "__main__":
    bot = Bot()
    bot.perguntas_input()
