import inspect
from logging import error
from random import expovariate
from re import T
import mysql.connector
cnx = mysql.connector.connect(user='root', password='Arte2573top', host='10.150.1.222', database='Celeiro')
from os import system, name
from time import sleep
from datetime import date
import math
import apoio


def clear():
    if name == 'int':
        _ = system('cls')
    else:
        _ = system('clear')

class Main:
    def __init__(self, rotina=0, opt=0, total={}):
        self.rotina = rotina
        self.opt = opt
        self.total = total
        

    def venda(self,tabela="lanches",opt_produto=1,quantidade=1 ):
        clear()
        while opt_produto != 99 :    
            clear()
            this_function_name = inspect.currentframe().f_code.co_name.upper()
            apoio.sublinha ("{} - {}".format(this_function_name,tabela))

# --------- CONEXÃO COM O BANCO DE DADOS
            query_vendas = cnx.cursor()
            query_vendas.execute("SELECT Nome FROM {}".format(tabela))
            resulta_nome = query_vendas.fetchall()
            query_vendas.execute("SELECT Valor FROM {}".format(tabela))
            resulta_valor = query_vendas.fetchall()
# --------- CARREGA PRODUTOS NA TELA
            for x in range (len(resulta_nome)):
                 nome_produto =  str(resulta_nome[x]).strip("(),'")
                 if x+1 > 9:
                    print (x+1, nome_produto.ljust(21), ' - R$'+str(resulta_valor[x]).strip(')(,'))
                 else:
                     print (x+1, nome_produto.ljust(22), ' - R$'+str(resulta_valor[x]).strip(')(,'))
            
            tamanho = len(str(self.total)) + 10
            if tamanho > 40:
                tamanho = 40
            apoio.sublinha("PEDIDO",40)

# --------- CARREGA TOTAL
            for item in self.total:
                print(f'{item:<15} R${self.total[item]["valor"]}   Unidades:{self.total[item]["qtd"]}')
                
            try:
                valor_compra = sum(d['total'] for d in self.total.values() if d)
                print ('TOTAL: {}'.format(round(valor_compra,2)))
            except:
                print("erro")

# --------- MOMENTO DA ESCOLHA 01 
            try:
                opt_produto = (int(input(f'\n- Digite o código  (99 para voltar,909 para fechar ):  ')) -1 )
            except:
                apoio.erro("Opção inexistente! Escolha um número válido.")
                self.venda()
            else:
                if opt_produto == 98:
                    self.inicio(0,valor_compra)
                if opt_produto == 908:
                    self.fecha_venda(valor_compra)

                elif opt_produto > len(resulta_nome) -1:
                    apoio.erro("Opcao fora da lista")
                    self.venda
                else:
                    nome = str(resulta_nome[opt_produto]).strip("(),'")
                    valor = float(str(resulta_valor[opt_produto ]).strip(')(,'))
                    try:
                        self.total[nome]['tabela'] = {tabela}
                        self.total[nome]['valor'] = round(valor,2)
                        self.total[nome]['qtd'] = self.total[nome].get('qtd', 1) + 1
                        self.total[nome]['total'] = round(self.total[nome].get('qtd',0) * self.total[nome].get('valor',0),2)

                    except :
                        
                        self.total[nome] = {}
                        self.total[nome]['valor'] = round(valor,1)
                        self.total[nome]['qtd'] = self.total[nome].get('qtd', 0) + 1
                        self.total[nome]['total'] = round(self.total[nome].get('qtd',0) * self.total[nome].get('valor',0),2)
                        self.total[nome]['tabela'] = {tabela}
                        
        #return (opt_produto, valor_compra)
    
    
    def fecha_venda(self,valor_compra=0):
        clear()
        this_function_name = inspect.currentframe().f_code.co_name.upper()
        apoio.sublinha(this_function_name)
        
        if  valor_compra:
            print('\nSegue listagem e valor total:\n')
            for produto in self.total:
                print(f'\033[0;37m > ({self.total[produto]["qtd"]}) {produto:<15}', ' R$',f'{self.total[produto]["valor"]}')
            print ("\033[1;33m TOTAL:                ","R$ "+str(round(valor_compra,2)))
        sleep(1.5)
        print ("_" * 40 )
        confirma = str(input(f'\033[0;33m* Fechar pedido?\n\033[3;37m(ok para confirmar, ENTER para cancelar): '))
        if confirma == "ok":
            try:
                seleciona = cnx.cursor(buffered=True)
                mysql_insert_vendas = f"INSERT INTO vendas (data,valor) VALUES (now(),{valor_compra}) "
                seleciona.execute(mysql_insert_vendas)
                cnx.commit()
                
                mysql_query_ultima_venda = "SELECT id_venda FROM vendas ORDER BY id_venda DESC LIMIT 1"
                seleciona.execute(mysql_query_ultima_venda)
                id_venda = seleciona.fetchall()
                id_venda = apoio.limpa_int(id_venda)
                
                
# -------------- Insere produtos vendidos             
                for item in self.total:
                    try:
                        tabela = (self.total[item]['tabela'])
                        tabela = str(tabela)
                        tabela = (tabela).strip("'' }{][")
                        query_produto_id = f'SELECT id FROM {tabela} where Nome="{item}"'
                        seleciona.execute(query_produto_id)
                        id_item = seleciona.fetchall()
                        qtd_item = (self.total[item]['qtd'])
                        #["{'lanches'}"]
                        id_item = apoio.limpa_int(id_item)
                        qtd_item = apoio.limpa_int(qtd_item) 
                        
                        print ("Inserindo pedido...")
                        #print("Qtd:", {qtd_item}, "Id item:", {id_item}, " Pedido Nº:",{id_venda}, "Tabela:",{tabela})
                        sleep(2)
                        insere_prod_vendidos =  f"INSERT INTO prod_vendidos (id, id_produto, quantidade) VALUES ({id_venda}, {id_item}, {qtd_item});"
                        seleciona.execute(insere_prod_vendidos)
                        cnx.commit()

                    except Exception as erro: 
                       print ("Deu ruim")
                       print (erro)
                       sleep(12)

                apoio.txt_cor(f"PEDIDO Nº {id_venda}\nConfirmado!!","verde")
                self.total = {}; valor_compra = 0; id_venda = 0; qtd_item = 0; id_item = 0; sleep(3)
                self.inicio(0)
            except Exception as erro:
                print(erro)
                sleep(60)
        else :
            self.venda()


    def exclui_pedido(self):
        self.total={}


    def inicio(self, opcao_inicio, valor_compra=0):
        clear()
        apoio.sublinha("MENU PRINCIPAL")
        try:
            if self.total:
                print('\n\033[1;32mPEDIDO EM ABERTO:\033[3;33m')
                for produto in self.total:
                   # print(f'\033[32m >{produto:<10}', ' R$',f'{self.total[produto]}')
                    print(f'\033[0;37m * ({self.total[produto]["qtd"]}) {produto:<15}', ' R$',f'{self.total[produto]["valor"]}')
                print(f'_____________________________\033[0;37m')
           
            opcao_inicio = int(input("\n 1  - Venda\n 2  - Cadastro de Produto\n 3  - Consulta\n 4  - Fechar pedido\n 5  - Excluir pedido \n 00 - Sair\n\n\033[33m  Escolha a opção: \033[37m"))
        
        except Exception as erro:
            apoio.erro(f'Código inválido 1 ** {erro}')
            self.inicio(0)
        
        else:
            clear()
            apoio.sublinha("Pedido")
            if opcao_inicio == 1:
                
                try:
                    opcao = int(input("\n 1 - Lanches\n 2 - Bebidas\n 3 - Combos\n\n\033[33m Escolha a opção:\033[37m " ))
                    if opcao == 1:
                        self.venda((str("lanches")))
                    elif opcao == 2:
                        self.venda(str("bebidas"))
                    elif opcao == 3:
                        self.consulta()

                    else:
                        print ("CAiu aqui no else")
                        sleep(3)
                except:
                    self.inicio(1)       

            elif opcao_inicio == 3:
                self.consulta()

            elif opcao_inicio == 4:
                self.fecha_venda(valor_compra)

            elif opcao_inicio == 5:
                if self.total:
                    apoio.txt_cor("   Pedido excluído!", "verde")
                    sleep(3)
                    self.exclui_pedido()
                    self.inicio(0)
                else:
                    self.inicio(0)
            else:
                apoio.erro("Opção inválida")
                self.inicio(0)


    def consulta_query (self, parametro):
        pass


    def consulta_menu (self, opt,data="2021-06-17"):
        hoje = date.today()
        switcher = {
                1: hoje,
                2: data,
                }
        return switcher.get(opt, "Opcao inválida")


    def consulta (self):
        clear()
        this_function_name = inspect.currentframe().f_code.co_name.upper()
        apoio.sublinha (this_function_name)

        
        try:
            opcao = int(input("\nSelecione a opção abaixo:\n\n 1 - Total hoje\n 2 - Total outra data\n\n>: "))
        except:
            apoio.erro("Incorreto")
        else:
            #consulta =f'SELECT  data, id_produto, quantidade, valor,id_venda FROM vendas INNER JOIN prod_vendidos \
                    #ON vendas.id_venda = prod_vendidos.id WHERE {self.consulta_menu(opcao)}'
            if opcao == int(2):
                dia = input("\nDigite a data (ex: ano/mês/dia 2021/06/17)>: ")
                consulta =f'SELECT valor  FROM vendas WHERE data="{dia}"'  
                seleciona = cnx.cursor(buffered=True)
                vendas = {}

            elif opcao == int(1):
                consulta =f'SELECT valor  FROM vendas WHERE data="{self.consulta_menu(opcao)}"'
                seleciona = cnx.cursor(buffered=True)
                vendas = {}
            
            seleciona.execute(consulta)
            resulta =  seleciona.fetchall()
            for i in range (len(resulta)):
                vendas[i] = (str(resulta[i]).strip(')(,'))
                vendas[i] = float(vendas[i])
            valores = vendas.values() 
            valor_final = round(math.fsum(valores),2)
            print (f"\n\033[0;33m TOTAL hoje ({self.consulta_menu(opcao)}): \033[1;33mR$ {valor_final} \n\n\033[0;37m")
            sleep(4)
            self.inicio(0)

clear()
opcao = Main()
opcao.inicio(0)
exit(0)