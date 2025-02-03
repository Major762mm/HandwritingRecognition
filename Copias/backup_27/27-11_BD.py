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

class FornecedorDB:
    
    def __init__(self, db_name='fornecedores.db'):
        self.db_name = db_name
        self.criar_banco()

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

    def editar_fornecedor(fornecedor_id, nome, cnpj, telefone, endereco, categoria_id):
        conn = sqlite3.connect('fornecedores.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE fornecedores
        SET nome = ?, cnpj = ?, telefone = ?, endereco = ?, categoria_id = ?
        WHERE id = ?
        ''', (nome, cnpj, telefone, endereco, categoria_id, fornecedor_id))

        conn.commit()
        print(f"Fornecedor ID {fornecedor_id} atualizado com sucesso!")

        conn.close()

    def obter_categorias(self):
        query = "SELECT id, nome, codigo FROM categorias"
        return self.executar_query(query)
    
    def obter_fornecedores_por_categoria(self, categoria_id):
        query = "SELECT id, nome FROM fornecedores WHERE categoria_id = ?"
        return self.executar_query(query, (categoria_id,))

    def executar_query(self, query, params=(), fetchone=False, fetchall=False):
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetchone:
                resultado = cursor.fetchone()
            elif fetchall:
                resultado = cursor.fetchall()
            else:
                conn.commit()
                resultado = None
            return resultado
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
#
db.listar_categorias()
#db.listar_fornecedores()
#
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
            0:      ("Conta - Agua/Luz", None)
    } 
    