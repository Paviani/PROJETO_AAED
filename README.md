# PROJETO_AAED
Repositório contendo o projeto final da disciplina de Análise de Algoritmos e Estrutura de Dados

# Projeto Final de Análise de Algoritmo e Estrutura de Dados
“Análise e Visualização de Dados de Consumo de Água via IoT Utilizando Árvores AVL em Python”

## Descrição do Projeto

Este projeto visa simular o monitoramento do consumo de água em diferentes setores de um campus universitário. Utilizamos uma Árvore AVL para armazenar e organizar os dados de consumo de água de forma eficiente. Além disso, o projeto inclui uma interface de usuário desenvolvida com Streamlit para uma visualização mais intuitiva dos dados.

## Pré-requisitos

- Python 3.11
- Pip (Gerenciador de pacotes Python)

## Como Instalar

1. Clone o repositório para o seu computador local.
2. Navegue até o diretório do projeto.
3. Instale as dependências usando o comando abaixo:

```bash
pip install -r requirements.txt
```

## Como Executar

1. Navegue até o diretório onde o arquivo `coletor.py` está localizado.
2. Execute o comando:

```bash
streamlit run coletor.py
```

Isso iniciará o servidor Streamlit e abrirá uma nova janela no navegador com a interface do usuário.

## Estrutura do Projeto

- `coletor.py`: Script principal que contém toda a lógica e as estruturas de dados.
- `dados/`: Pasta contendo dados em formato CSV. (Que representa os dados ordenados pela árvore AVL dos payloads dos endpoints.)
- `dados_mqtt/`: Pasta contendo dados em formato JSON. (Que representa os payloads enviados pelos endpoints.)
- `requirements.txt`: Arquivo contendo todas as bibliotecas necessárias para executar o projeto.

## Funcionalidades

1. **Leitura dos Dados**: Lê os dados de consumo de água de arquivos JSON.
2. **Armazenamento dos Dados**: Armazena os dados em uma Árvore AVL.
3. **Visualização dos Dados**: Oferece uma interface de usuário para visualizar os dados.

## Autores

- João Antonio Resende Paviani

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
