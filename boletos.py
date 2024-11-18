import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui
import keyboard
from plyer import notification  # Para enviar notificações
from visao import detectar_e_clicar_imagem  # Importar a função do visao.py

class Bot(DesktopBot):
    def action(self, execution=None):
        while True:
            print("Iniciando nova iteração do loop.")
            self.wait(2000)  # Espera de 2 segundos
            
            # Primeiro clique e espera de 3 segundos
            self.click_at(1003, 114)
            print("Clique realizado na posição (1003, 114).")
            self.notificar("Clique realizado", "Posição (1003, 114)")
            self.wait(3000)
            
            # Clique no campo e aguarda o texto ser inserido
            self.click_at(615,269)
            self.click_at(615,269)
            self.aguardar_digitar("Valor total")  # Aguarda inserção de número
            self.aguardar_tecla_insert("Etapa 1")  # Aguarda tecla Insert
            print("Esperando após digitar o Valor.")
            self.notificar("Esperando", "Após digitar o valor")
            
            # Aguardar digitação de texto e Insert para a "Categoria"
            keyboard.press_and_release('tab')
            self.aguardar_digitar_texto("Categoria")
            self.aguardar_tecla_insert("Etapa 2")
            print("Esperando após digitar a categoria.")
            self.notificar("Esperando", "Após digitar o categoria")
            
            # Ações com Tab e setas
            self.click_at(524, 337)
            self.wait(0.2)
            for i in range(3):
                pyautogui.press('down')
            self.aguardar_tecla_insert("Etapa 3")
            print("Tecla 'Enter1' pressionada.")
            
            self.click_at(825, 306)
            
            # Pular campos com Tab
            for _ in range(4):
                keyboard.press_and_release('tab')
            
            # NFe e próxima etapa
            self.aguardar_digitar("Numero NFe")
            self.aguardar_tecla_insert("Etapa 4")
            print("Esperando após digitar a NFe.")
            self.notificar("Esperando", "Após digitar o NFe")
            
            # Continuar navegação com Tab
            for _ in range(3):
                keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'NFe'.")
            
            # Aguardar texto do Fornecedor
            self.aguardar_digitar_texto("Fornecedor")
            self.click_at(1544, 538)
            self.aguardar_tecla_insert("Etapa 5")
            print("Esperando após digitar o Fornecedor.")
            self.notificar("Esperando", "Após digitar o Fornecedor")
            
            self.click_at(1544, 538)
            self.click_at(1544, 538)
            
            # *** Usar visão computacional aqui ***
            # Acionando a função de visão computacional para clicar no botão da imagem 'botao.png'
            print("Tentando localizar e clicar no botão através da visão computacional...")
            posicao = detectar_e_clicar_imagem('botao.png')
            
            if posicao:
                print(f"Imagem encontrada e clicada na posição: {posicao}")
            else:
                print("Imagem não encontrada.")

            # Tab para pular campos e depois inserir número de parcelas
            for _ in range(3):
                keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'Fornecedor'.")
            
            self.aguardar_digitar("N° Parcelas")
            self.aguardar_tecla_insert("Etapa 6")
            print("Esperando após digitar a N° Parcelas.")
            self.notificar("Esperando", "Após digitar o N° Parcelas")
            
            self.aguardar_digitar("N° Parcelas")
            self.aguardar_tecla_insert("Etapa 6")
            print("Esperando após digitar a N° Parcelas.")
            self.notificar("Esperando", "Após digitar o N° Parcelas")
            
            # Preencher campos e aguardar outros inputs
            keyboard.press_and_release('tab')
            self.paste("BOLETO")
            keyboard.press_and_release('tab')
            
            self.aguardar_digitar("Banco")
            self.aguardar_tecla_insert("Etapa 7")
            print("Esperando após digitar o Banco.")
            self.notificar("Esperando", "Após digitar o Banco")
            
            # Tab e preenchimento do campo Mensal
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' após o banco.")
            self.notificar("Tecla 'Tab' pressionada", "Após o banco")
            self.wait(1)
            
            self.paste("Mensal")
            keyboard.press_and_release('tab')
            
            # Vencimento e aguardar tecla Insert
            self.aguardar_digitar("Vencimento")
            self.aguardar_tecla_insert("Etapa 8")
            print("Esperando após digitar o Vencimento.")
            self.notificar("Esperando", "Após digitar o Vencimento")
            keyboard.press_and_release('tab')
            keyboard.press_and_release('tab')
            keyboard.press_and_release('enter')
            
            # Pular 5 campos com Tab
            for _ in range(5):
                pyautogui.press('tab')
            
            # Aguarda o número da fatura e digita a data
            self.aguardar_digitar("N° Fatura")
            self.aguardar_tecla_insert("Etapa 8")
            print("Esperando após digitar a N° Fatura.")
            self.notificar("Esperando", "Após digitar o N° Fatura")
            keyboard.press_and_release('tab')
            
            self.click_at(1320, 738)
            self.click_at(1320, 738)
            self.aguardar_digitar("Data")
            self.aguardar_tecla_insert("Etapa 8")
            print("Esperando após digitar a Data.")
            self.notificar("Esperando", "Após digitar a Data")
            
            # Fechar o processo
            self.click_at(1370, 625)
            self.wait(1)
            self.click_at(1399, 654)
            self.click_at(1447, 204)
            
    # Função para aguardar a tecla Insert
    def aguardar_tecla_insert(self, etapa):
        print(f"Aguardando a tecla Insert ({etapa})...")
        self.notificar("Aguardando", f"A tecla Insert ({etapa})")
    
        while True:
            # Captura os eventos do teclado e verifica se a tecla pressionada foi o Insert
            event = keyboard.read_event()
        
            if event.event_type == keyboard.KEY_DOWN:
            # Verifica se a tecla é o Insert (pode variar conforme o teclado)
                if event.name == 'insert':  # Verifica se o nome da tecla é exatamente 'insert'
                    print(f"Tecla Insert pressionada ({etapa}).")
                    self.notificar("Tecla Insert pressionada", etapa)
                    break

        # Adiciona uma pausa para evitar sobrecarga no loop
        self.wait(0.1)


    # Função para aguardar a inserção de número
    def aguardar_digitar(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            if keyboard.read_event().name.isnumeric():
                print(f"Texto inserido no campo {campo}.")
                self.notificar("Texto inserido", campo)
                break
            self.wait(0.1)
    
    # Função para aguardar a inserção de texto alfanumérico
    def aguardar_digitar_texto(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name.isalnum() or event.name in ['space', 'enter', 'backspace', 'tab', 'shift']:
                    print(f"Texto inserido no campo {campo}.")
                    self.notificar("Texto inserido", campo)
                    break
            self.wait(0.1)

    # Função para enviar notificações
    def notificar(self, titulo, mensagem):
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=2  # Tempo que a notificação ficará visível (em segundos)
        )

if __name__ == "__main__":
    Bot.main()
