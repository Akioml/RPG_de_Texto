# npc.py

class Npc:
    def __init__(self, nome, raca, classe, fala_inicial=None, hostil=False, hp=100, ataque=30):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.fala_inicial = fala_inicial
        self.hostil = hostil
        self.hp = hp
        self.ataque = ataque

    def exibir_info(self):
        print(f"{self.nome}, o {self.classe} ({self.raca})")

    def esta_vivo(self):
        return self.hp > 0


def carregar_npcs():
    dados_npcs = [
        {
            "nome": "Alric",
            "raca": "Humano",
            "classe": "Mensageiro",
            "hostil": False
        },
        {
            "nome": "Thorne",
            "raca": "Humano",
            "classe": "Ladino",
            "hostil": True
        },

        {
            "nome": "Gisa",
            "raca": "Humano",
            "classe": "Arqueira",
            "hostil": True
        },

        {
            "nome": "Hloddoviko",
            "raca": "Humano",
            "classe": "Gurreiro",
            "hostil": True
        },

        {
            "nome": "Wilfred",
            "raca": "Humano",
            "classe": "Mago",
            "hostil": True
        }
    ]

    return {dados["nome"]: Npc(**dados) for dados in dados_npcs}
