from botcity.core import DesktopBot
import pandas as pd
import time

class Bot(DesktopBot):
    def action(self, execution=None):
        # Carregar a planilha
        self.planilha = pd.read_excel("FROTAS_PATRIMONIO (10).xlsx")
        print("Colunas disponíveis na planilha:", self.planilha.columns)

        # Definir a lista de números de frota a serem processados
        lista_frotas = [
            
            195, 196,
            197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208,
            209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220,
            221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232,
            233, 234, 235, 236, 237, 238, 239, 242, 243, 244, 245, 246,
            247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258,
            259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270,
            271, 272, 273, 274, 275, 276, 277, 278, 279, 280
        ]

        # Coordenadas para tipos de rodado
        rodado_coords = {
            "TOCO": (1219, 276),
            "OUTROS": (1230, 343),
            "UTILITARIO": (1231, 330),
            "VAN": (1239, 306),
            "CAVALO MECANICO": (1244, 288),
            "TRUCK": (1228, 254),
        }

        # Processar cada frota na lista
        for frota_num in lista_frotas:
            print(f"Iniciando processamento da frota Nº {frota_num}...")

            # Filtrar a linha correspondente à frota atual
            linha = self.planilha[self.planilha['Nº FROTA'] == frota_num]
            if linha.empty:
                print(f"Frota Nº {frota_num} não encontrada na planilha. Pulando...")
                continue

            # Obter a primeira ocorrência
            linha = linha.iloc[0]

            # Processar frota
            try:
                self.processar_frota(linha, rodado_coords)
                print(f"Frota Nº {frota_num} processada com sucesso.\n")
            except Exception as e:
                print(f"Erro ao processar a frota Nº {frota_num}: {e}\n")
                continue

    def processar_frota(self, linha, rodado_coords):
        """
        Processa o cadastro de uma única frota com base nos dados fornecidos.
        """
        # Clique inicial na interface
        self.double_click_at(591, 136)
        self.control_a()
        time.sleep(0.5)

        # Cole o número da frota
        self.paste(str(linha['Nº FROTA']))
        time.sleep(0.5)

        # Clique no campo de frota
        self.double_click_at(653, 163)
        time.sleep(5)

        # Preenche os campos
        campos = {
            'MARCA': (683, 288),
            'MODELO': (869, 288),
            'ANO_FAB': (661, 339),
            'ANO_MOD': (548, 344),
            'PLACA': (547, 394),
            'CAPACIDADE PESO': (873, 557),
            'CAPACIDADE PESO': (771, 558),
            'PESO SECO': (880, 504),
            'CAIXA FRIA': (560, 558),
            'ALTURA': (987, 558),
            'LARGURA': (1085, 558),
            'PROFUNDIDADE': (1203, 557),
            'M. CUBICA': (878, 557),
            'VOL. CF': (647, 558),
            'VOL. CS': (984, 504),
            'Nº MODULOS': (1302, 559),
            'CHASSI': (924, 612),
            'RENAVAN': (1173, 608),
            'SET_METRIC': (1153, 666)
        }

        for campo, (x, y) in campos.items():
            valor = linha[campo]
            self.paste_field(valor, x, y)
            time.sleep(0.25)

        # Definir rodado com base no valor da coluna "Rodado"
        self.click_at(1286, 234)
        coluna_rodado = [col for col in self.planilha.columns if 'rodado' in col.lower()]
        if coluna_rodado:
            rodado = linha[coluna_rodado[0]]
        else:
            raise ValueError("Coluna 'RODADO' não encontrada na planilha.")

        if pd.notna(rodado) and rodado.upper() in rodado_coords:
            coords = rodado_coords[rodado.upper()]
            self.click_at(*coords)
            time.sleep(0.25)
        else:
            print(f"Rodado '{rodado}' não reconhecido ou não preenchido para a frota.")
            
        

        # Clique no botão de salvar ou ir para o próximo registro
        self.click_at(1290, 858)
        time.sleep(2)
        
         # Clique inicial na interface
        #self.double_click_at(591, 136)
        #self.control_a()
        #time.sleep(0.5)

        ## Cole o número da frota
        #self.paste(str(linha['Nº FROTA']))
        #time.sleep(0.5)
        #
        #self.double_click_at(1153, 666)
        #
        #self.paste(str(linha['SET_EQP']))
        ##salva
        #self.click_at(1290, 858)
        #time.sleep(2)

    def paste_field(self, text, x, y):
        """
        Função para colar diretamente um valor em um campo específico.
        """
        if pd.notna(text):  # Verifica se há valor e não é NaN
            self.double_click_at(x, y)  # Clica no campo
            self.control_a()  # Seleciona todo o conteúdo do campo
            self.paste(str(text))  # Cola o novo valor

    def double_click_at(self, x, y):
        """
        Realiza um clique duplo em uma posição específica.
        """
        self.click_at(x, y)
        self.wait(0.05)
        self.click_at(x, y)


if __name__ == "__main__":
    bot = Bot()
    bot.action()
