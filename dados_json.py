import json
import os

def verificar_ou_criar_json(caminho_json):
    if not os.path.exists(caminho_json):
        with open(caminho_json, 'w') as f:
            json.dump({}, f)

def carregar_pontuacao(caminho_json, nome_jogador):
    with open(caminho_json, 'r') as f:
        dados = json.load(f)

        return dados.get(nome_jogador, 0)  # Retorna 0 se o nome não estiver no JSON

def atualizar_pontuacao(caminho_json, nome_jogador, nova_pontuacao):
    with open(caminho_json, 'r') as f:
        dados = json.load(f)

    if nome_jogador in dados:
        if nova_pontuacao > dados[nome_jogador]:
            dados[nome_jogador] = nova_pontuacao
    else:
        dados[nome_jogador] = nova_pontuacao

    with open(caminho_json, 'w') as f:
        json.dump(dados, f, indent=4)
def load_ranking_from_json():
    try:
        with open('pontuacoes.json', 'r') as file:
            data = json.load(file)
        # Ordenar o ranking pela pontuação (maior para menor)
        ranking = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return ranking
    except FileNotFoundError:
        return []