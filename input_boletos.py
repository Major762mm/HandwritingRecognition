import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading
from bancos_e_funções import FornecedorDB, bancos
import sqlite3
import logging
import json
from datetime import datetime
import pynput
#from Copias/copia_banco import bancos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("Categoria adicionada com sucesso")


class Bot(DesktopBot):
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
            self.dados_lancamento = []
            #self.coletando_log = False
            #self.log_atual = {"valor": "", "NFe": "", "vencimento": ""}  # Inicializa campos vazios
            #self.campo_atual = "valor"  # Define qual campo está sendo preenchido
        self.db = FornecedorDB("fornecedores.db")
        #self.db.criar_banco()

    
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
            self.click_at(607, 1062)
            self.wait(1)
            self.click_at(607, 1062)
            print("\nMenu Principal:")
            print("1: Adicionar Categoria")
            print("2: Adicionar Fornecedor")
            print("3: Fazer lançamento")
            print("4: Esquema com boletos")
            print("5: Excluir categoria")
            print("6: Listar categorias")
            print("7: Listar fornecedores")
            print("8: Editar categoria")
            print("9: Editar fornecedor")
            print("0: Sair")
    
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                self.adicionar_categoria()
            elif escolha == "2":
                self.adicionar_fornecedor()
            elif escolha == "3":
                self.lancamentos()
            elif escolha == "4":
                print("Sem função...")
            elif escolha == "5":
                self.excluir_categoria()
            elif escolha == "6":
                self.db.listar_categorias()
            elif escolha == "7":
                self.db.listar_fornecedores()
            elif escolha == "8":
                self.db.editar_categoria()
            elif escolha == "9":
                self.db.editar_fornecedor()
            elif escolha == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida. Tente novamente.")
        
    def adicionar_categoria(self):
        while True:
            nome = input("\nDigite o nome da categoria (ou 0 para sair): ").strip()
            if nome == "0":
                print("Saindo para o menu principal...")
                self.iniciar()
                return

            if not nome:
                print("O nome da categoria não pode estar vazio.")
                continue

            if self.db.verificar_categoria_existente(nome):
                print(f"A categoria '{nome}' já está cadastrada.")
                continue

            codigo = input("Digite o código da categoria (ou pressione Enter para ignorar): ").strip()
            codigo = codigo if codigo else None

            self.db.cadastrar_categoria(nome, codigo)
            print(f"Categoria '{nome}' adicionada com sucesso!")
            break

    def adicionar_fornecedor(self):
        while True:
            categorias = self.db.listar_categorias()

            if not categorias:
                print("\nNenhuma categoria cadastrada. Adicione uma categoria primeiro.")
                return

            print("\nCategorias disponíveis:")
            for categoria in categorias:
                print(f"{categoria[0]}: {categoria[1]}")
            print("0: Sair para o menu principal")

            try:
                categoria_id = int(input("\nDigite o ID da categoria para adicionar um fornecedor: "))
                if categoria_id == 0:
                    print("Saindo para o menu principal...")
                    self.iniciar()
                    return

                categoria_selecionada = next((cat for cat in categorias if cat[0] == categoria_id), None)
                if not categoria_selecionada:
                    print("ID da categoria inválido. Tente novamente.")
                    continue

                print(f"\nCategoria selecionada: {categoria_selecionada[1]}")

                fornecedores = self.db.obter_fornecedores_por_categoria(categoria_id)
                if fornecedores:
                    print(f"\nFornecedores já cadastrados na categoria '{categoria_selecionada[1]}':")
                    for fornecedor in fornecedores:
                        print(f"{fornecedor['id']}: {fornecedor['nome']}")
                else:
                    print(f"\nNenhum fornecedor encontrado na categoria '{categoria_selecionada[1]}'. Você pode adicionar um novo fornecedor.")

                nome = input("\nDigite o nome do fornecedor a ser adicionado: ").strip()
                if not nome:
                    print("Nome do fornecedor não pode estar vazio.")
                    continue

                conn = self.db.conectar()
                cursor = conn.cursor()

                try:
                    cursor.execute(
                        'INSERT INTO fornecedores (nome, categoria_id) VALUES (?, ?)',
                        (nome, categoria_id)
                    )
                    conn.commit()
                    print(f"Fornecedor '{nome}' adicionado com sucesso!")
                    break
                except sqlite3.Error as e:
                    print(f"Erro ao adicionar fornecedor: {e}")
                finally:
                    conn.close()

            except ValueError:
                print("Entrada inválida. Por favor, insira um número válido.")

    def selecionar_categoria(self):
        print("\n--- Seleção de Categoria ---")
    
        categorias = self.db.obter_categorias()
        if not categorias:
            print("Nenhuma categoria cadastrada.")
            return
    
        while True:
            print("\nCategorias disponíveis:")
            for categoria in categorias:
                print(f"{categoria['id']}: {categoria['nome']}")
            print("0: Sair para o menu principal")
    
            try:
                escolha = int(input("Digite o número da categoria desejada: "))
                if escolha == 0:
                    print("Saindo para o menu principal...")
                    self.iniciar()
                    return
    
                categoria_selecionada = next((cat for cat in categorias if cat["id"] == escolha), None)
                if categoria_selecionada:
                    self.categoria = categoria_selecionada["nome"]
                    self.codigo_categoria = categoria_selecionada.get("codigo")
                    print(f"\nVocê selecionou: {self.categoria} (Código: {self.codigo_categoria or 'N/A'})")
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
    
        fornecedores = self.db.obter_fornecedores_por_categoria(categoria_selecionada["id"])
    
        if not fornecedores:
            print("Nenhum fornecedor disponível para esta categoria.")
            self.fornecedor = None
        else:
            while True:
                print("\nFornecedores disponíveis:")
                for fornecedor in fornecedores:
                    print(f"{fornecedor['id']}: {fornecedor['nome']}")
                print("0: Sair para o menu principal")
    
                try:
                    escolha = int(input("Digite o número do fornecedor desejado: "))
                    if escolha == 0:
                        print("Saindo para o menu principal...")
                        self.iniciar()
                        return
    
                    fornecedor_selecionado = next(
                        (forn for forn in fornecedores if forn["id"] == escolha), None
                    )
                    if fornecedor_selecionado:
                        self.fornecedor = fornecedor_selecionado["nome"]
                        print(f"\nVocê selecionou o fornecedor: {self.fornecedor}")
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")
                    
            while True:
                try:
                    self.parcelas = int(input("Digite o número de parcelas: "))
                    print(f"\nNúmero de parcelas selecionado: {self.parcelas}")
                    break
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")

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
                    if int(escolha) in self.alterar_valor:
                        self.escolha_alterar_valor = escolha
                        return escolha
                    else:
                        print("Opção inválida.")
                except ValueError:
                    print("Insira um número.")
        else:
            print("Não é necessário alterar o valor, pois é apenas 1 parcela.")
            self.escolha_alterar_valor = '1' 
            return '1' 
        
    def excluir_categoria(self):
        try:
            # Solicitar ao usuário o ID ou comando para exclusão
            #print("Digite o ID da categoria que deseja excluir.")
            #print("Para excluir todas as categorias, digite '@ALL'.")
            #print("Para excluir múltiplas categorias, insira os IDs separados por vírgula (exemplo: 1,2,3).")
            entrada = input("Sua escolha: ").strip()

            conn = sqlite3.connect('fornecedores.db')
            cursor = conn.cursor()

            if entrada == "@ALL":
                confirmacao = input("Você tem certeza que deseja excluir TODAS as categorias? Digite 'CONFIRMAR' para prosseguir: ").strip()
                if confirmacao == "CONFIRMAR":
                    cursor.execute('DELETE FROM categorias')
                    conn.commit()
                    print("Todas as categorias foram excluídas com sucesso!")
                else:
                    print("Exclusão de todas as categorias cancelada.")
            elif "," in entrada:  # Excluir múltiplas categorias
                ids = [int(id.strip()) for id in entrada.split(",")]
                categorias_nao_excluidas = []

                for categoria_id in ids:
                    cursor.execute('SELECT * FROM fornecedores WHERE categoria_id = ?', (categoria_id,))
                    fornecedores = cursor.fetchall()

                    if fornecedores:
                        categorias_nao_excluidas.append(categoria_id)
                    else:
                        cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
                conn.commit()

                print("Categorias especificadas excluídas, exceto as seguintes com fornecedores associados:")
                print(", ".join(map(str, categorias_nao_excluidas)) if categorias_nao_excluidas else "Nenhuma.")
            else:  # Excluir uma única categoria
                categoria_id = int(entrada)

                cursor.execute('SELECT * FROM fornecedores WHERE categoria_id = ?', (categoria_id,))
                fornecedores = cursor.fetchall()

                if fornecedores:
                    print("Não é possível excluir esta categoria, pois há fornecedores associados a ela.")
                else:
                    cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))
                    conn.commit()
                    print(f"Categoria com ID {categoria_id} excluída com sucesso!")

            # Reordenar IDs das categorias após qualquer exclusão
            cursor.execute('SELECT id FROM categorias ORDER BY id')
            categorias = cursor.fetchall()

            # Reorganizar as IDs em ordem numérica
            for index, (id_atual,) in enumerate(categorias, start=1):
                cursor.execute('UPDATE categorias SET id = ? WHERE id = ?', (index, id_atual))
            conn.commit()
            print("IDs das categorias reordenados com sucesso.")
            self.db.listar_categorias()

        except ValueError:
            print("Erro: Por favor, insira um número válido para o ID ou use os comandos indicados.")
        except sqlite3.Error as e:
            print(f"Erro ao excluir a categoria: {e}")
        finally:
            if 'conn' in locals() and conn:
                conn.close()
 
    def executar_automacao(self):
        print("Iniciando nova iteração do loop.")
        self.wait(2000)
        self.click_at(1003, 114)
        print("Clique realizado na posição (1003, 114).")
        self.notificar("Clique realizado", "Posição (1003, 114)")
        self.wait(1)
        #self.click_at(1227, 703)
        self.wait(3000)
        self.double_click_at(615,269)
        
        if self.parcelas > 1:
            self.calculadora()
        else:
            self.comportamento_para_nao()
            # Clique no campo e aguarda o texto ser inserido
            
        #listener = self._monitorar_teclado()
        #self.logs("iniciar")
        #self._monitorar_teclado()
        self.aguardar_tecla_insert("Etapa 1")  # Aguarda tecla Insert
        #self.logs("finalizar")
        #listener.stop()
        print("Esperando após digitar o Valor.")
        #self.notificar("Esperando", "Após digitar o valor")
        # Aguardar digitação de texto e Insert para a "Categoria"
        keyboard.press_and_release('tab')
        # Preenche somente o código se existir, senão preenche o nome
        self.wait(1)
        print(f"Valor inicial - categoria: {self.categoria}, codigo_categoria:{self.codigo_categoria}")
        try:
            if self.codigo_categoria:  # Verifica se o código da categoria tem um valor
                print(f"Usando o código da categoria: {self.codigo_categoria}")
                keyboard.write(str(self.codigo_categoria))  # Converte para string
            elif self.categoria:  # Verifica se o nome da categoria tem um valor
                print(f"Usando o nome da categoria: {self.categoria}")
                keyboard.write(self.categoria)  # Escreve diretamente
            else:
                # Se ambos forem None ou vazios, exibe a mensagem de erro
                print("Nenhum dado disponível para preencher a categoria.")
        except Exception as e:
            print(f"Erro ao preencher a categoria: {e}")
        #self.logs()

        time.sleep(0.25)
        #self.aguardar_tecla_insert("Etapa 2")
        #print("Esperando após digitar a categoria.")
        #self.notificar("Esperando", "Após digitar o categoria")
        # Ações com Tab e setas
        self.click_at(524, 337)
        self.wait(0.2)
        self.realizar_acao_por_categoria()
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
        #self.logs()
        print("Esperando após digitar a NFe.")
        self.notificar("Esperando", "Após digitar o NFe")
        # Continuar navegação com Tab
        self.pular_campos(3)
        print("Tecla 'Tab' pressionada após 'NFe'.")
        # Aguardar texto do 
        self.wait(0.50)
        keyboard.write(str(self.fornecedor))
        self.wait(0.50)
        self.double_click_at(1544, 538)
        #self.logs()
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
        #self.logs()
        print("Esperando após digitar o Vencimento.")
        self.notificar("Esperando", "Após digitar o Vencimento")
        self.pular_campos(2)
        keyboard.press_and_release('enter')
        self.selecionar_comportamento_parcelas()
     
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
        if not self.dados_lancamento:
            print("Nenhum dado para salvar.")
            return
        # Gera um nome de arquivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"log_lancamentos_{timestamp}.json"
        # Salva os dados em um arquivo JSON
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(self.dados_lancamento, arquivo, ensure_ascii=False, indent=4)
        print(f"Arquivo de log gerado: {nome_arquivo}")
        self.dados_lancamento = []  # Reseta a lista após salvar
        # Notificação de conclusão
        self.notificar("Processo Finalizado", f"Log salvo em {nome_arquivo}")
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
    
    def inicializar_dados(self, categorias, fornecedores):
        cursor = self.conn.cursor()

        # Adiciona categorias iniciais
        for categoria in categorias:
            cursor.execute(
                "INSERT OR IGNORE INTO categorias (nome, codigo) VALUES (?, ?)",
                (categoria["nome"], categoria.get("codigo")),
            )

        # Adiciona fornecedores iniciais
        for fornecedor in fornecedores:
            cursor.execute(
                """
                INSERT OR IGNORE INTO fornecedores (categoria_id, nome)
                VALUES (
                    (SELECT id FROM categorias WHERE nome = ?),
                    ?
                )
                """,
                (fornecedor["categoria"], fornecedor["nome"]),
            )

        self.conn.commit()

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

    #def logs(self, etapa):
    #    """
    #    Ativa ou finaliza a coleta de logs com base na etapa fornecida.
    #    """
    #    if etapa == "iniciar":
    #        print("Coleta de logs iniciada.")
    #        self.coletando_log = True
    #    elif etapa == "finalizar":
    #        print("Coleta de logs finalizada.")
    #        self.coletando_log = False
    #        self.dados_lancamento.append(self.log_atual.copy())  # Armazena o log
    #        print("Dados coletados:", self.log_atual)
    #        self.log_atual = {"valor": "", "NFe": "", "vencimento": ""}  # Reseta o log atual
#
    #def _monitorar_teclado(self):
    #    """
    #    Monitora teclas pressionadas enquanto a coleta de logs está ativa.
    #    """
    #    def on_press(key):
    #        if not self.coletando_log:
    #            return  # Não registra nada se a coleta não está ativa
#
    #        try:
    #            # Captura teclas alfanuméricas
    #            if hasattr(key, 'char') and key.char:
    #                self.log_atual[self.campo_atual] += key.char  # Adiciona à string atual
    #            # Lida com teclas especiais como backspace
    #            elif key == pynput.keyboard.Key.backspace:
    #                self.log_atual[self.campo_atual] = self.log_atual[self.campo_atual][:-1]
    #            # Depuração para exibir o valor atual do campo
    #            print(f"{self.campo_atual}: {self.log_atual[self.campo_atual]}")
    #        except Exception as e:
    #            print(f"Erro ao capturar tecla: {e}")
#
    #    # Inicia o monitoramento do teclado em um ouvinte separado
    #    listener = pynput.keyboard.Listener(on_press=on_press)
    #    listener.start()
    #    return listener

    def lancamentos(self):
        while True:
            
            self.selecionar_categoria()

            self.selecionar_banco()

                # Perguntar sobre alteração de valores
            self.selecionar_alteracao_valor(self.parcelas)

                # Executar automação com base nas escolhas
            self.executar_automacao()

                # Finalizar o processo
            self.finalizar_processo()
            print("\nIniciando novo processo de automação.")
            self.click_at(607, 1062)
            
    def realizar_acao_por_categoria(self):
        print("\n--- Realizando ações baseadas na categoria selecionada ---")

        if not hasattr(self, 'codigo_categoria'):
            print("Nenhuma categoria foi selecionada. Certifique-se de executar 'selecionar_categoria' primeiro.")
            return

        if self.codigo_categoria == ["4", "5"]:  # Use o código da categoria ou o nome, conforme sua lógica
            for i in range(5):
                py.press('down')
            print("Categoria específica detectada: Opção 1 (Código 4 ou 5).")
        else:
            for i in range(3):
                py.press('down')
            print("Categoria geral detectada: Opção 2.")

if __name__ == "__main__":
    try:
        # Inicializa o bot e o banco de dados
        bot = Bot()  # Certifique-se de que a classe 'Bot' está importada corretamente
        db = sqlite3.connect("dados.db")  # Substitua pelo nome correto do banco
        bot.db = db

        # Inicia o bot
        bot.iniciar()

        # Chamadas dos métodos do bot
        bot.adicionar_categoria()
        bot.adicionar_fornecedor()
        bot.selecionar_categoria()
        bot.selecionar_banco()
        bot.alterar = bot.selecionar_alteracao_valor(bot.parcelas)
        bot.executar_automacao()
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    
    finally:
        # Garante que o banco de dados seja fechado corretamente
        if 'db' in locals() and db:
            db.close()
            
        



