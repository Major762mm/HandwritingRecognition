import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading
from bancos_e_funções import bancos, fornecedores, Database
import sqlite3


class Bot(DesktopBot):
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
        
        self.db = Database("lancamentos.db")
        
        # Inicializando 'self.categorias' dentro do método action
        self.categorias = { 
            1: ("Manutenção de Veiculos", None),
            2: ("Manutenção e conservação predial", "4.2.3.19"),
            3: ("Manutenção de maquinas", "4.2.3.28"),
            4: ("Peças corretivas", "4.2.3.17.2.1"),
            5: ("Peças preventivas", "4.2.3.17.1.1"),
            6: ("Combustivel e lubrificantes", "4.2.3.21"),
            7: ("Aluguéis", "4.2.3.10"),
            8: ("Energia", "4.2.3.11"),
            9: ("Agua e esgoto", "4.2.3.12"),
            10: ("Material limpeza", None),
            11: ("Serviços de terceiros", "4.2.3.20"),
            12: ("Taxas", "4.2.3.23"),
            13: ("Despesas com refeitorio - Matriz", "4.2.3.37"),
            14: ("Material escritorio", "4.2.3.15"),
            15: ("Despesas com Alimentação - Curitiba", "4.2.9.15"),
            16: ("Telefones", "4.2.3.13")
            
            }


        self.alterar_valor = {
            1: ("Não"),
            2: ("Sim")
        }
        
        self.calculadora_ask = {
            1: ("Não"),
            2: ("Sim")
        }
         
        self.categoria = None
        self.parcelas = 1
        self.banco = None
        self.nome_banco = None
        self.alterar = None
        self.escolha = None
        self.calculadora_ask = None
        
        self.iniciar()
        
    def iniciar(self):
        while True:
            print("\nMenu Principal:")
            print("1: Adicionar Categoria")
            print("2: Adicionar Fornecedor")
            print("3: Selecionar Categoria e Continuar Processo")
            print("4: Esquema com boletos")
            print("0: Sair")
    
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                self.adicionar_categoria()
            elif escolha == "2":
                self.adicionar_fornecedor()
            elif escolha == "3":
                print("\nIniciando novo processo de automação.")
                
                # Resetando atributos para o novo processo
                self.categoria = None
                self.parcelas = 1
                self.banco = None
                self.nome_banco = None
                self.alterar = None
                self.escolha = None
                self.calculadora_ask = None
                
                # Selecionar categoria
                self.selecionar_categoria()
                
                # Selecionar banco
                self.selecionar_banco()
                
                # Perguntar sobre alteração de valores
                self.selecionar_alteracao_valor(self.parcelas)
                
                # Executar automação com base nas escolhas
                self.executar_automacao()
                
                # Finalizar o processo
                self.finalizar_processo()
            elif escolha == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida. Tente novamente.")

    def adicionar_fornecedor(self):
        print("\n--- Adicionar Fornecedor ---")

        categorias = self.db.listar_categorias()
        if not categorias:
            print("Nenhuma categoria disponível. Adicione uma categoria primeiro.")
            return

        print("Categorias disponíveis:")
        for cat_id, nome, _ in categorias:
            print(f"{cat_id}: {nome}")

        while True:
            try:
                escolha = int(input("Escolha a categoria pelo número correspondente: "))
                for cat_id, nome, _ in categorias:
                    if escolha == cat_id:
                        nome_fornecedor = input("Digite o nome do fornecedor: ").strip()
                        if nome_fornecedor:
                            self.db.adicionar_fornecedor(cat_id, nome_fornecedor)
                            print(f"Fornecedor '{nome_fornecedor}' adicionado à categoria '{nome}' com sucesso!")
                        else:
                            print("Nome do fornecedor não pode ser vazio.")
                        return
                print("Categoria inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def adicionar_categoria(self):
        nome = input("Digite o nome da categoria: ")
        codigo = input("Digite o código da categoria (ou pressione Enter para ignorar): ")
        self.db.adicionar_categoria(nome, codigo if codigo else None)
        print(f"Categoria '{nome}' adicionada com sucesso!")

    def selecionar_categoria(self):
        print("\n--- Seleção de Categoria ---")

        categorias = self.db.listar_categorias()
        if not categorias:
            print("Nenhuma categoria disponível. Adicione uma categoria primeiro.")
            return False

        print("Categorias disponíveis:")
        for cat_id, nome, codigo in categorias:
            print(f"{cat_id}: {nome} (Código: {codigo or 'N/A'})")

        while True:
            try:
                escolha = int(input("Digite o número da categoria desejada: "))
                for cat_id, nome, _ in categorias:
                    if escolha == cat_id:
                        self.categoria = nome
                        self.categoria_id = cat_id
                        print(f"Categoria selecionada: {nome}")
                        return True
                print("Categoria inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Digite um número.")

    def selecionar_banco(self):
        while True:
            try:
                codigo_banco = int(input("Digite o código de identificação do banco: "))
                if codigo_banco in bancos:
                    self.nome_banco, _ = bancos[codigo_banco]
                    self.codigo_banco = codigo_banco
                    print(f"Iniciando script para {self.categoria} com {self.parcelas} parcela(s) no Banco {self.nome_banco}")
                    break
                else:
                    print("Código de banco inválido! Tente novamente.")
            except ValueError:
                print("Entrada inválida. Tente novamente.")
                              
    def selecionar_alteracao_valor(self, parcelas):
        print("Deseja alterar o valor?")
        # Se o número de parcelas for maior que 1, oferece a opção de alterar
        if parcelas > 1:
            for numero, descricao in self.alterar_valor.items():
                print(f"{numero}: {descricao}")
            while True:
                try:
                    escolha = input("Informe: ").strip()
                    print(f"Você escolheu: '{escolha}' com código ASCII {ord(escolha)}")
                    # Verificando se a escolha está no dicionário
                    if int(escolha) in self.alterar_valor:
                        self.escolha_alterar_valor = escolha
                        return escolha
                    else:
                        print("Opção inválida.")
                except ValueError:
                    print("Insira um número.")
        else:
            # Caso a quantidade de parcelas seja 1, não oferece a opção de alterar valor
            print("Não é necessário alterar o valor, pois é apenas 1 parcela.")
            self.escolha_alterar_valor = '1'  # Armazenando um valor padrão para não alterar
            return '1'  # Retornando valor padrão
        # Iniciar a automação
        
    def executar_automacao(self):
        print("Iniciando nova iteração do loop.")
        self.wait(2000)  # Espera de 2 segundos
        # Primeiro clique e espera de 3 segundos
        self.click_at(1003, 114)
        print("Clique realizado na posição (1003, 114).")
        self.notificar("Clique realizado", "Posição (1003, 114)")
        self.wait(3000)
        self.double_click_at(615,269)
        
        if self.parcelas > 1:
            self.calculadora()
        else:
            self.comportamento_para_nao()
            # Clique no campo e aguarda o texto ser inserido        
        self.aguardar_tecla_insert("Etapa 1")  # Aguarda tecla Insert
        print("Esperando após digitar o Valor.")
        #self.notificar("Esperando", "Após digitar o valor")
        # Aguardar digitação de texto e Insert para a "Categoria"
        keyboard.press_and_release('tab')
        # Preenche somente o código se existir, senão preenche o nome
        if self.codigo_categoria:
            keyboard.write(self.codigo_categoria)  # Preenche só o código
        else:
            keyboard.write(self.categoria)  # Preenche o nome
        time.sleep(0.25)
        #self.aguardar_tecla_insert("Etapa 2")
        #print("Esperando após digitar a categoria.")
        #self.notificar("Esperando", "Após digitar o categoria")
        # Ações com Tab e setas
        self.click_at(524, 337)
        self.wait(0.2)
        if self.escolha in [4, 5]:
            for i in range(5):
                py.press('down')
            print("Numero detectado, opção 1")
        else:
            for n in range(3):
                py.press('down')
            print("Numero nao detectado, opção 2")
        time.sleep(0.25)
        self.click_at(825, 306)
        #self.click_at(825, 306)
        time.sleep(0.25)    
        # Pular campos com Tab
        for _ in range(4):
            keyboard.press_and_release('tab')
        time.sleep(0.25)    
        # NFe e próxima etapa
        self.aguardar_digitar("Numero NFe")
        self.aguardar_tecla_insert("Etapa 4")
        print("Esperando após digitar a NFe.")
        self.notificar("Esperando", "Após digitar o NFe")
        # Continuar navegação com Tab
        self.pular_campos(3)
        print("Tecla 'Tab' pressionada após 'NFe'.")
        # Aguardar texto do Fornecedor
        self.paste(str(self.fornecedor))
        self.double_click_at(1544, 538)
        #self.aguardar_tecla_insert("Etapa 5")
        print("Esperando após digitar o Fornecedor.")
        self.notificar("Esperando", "Após digitar o Fornecedor")
        self.wait(0.50)
        # Tab para pular campos e depois inserir número de parcelas
        for _ in range(3):
            keyboard.press_and_release('tab')
        print("Tecla 'Tab' pressionada após 'Fornecedor'.")
        #self.aguardar_digitar("N° Parcelas")
        self.wait(1)
        keyboard.write(str(self.parcelas))
        self.wait(0.25)
        # Preencher campos e aguardar outros inputs
        keyboard.press_and_release('tab')
        self.wait(0.25)
        keyboard.write(str("BOLETO"))
        self.wait(0.25)
        keyboard.press_and_release('tab')
        time.sleep(0.50)
        keyboard.write(str(self.codigo_banco))
        time.sleep(0.50)
        keyboard.press_and_release('tab')
        self.notificar("Tecla 'Tab' pressionada", "Após o banco")
        self.wait(0.25)
        keyboard.write(str("Mensal"))
        keyboard.press_and_release('tab')
        # Vencimento e aguardar tecla Insert
        self.aguardar_digitar("Vencimento")
        self.aguardar_tecla_insert("Etapa 8")
        print("Esperando após digitar o Vencimento.")
        self.notificar("Esperando", "Após digitar o Vencimento")
        self.pular_campos(2)
        keyboard.press_and_release('enter')
        self.selecionar_comportamento_parcelas()
        # Comportamento baseado na quantidade de parcelas
     
    def selecionar_comportamento_parcelas(self):
        print("Selecionando comportamento para o número de parcelas...")

        if self.parcelas == 1:
            self.comportamento_uma_parcela()
            print("Executando comportamento para uma parcela.")
        elif self.parcelas == 2:
            self.comportamento_2_parcelas()
            print("Executando comportamento para duas parcelas.")
        elif self.parcelas == 3:
            self.comportamento_3_parcelas()
        else:
            print(f"Número de parcelas ({self.parcelas}) não suportado. Adicione um novo comportamento se necessário.")
          
    def comportamento_uma_parcela(self):
        time.sleep(2)
        #Ir para N° Documento
        for n in range (5):
            keyboard.press_and_release('tab')
        print("Executando comportamento para 1 parcela.")
        self.wait(1)
        self.aguardar_digitar("N° Fatura")
        self.aguardar_tecla_insert("Etapa 8-1")
        print("Esperando após digitar a N° Fatura.")
        self.notificar("Esperando", "Após digitar o N° Fatura")
        keyboard.press_and_release('tab')
            
        self.double_click_at(1320, 738)
        self.aguardar_digitar("Data")
        self.aguardar_tecla_insert("Etapa 8-1")
        print("Esperando após digitar a Data.")
        self.notificar("Esperando", "Após digitar a Data")
    
        # **Novo código: Fechar e salvar após digitar a Data**
        self.finalizar_processo()
     
    def comportamento_2_parcelas(self):
        print(f"Executando comportamento para {self.parcelas} parcelas.")
        # Adicione aqui o que o script deve fazer com múltiplas parcelas
        time.sleep(2)
        if self.escolha_alterar_valor == '2':
            self.comportamento_para_sim()
            print("Valor de alterar_valor é 2, chamando comportamento_para_sim")
        elif self.escolha_alterar_valor == '1':
            self.comportamento_para_nao()
            print("Valor de alterar_valor não é 2, chamando comportamento_para_nao")
        else:
            print("Entrada inválida! Digite 1 para 'não' ou 2 para 'sim'.")
            
        self.pular_campos(5)
        
        self.aguardar_digitar("N° Fatura")
        self.aguardar_tecla_insert("Etapa 8-2")
        print("Esperando após digitar a N° Fatura.")
        self.notificar("Esperando", "Após digitar o N° Fatura")
        
        self.double_click_at(1452, 716) #Clique fora da tela
        self.double_click_at(1151, 735) 
        
        self.control_c()
        
        self.double_click_at(1140, 762)
        
        self.control_v()
        
        py.press('right')
        
        self.double_click_at(1142, 761)
        
        py.press('right')
        
        self.aguardar_digitar("Fatura 2")
        self.aguardar_tecla_insert("Etapa 8-2")
        

        keyboard.press_and_release('tab')
            
        self.double_click_at(1320, 738)
        self.aguardar_digitar("Data Fat-1")
        self.aguardar_tecla_insert("Etapa 10")
        
        self.double_click_at(1313, 760)
        self.aguardar_digitar("Data Fat-2")
        self.aguardar_tecla_insert("Etapa 11")
        # **Novo código: Fechar e salvar após digitar a Data**
        self.finalizar_processo()

    def comportamento_3_parcelas(self):  
        print(f"Executando comportamento para {self.parcelas} parcelas.")
        # Adicione aqui o que o script deve fazer com múltiplas parcelas
        time.sleep(2)
        if self.escolha_alterar_valor == '2':
            self.comportamento_para_sim()
            print("Valor de alterar_valor é 2, chamando comportamento_para_sim")
        elif self.escolha_alterar_valor == '1':
            self.comportamento_para_nao()
            print("Valor de alterar_valor não é 2, chamando comportamento_para_nao")
        else:
            print("Entrada inválida! Digite 1 para 'não' ou 2 para 'sim'.")
            
        self.click_at(951, 737)
        self.setas_mov('right', 2, 'up', 3)
        
        self.aguardar_digitar("N° Fatura")
        self.aguardar_tecla_insert("Etapa 8-2")
        print("Esperando após digitar a N° Fatura.")
        self.notificar("Esperando", "Após digitar o N° Fatura")
        
        self.double_click_at(1452, 716)
        self.double_click_at(1151, 735) # Fatura 1
 
        self.control_c()
        
        self.double_click_at(1140, 762) #Fatura 2
        
        self.control_v()
        
        py.press('right')
        
        self.double_click_at(1142, 761)
        
        py.press('right')
        
        self.aguardar_digitar("Fatura 2")
        self.aguardar_tecla_insert("Etapa 8-2")
        
        self.double_click_at(1142, 761)
 
        self.control_c()
        
        self.double_click_at(1156, 784)
        
        self.control_v()
        
        py.press('right')
        
        self.double_click_at(1156, 784)
        
        py.press('right')

        self.aguardar_digitar("Fatura 3")
        self.aguardar_tecla_insert("Etapa 8-3")
        
        keyboard.press_and_release('tab')
            
        self.double_click_at(1320, 738)
        self.aguardar_digitar("Data Fat-1")
        self.aguardar_tecla_insert("Etapa 10")
        
        
        self.double_click_at(1313, 760)
        self.aguardar_digitar("Data Fat-2")
        self.aguardar_tecla_insert("Etapa 11")
        
        self.double_click_at(1312, 783)
        self.aguardar_digitar("Data Fat-3")
        self.aguardar_tecla_insert("Etapa 12")
        
        self.finalizar_processo()
    
    def finalizar_processo(self):
            """Função para salvar e fechar o processo após preencher os campos."""
            print("Finalizando o processo...")
        
            # Clique no botão 'Salvar'
            self.click_at(1370, 625)  # Ajuste as coordenadas se necessário
            self.wait(1)
        
            # Clique no botão 'Fechar'
            self.click_at(1399, 654)  # Ajuste as coordenadas se necessário
            self.click_at(1447, 204)  # Ajuste as coordenadas se necessário
        
            print("Processo salvo e finalizado.")

    def find_multiple_images(self, images, matching=0.97, waiting_time=10000):
        for image in images:
            if self.find(image, matching=matching, waiting_time=waiting_time):
                print(f"Imagem '{image}' encontrada.")
                return True  # Retorna True ao encontrar a primeira imagem correspondente
        print("Nenhuma das imagens foi encontrada.")
        return False  # Retorna False se nenhuma imagem for encontrada

    def calculadora(self):
        os.system("calc")
        self.aguardar_tecla_insert("Etapa 1.1")
        self.control_a()
        self.control_c()
        self.click_at(1196, 389)
        self.double_click_at(615,269)
        self.control_v()
    
    def pular_campos(self, num):
        for _ in range(num):
            keyboard.press_and_release('tab')
  
    def setas_mov(self, *args):
        # Verifica se os argumentos são pares (direção, quantidade)
        if len(args) % 2 != 0:
            print("Erro: Argumentos devem ser pares de direção e quantidade.")
            return

        # Itera sobre os argumentos em pares
        for i in range(0, len(args), 2):
            direcao = args[i]
            quantidade = args[i + 1]

            # Move na direção e quantidade especificadas
            for _ in range(quantidade):
                keyboard.press_and_release(direcao)

    def double_click_at(self, x, y):
        """Realiza um clique duplo em uma posição específica."""
        self.click_at(x, y)
        self.wait(0.05)  # Pequeno intervalo entre os cliques
        self.click_at(x, y)
       
    def input_numerico(self, mensagem):
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        
    def comportamento_para_sim(self):
        print("Executando comportamento_para_sim")
        #Ir para N° Documento
        for n in range (3):
            keyboard.press_and_release('tab')
        self.wait(1)
        
        self.double_click_at(951, 737)
        time.sleep(0.25)
        #py.press('right')
        self.aguardar_digitar("Alteração de Valor 1")
        self.aguardar_tecla_insert("alteração de valor 1")
        print("Alteração de Valor 1 confirmada")
        
        self.double_click_at(944, 765)
        time.sleep(0.25)
        py.press('right')
        self.aguardar_digitar("Alteração de Valor 2")
        self.aguardar_tecla_insert("alteração de valor 2")
        print("Alteração de Valor 2 confirmada")
        
        # Lista das possíveis imagens a serem encontradas
        imagens_numero_3 = ["numero_3_1", "numero_3_2", "numero_3_3", "numero_3_4"]

        # Tenta encontrar uma das imagens
        if self.find_multiple_images(imagens_numero_3, matching=0.97, waiting_time=10000):
            # Se alguma imagem for encontrada, executa as ações desejadas
            self.double_click_at(954, 787)
            time.sleep(0.25)
            py.press('right')
            self.aguardar_digitar("Alteração de Valor 3")
            self.aguardar_tecla_insert("alteração de valor 3")
            print("Alteração de Valor 3 confirmada")
        else:
            # Se nenhuma imagem for encontrada, apenas imprime uma mensagem
            print("Imagem não encontrada")

            
        if not self.find( "numero_4", matching=0.97, waiting_time=5000):
            self.not_found("numero_4")
        
        if not self.find( "numero_5", matching=0.97, waiting_time=5000):
            self.not_found("numero_5")
        
        if not self.find( "numero_6", matching=0.97, waiting_time=5000):
            self.not_found("numero_6") 
        
    def comportamento_para_nao(self):
    # Não faz nenhuma alteração, apenas continua o fluxo
        print("Nenhuma alteração de valor necessária.")
        # Apenas um log informativo, sem nenhuma ação extra

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
                        if not self.reiniciar_solicitado:
                            self.reiniciar_solicitado = True
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

    def not_found(self, numero):
        print(f"Elemento '{numero}' não encontrado. Verifique a imagem ou a configuração.")
        
if __name__ == "__main__":
    try:
        bot = Bot()
        bot.iniciar()  # Garanta que o método correto seja chamado
        bot.db = db
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    bot.selecionar_categoria()
    bot.selecionar_banco()
    bot.alterar = bot.selecionar_alteracao_valor(bot.parcelas)
    bot.executar_automacao()


    