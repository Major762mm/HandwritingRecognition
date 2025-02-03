"""
WARNING:

Please make sure you install the bot with `pip install -e .` in order to get all the dependencies
on your Python environment.

Also, if you are using PyCharm or another IDE, make sure that you use the SAME Python interpreter
as your IDE.

If you get an error like:
```
ModuleNotFoundError: No module named 'botcity'
```

This means that you are likely using a different Python interpreter than the one used to install the bot.
To fix this, you can either:
- Use the same interpreter as your IDE and install your bot with `pip install -e .`
- Use the same interpreter as the one used to install the bot (`pip install -e .`)

Please refer to the documentation for more information at https://documentation.botcity.dev/
"""
import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui
import keyboard
from plyer import notification  # Para enviar notificações

class Bot(DesktopBot):
    def action(self, execution=None):
        
        while True:  # Loop principal para reiniciar o processo
            # Início: Obter placa
            self.wait(5000)
            self.click_at(85 ,263)
            self.notificar("Clique realizado", "Posição (85, 263)")
            for i in range(1):
                pyautogui.press('down')
                self.wait(1)
            for i in range(2):
                pyautogui.press('right')
                self.wait(1)
            keyboard.press_and_release('control+c')
            self.wait(3)
            self.notificar("Copiado", "seguindo para o próximo passo")
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            pyautogui.keyUp('alt')
            self.notificar("Trocando de página...", "seguindo")
            self.wait(2)
            
            # Pesquisar | Pós alt+tab
            self.click_at(906, 102)
            self.click_at(375, 102)
            self.wait(1)
            keyboard.press_and_release('control+v')
            self.wait(3)
            
            if not self.find("alvo", matching=0.97, waiting_time=15000):
                self.not_found("alvo")
                self.notificar("Objeto não encontrado", "Voltando e reiniciando...")
                self.reiniciar_processo()
            else:
                self.notificar("Objeto encontrado", "Prosseguindo...")
                self.aguardar_tecla_enter("Aguardando liberação...")
                self.notificar("Liberado", "fechando...")
                
                # Verifica se a tecla Insert foi pressionada
                self.aguardar_tecla_insert("Aguardando confirmação de email já registrado")
                self.reiniciar_processo()
                self.notificar("Email já registrado", "Fechando...")

                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')
                self.wait(3)
                self.click_at(1458, 160)
                self.wait(1)                
                self.click_at(286, 161)
                self.wait(2)
                self.click_at(907, 102)
                self.wait(0.5)
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')
                self.wait(2)
                keyboard.press_and_release('alt+down')
                keyboard.press_and_release('home')
                # Apos o home, o loop tem que voltar para o começo por que mudou de página, ai tem que fazer a mesma coisa
                
                
                self.wait(3)
                self.click_at(1458, 160)
                self.wait(1)                
                self.click_at(286, 161)
                self.wait(2)
                self.click_at(907, 102)
                self.wait(0.5)
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')

                self.wait(2)
                keyboard.press_and_release('alt+down')
                keyboard.press_and_release('home')
            
                
    def reiniciar_processo(self):
        # Lógica para voltar à página inicial e reiniciar o processo
        print("Reiniciando o processo...", " ")
        self.notificar("Reiniciado", "Voltando à página inicial")
        #Fechar e apagar pesquisas
        self.click_at(907, 102)
        self.wait(0.5)
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        pyautogui.keyUp('alt')  # Voltar para a página inicial
        self.wait(2)
        keyboard.press_and_release('alt+down')
        
        # Continue adicionando o que for necessário para reiniciar completamente
        self.notificar("Processo reiniciado", "Recomeçando a busca")

    def not_found(self, target):
        print(f"Alvo '{target}' não encontrado.")
        self.notificar("Alvo não encontrado", f"Alvo '{target}' não encontrado.")

    def aguardar_tecla_enter(self, etapa):
        print(f"Aguardando a tecla Enter ({etapa})...")
        self.notificar("Aguardando", f"A tecla Enter ({etapa})")
        while True:
            if keyboard.is_pressed('enter'):
                print(f"Tecla Enter pressionada ({etapa}).")
                self.notificar("Tecla Enter pressionada", etapa)
                break
            self.wait(0.1)  # Pequeno delay para não sobrecarregar o loop

    def aguardar_tecla_insert(self, etapa):
        print(f"Aguardando a tecla Insert ({etapa})...")
        self.notificar("Aguardando", f"A tecla Insert ({etapa})")
        while True:
            if keyboard.is_pressed('insert'):
                print(f"Tecla Insert pressionada ({etapa}).")
                self.notificar("Tecla Insert pressionada", etapa)
                break
            self.wait(0.1)  # Pequeno delay para não sobrecarregar o loop

    def notificar(self, titulo, mensagem):
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=2  # Tempo que a notificação ficará visível (em segundos)
        )

if __name__ == "__main__":
    Bot.main()



















