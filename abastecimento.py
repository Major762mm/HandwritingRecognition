import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui
import keyboard
from plyer import notification  # Para enviar notificações

class Bot(DesktopBot):
    def action(self, execution=None):
        while True:
            print("Iniciando nova iteração do loop.")
            self.wait(2000)
            
            # Primeiro clique e tab
            self.click_at(595, 255)
            print("Clique realizado na posição (595, 255).")
            #self.notificar("Clique realizado", "Posição (595, 255)")
            keyboard.press_and_release('tab')
            for i in range(0):
                pyautogui.press('up')
                self.wait(1)
            print("Tecla 'Tab' pressionada.")
            
            # Espera pela tecla Enter na primeira etapa
            self.aguardar_tecla_enter("Etapa 1")
            
            # Pressiona tab e aguarda novamente a tecla Enter
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada novamente.")
            #self.notificar("Tecla 'Tab' pressionada", "Etapa 1")
            self.wait(0.5)
            
            # Pressiona a seta para baixo 6 vezes
            for i in range(6):
                pyautogui.press('down')
                self.wait(1)
                print(f"Tecla 'Down' pressionada {i+1} vez(es).")
                #self.notificar("Tecla 'Down' pressionada", f"Vez {i+1}")
            
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada após 'Down'.")
            #self.notificar("Tecla 'Tab' pressionada", "Após 'Down'")
            self.wait(2)
            
            # Espera pela tecla Enter na segunda etapa
            keyboard.press_and_release('tab')
            print("Tecla 'Tab' pressionada antes da segunda etapa.")
            #self.notificar("Tecla 'Tab' pressionada", "Antes da segunda etapa")
            self.wait(1)
            
            self.click_at(729, 391)
            self.wait(3)
            self.aguardar_tecla_enter("Etapa 2")
            keyboard.press_and_release('tab')
            
            # Litros
            # Aguarda a tecla Enter após a digitação
            self.aguardar_digitar("Litros")
            self.aguardar_tecla_enter("Etapa 3")
            print("Esperando após digitar os litros.")
            #self.notificar("Esperando", "Após digitar os litros")
            
            self.wait(2)

            # Odômetro         
            keyboard.press_and_release('tab')  
            self.aguardar_digitar("Odômetro")
            self.aguardar_tecla_enter("Etapa 4")
            self.notificar("Tecla 'Enter' pressionada", "Etapa 4")
            keyboard.press_and_release('tab')
            keyboard.press_and_release('tab')
            self.wait(3)
            
            #Operador
            keyboard.press_and_release('down')
            self.wait(4)
            
            #Salva
            self.click_at(324, 615)
            self.moveTo(319, 646)
            self.wait(2)
            
            #Novo cadastro
            self.aguardar_tecla_enter("Etapa 5")
            #self.notificar("Tecla 'Enter' pressionada", "Etapa 5")
            self.click_at(258, 688)
            self.wait(2)
        
        
    def aguardar_tecla_enter(self, etapa):
        print(f"Aguardando a tecla Enter ({etapa})...")
        #self.notificar("Aguardando", f"A tecla Enter ({etapa})")
        while True:
            if keyboard.is_pressed('enter'):
                print(f"Tecla Enter pressionada ({etapa}).")
                self.notificar("Tecla Enter pressionada", etapa)
                break
            self.wait(0.1)  # Pequeno delay para não sobrecarregar o loop

    def aguardar_digitar(self, campo):
        print(f"Aguardando inserção de texto no campo {campo}...")
        #self.notificar("Aguardando", f"Inserção de texto no campo {campo}")
        while True:
            if keyboard.read_event().name.isnumeric():
                print(f"Texto inserido no campo {campo}.")
                #self.notificar("Texto inserido", campo)
                break
            self.wait(0.1)

    #def notificar(self, titulo, mensagem):
    #    notification.notify(
    #        title=titulo,
    #        message=mensagem,
    #        timeout=2  # Tempo que a notificação ficará visível (em segundos)
    #    )

if __name__ == "__main__":
    Bot.main()