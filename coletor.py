# Importando os módulos necessários
import os
import json
import csv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

cod_inicio = time.time()
# print("Diretório atual:", os.getcwd())

# Caminho absoluto para a pasta 'dados'
caminho_pasta_dados = 'dados'

# Verifica se a pasta 'dados' existe. Se não, cria a pasta. teste2
if not os.path.exists(caminho_pasta_dados):
    os.makedirs(caminho_pasta_dados)

# Caminho para o diretório que contém os arquivos
diretorio = 'dados_mqtt'

# Listar todos os arquivos no diretório
arquivos = os.listdir(diretorio)

# Filtrar apenas os arquivos JSON
arquivos_json = [f for f in arquivos if f.endswith('.json')]


# Classe para representar os nós da árvore AVL
class No:
    def __init__(self, timestamp, dado):
        self.esquerda = None
        self.direita = None
        self.timestamp = timestamp
        self.dado = dado
        self.altura = 1

# Função para inserir um novo nó na árvore AVL
def inserir_no(raiz, timestamp, dado):
    if raiz is None:
        return No(timestamp, dado)
    else:
        if timestamp < raiz.timestamp:
            raiz.esquerda = inserir_no(raiz.esquerda, timestamp, dado)
        else:
            raiz.direita = inserir_no(raiz.direita, timestamp, dado)
    
    raiz.altura = 1 + max(altura(raiz.esquerda), altura(raiz.direita))
    return balancear(raiz)

# Função para obter a altura de um nó
def altura(no):
    if no is None:
        return 0
    return no.altura

# Função para balancear um nó na árvore AVL
def balancear(no):
    if no is None:
        return no

    balanceamento = altura(no.esquerda) - altura(no.direita)

    # Rotação Simples à Direita
    if balanceamento > 1:
        if no.timestamp < no.esquerda.timestamp:
            return rotacao_direita(no)

    # Rotação Simples à Esquerda
    if balanceamento < -1:
        if no.timestamp > no.direita.timestamp:
            return rotacao_esquerda(no)

    return no

# Função para realizar a rotação simples à direita
def rotacao_direita(y):
    x = y.esquerda
    T = x.direita

    x.direita = y
    y.esquerda = T

    y.altura = 1 + max(altura(y.esquerda), altura(y.direita))
    x.altura = 1 + max(altura(x.esquerda), altura(x.direita))

    return x

# Função para realizar a rotação simples à esquerda
def rotacao_esquerda(x):
    y = x.direita
    T = y.esquerda

    y.esquerda = x
    x.direita = T

    x.altura = 1 + max(altura(x.esquerda), altura(x.direita))
    y.altura = 1 + max(altura(y.esquerda), altura(y.direita))

    return y

# Função para realizar a travessia "in-order" na árvore e armazenar os nós em uma lista
def travessia_inorder(raiz, resultado):
    if raiz:
        travessia_inorder(raiz.esquerda, resultado)
        resultado.append(raiz.dado)
        travessia_inorder(raiz.direita, resultado)

# Função para ler um arquivo JSON
def ler_arquivo_json(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return json.load(f)

# Função para gerar um arquivo CSV a partir dos dados ordenados
def gerar_csv(dados_ordenados):
    cabecalho = ['devAddr', 'timestamp', 'setor', 'valorAgua']
    with open(os.path.join(caminho_pasta_dados, 'dados_ordenados.csv'), 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(cabecalho)
        for dado in dados_ordenados:
            escritor.writerow([dado['devAddr'], dado['timestamp'], dado['setor'], dado['valorAgua']])

# Inicializando a árvore AVL
raiz = None

# Leitura de vários arquivos JSON e inserção na árvore AVL
for nome_arquivo in arquivos_json:
    caminho_completo = os.path.join(diretorio, nome_arquivo)
    try:
        dado = ler_arquivo_json(caminho_completo)
        timestamp = dado['timestamp']
        raiz = inserir_no(raiz, timestamp, dado)
    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
    except json.JSONDecodeError:
        print(f"O arquivo {nome_arquivo} não é um JSON válido.")

# Realizando a travessia in-order e armazenando os dados em uma lista
dados_ordenados = []
travessia_inorder(raiz, dados_ordenados)

# Gerando o arquivo CSV
gerar_csv(dados_ordenados)

# Função para gerar um arquivo CSV a partir dos dados ordenados
def gerar_csv(dados_ordenados, nome_arquivo):
    cabecalho = ['devAddr', 'timestamp', 'setor', 'valorAgua']
    with open(os.path.join(caminho_pasta_dados, nome_arquivo), 'w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(cabecalho)
        for dado in dados_ordenados:
            escritor.writerow([dado['devAddr'], dado['timestamp'], dado['setor'], dado['valorAgua']])

# Gerando o arquivo CSV
gerar_csv(dados_ordenados, 'dados_ordenados.csv')

# Carregar os dados do CSV
# @st.cache_data  # Esta linha melhora o desempenho ao ler o arquivo apenas uma vez
def load_data():
    return pd.read_csv("dados/dados_ordenados.csv")

# Carregar os dados pela primeira vez
df = load_data()
    

# Botão para recarregar dados
if st.button('Recarregar Dados'):
    df = load_data() 

# Título da página
st.title("Análise de Consumo de Água")

# Mostrar os dados brutos em uma tabela
st.write("Dados brutos:")
st.write(df)

# Criar um gráfico de barras para o consumo de água por setor
st.write("Gráfico de Consumo de Água por Setor:")
fig1, ax1 = plt.subplots()
df.groupby("setor")["valorAgua"].sum().plot(kind='bar', ax=ax1)
ax1.set_ylabel("Consumo de Água")
st.pyplot(fig1)

# Criar um gráfico de pizza para o consumo de água por setor
st.write("Gráfico de Pizza de Consumo de Água por Setor:")
fig2, ax2 = plt.subplots()
df.groupby("setor")["valorAgua"].sum().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2)
ax2.axis('equal')  # Manter a proporção de aspecto igual garante que o gráfico de pizza seja desenhado como um círculo.
st.pyplot(fig2)

cod_fim = time.time()

#Calculando tempo de execução do código:
tempo_execucao = cod_fim - cod_inicio
print(f'Tempo de execução de {tempo_execucao}')