import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading
import sqlite3
import logging

# Criação do banco de dados e das tabelas


categorias_iniciais = [

    {"nome": "Manutençao de Veículos", "codigo": None, "fornecedores": ["DVA veiculos", "Victor dos santos", "furgoes isoppo", "Rf Comercio", "Posto de molas", "Mezaroba com", "Mecanica Rosso", "Duarte Diesel", "RF - Sul", "Obemolas", "Center Valvulas", "Scherer", "Energiluz", "Molas Lambari", "Dirlete", "Lavacao master"]},
    {"nome": "Manutençao e Conservação Predial", "codigo": "4.2.3.19", "fornecedores": ["Madeireira u", "Oxi-genio", "dufrio", "Buachack", "Goedert LTDA", "Dominik", "Energiluz", "Rosso Materiais", "Guga gaz", "Luciano servicos", "Conexão posto"]},
    {"nome": "Manutençao de Máquinas", "codigo": "4.2.3.28", "fornecedores": ["Heth Maquinas", "Ambiente sul", "Maxus Impl", "Videfrigo", "Frigelar", "Guga gaz", "Dufrio"]},
    {"nome": "Peças Corretivas", "codigo": "4.2.3.17.2.1", "fornecedores": ["Scherer", "Valcanaia", "Disauto", "Atacado Diesel", "Casa do compressor", "Dva Veiculos", "center Valvulas", "Para-brisa", "P pneus", "Molas lambari", "buzetti", "Auto center", "Rex - radiadores", "Orbid S.A", "W C L Motopecas"]},
    {"nome": "Peças Preventivas", "codigo": "4.2.3.17.1.1", "fornecedores": ["Scherer", "Valcanaia", "Disauto", "Atacado Diesel", "Casa do compressor", "Dva Veiculos", "center Valvulas", "Para-brisa", "P pneus", "Molas lambari", "buzetti", "Auto center", "Rex - radiadores", "Orbid S.A", "W C L Motopecas"]},
    {"nome": "Combustível e Lubrificantes", "codigo": "4.2.3.21", "fornecedores": ["Agricopel comercio", "Romano Diesel", "Planalto Com", "Rudnick", "Auto posto dallabona iii", "posto 4 irmaos", "marajo", "Nac Sul", "Maucor", "Conexão posto", "Posto e Restaurante", "Ongarato"]},
    {"nome": "Aluguéis", "codigo": "4.2.3.10", "fornecedores": ["A&B locadora", "heth maquinas", "Macromaq", "Aluga maquinas Sul"],},
    {"nome": "Energia", "codigo": "4.2.3.11", "fornecedores": ["Celesc", "Coop de energia eletrica", "Copel Distribuição"]},
    {"nome": "Água e Esgoto", "codigo": "4.2.3.12", "fornecedores": ["Companhia Catarinense de Águas", "Sanepar", "Semasa"]},
    {"nome": "Material de Limpeza", "codigo": None, "fornecedores": ["Goedert LTDA", "KL industria", "Mais clean", "KL produtos", "limpel"]},
    {"nome": "Serviços de Terceiros", "codigo": "4.2.3.20", "fornecedores": ["SBM renovadora", "A&E locadora", "Katia regina", "P4 Comunicação", "Rico lavação", "STZ Comunicação", "Hoff S.A", "P pneus serviços"]},
    {"nome": "Taxas", "codigo": "4.2.3.23", "fornecedores": ["BSB comercio", "cento e um velocimetros"]},
    {"nome": "Despesas com Refeitório - Matriz", "codigo": "4.2.3.37", "fornecedores": ["Camilo e tutumi", "Armazem agua", "Guga gaz", "Panificadora fazendinha", "Frutas na caixa"]},
    {"nome": "Material de Escritório", "codigo": "4.2.3.15", "fornecedores": ["Alexandre livramento", "Multwork comercial", "Contabilista suprimentos", "Reval atacado", "SRC embalagens"]},
    {"nome": "Despesas com Alimentação - Curitiba", "codigo": "4.2.9.15", "fornecedores": ["Camilo e tutumi", "Armazem agua", "Guga gaz", "Panificadora fazendinha", "Frutas na caixa"]},
    {"nome": "Telefones", "codigo": "4.2.3.13", "fornecedores": ["Claro S/A", "TIM S.A", "VIVO"]},

]

class FornecedorDB:
    
    def __init__(self, db_name='fornecedores.db'):
        self.db_name = db_name
        self.criar_banco()
        #self.inserir_dados_iniciais(categorias_iniciais)
        self.reordenar_ids()
       
    def conectar(self):
        """Estabelece conexão com o banco de dados."""
        db_path = os.path.abspath('fornecedores.db')
        return sqlite3.connect(db_path)
     
    def criar_banco(self):
        """Cria o banco de dados e as tabelas, caso necessário."""
        
        conn = self.conectar()
        cursor = conn.cursor()

        # Criação das tabelas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                codigo TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')

        conn.commit()
        conn.close()
        
        # Mostrar o log apenas uma vez
        if not os.path.exists(self.db_name):
            print("Criando novo banco de dados...")
        else:
            print("Banco de dados já existe.")

    def cadastrar_categoria(self, nome, codigo=None):
        """Adiciona uma nova categoria ao banco de dados."""
        conn = self.conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO categorias (nome, codigo) VALUES (?, ?)", (nome, codigo))
            conn.commit()  # Garante que as alterações são salvas
        except sqlite3.IntegrityError as e:
            print(f"Erro ao adicionar categoria: {e}")
        finally:
            conn.close()  # Fecha a conexão corretamente

    def listar_categorias(self):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        # Corrigindo a query SQL
        cursor.execute('SELECT id, nome FROM categorias')
        categorias = cursor.fetchall()

        if categorias:
            print("\nCategorias disponíveis:")
            for categoria in categorias:
                print(f"ID: {categoria[0]}, Nome: {categoria[1]}")
        else:
            print("\nNenhuma categoria cadastrada.")

        conn.close()
        return categorias  # Retorne o resultado obtido no cursor local

    def cadastrar_fornecedor(self, nome, categoria_id):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO fornecedores (nome, categoria_id)
        VALUES (?, ?)
        ''', (nome, categoria_id))

        conn.commit()
        conn.close()
        print(f"Fornecedor '{nome}' cadastrado na categoria ID {categoria_id} com sucesso!")

    @staticmethod
    def listar_fornecedores():
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT f.id, f.nome, c.nome 
        FROM fornecedores f
        LEFT JOIN categorias c ON f.categoria_id = c.id
        ''')
        fornecedores = cursor.fetchall()

        if fornecedores:
            print("\nFornecedores cadastrados:")
            for fornecedor in fornecedores:
                print(f"ID: {fornecedor[0]}, Nome: {fornecedor[1]} Categoria: {fornecedor[2]}")
        else:
            print("\nNenhum fornecedor cadastrado.")

        conn.close()

    def verificar_categoria_existente(self, nome):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM categorias WHERE nome = ?', (nome,))
        categoria = cursor.fetchone()
        conn.close()

        return categoria is not None

    def excluir_categoria(id_categoria):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        # Verificar se há fornecedores associados à categoria
        cursor.execute('SELECT * FROM fornecedores WHERE categoria_id = ?', (id_categoria,))
        fornecedores = cursor.fetchall()

        if fornecedores:
            print("Não é possível excluir esta categoria, pois há fornecedores associados a ela.")
        else:
            cursor.execute('DELETE FROM categorias WHERE id = ?', (id_categoria,))
            conn.commit()
            print(f"Categoria com ID {id_categoria} excluída com sucesso!")

        conn.close()

    def verificar_fornecedor_existente(self, categoria_id, nome):
        query = "SELECT id FROM fornecedores WHERE categoria_id = ? AND nome = ?"
        return bool(self.executar_query(query, (categoria_id, nome), fetchone=True))

    def excluir_fornecedor(id_fornecedor):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM fornecedores WHERE id = ?', (id_fornecedor,))
        conn.commit()
        conn.close()
        print(f"Fornecedor com ID {id_fornecedor} excluído com sucesso!")
   
    def editar_categoria(self):
        db.listar_categorias()
        categoria_id = int(input("Digite o ID da categoria que deseja editar: "))

        # Verificar se a categoria existe
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categorias WHERE id = ?", (categoria_id,))
        categoria = cursor.fetchone()

        if not categoria:
            print(f"Categoria com ID {categoria_id} não encontrada.")
            conn.close()
            return

        # Solicitar novos valores para a categoria
        novo_nome = input("Digite o novo nome da categoria (ou pressione Enter para manter): ") or categoria[1]
        novo_codigo = input("Digite o novo código da categoria (ou pressione Enter para manter): ") or categoria[2]

        # Atualizar a categoria
        cursor.execute('''
        UPDATE categorias
        SET nome = ?, codigo = ?
        WHERE id = ?
        ''', (novo_nome, novo_codigo, categoria_id))

        conn.commit()
        print(f"Categoria ID {categoria_id} atualizada com sucesso!")
        conn.close()

        
        #Uso
        # Atualizar apenas o nome da categoria
        #self.editar_categoria(categoria_id=1, nome="Manutencao de veiculos")
        
        # Atualizar apenas o código da categoria
        #editar_categoria(categoria_id=3, codigo="12345")
        
        # Atualizar o nome e o código da categoria
        #editar_categoria(categoria_id=3, nome="Outra Categoria", codigo="67890")

    def editar_fornecedor(self):
        """
        Edita os dados de um fornecedor no banco de dados, com base na categoria selecionada.
        """
        # Listar as categorias disponíveis
        categorias = db.listar_categorias()
        if not categorias:
            print("Nenhuma categoria encontrada. Adicione categorias antes de editar fornecedores.")
            return

        # Exibir categorias disponíveis
        print("\nCategorias disponíveis:")
        for categoria in categorias:
            print(f"{categoria[0]}: {categoria[1]}")

        # Solicitar a categoria desejada
        try:
            categoria_id = int(input("Digite o ID da categoria para filtrar os fornecedores: "))
            categoria_selecionada = next((cat for cat in categorias if cat[0] == categoria_id), None)

            if not categoria_selecionada:
                print("Categoria não encontrada. Verifique o ID e tente novamente.")
                return

            # Listar fornecedores da categoria selecionada
            fornecedores = db.obter_fornecedores_por_categoria(categoria_id)
            if not fornecedores:
                print(f"Nenhum fornecedor encontrado para a categoria '{categoria_selecionada[1]}'.")
                return

            print(f"\nFornecedores da categoria '{categoria_selecionada[1]}':")
            for fornecedor in fornecedores:
                print(f"{fornecedor['id']}: {fornecedor['nome']}")  # Adaptado ao formato de dicionário

            # Solicitar o fornecedor a ser editado
            fornecedor_id = int(input("Digite o ID do fornecedor que deseja editar: "))
            fornecedor_selecionado = next((f for f in fornecedores if f["id"] == fornecedor_id), None)

            if not fornecedor_selecionado:
                print("Fornecedor não encontrado. Verifique o ID e tente novamente.")
                return

            # Solicitar novos valores
            print(f"\nFornecedor atual: Nome='{fornecedor_selecionado['nome']}'")
            novo_nome = input("Digite o novo nome do fornecedor (ou pressione Enter para manter): ") or fornecedor_selecionado['nome']

            # Atualizar o fornecedor no banco de dados
            with sqlite3.connect('fornecedores.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE fornecedores
                    SET nome = ?, categoria_id = ?
                    WHERE id = ?
                ''', (novo_nome, categoria_id, fornecedor_id))

                conn.commit()
                print(f"\nFornecedor ID {fornecedor_id} atualizado com sucesso!")

        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")
        except sqlite3.Error as e:
            print(f"Erro ao editar o fornecedor: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    def obter_categorias(self):
        query = "SELECT id, nome, codigo FROM categorias"
        resultados = self.executar_query(query)
    
        if resultados is None:
            return []  # Retorna uma lista vazia se não houver resultados
        else:
            return [{"id": categoria[0], "nome": categoria[1], "codigo": categoria[2]} for categoria in resultados]

    def obter_fornecedores_por_categoria(self, categoria_id):
        query = "SELECT id, nome FROM fornecedores WHERE categoria_id = ?"
        resultados = self.executar_query(query, (categoria_id,))
        # Convertendo os resultados para uma lista de dicionários
        fornecedores = [{"id": row[0], "nome": row[1]} for row in resultados]
        return fornecedores

    def executar_query(self, query, params=None):
        try:
            conn = sqlite3.connect('fornecedores.db')
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.fetchall()  # Retorna todos os resultados
        except sqlite3.Error as e:
            print(f"Erro ao executar consulta: {e}")
            return []  # Retorna uma lista vazia em caso de erro
        finally:
            conn.close()

    def reordenar_ids(self):
        try:
            conn = sqlite3.connect('fornecedores.db')
            cursor = conn.cursor()

            # Criar tabela temporária com IDs automáticos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS temp_categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    codigo TEXT
                )
            ''')

            # Copiar dados para a tabela temporária, garantindo a ordem pela ID original
            cursor.execute('''
                INSERT INTO temp_categorias (nome, codigo)
                SELECT nome, codigo FROM categorias
                ORDER BY id  -- Ordenando pela ID original
            ''')

            # Excluir a tabela original
            cursor.execute('DROP TABLE categorias')

            # Renomear a tabela temporária para o nome original
            cursor.execute('ALTER TABLE temp_categorias RENAME TO categorias')

            conn.commit()
            print("IDs reorganizados com sucesso.")

        except sqlite3.Error as e:
            print(f"Erro ao reorganizar IDs: {e}")
        finally:
            conn.close()

    def inserir_dados_iniciais(self, dados):  # Responsável por alimentar o banco de dados
        try:
            conn = sqlite3.connect('fornecedores.db')
            cursor = conn.cursor()

            # Inserir categorias e fornecedores
            for item in dados:
                # Verificar se a categoria já existe pelo nome
                cursor.execute('SELECT id FROM categorias WHERE nome = ?', (item['nome'],))
                categoria = cursor.fetchone()

                if not categoria:
                    # Inserir categoria com nome e código
                    cursor.execute('INSERT INTO categorias (nome, codigo) VALUES (?, ?)', (item['nome'], item['codigo']))
                    categoria_id = cursor.lastrowid
                else:
                    categoria_id = categoria[0]

                # Inserir fornecedores associados à categoria
                for fornecedor in item.get('fornecedores', []):
                    cursor.execute(
                        'SELECT id FROM fornecedores WHERE nome = ? AND categoria_id = ?',
                        (fornecedor, categoria_id)
                    )
                    fornecedor_existente = cursor.fetchone()
                    if not fornecedor_existente:
                        # Inserir fornecedor se não existir
                        cursor.execute(
                            'INSERT INTO fornecedores (nome, categoria_id) VALUES (?, ?)',
                            (fornecedor, categoria_id)
                        )

            conn.commit()
            print("Dados iniciais inseridos com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados iniciais: {e}")
        finally:
            conn.close()


                
if __name__ == "__main__":
    app = FornecedorDB()
    # Chame criar_banco apenas uma vez, ou verifique antes
    #app.menu_principal()

db = FornecedorDB()
#db.cadastrar_categoria("Manutencao de veiculos")
#db.cadastrar_categoria("Pecas de reposicao")

#categorias = db.listar_categorias()
#print("Categorias disponíveis:")
#for categoria in categorias:
#    print(f"ID: {categoria[0]}, Nome: {categoria[1]}")

#db.listar_categorias()
#db.listar_fornecedores()

#  Testar cadastro de fornecedor
#db.cadastrar_fornecedor("Loja de Pecas", 1)  # Associando à categoria com ID 1
#db.cadastrar_fornecedor("Oficina do Pedro", 1)
#db.cadastrar_fornecedor("Distribuidora de Peças", 2)

# Listar fornecedores (você pode adicionar este método caso precise)

bancos = {
            654:	("A.J. RENNER S.A.", None),
            246:	("ABC-BRASIL S.A.", None),
            213:	("ARBI S.A.", None),
            19:	    ("AZTECA DO BRASIL , None),A.", None),
            25:	    ("BANCO ALFA", None),
            241:    ("Banco Classico S.A", None),
            83:	    ("BANCO DA CHINA BRASIL S.A.", None),
            300:    ("BANCO DE LA NACION ARGENTINA", None),
            495:    ("BANCO DE LA PROVINCIA DE BUENOS AIRES", None),
            494:    ("BANCO DE LA REPUBLICA ORIENTAL DEL URUGUAY", None),
            1:      ("BANCO DO BRASIL", None),
            37:	    ("BANCO DO ESTADO DO PARÁ S.A", None),
            456:	("BANCO TOKYO MITSUBISH UFJ BRASIL S.A", None),
            370:	("BANCO WESTLB DO BRASIL", None),
            756:	("SICOOB", None),
            47:	    ("BANESE", None),
            33:	    ("SANTANDER", None),
            21:	    ("BANESTES", None),
            719:	("BANIF-BANCO INTERNACIONAL DO FUNCHAL (BRASIL) S.A", None),
            755:	("BANK OF AMERICA MERRILL LYNCH BANCO MULTIPLO S.A.", None),
            41:	    ("BANRISUL", None),
            740:	("BARCLAYS S.A.", None),
            3:      ("BASA", None),
            107:	("BBM S.A", None),
            81:	    ("BBN BANCO BRASILEIRO DE NEGOCIOS S.A", None),
            250:	("BCV - BANCO DE CREDITO E VAREJO S.A", None),
            36:	    ("BEM", None),
            122:	("BERJ S.A", None),
            78:	    ("BES INVESTIMENTO DO BRASIL SA - BANCO DE INVESTIM.", None),
            739:	("BGN S.A.", None),
            320:	("BIC BANCO", None),
            96:	    ("BM&F DE SERV. DE LIQUIDACAO E CUSTODIA S.A", None),
            394:	("BMC S.A.", None),
            318:	("BMG S.A.", None),
            4:      ("BNB", None),
            752:	("BNP PARIBAS BRASIL S.A", None),
            17:	    ("BNY MELLON S.A.", None),
            248:	("BOA VISTA INTERATLANTICO S.A", None),
            218:	("BONSUCESSO S.A.", None),
            69:	    ("BPN BRASIL BANCO MULTIPLO S.A", None),
            65:	    ("BRACCE S.A.", None),
            237:	("BRADESCO", None),
            225:	("BRASCAN S.A.", None),
            125:	("BRASIL PLURAL S.A. BANCO MULTIPLO", None),
            70:	    ("BRB", None),
            92:	    ("BRICKELL S A CREDITO, FINANCIAMENTO E INVESTIMENTO", None),
            208:	("BTG PACTUAL S.A.", None),
            263:	("CACIQUE S.A.", None),
            104:	("CAIXA ECON. FEDERAL", None),
            473:	("CAIXA GERAL - BRASIL S.A.", None),
            412:	("CAPITAL S.A.", None),
            40:	    ("CARGILL S.A", None),
            112:	("CC UNICRED BRASIL CENTRAL", None),
            84:	    ("CC UNIPRIME NORTE DO PARANA", None),
            114:	("CECOOPES-CENTRAL DAS COOP DE ECON E CRED MUTUO", None),
            85:	    ("AILOS", None),
            266:	("CEDULA S.A.", None),
            233:	("CIFRA S.A.", None),
            745:	("CITIBANK", None),
            477:	("Citibank N.A.", None),
            90:	    ("COOPERATIVA CENTRAL DE CREDITO DO ESTADO DE SP", None),
            97:	    ("COOPERATIVA CENTRAL DE CREDITO NOROESTE BRASILEIRO", None),
            89:	    ("COOPERATIVA DE CREDITO RURAL DA REGIAO DA MOGIANA", None),
            75:	    ("CR2 S.A", None),
            98:	    ("CREDIALIANCA COOPERATIVA DE CREDITO RURAL", None),
            222:	("CREDIT AGRICOLE BRASIL S.A.", None),
            505:	("CREDIT SUISSE (BRASIL) S.A.", None),
            707:	("DAYCOVAL", None),
            487:	("DEUTSCHE BANK S. A. - BANCO ALEMAO", None),
            214:	("DIBENS S.A.", None),
            265:	("FATOR S.A.", None),
            224:	("FIBRA", None),
            626:	("FICSA S.A.", None),
            121:	("GERADOR S.A.", None),
            612:	("GUANABARA S.A.", None),
            62:	    ("HIPERCARD BANCO MULTIPLO S.A", None),
            399:	("HSBC", None),
            63:	    ("IBI", None),
            604:	("INDUSTRIAL DO BRASIL S. A.", None),
            653:	("INDUSVAL S.A.", None),
            492:	("ING BANK N.V.", None),
            630:	("INTERCAP S.A.", None),
            77:	    ("INTERMEDIUM S.A.", None),
            249:	("Investcred Unibanco", None),
            341:	("ITAÚ", None),
            652:	("ITAU HOLDING FINANCEIRA S.A", None),
            184:	("Itaú-BBA", None),
            74:	    ("J. SAFRA S.A.", None),
            376:	("J.P. MORGAN S.A.", None),
            217:	("JOHN DEERE S.A.", None),
            488:	("JPMORGAN CHASE BANK", None),
            76:	    ("KDB DO BRASIL S.A", None),
            757:	("KEB DO BRASIL S.A.", None),
            600:	("Luso Brasileiro", None),
            243:	("MAXIMA S.A.", None),
            389:	("MERCANTIL DO BRASIL", None),
            746:	("MODAL S.A.", None),
            66:	    ("MORGAN STANLEY DEAN WITTER S.A", None),
            14:	    ("NATIXIS BRASIL S.A. - BANCO MòLTIPLO", None),
            753:	("NBC BANK BRASIL S.A.- BANCO MULTIPLO", None),
            45:	    ("OPPORTUNITY S.A.", None),
            79:	    ("ORIGINAL DO AGRONEGOCIO S.A.", None),
            212:	("ORIGINAL S.A.", None),
            623:	("PANAMERICANO", None),
            254:	("PARANA BANCO S.A.", None),
            611:	("PAULISTA", None),
            613:	("PECUNIA S.A.", None),
            94:	    ("PETRA S.A.", None),
            643:	("PINE S.A.", None),
            735:	("POTTENCIAL S.A.", None),
            747:	("RABOBANK INTERNATIONAL BRASIL S.A.", None),
            88:	    ("RANDON S.A.", None),
            633:	("RENDIMENTO S.A.", None),
            741:	("RIBEIRÃO PRETO", None),
            120:	("RODOBENS S.A", None),
            453:	("RURAL", None),
            72:	    ("RURAL MAIS S.A", None),
            422:	("SAFRA", None),
            751:	("SCOTIABANK BRASIL S.A BANCO MULTIPLO", None),
            743:	("SEMEAR S.A.", None),
            748:	("SICREDI", None),
            749:	("SIMPLES S.A.", None),
            366:	("SOCIETE GENERALE BRASIL S.A", None),
            637:	("SOFISA S.A.", None),
            464:	("SUMITOMO MITSUI BRASILEIRO S.A.", None),
            82:	    ("TOPAZIO S.A.", None),
            634:	("Triangulo", None),
            230:	("UNICARD BANCO MULTIPLO S.A", None),
            91:	    ("UNICRED CENTRAL RS - CENTRAL DE COOP ECON CRED MUT", None),
            87:	    ("UNICRED CENTRAL SANTA CATARINA", None),
            99:	    ("UNIPRIME CENTRAL - CENTRAL INT DE COOP DE CRED LTD", None),
            655:	("VOTORANTIM", None),
            610:	("VR S.A.", None),
            119:	("WESTERN UNION DO BRASIL S.A.", None),
            124:	("WOORI BANK DO BRASIL S.A", None),
            136:	("Unicred", None),
            0:      ("Conta - Agua/Luz", None),
            461:    ("Asaas", None)
    } 



##########################Funções desativadas####################
#def inserir_dados_iniciais(self, dados): #responsavel por alimentar o banco de dados
    #    try:
    #        conn = sqlite3.connect('fornecedores.db')
    #        cursor = conn.cursor()

    #        for item in dados:
    #            # Inserir a categoria, se não existir
    #            cursor.execute('SELECT id FROM categorias WHERE nome = ?', (item['categoria'],))
    #            categoria = cursor.fetchone()

    #            if not categoria:
    #                cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (item['categoria'],))
    #                categoria_id = cursor.lastrowid
    #            else:
    #                categoria_id = categoria[0]

    #            # Inserir fornecedores associados à categoria
    #            for fornecedor in item['fornecedores']:
    #                cursor.execute('SELECT id FROM fornecedores WHERE nome = ? AND categoria_id = ?', (fornecedor, categoria_id))
    #                fornecedor_existente = cursor.fetchone()

    #                if not fornecedor_existente:
    #                    cursor.execute(
    #                        'INSERT INTO fornecedores (nome, categoria_id) VALUES (?, ?)',
    #                        (fornecedor, categoria_id)
    #                    )

    #        conn.commit()
    #        print("Dados iniciais inseridos com sucesso!")
    #    except sqlite3.Error as e:
    #            print(f"Erro ao inserir dados iniciais: {e}")