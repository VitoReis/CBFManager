def get_collections(db):
    return {
        "jogadores": db["jogadores"],
        "equipes": db["equipes"],
        "jogos": db["jogos"],
        "estatisticas": db["estatisticas"],
        "pessoas": db["pessoas"],
    }
