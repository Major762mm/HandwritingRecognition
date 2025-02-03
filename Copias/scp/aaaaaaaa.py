import pandas as pd
from botcity.core import DesktopBot

# BotCity Class
class Bot(DesktopBot):
    def action(self, execution=None):
        # Carregar a planilha com os dados
        planilha_path = "FROTAS_PATRIMONIO.xlsx"
        dados = pd.read_excel(planilha_path, header=0)  # Indica que a primeira linha é o cabeçalho
        
        # Iterar sobre as linhas
        for _, row in dados.iterrows():
            print(row['Nº FROTA'], row['MARCA'], row['MODELO'], row['ANO_FAB'],
       row['ANO_MOD' ], row['PLACA'], row['DATA AQUISIÇÂO'], row['CAPACIDADE PESO'], row['Baú_Modelo' ],
       row['ALTURA'], row['LARGURA'], row['PROFUNDIDADE'], row['Nº MODULOS'], row['CHASSI'], 
       row['RENAVAN'], row['FRIO MARCA'], row['FRIO MODELO'], row['BAIXADO?'])     

       # Teste: exiba alguns valores
        # Exibir colunas para debug
        #print("Colunas da planilha:", dados.columns)
        
        
        
        # Substitua pela lista de frotas que você deseja processar
        frotas = [
            1, 2, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 
            25, 26, 28, 32, 35, 36, 37, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 
            57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 
            75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 
            92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 109, 110, 112, 
            113, 115, 116, 117, 118, 119, 120, 121, 122, 127, 128, 129, 130, 
            131, 132, 133, 134, 138, 139, 140, 141, 142, 143, 144, 145, 146, 
            147, 148, 149, 150, 153, 154, 155, 156, 157, 158, 159, 163, 164, 
            165, 166, 167, 168, 169, 170, 172, 173, 174, 175, 176, 177, 178, 
            179, 180, 181, 182, 183, 184, 185, 186, 187, 189, 195, 196, 197, 
            200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 
            215, 216, 217, 218, 219, 244, 245, 246, 247, 248, 249, 250, 251, 
            252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 
            265, 266, 267, 269, 270
        ]
        
        for frota in frotas:
            print(f"Processando frota: {frota}")
            
            # Verificar se a coluna existe
            try:
                # Acessar a coluna 'Frota' pelo índice numérico ou nome
                if 'Frota' in dados.columns:
                    coluna_frota = 'Nº FROTA'
                else:
                    coluna_frota = dados.columns[0]  # Pega a primeira coluna (caso o nome não seja 'Frota')
                    
                # Filtrar a frota
                linha = dados[dados[coluna_frota] == int(frota)]
            except Exception as e:
                print(f"Erro ao acessar a coluna 'Frota': {e}")
                continue  # Pule para a próxima frota
            
            if linha.empty:
                print(f"Frota {frota} não encontrada!")
                continue
            
            # Obter os dados associados
            marca = linha.iloc[0][dados.columns[1]]  # Pega a segunda coluna (Modelo do caminhão)
            print(f"Frota: {frota}, Marca: {marca}")
            
            # Dicionário de mapeamento
            tipo_veiculo = {
                "M.BENZ/ ACCELO 1016 CE": "toco",
                "M.BENZ/ACCELO 815": "toco",
                "VOLKS 8-160": "toco",
                "VOLKS 8-150": "toco",
                "FORD/CARGO 816": "toco",
                "VW/11.180 DRC 4X2": "toco",
                "M.BENZ/ACCELO 1017 CE": "toco",
                "VW/24.280 CRM 6x2": "toco",
                "VW/DELIVERY 11.180": "toco",

                "SR/ RECRUSUL": "Outros",
                "SR/ THERMOSUL": "Outros",
                "SR/RANDON SR FG": "Outros",
                "SR/NIJU": "Outros",
                "SR/IBIPORA SR3E FRIG": "Outros",
                "SR/RANDON SR FG FR 03E": "Outros",
                "SR/IBIPORA SR2ED CF": "Outros",
                "HONDA / CG 160 CARGO": "Outros",
                "HONDA / CG 125 CARGO": "Outros",
                
                "FIAT/FIORINO": "Utilitarios",

                "M.BENZ 417 SPRINTER F": "Van",
                "SPRINTER": "Van",
            }
            
            # Determinar o tipo de veículo
            tipo = tipo_veiculo.get(marca, "Desconhecido")
            print(f"Tipo de veículo: {tipo}")
            
            # Automação com base nos dados
            self.type_keys(str(frota))  # Digitar o número da frota
            self.enter()  # Confirmar
            
            # Lógica de automação por tipo de veículo
            if tipo == "toco":
                self.click_at(594, 137)
                self.wait(0.25)
                self.paste(frota)
                self.double_click_at(647, 162)
                self.wait(0.25)
                self.click_at(1284, 233)
                self.wait(0.25)
                #
                self.click_at(1219, 276) #aqui onde define o rodado, apenas aqui deve ser alterado
                #
                self.click_at(1297, 859)
                self.wait(0.25)
                self.click_at(1387, 172) #Finalizado
                pass
            elif tipo == "Outros":
                self.click_at(594, 137)
                self.wait(0.25)
                self.paste(frota)
                self.double_click_at(647, 162)
                self.wait(0.25)
                self.click_at(1284, 233)
                #
                self.click_at(1230, 343) #aqui onde define o rodado, apenas aqui deve ser alterado
                #
                self.wait(0.25)
                self.click_at(1297, 859)
                self.wait(0.25)
                self.click_at(1387, 172) #Finalizado
                pass
            elif tipo == "Utilitarios":
                self.click_at(594, 137)
                self.wait(0.25)
                self.paste(frota)
                self.double_click_at(647, 162)
                self.wait(0.25)
                self.click_at(1284, 233)
                #
                self.click_at(1231, 330) #aqui onde define o rodado, apenas aqui deve ser alterado
                #
                self.wait(0.25)
                self.click_at(1297, 859)
                self.wait(0.25)
                self.click_at(1387, 172) #Finalizado
                pass
            elif tipo == "Van":
                self.click_at(594, 137)
                self.wait(0.25)
                self.paste(frota)
                self.double_click_at(647, 162)
                self.wait(0.25)
                self.click_at(1284, 233)
                #
                self.click_at(1239, 306) #aqui onde define o rodado, apenas aqui deve ser alterado
                #
                self.wait(0.25)
                self.click_at(1297, 859)
                self.wait(0.25)
                self.click_at(1387, 172) #Finalizado
                pass
            else:
                print(f"Tipo de veículo para frota {frota} não reconhecido. Nenhuma ação executada.")
        
        print("Automação concluída para todas as frotas!")

    def not_found(self):
        print("Elemento não encontrado na tela.")

    def double_click_at(self, x, y):
        """Realiza um clique duplo em uma posição específica."""
        self.click_at(x, y)
        self.wait(0.05)  # Pequeno intervalo entre os cliques
        self.click_at(x, y)


# Execução
if __name__ == "__main__":
    Bot.main()
