import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading

class Bot(DesktopBot):
    reiniciar_solicitado = False  # Variável para evitar múltiplos reinícios
    
    def action(self, execution=None):
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
            
        while True:
            # Reiniciar o script se solicitado
            if self.reiniciar_solicitado:
                self.reiniciar_solicitado = False
                print("Reiniciando o script...")
                self.reiniciar_estado()
                continue  # Reinicia o loop principal
            
            print("Iniciando nova iteração do loop.")
            self.wait(2000)  # Espera de 2 segundos
            
            # Primeiro clique e espera de 3 segundos
            self.click_at(1003, 114)
            print("Clique realizado na posição (1003, 114).")
            #self.notificar("Clique realizado", "Posição (1003, 114)")
            self.wait(3000)
            
            # Clique no campo e aguarda o texto ser inserido
            self.click_at(615,269)
            self.click_at(615,269)
            self.aguardar_digitar("Valor total")  # Aguarda inserção de número
            self.aguardar_tecla_insert("Etapa 1")  # Aguarda tecla Insert
            print("Esperando após digitar o Valor.")
            #self.notificar("Esperando", "Após digitar o valor")
            
            # Aguardar digitação de texto e Insert para a "Categoria"
            keyboard.press_and_release('tab')
            self.aguardar_digitar_texto("Categoria")
            self.aguardar_tecla_insert("Etapa 2")
            print("Esperando após digitar a categoria.")
            #self.notificar("Esperando", "Após digitar o categoria")
            
            # Ações com Tab e setas
            self.click_at(524, 337)
            self.wait(0.2)
            for i in range(3):
                pyautogui.press('down')
            self.aguardar_tecla_insert("Etapa 3")
            print("Tecla 'Enter1' pressionada.")
            
            self.click_at(825, 306)
            #self.click_at(825, 306)
            
            # Pular campos com Tab
            for _ in range(4):
                keyboard.press_and_release('tab')
            
            # NFe e próxima etapa
            self.aguardar_digitar("Numero NFe")
            self.aguardar_tecla_insert("Etapa 4")
            print("Esperando após digitar a NFe.")
            #self.notificar("Esperando", "Após digitar o NFe")
            
            # Continuar navegação com Tab
            for _ in range(3):
                keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'NFe'.")
            
            # Aguardar texto do Fornecedor
            self.aguardar_digitar_texto("Fornecedor")
            self.click_at(1544, 538)
            self.aguardar_tecla_insert("Etapa 5")
            print("Esperando após digitar o Fornecedor.")
            #self.notificar("Esperando", "Após digitar o Fornecedor")
            
            self.click_at(1544, 538)
            self.click_at(1544, 538)
            
            #ação da visao computacional pra dar dois cliques no botao.png
            
            # Tab para pular campos e depois inserir número de parcelas
            for _ in range(3):
                keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'Fornecedor'.")
            
            self.aguardar_digitar("N° Parcelas")
            self.aguardar_tecla_insert("Etapa 6")
            print("Esperando após digitar a N° Parcelas.")
            #self.notificar("Esperando", "Após digitar o N° Parcelas")
            
            # Preencher campos e aguardar outros inputs
            keyboard.press_and_release('tab')
            self.paste("BOLETO")
            keyboard.press_and_release('tab')
            
            self.aguardar_digitar("Banco")
            self.aguardar_tecla_insert("Etapa 7")
            print("Esperando após digitar o Banco.")
            #elf.notificar("Esperando", "Após digitar o Banco")
            
            # Tab e preenchimento do campo Mensal
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' após o banco.")
            #self.notificar("Tecla 'Tab' pressionada", "Após o banco")
            self.wait(1)
            
            self.paste("Mensal")
            keyboard.press_and_release('tab')
            
            # Vencimento e aguardar tecla Insert
            self.aguardar_digitar("Vencimento")
            self.aguardar_tecla_insert("Etapa 8")
            print("Esperando após digitar o Vencimento.")
            #self.notificar("Esperando", "Após digitar o Vencimento")
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
            #self.notificar("Esperando", "Após digitar o N° Fatura")
            keyboard.press_and_release('tab')
            
            self.click_at(1320, 738)
            self.click_at(1320, 738)
            self.aguardar_digitar("Data")
            self.aguardar_tecla_insert("Etapa 8")
            print("Esperando após digitar a Data.")
            #self.notificar("Esperando", "Após digitar a Data")
            
            # Fechar o processo
            self.click_at(1370, 625)
            self.wait(1)
            self.click_at(1399, 654)
            self.click_at(1447, 204)

            
    def monitorar_teclas(self):
        """Função para monitorar as teclas 'Q' e 'ESC' em paralelo."""
        while True:
            if keyboard.is_pressed('q'):
                start_time = time.time()
                while keyboard.is_pressed('q'):
                    if time.time() - start_time >= 3:  # Se "Q" for pressionada por 3 segundos
                        if not self.reiniciar_solicitado:  # Verifica se já está reiniciando
                            self.reiniciar_solicitado = True
                            print("Tecla 'Q' pressionada por 3 segundos. Reiniciando o script...")
                            #self.notificar("Reiniciando", "Tecla 'Q' pressionada por 3 segundos")
                        return  # Retorna para o loop principal, onde o reinício será tratado

            # Verifica se a tecla "ESC" está pressionada por 5 segundos para encerrar o script
            if keyboard.is_pressed('esc'):
                start_time = time.time()
                while keyboard.is_pressed('esc'):
                    if time.time() - start_time >= 3:  # Se "ESC" for pressionada por 5 segundos
                        print("Tecla 'ESC' pressionada por 5 segundos. Encerrando o script...")
                        #self.notificar("Encerrando", "Tecla 'ESC' pressionada por 5 segundos")
                        os._exit(0)  # Encerra o programa forçadamente

            time.sleep(0.1)  # Pequena pausa para não sobrecarregar o loop de verificação
    
    # Função para aguardar a tecla Insert
    def aguardar_tecla_insert(self, etapa):
        print(f"Aguardando a tecla Insert ({etapa})...")
        #self.notificar("Aguardando", f"A tecla Insert ({etapa})")
    
        while True:
            # Captura os eventos do teclado e verifica se a tecla pressionada foi o Insert
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'insert':  # Verifica se o nome da tecla é exatamente 'insert'
                    print(f"Tecla Insert pressionada ({etapa}).")
                    #self.notificar("Tecla Insert pressionada", etapa)
                    break
            self.wait(0.1)


    # Função para aguardar a inserção de número
    def aguardar_digitar(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        #self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            if keyboard.read_event().name.isnumeric():
                print(f"Texto inserido no campo {campo}.")
                #self.notificar("Texto inserido", campo)
                break
            self.wait(0.1)
    
    # Função para aguardar a inserção de texto alfanumérico
    def aguardar_digitar_texto(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        #self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name.isalnum() or event.name in ['space', 'enter', 'backspace', 'tab', 'shift']:
                    print(f"Texto inserido no campo {campo}.")
                    #self.notificar("Texto inserido", campo)
                    break
            self.wait(0.1)

    def reiniciar_estado(self):
        print("Resetando estado do bot.")
        self.wait(1) 

    # Função para enviar notificações
    #def notificar(self, titulo, mensagem):
    #    notification.notify(
    #        title=titulo,
    #        message=mensagem,
    #        timeout=2  # Tempo que a notificação ficará visível (em segundos)
    #    )

if __name__ == "__main__":
    Bot.main()