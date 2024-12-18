import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading
from bancos_e_funções import bancos


class Bot(DesktopBot):
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
        
        self.categorias = { 
            1: ("Manutenção de Veiculos", None),
            2: ("Manutenção e conservação predial", "4.2.3.19"),
            # Resto das categorias...
        }
        
        self.alterar_valor = {
            1: "Não",
            2: "Sim"
        }
        
        self.categoria = None
        self.parcelas = None
        self.banco = None
        self.nome_banco = None
        self.alterar = None
        self.escolha = None
        self.iniciar()
        
    def iniciar(self):
        # Entrada simplificada para seleção e preenchimento
        self.selecionar_categoria()
        self.parcelas = self.input_numerico("Digite o número de parcelas: ")
        self.banco = self.selecionar_banco()
        self.alterar = self.selecionar_alteracao_valor() if self.parcelas > 1 else None
        self.executar_automacao()

    def selecionar_categoria(self):
        print("Selecione o tipo de lançamento:")
        for numero, categoria in self.categorias.items():
            print(f"{numero}: {categoria[0]}")
        while True:
            try:
                escolha = int(input("Digite o número da categoria: "))
                if escolha in self.categorias:
                    self.categoria, self.codigo_categoria = self.categorias[escolha]
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

    def input_numerico(self, mensagem):
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

    def selecionar_banco(self):
        while True:
            try:
                codigo_banco = int(input("Digite o código do banco: "))
                if codigo_banco in bancos:
                    nome_banco, _ = bancos[codigo_banco]
                    print(f"Selecionado banco: {nome_banco}")
                    return codigo_banco
                else:
                    print("Código inválido.")
            except ValueError:
                print("Código de banco inválido.")

    def selecionar_alteracao_valor(self):
        print("Deseja alterar o valor?")
        for numero, descricao in self.alterar_valor.items():
            print(f"{numero}: {descricao}")
        while True:
            try:
                escolha = int(input("Informe: "))
                if escolha in self.alterar_valor:
                    return escolha
                else:
                    print("Opção inválida.")
            except ValueError:
                print("Insira um número.")
    
    def executar_automacao(self):
        # Estrutura principal para automação
        print(f"Iniciando automação para {self.categoria}...")
        # Inicie o processo automatizado com as funções desenvolvidas...
    
    def comportamento_uma_parcela(self):
        # Código específico para uma parcela com encapsulamento dos cliques e preenchimentos
        self.pular_campos(5)
        self.aguardar_digitar("N° Fatura")
        self.notificar("Preenchimento concluído", "Para 1 parcela")
    
    def pular_campos(self, num):
        for _ in range(num):
            keyboard.press_and_release('tab')
    
    # Outras funções...
