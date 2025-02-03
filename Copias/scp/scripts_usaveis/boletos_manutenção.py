import os
from PIL import Image
from botcity.core import DesktopBot
import pyautogui as py
import keyboard
from plyer import notification  # Para enviar notificações
import time
import threading
from bancos_e_funções import bancos
from bancos_e_funções import comportamento_2_parcelas


class Bot(DesktopBot):
    reiniciar_solicitado = False  # Variável para evitar múltiplos reinícios
    
    def __init__(self):
        super().__init__()
        if not hasattr(self, 'monitorando_teclas'):
            self.monitorando_teclas = True
            threading.Thread(target=self.monitorar_teclas, daemon=True).start()
        
        
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
            15: ("Despesas com Alimentação - Curitiba", "4.2.9.15")
           
            }
        


        self.alterar_valor = {
            1: ("Não"),
            2: ("Sim")
        }

        self.esquema_boleto = {
            1: ("Não"),
            2: ("Sim")
        }
         
        #self.valor_total = None
        self.categoria = None
        self.parcelas = None
        self.banco = None
        self.nome_banco = None
        self.alterar = None
        self.escolha = None
        self.esquema = None
        self.total = 0.0
        
        while True:
            self.iniciar()
        
    def iniciar(self):
    #    # Capturar informações iniciais
    #    self.valor_total = input("Digite o valor total: ")
        
        #self.valor_total = None
        self.categoria = None
        self.parcelas = None
        self.banco = None
        self.nome_banco = None
        self.alterar = None
        self.escolha = None
        self.esquema = None
        self.mesma_data = None
        self.total = 0
        
        #print("Precisa somar os valores?")
        #for numero, opcao in self.esquema_boleto.items():
        #    print(f"{numero}: {opcao}")
        #while True:
        #    
        #    try:
        #        escolha_sim_nao = int(input("Informe 1 para Não e 2 para Sim: "))
        #        if escolha_sim_nao in self.esquema_boleto:
        #            if escolha_sim_nao == 2:  # Se escolher "Sim"
        #                self.comportamento_somar()
        #            else:  # Se escolher "Não"
        #                self.comportamento_nao_somar()
        #            break
        #        else:
        #            print("Opção inválida. Tente novamente.")
        #    except ValueError:
        #        print("Entrada inválida. Por favor, insira um número.")
        
        # Mostrar as categorias disponíveis
        print("Selecione o tipo de lançamento:")
        for numero, categoria in self.categorias.items():
            print(f"{numero}: {categoria}")
        
        # Capturar a escolha da categoria
        while True:
            self.click_at(605, 1062)
            try:
                self.escolha = int(input("Digite o número da categoria: "))
                if self.escolha in self.categorias:
                    self.categoria, self.codigo_categoria = self.categorias[self.escolha]
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        
        self.parcelas = int(input("Digite o número de parcelas: "))
        #self.banco = int(input("Digite o código de identificação do Banco: "))
        
        codigo_banco = int(input("Digite o código de identificação do banco: "))
        
        if self.parcelas != 1:
            print("Precisa Alterar o valor?")
            for numero, self.alterar in self.alterar_valor.items():
                print(f"{numero}: {self.alterar}")
            while True:
                try:
                    escolha_sim_nao = int(input("Informe: "))
                    if escolha_sim_nao in self.alterar_valor:
                        self.alterar_valor  = self.alterar_valor[escolha_sim_nao]
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                except ValueError:
                    print("Entrada inválida. Por favor, insira um número.")
        
        #FAZER SCRIPT PARA REALIZAR SOMA DAS PARCELAS, TANTO EM PARCELADO E ESQUEMA DE BOLETOS
        
        
        
        # Verificar se o código existe no dicionário
        if codigo_banco in bancos:
            self.nome_banco, _ = bancos[codigo_banco]
            self.codigo_banco = codigo_banco
            print(f"Iniciando script para {self.categoria} com {self.parcelas} parcela(s) no Banco {self.nome_banco}")
            
        else:
            print("Código de banco inválido!")
        
        
        # Iniciar a automação
        self.executar_automacao()

    def executar_automacao(self):
        
        if self.reiniciar_solicitado:
            self.reiniciar_solicitado = False
            print("Reiniciando o script...")
            self.reiniciar_estado()
                # Reinicia o loop principal
            
        print("Iniciando nova iteração do loop.")
        self.wait(2000)  # Espera de 2 segundos


        # Primeiro clique e espera de 3 segundos
        self.click_at(1003, 114)
        print("Clique realizado na posição (1003, 114).")
        self.notificar("Clique realizado", "Posição (1003, 114)")
        self.wait(3000)
            
            # Clique no campo e aguarda o texto ser inserido
        self.click_at(615,269)
        self.click_at(615,269)
        # Verifica se self.total está definido corretamente
        if self.total > 0:  # Verifica se total é positivo
            keyboard.write(str(self.total))  # Aguarda inserção de número
        else:
            print("Valor total não definido ou inválido.")
        self.aguardar_tecla_insert("Etapa 1")  # Aguarda tecla Insert
        print("Esperando após digitar o Valor.")
        self.notificar("Esperando", "Após digitar o valor")
            
        # Aguardar digitação de texto e Insert para a "Categoria"
        keyboard.press_and_release('tab')
        
        # Preenche somente o código se existir, senão preenche o nome
        if self.codigo_categoria:
            keyboard.write(self.codigo_categoria)  # Preenche só o código
        else:
            keyboard.write(self.categoria)  # Preenche o nome
        
        
        
        #for caractere in categoria_nome:
        #    keyboard.write(caractere)  # Digita cada caractere no campo de texto

        # Cole o nome da categoria no campo de texto
        #keyboard.write(categoria_nome)
    
        ############### PROBLEMAS COM NOME DUPLICADO NA CATEGORIA ################
        # Note:: De uma forma misteriosa o problema foi resolvido, dessa forma acredito
        # que nao é mais nescessario clicar insert na etapa 2.
        self.aguardar_tecla_insert("Etapa 2")
        print("Esperando após digitar a categoria.")
        self.notificar("Esperando", "Após digitar o categoria")
            
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

        #self.aguardar_tecla_insert("Etapa 3")
        #print("Tecla 'Insert' pressionada.")
            
        self.click_at(825, 306)
        #self.click_at(825, 306)
            
        # Pular campos com Tab
        for _ in range(4):
            keyboard.press_and_release('tab')
            
        # NFe e próxima etapa
        self.aguardar_digitar("Numero NFe")
        self.aguardar_tecla_insert("Etapa 4")
        print("Esperando após digitar a NFe.")
        self.notificar("Esperando", "Após digitar o NFe")
            
        # Continuar navegação com Tab
        for _ in range(3):
            keyboard.press_and_release('tab')
        print("Tecla 'Tab' pressionada após 'NFe'.")
            
        # Aguardar texto do Fornecedor
        self.aguardar_digitar_texto("Fornecedor")
        self.click_at(1544, 538)
        self.aguardar_tecla_insert("Etapa 5")
        print("Esperando após digitar o Fornecedor.")
        self.notificar("Esperando", "Após digitar o Fornecedor")
            
        self.click_at(1544, 538)
        self.click_at(1544, 538)
            
        #ação da visao computacional pra dar dois cliques no botao.png
            
        # Tab para pular campos e depois inserir número de parcelas
        for _ in range(3):
            keyboard.press_and_release('tab')
        print("Tecla 'Tab' pressionada após 'Fornecedor'.")
        self.wait(1)
        
        #self.aguardar_digitar("N° Parcelas")
        self.paste(str(self.parcelas))
        #self.aguardar_tecla_insert("Etapa 6")
        #print("Esperando após digitar a N° Parcelas.")
        #self.notificar("Esperando", "Após digitar o N° Parcelas")
            
        # Preencher campos e aguardar outros inputs
        keyboard.press_and_release('tab')
        self.paste("BOLETO")
        keyboard.press_and_release('tab')
            
        self.paste(str(self.codigo_banco))
        #self.aguardar_tecla_insert("Etapa 7")
        #print("Esperando após digitar o Banco.")
        #self.notificar("Esperando", "Após digitar o Banco")
        
        # Tab e preenchimento do campo Mensal
        keyboard.press_and_release('tab')
        print("Tecla 'Tab' após o banco.")
        self.notificar("Tecla 'Tab' pressionada", "Após o banco")
        self.wait(1)
            
        self.paste("Mensal")
        keyboard.press_and_release('tab')
            
        # Vencimento e aguardar tecla Insert
        self.aguardar_digitar("Vencimento")
        self.aguardar_tecla_insert("Etapa 8")
        print("Esperando após digitar o Vencimento.")
        self.notificar("Esperando", "Após digitar o Vencimento")
        keyboard.press_and_release('tab')
        keyboard.press_and_release('tab')
        keyboard.press_and_release('enter')
        
        
        
            
        #keyboard.press_and_release('tab')
        #keyboard.press_and_release('tab')
        #keyboard.press_and_release('tab')
        #keyboard.press_and_release('tab')
        #keyboard.press_and_release('tab')
        
    def definir_comportamento(self):
        comportamentos = {
                1: self.comportamento_uma_parcela,
                2: self.comportamento_2_parcelas,
                3: self.comportamento_3_parcelas,
                4: self.comportamento_4_parcelas,
                5: self.comportamento_5_parcelas,
                6: self.comportamento_6_parcelas,
            }
        comportamento = comportamentos.get(self.parcelas, self.comportamento_multiplas_parcelas)
        comportamento()
            
    def comportamento_uma_parcela(self):
        
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
            
        self.click_at(1320, 738)
        self.click_at(1320, 738)
        self.aguardar_digitar("Data")
        self.aguardar_tecla_insert("Etapa 8-1")
        print("Esperando após digitar a Data.")
        self.notificar("Esperando", "Após digitar a Data")
    
        # **Novo código: Fechar e salvar após digitar a Data**
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
    

    

    

    def comportamento_nao_somar(self):
        print(" ")
        
    def comportamento_para_sim(self):
        
        #Ir para N° Documento
        for n in range (3):
            keyboard.press_and_release('tab')
        
        self.click_at(951, 737)
        self.click_at(951, 737)
        py.press('right')
        self.aguardar_digitar("Alteração de Valor 1")
        
        self.click_at(944, 765)
        self.click_at(944, 765)
        py.press('right')
        self.aguardar_digitar("Alteração de Valor 2")
        self.aguardar_tecla_insert("Etapa 8-1-1")
        
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

    # Funções de espera e interação
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

    def reiniciar_estado(self):
        print("Resetando estado do bot.")
        self.wait(1)

    def paste(self, text):
        py.write(text)

    def wait(self, milliseconds):
        time.sleep(milliseconds / 1000)
        
    def notificar(self, titulo, mensagem):
        notification.notify(
            title=titulo,
            message=mensagem,
            timeout=2
        )

if __name__ == "__main__":
    try:
        bot = Bot()
        bot.iniciar()  # Garanta que o método correto seja chamado
    except Exception as e:
        print(f"Ocorreu um erro: {e}")






    #def comportamento_uma_parcela(self):
    #    print("Executando comportamento para 1 parcela.")
    #    # Adicione aqui o que o script deve fazer com 1 parcela
    #    self.finalizar_processamento()

    #def comportamento_multiplas_parcelas(self):
    #    print(f"Executando comportamento para {self.parcelas} parcelas.")
    #    # Adicione aqui o que o script deve fazer com múltiplas parcelas
    #    self.finalizar_processamento()

    #def finalizar_processamento(self):
    #    # Finaliza a automação com base nas etapas de comportamento
    #    self.click_at(1447, 204)
    #    print("Processamento finalizado.")
    #    self.notificar("Finalizado", "Lançamento completo.")



# Funções Utilitárias
    # ------------------------
    
    #def comportamento_somar(self):
    #    
    #    total = 0  # Inicializa o total como 0
#
    ## Pergunta se os boletos têm a mesma data
    #    mesma_data = input("Os boletos têm a mesma data? (s/n): ").strip().lower()
#
    ## Verifica se a entrada é válida
    #    if mesma_data not in ['s', 'n']:
    #        print("Entrada inválida. Por favor, digite 's' para sim ou 'n' para não.")
    #        return  # Sai da função se a entrada for inválida, mas não deveria sair aqui em entradas corretas
#
    ## Pergunta quantas somas serão feitas
    #    while True:
    #        try:
    #            qtd_somas = int(input("Quantas somas serão feitas? "))
    #            break  # Se for uma entrada válida, sai do loop
    #        except ValueError:
    #            print("Entrada inválida. Por favor, insira um número válido.")
#
    ## Captura os valores que serão somados
    #    for i in range(qtd_somas):
    #        while True:
    #            try:
    #                valor = float(input(f"Digite o valor {i + 1}: "))
    #                total += valor  # Adiciona o valor ao total
    #                break
    #            except ValueError:
    #                print("Entrada inválida. Por favor, insira um valor numérico.")
#
    ## Exibe o total somado
    #    print(f"Total somado: {total}")
    #
    ## Aqui você pode adicionar a funcionalidade para colar o valor no campo, se necessário
    ## self.paste_total(total)
    #    return total  # Retorna o total se precisar usá-lo em outro lugar

