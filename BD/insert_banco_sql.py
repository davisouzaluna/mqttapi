import json
import pymysql#precisa instalar a 
import time
import os


NOME_ARQUIVO=[('ultrassom.json')]#tupla com os nomes dos tópicos
caminho_do_diretorio = '../IOT/SUBSCRIBER-E-JSON'
#configurações do banco                                             
host_banco="localhost"
user_banco="root"
passwd_banco="root"
db_nome_banco="Reluz_API"
porta_banco = 3306
tempo_espera_insert=1


operacao_insert= "INSERT INTO monitoramento(mensagem,topico,qos) VALUES(%s, %s, %s)"#Não altere muito aqui, mas se alterar, verifique o laço for com os dados do json

for i in range(len(NOME_ARQUIVO)):
    caminho_do_arquivo = f'../IOT/{NOME_ARQUIVO[i]}'#percorre o array NOME_ARQUIVO
    
    #Verifica se o arquivo existe
    if os.path.exists(caminho_do_arquivo):
        
        
        #Conectar com o banco    
        conexao = pymysql.connect(host=host_banco,port=porta_banco, user=user_banco, passwd=passwd_banco, db=db_nome_banco)
        cursor = conexao.cursor()
        
        try:
            #inserir os dados do JSON a cada segundo
            while True:
                #abre o arquivo
                with open(caminho_do_arquivo) as f:
                    dados = json.load(f)#Carregar o arquivo json e guardar na variavel dados
                for dado in dados:
                    mensagem = dado['mensagem']
                    topico = dado['topico']
                    qos = dado['qos']
                    
                    #insert no BD
                    cursor.execute(operacao_insert,(mensagem,topico,qos))
                    
                    #confirmar a inserção
                    conexao.commit()
                time.sleep(tempo_espera_insert)
                
        except KeyboardInterrupt:
            
            conexao.close()#fecha a conexão
            print("\nConexão com o banco encerrada e programa fechado com sucesso\n")
            
        except Exception as e:
            
            conexao.close()
            print("\nOcorreu um erro: ",str(e))
                    
                
        
    else:
        print("O arquivo não existe")