import sqlite3
from botcity.core import DesktopBot
import threading


categorias_iniciais = [

    {"id": 1, "nome": "Manutenção de Veículos", "codigo": None},

    {"id": 2, "nome": "Manutenção e Conservação Predial", "codigo": "4.2.3.19"},

    {"id": 3, "nome": "Manutenção de Máquinas", "codigo": "4.2.3.28"},

    {"id": 4, "nome": "Peças Corretivas", "codigo": "4.2.3.17.2.1"},

    {"id": 5, "nome": "Peças Preventivas", "codigo": "4.2.3.17.1.1"},

    {"id": 6, "nome": "Combustível e Lubrificantes", "codigo": "4.2.3.21"},

    {"id": 7, "nome": "Aluguéis", "codigo": "4.2.3.10"},

    {"id": 8, "nome": "Energia", "codigo": "4.2.3.11"},

    {"id": 9, "nome": "Água e Esgoto", "codigo": "4.2.3.12"},

    {"id": 10, "nome": "Material de Limpeza", "codigo": None},

    {"id": 11, "nome": "Serviços de Terceiros", "codigo": "4.2.3.20"},

    {"id": 12, "nome": "Taxas", "codigo": "4.2.3.23"},

    {"id": 13, "nome": "Despesas com Refeitório - Matriz", "codigo": "4.2.3.37"},

    {"id": 14, "nome": "Material de Escritório", "codigo": "4.2.3.15"},

    {"id": 15, "nome": "Despesas com Alimentação - Curitiba", "codigo": "4.2.9.15"},

    {"id": 16, "nome": "Telefones", "codigo": "4.2.3.13"},

]

fornecedores_iniciais = [

    {"categoria": "Manutenção de Veiculos", "fornecedores": [

        "DVA veiculos", "Victor dos santos", "furgoes isoppo", "Rf Comercio", 

        "Posto de molas", "Mezaroba com", "Mecanica Rosso", "Duarte Diesel", 

        "RF - Sul", "Obemolas", "Center Valvulas", "Scherer", "Energiluz", 

        "Molas Lambari", "Dirlete", "Lavacao master"

    ]},

    {"categoria": "Manutenção e conservação predial", "fornecedores": [

        "Madeireira u", "Oxi-genio", "dufrio", "Buachack", "Goedert LTDA", 

        "Dominik", "Energiluz", "Rosso Materiais", "Guga gaz", "Luciano servicos", 

        "Conexão posto"

    ]},

    {"categoria": "Manutenção de maquinas", "fornecedores": [

        "Heth Maquinas", "Ambiente sul", "Maxus Impl", "Videfrigo", 

        "Frigelar", "Guga gaz", "Dufrio"

    ]},

    {"categoria": "Peças corretivas", "fornecedores": [

        "Scherer", "Valcanaia", "Disauto", "Atacado Diesel", 

        "Casa do compressor", "Dva Veiculos", "center Valvulas", 

        "Para-brisa", "P pneus", "Molas lambari", "buzetti", 

        "Auto center", "Rex - radiadores", "Orbid S.A", "W C L Motopecas"

    ]},

    {"categoria": "Peças preventivas", "fornecedores": [

        "Scherer", "Valcanaia", "Disauto", "Atacado Diesel", 

        "Casa do compressor", "Dva Veiculos", "center Valvulas", 

        "Para-brisa", "P pneus", "Molas lambari", "buzetti", 

        "Auto center", "Rex - radiadores", "Orbid S.A", "W C L Motopecas"

    ]},

    {"categoria": "Combustivel e lubrificantes", "fornecedores": [

        "Agricopel comercio", "Romano Diesel", "Planalto Com", "Rudnick", 

        "Auto posto dallabona iii", "posto 4 irmaos", "marajo", "Nac Sul", 

        "Maucor", "Conexão posto", "Posto e Restaurante", "Ongarato"

    ]},

    {"categoria": "Aluguéis", "fornecedores": [

        "A&B locadora", "heth maquinas", "Macromaq", "Aluga maquinas Sul"

    ]},

    {"categoria": "Energia", "fornecedores": [

        "Celesc", "Coop de energia eletrica", "Copel Distribuição"

    ]},

    {"categoria": "Agua e esgoto", "fornecedores": [

        "Companhia Catarinense de Águas", "Sanepar", "Semasa"

    ]},

    {"categoria": "Material limpeza", "fornecedores": [

        "Goedert LTDA", "KL industria", "Mais clean", 

        "KL produtos", "limpel"

    ]},

    {"categoria": "Serviços de terceiros", "fornecedores": [

        "SBM renovadora", "A&E locadora", "Katia regina", 

        "P4 Comunicação", "Rico lavação", "STZ Comunicação", 

        "Hoff S.A", "P pneus serviços"

    ]},

    {"categoria": "Taxas", "fornecedores": [

        "BSB comercio", "cento e um velocimetros"

    ]},

    {"categoria": "Despesas com refeitorio - Matriz", "fornecedores": [

        "Camilo e tutumi", "Armazem agua", "Guga gaz", 

        "Panificadora fazendinha", "Frutas na caixa"

    ]},

    {"categoria": "Material escritorio", "fornecedores": [

        "Alexandre livramento", "Multwork comercial", 

        "Contabilista suprimentos", "Reval atacado", "SRC embalagens"

    ]},

    {"categoria": "Despesas com Alimentação - Curitiba", "fornecedores": [

        "Camilo e tutumi", "Armazem agua", "Guga gaz", 

        "Panificadora fazendinha", "Frutas na caixa"

    ]},

    {"categoria": "Telefones", "fornecedores": [

        "Claro S/A", "TIM S.A", "VIVO"

    ]}

]

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def inicializar_dados(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Criação da tabela de categorias, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                codigo TEXT
            )
        ''')

        # Criação da tabela de fornecedores, se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            );

        ''')

        # Adicionar dados iniciais de categorias se não existirem
        for categoria in categorias_iniciais:
            if not self.verificar_categoria_existente(categoria['nome']):
                self.adicionar_categoria(categoria['nome'], categoria['codigo'])

        conn.commit()
        conn.close()

    def adicionar_categoria(self, nome, codigo):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categorias (nome, codigo) VALUES (?, ?)", (nome, codigo))
        conn.commit()
        conn.close()

    def adicionar_fornecedor(self, nome, categoria_id):
        conn = self.connect()
        cursor = conn.cursor()

        # Verificar se a categoria existe antes de inserir o fornecedor
        cursor.execute("SELECT id FROM categorias WHERE id = ?", (categoria_id,))
        categoria = cursor.fetchone()

        if categoria:
            cursor.execute(
                "INSERT INTO fornecedores (nome, categoria_id) VALUES (?, ?)",
                (nome, categoria_id)
            )
            conn.commit()
            print(f"Fornecedor '{nome}' adicionado com sucesso à categoria com ID {categoria_id}.")
        else:
            print(f"Erro: Categoria com ID {categoria_id} não encontrada.")

        conn.close()

    def verificar_categoria_existente(self, nome):
        conn = self.connect()
        cursor = conn.cursor()

        # Verifica se a categoria existe no banco de dados
        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (nome,))
        categoria = cursor.fetchone()
        conn.close()
        return categoria is not None

    def verificar_fornecedor_existente(self, nome, categoria_id):
        conn = self.connect()
        cursor = conn.cursor()

        # Verifica se o fornecedor existe associado à categoria
        cursor.execute(
            "SELECT id FROM fornecedores WHERE nome = ? AND categoria_id = ?",
            (nome, categoria_id)
        )
        fornecedor = cursor.fetchone()
        conn.close()

        return fornecedor is not None

    def obter_categoria_id(self, nome):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (nome,))
        categoria = cursor.fetchone()
        conn.close()
        return categoria['id'] if categoria else None

    def obter_categorias(self):
        conn = self.connect()  # Cria uma conexão com o banco
        cursor = conn.cursor()  # Cria o cursor associado à conexão
        query = "SELECT id, nome, codigo FROM categorias"
        cursor.execute(query)
        resultados = cursor.fetchall()  # Obtem os resultados da consulta
        conn.close()  # Fecha a conexão
        # Converte os resultados em uma lista de dicionários
        categorias = [dict(zip(["id", "nome", "codigo"], resultado)) for resultado in resultados]
        return categorias

    def obter_fornecedores(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, categoria_id FROM fornecedores")
        resultados = cursor.fetchall()
        conn.close()
        fornecedores = [dict(zip(["id", "nome", "categoria_id"], resultado)) for resultado in resultados]
        return fornecedores

    def apagar_categoria(self, nome, categoria_id):
        conn = self.connect()
        cursor = conn.cursor()
        
        # Verificando se a categoria existe com o nome e ID fornecidos
        cursor.execute("SELECT * FROM categorias WHERE nome = ? AND id = ?", (nome, categoria_id))
        categoria = cursor.fetchone()

        if categoria:
            cursor.execute("DELETE FROM categorias WHERE nome = ? AND id = ?", (nome, categoria_id))
            conn.commit()
            print(f"Categoria '{nome}' com ID {categoria_id} apagada com sucesso.")
        else:
            print(f"Nenhuma categoria encontrada com o nome '{nome}' e ID {categoria_id}.")
        
        conn.close()

    def apagar_fornecedor(self, nome, categoria_id):
        conn = self.connect()
        cursor = conn.cursor()

        # Verificando se o fornecedor existe com o nome e categoria_id fornecidos
        cursor.execute("SELECT * FROM fornecedores WHERE nome = ? AND categoria_id = ?", (nome, categoria_id))
        fornecedor = cursor.fetchone()

        if fornecedor:
            cursor.execute("DELETE FROM fornecedores WHERE nome = ? AND categoria_id = ?", (nome, categoria_id))
            conn.commit()
            print(f"Fornecedor '{nome}' com categoria ID {categoria_id} apagado com sucesso.")
        else:
            print(f"Nenhum fornecedor encontrado com o nome '{nome}' e categoria ID {categoria_id}.")
        
        conn.close()

# Criando uma instância do banco de dados
db = Database("dados.db")

# Inicializando o banco (criação das tabelas e inserção das categorias iniciais)
db.inicializar_dados()

# Verificando as categorias inseridas
categorias = db.obter_categorias()
print("Categorias cadastradas:")
for categoria in categorias:
    print(f"ID: {categoria['id']}, Nome: {categoria['nome']}, Código: {categoria['codigo']}")


categoria_id = db.obter_categoria_id("Categoria A")
#Adicionar ou remover dados do banco
#db.adicionar_categoria("Categoria A", "12345")
#db.adicionar_categoria("Categoria B", "67890")
#db.adicionar_fornecedor("Fornecedor 1", categoria_id)
#db.adicionar_fornecedor("Fornecedor 2", categoria_id)



# Apagar um fornecedor
#db.apagar_fornecedor("Fornecedor 1", categoria_id)

# Apagar uma categoria
#db.apagar_categoria("Categoria B", 4)
#db.apagar_categoria("Categoria A", 3)

# Verificando novamente as categorias após exclusões
categorias = db.obter_categorias()
for categoria in categorias:
    print(f"ID: {categoria['id']}, Nome: {categoria['nome']}, Código: {categoria['codigo']}")


fornecedores = db.obter_fornecedores()
for fornecedor in fornecedores:
    if len(fornecedor) == 3:  # Verifica se a tupla tem 3 elementos (id, nome, codigo)
        print(f"ID: {fornecedor['id']}, Nome: {fornecedor['nome']}, Categoria: {fornecedor['categoria_id']}")
    else:
        print(f"Nome: {fornecedor['nome']}, Código: {fornecedor['codigo']}")


    # Adicione métodos da classe Bot conforme necessário
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
    
