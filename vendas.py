from Celeiro.main import Main
import apoio
import inspect
import mysql.connector
cnx = mysql.connector.connect(user='root', password='Arte2573top', host='10.150.1.222', database='Celeiro')

class Vendas:
    def __init__(self) -> None:
        pass

    def venda(self,tabela="lanches",opt_produto=1,quantidade=1 ):
        apoio.clear()
        while opt_produto != 99 :    
            apoio.clear()
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
            
            tamanho = len(str(Main.total)) + 10
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
