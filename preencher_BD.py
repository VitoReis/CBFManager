import datetime
from database.connection import get_db
from database.models import get_collections
from bson import ObjectId

db = get_db()
collections = get_collections(db)

# CADASTRAR EQUIPES
def cadastrar_equipes():
    equipes = [
        {"nome": "Flamengo"},
        {"nome": "Palmeiras"},
        {"nome": "São Paulo"},
        {"nome": "Vasco da Gama"},
        {"nome": "Corinthians"}
    ]

    equipe_ids = {}
    for equipe in equipes:
        equipe_existente = collections["equipes"].find_one({"nome": equipe["nome"]})
        if not equipe_existente:
            result = collections["equipes"].insert_one(equipe)
            equipe_ids[equipe["nome"]] = result.inserted_id  # Armazena o ID da equipe
            print(f"Equipe {equipe['nome']} cadastrada com ID {result.inserted_id}!")
        else:
            equipe_ids[equipe["nome"]] = equipe_existente["_id"]
            print(f"Equipe {equipe['nome']} já existe com ID {equipe_existente['_id']}!")

    return equipe_ids


# CADASTRAR JOGADORES
def cadastrar_jogadores(equipe_ids):
    jogadores = [
        {"nome": "Gabigol", "equipe_id": equipe_ids["Flamengo"], "numero": 9},
        {"nome": "Dudu", "equipe_id": equipe_ids["Palmeiras"], "numero": 7},
        {"nome": "Pato", "equipe_id": equipe_ids["São Paulo"], "numero": 11},
        {"nome": "Talles Magno", "equipe_id": equipe_ids["Vasco da Gama"], "numero": 7},
        {"nome": "Jô", "equipe_id": equipe_ids["Corinthians"], "numero": 77}
    ]

    for jogador in jogadores:
        jogador_existente = collections["jogadores"].find_one(
            {"equipe_id": jogador["equipe_id"], "numero": jogador["numero"]})
        if not jogador_existente:
            collections["jogadores"].insert_one(jogador)
            print(f"Jogador {jogador['nome']} da equipe {jogador['equipe_id']} cadastrado!")
        else:
            print(f"Jogador {jogador['nome']} já existe!")


# CADASTRAR JOGOS
def cadastrar_jogos(equipe_ids):
    jogos = [
        {"data": str(datetime.date(2023, 3, 28)), "hora": "19:00", "local": "Maracanã",
         "equipe1_id": equipe_ids["Flamengo"], "equipe2_id": equipe_ids["Palmeiras"]},
        {"data": str(datetime.date(2023, 3, 29)), "hora": "21:00", "local": "Morumbi",
         "equipe1_id": equipe_ids["São Paulo"], "equipe2_id": equipe_ids["Corinthians"]},
        {"data": str(datetime.date(2023, 3, 30)), "hora": "20:00", "local": "São Januário",
         "equipe1_id": equipe_ids["Vasco da Gama"], "equipe2_id": equipe_ids["Flamengo"]},
    ]

    for jogo in jogos:
        jogo_existente = collections["jogos"].find_one(
            {"$or": [{"equipe1_id": jogo["equipe1_id"], "equipe2_id": jogo["equipe2_id"]},
                     {"equipe1_id": jogo["equipe2_id"], "equipe2_id": jogo["equipe1_id"]}]})
        if not jogo_existente:
            collections["jogos"].insert_one(jogo)
            print(f"Jogo entre {jogo['equipe1_id']} e {jogo['equipe2_id']} cadastrado!")
        else:
            print(f"Jogo entre {jogo['equipe1_id']} e {jogo['equipe2_id']} já existe!")


# CADASTRAR ESTATISTICAS
def cadastrar_estatisticas(jogadores, jogos):
    estatisticas = [
        {"jogo_id": jogos[0]['_id'], "jogador_id": jogadores[0]['_id'], "gols": 2, "cartoes": 0},
        {"jogo_id": jogos[1]['_id'], "jogador_id": jogadores[1]['_id'], "gols": 1, "cartoes": 1},
        {"jogo_id": jogos[2]['_id'], "jogador_id": jogadores[2]['_id'], "gols": 0, "cartoes": 2},
    ]

    for estatistica in estatisticas:
        estatistica_existente = collections["estatisticas"].find_one(
            {"jogo_id": estatistica["jogo_id"], "jogador_id": estatistica["jogador_id"]})
        if not estatistica_existente:
            collections["estatisticas"].insert_one(estatistica)
            print(f"Estatísticas de jogador {estatistica['jogador_id']} no jogo {estatistica['jogo_id']} registradas!")
        else:
            print(f"Estatísticas de jogador {estatistica['jogador_id']} no jogo {estatistica['jogo_id']} já existem!")


# MAIN
def preencher_bd():
    equipe_ids = cadastrar_equipes()
    jogadores = cadastrar_jogadores(equipe_ids)
    jogos = cadastrar_jogos(equipe_ids)

    jogadores = list(collections["jogadores"].find())
    jogos = list(collections["jogos"].find())

    cadastrar_estatisticas(jogadores, jogos)


if __name__ == "__main__":
    preencher_bd()
    print("Banco de dados populado com sucesso!")
