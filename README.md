# CBFManager
Este projeto faz parte do trabalho prático da disciplina de **Banco de Dados** do curso de **Ciência da Computação** na **Universidade Federal de São João del-Rei (UFSJ)**. O objetivo é desenvolver um sistema para gerenciar e visualizar informações sobre o **Campeonato Brasileiro de Futebol 2023**, utilizando **MongoDB** como banco de dados e **Streamlit** para a interface web.

## 🎯 Funcionalidades  
- Cadastro de jogadores e equipes  
- Registro de partidas e estatísticas individuais  
- Consulta de informações sobre o campeonato  
- Interface amigável para administração e consulta  

## 🏗️ Tecnologias Utilizadas  
- **Python** 🐍  
- **Streamlit** 🎨 (Interface Web)  
- **MongoDB** 🗄️ (Banco de Dados NoSQL)  
- **Pymongo** 🔗 (Integração com MongoDB)  

## 📂 Estrutura do Projeto  
```
CBFManager/
│── app.py                  # Aplicação principal (Streamlit)
│── requirements.txt        # Dependências do projeto
│── config.py               # Configuração do MongoDB
│── database/
│   │── connection.py       # Conexão com MongoDB
│   │── models.py           # Modelos das entidades
│── modules/
│   │── jogadores.py        # Cadastro e consulta de jogadores
│   │── equipes.py          # Cadastro e consulta de equipes
│   │── jogos.py            # Cadastro e consulta de jogos
│   │── estatisticas.py     # Registro e consulta de estatísticas
```

## 🚀 Como Executar  
1 - Clone o repositório:  
```bash
git clone https://github.com/VitoReis/CBFManager.git
cd CBFManager
```
2 - Instale as dependências:  
```bash
pip install -r requirements.txt
```
3 - Inicie o MongoDB e rode o app:  
```bash
streamlit run app.py
```

## 📌 Sobre o Trabalho

📋 *O diagrama do banco de dados pode ser encontrado no arquivo CBFManager.drawio, utilize o site [draw.io](https://app.diagrams.net/) para visualiza-lo*

💡 *Este sistema foi projetado para ser facilmente adaptável a outros campeonatos e temporadas futuras!* ⚽📊

---