from botcity.core import DesktopBot
import pandas as pd
import time

# Subclasse do BotCity
class Bot(DesktopBot):
    def action(self, execution=None):
        # Carregue a planilha
        planilha = pd.read_excel("FROTAS_PATRIMONIO (1).xlsx")
        
        
        
        # Itere sobre as linhas da planilha
        for _, linha in planilha.iterrows():
            
            # Primeiro clique
            self.click_at(594, 136)  # Clique inicial na interface
            self.paste((linha['Nº FROTA']))
            self.double_click_at(653, 163)
            time.sleep(5)  # Aguarda um pouco para carregar a interface
            # Clique e selecione a frota no campo inicia
            time.sleep(2)  # Aguarda para o sistema carregar os dados da frota
            
            # Preencha os campos conforme as coordenadas do sistema
            self.paste_field(linha['MARCA'], x=683, y=288)
            time.sleep(1)
            
            self.paste_field(linha['MODELO'], x=869, y=288)
            time.sleep(1)
            
            self.paste_field(linha['ANO_FAB'], x=661, y=339)
            time.sleep(1)
            
            self.paste_field(linha['ANO_MOD'], x=548, y=344)
            time.sleep(1)
            
            self.paste_field(linha['CAPACIDADE PESO'], x=766, y=560)
            time.sleep(1)
            
            self.paste_field(linha['ALTURA'], x=987, y=558)
            time.sleep(1)
            
            self.paste_field(linha['LARGURA'], x=1085, y=558)
            time.sleep(1)
            
            self.paste_field(linha['PROFUNDIDADE'], x=1203, y=557)
            time.sleep(1)
            
            self.paste_field(linha['Nº MODULOS'], x=1302, y=559)
            time.sleep(1)
            
            self.paste_field(linha['CHASSI'], x=924, y=612)
            time.sleep(1)
            
            self.paste_field(linha['RENAVAN'], x=1173, y=608)
            time.sleep(1)
            
            

            # Clique no botão de salvar ou ir para o próximo registro
            self.click_at(x=1290, y=858)  # Coordenadas do botão salvar
            time.sleep(2)  # Aguarda para salvar/ir para o próximo registro

    def paste_field(self, text, x, y):
        """
        Função para colar diretamente um valor em um campo específico.
        - text: Texto a ser colado
        - x, y: Coordenadas do campo
        """
        if text is not None:  # Verifica se há valor
            self.double_click_at(x, y)  # Clica no campo
            self.control_a()  # Seleciona todo o conteúdo do campo
            self.paste(str(text))  # Cola o novo valor

    def enter_key(self):
        """Simula o pressionamento da tecla Enter."""
        self.type_keys("{ENTER}")

    def double_click_at(self, x, y):
        """Realiza um clique duplo em uma posição específica."""
        self.click_at(x, y)
        self.wait(0.05)  # Pequeno intervalo entre os cliques
        self.click_at(x, y)
        
if __name__ == "__main__":
    bot = Bot()
    bot.action()
