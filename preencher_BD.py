import datetime
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId
import random

db = get_db()
collections = get_collections(db)


# CADASTRAR PESSOAS
def cadastrar_pessoas():
    pessoas = [
        {"login": "admin", "senha": "123", "tipo": "administrador"},
        {"login": "user", "senha": "123", "tipo": "usuario"},
    ]

    for pessoa in pessoas:
        pessoa_existente = collections["pessoas"].find_one({"login": pessoa["login"]})
        if not pessoa_existente:
            collections["pessoas"].insert_one(pessoa)
            print(f"Pessoa {pessoa['login']} cadastrada!")
        else:
            print(f"Pessoa {pessoa['login']} já existe!")


# CADASTRAR EQUIPES
def cadastrar_equipes():
    nomes_equipes = [
        "Flamengo",
        "Palmeiras",
        "São Paulo",
        "Vasco da Gama",
        "Corinthians",
        "Grêmio",
        "Internacional",
        "Cruzeiro",
        "Atlético-MG",
        "Bahia",
    ]
    for nome in nomes_equipes:
        equipe_existente = collections["equipes"].find_one({"nome": nome})
        if not equipe_existente:
            collections["equipes"].insert_one({"nome": nome})
            print(f"Equipe {nome} cadastrada!")
        else:
            print(f"Equipe {nome} já existe!")


# CADASTRAR JOGADORES
def cadastrar_jogadores():
    nomes_jogadores = [
        "Gabigol",
        "Dudu",
        "Pato",
        "Talles Magno",
        "Jô",
        "Suárez",
        "Alan Patrick",
        "Ronaldo",
        "Hulk",
        "Everton Ribeiro",
    ]
    equipes = list(collections["equipes"].find())
    jogadores = []

    for i, nome in enumerate(nomes_jogadores):
        equipe = equipes[i % len(equipes)]
        numero = random.randint(1, 99)
        jogador = {"nome": nome, "nome_equipe": equipe["nome"], "numero": numero}

        jogador_existente = collections["jogadores"].find_one(
            {"nome_equipe": jogador["nome_equipe"], "numero": jogador["numero"]}
        )
        if not jogador_existente:
            collections["jogadores"].insert_one(jogador)
            print(f"Jogador {nome} na equipe {equipe['nome']} cadastrado!")
        else:
            print(f"Jogador {nome} já existe!")

    return list(collections["jogadores"].find())


# CADASTRAR JOGOS
def cadastrar_jogos():
    locais = ["Maracanã", "Morumbi", "Mineirão", "Beira-Rio", "Fonte Nova"]
    equipes = list(collections["equipes"].find())
    jogos = []

    for i in range(10):
        e1, e2 = random.sample(equipes, 2)
        data = str(datetime.date(2023, 3, 20 + i))
        hora = f"{random.randint(16, 22)}:00"
        local = random.choice(locais)

        jogo = {
            "data": data,
            "hora": hora,
            "local": local,
            "nome_equipe1": e1["nome"],
            "nome_equipe2": e2["nome"],
        }

        jogo_existente = collections["jogos"].find_one(
            {
                "nome_equipe1": jogo["nome_equipe1"],
                "nome_equipe2": jogo["nome_equipe2"],
                "data": jogo["data"],
            }
        )
        if not jogo_existente:
            collections["jogos"].insert_one(jogo)
            print(f"Jogo {e1['nome']} x {e2['nome']} cadastrado!")
        else:
            print(f"Jogo entre {e1['nome']} e {e2['nome']} já existe!")

    return list(collections["jogos"].find())


# CADASTRAR ESTATÍSTICAS
def cadastrar_estatisticas(jogadores, jogos):
    estatisticas = []
    for i in range(10):
        jogador = random.choice(jogadores)
        jogo = random.choice(jogos)
        estatistica = {
            "jogo_id": jogo["_id"],
            "jogador_id": jogador["_id"],
            "gols": random.randint(0, 3),
            "cartoes": random.randint(0, 2),
        }

        estatistica_existente = collections["estatisticas"].find_one(
            {"jogo_id": estatistica["jogo_id"], "jogador_id": estatistica["jogador_id"]}
        )
        if not estatistica_existente:
            collections["estatisticas"].insert_one(estatistica)
            print(
                f"Estatística de {jogador['nome']} no jogo em {jogo['data']} cadastrada!"
            )
        else:
            print(f"Estatística de jogador já existe!")

    return


# MAIN
def preencher_bd():
    cadastrar_pessoas()
    cadastrar_equipes()
    jogadores = cadastrar_jogadores()
    jogos = cadastrar_jogos()
    cadastrar_estatisticas(jogadores, jogos)


if __name__ == "__main__":
    preencher_bd()
    print("Banco de dados populado com sucesso!")
