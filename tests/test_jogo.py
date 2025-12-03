import pytest

from codigo.jogo import primeiro_capitulo, confronto_mercenario
from codigo.jogo import mostrar_inimigos
from codigo.jogo import turno_jogador
from codigo.jogo import grupo_vivo
from codigo.personagem import Personagem, personagens
from codigo.grupo import criar_grupo
from codigo.jogo import turno_inimigos
from codigo.jogo import turno_combate
from codigo.jogo import iniciar_combate
from codigo.jogo import iniciar_jogo, carregar_npcs


from codigo.npc import Npc
from codigo.npc import carregar_npcs

@pytest.fixture
def grupo_de_teste():
    return  [
        Personagem("Luna", "Elfa", "1.75", "120", "Arqueira", 20),
        Personagem("Tharn", "Anão", "1.40", "200", "Guerreiro", 20),
        Personagem("Elric", "Humano", "1.80", "35", "Paladino", 18)
    ]

@pytest.fixture
def npcs_de_testes():
    return {
        "Alric": Personagem("Alric", "Humano", "1.70", "30", "Mensageiro", 5),
        "Thorne": Personagem("Thorne", "Orc", "2.00", "40", "Guerreiro", 25),
        "Gisa": Personagem("Gisa", "Humana", "1.65", "28", "Assassina", 22),
        "Hloddoviko": Personagem("Hloddoviko", "Anão", "1.30", "180", "Bárbaro", 23),
        "Wilfred": Personagem("Wilfred", "Humano", "1.85", "45", "Ladino", 21)
    }

@pytest.fixture
def inimigos_teste():
    return {
        "Thorne": Personagem("Thorne", "Orc", "2.00", "40", "Guerreiro", 25),
        "Gisa": Personagem("Gisa", "Humana", "1.65", "28", "Assassina", 22),
        "Hloddoviko": Personagem("Hloddoviko", "Anão", "1.30", "180", "Bárbaro", 23),
        "Wilfred": Personagem("Wilfred", "Humano", "1.85", "45", "Ladino", 21)
    }

def test_vericando_se_o_grupo_foi_criado_corretamente(grupo_de_teste):
    personagens.clear()
    personagens.extend(grupo_de_teste)

    resultado = criar_grupo()

    assert resultado == grupo_de_teste
    assert len(resultado) == 3
    assert all(isinstance(p, type(grupo_de_teste[0])) for p in resultado)

def test_criar_grupo_sem_personagens(capsys):
    personagens.clear()

    resultado = criar_grupo()

    captured = capsys.readouterr()

    assert resultado is None
    assert "Nenhum personagem foi criado" in captured.out

def test_verificar_se_o_grupo_esta_vivo(grupo_de_teste):
    entrada = grupo_vivo(grupo_de_teste)

    esperado = True

    assert esperado == entrada


def test_mostra_se_os_inimigos_carregaram_normalmente(capsys, inimigos_teste):
    mostrar_inimigos(inimigos_teste)

    captured = capsys.readouterr()
    saida = captured.out

    for nome in inimigos_teste:
        assert nome in saida

def test_turno_jogador_com_ataque(monkeypatch, capsys,grupo_de_teste,inimigos_teste):
    grupo = grupo_de_teste
    inimigos = inimigos_teste

    monkeypatch.setattr("builtins.input", lambda _: "1")

    inimigos_restantes = turno_jogador(grupo, inimigos)

    saida = capsys.readouterr().out

    assert "Turno de" in saida
    assert "ataca" in saida

def test_turno_inimigo_com_ataque(monkeypatch, capsys,grupo_de_teste,inimigos_teste):
    grupo = grupo_de_teste
    inimigos = inimigos_teste

    monkeypatch.setattr("builtins.input", lambda _: "1")

    herois_restantes = turno_inimigos(grupo, inimigos)

    saida = capsys.readouterr().out

    assert any(npc.nome in saida for npc in inimigos.values())

    # Verifique se algum personagem do grupo recebeu dano
    assert any(heroi.nome in saida for heroi in grupo)

def test_personagem_morto_nao_joga(capsys, monkeypatch):
    vivo = Personagem("Herói", 'Anão', 1.90, 52, 'Mago', 60, 100)
    morto = Personagem("Zumbi", 'Humano', 1.60, 30, 'Nenhuma', 20, 0)

    grupo = [vivo, morto]
    inimigos = {"Alric": Personagem("Alric", "Humano", 1.70, 30, "Gurreiro", 5, 100)}

    monkeypatch.setattr('builtins.input', lambda _: "1")

    turno_jogador(grupo, inimigos)

    captured = capsys.readouterr()

    assert "Turno de Herói" in captured.out
    assert "Herói ataca Alric" in captured.out

def test_turno_jogador_sem_inimigos_vivo(monkeypatch,capsys,grupo_de_teste):
    inimigos = {
        "A": Personagem("A", "Humano", 1.7, 30, "Guerreiro", 5, 0),
        "B": Personagem("B", "Elfo", 1.8, 120, "Arqueiro", 6, 0),
    }

    monkeypatch.setattr('builtins.input',lambda _: 1)

    resultado = turno_jogador(grupo_de_teste,inimigos)
    capture = capsys.readouterr()

    assert resultado == {}
    assert "Turno de" in capture.out
    assert "ataca" not in capture.out

def test_inimigo_derrotado_com_sobra_de_dano(monkeypatch, capsys):
    heroi = Personagem("Herói", "Humano", 1.80, 30, "Guerreiro", ataque=12, hp=100)
    grupo = [heroi]

    inimigo = Personagem("Goblin", "Criatura", 1.30, 20, "Ladrão", ataque=5, hp=10)
    inimigos = {"Goblin": inimigo}

    monkeypatch.setattr("builtins.input", lambda _: "1")

    resultado = turno_jogador(grupo, inimigos)
    captured = capsys.readouterr()

    assert "Herói ataca Goblin causando 12 de dano!" in captured.out
    assert "Goblin foi derrotado!" in captured.out
    assert resultado == {}

    # Como ele foi derrotado, não deve aparecer nos inimigos restantes
    assert resultado == {}

def test_turno_combate_grupo_vence(monkeypatch,capsys):
    heroi = Personagem("Herói", "Anão", 1.80, 50, "Guerreiro", 999, 100)  # Ataque muito alto
    grupo = [heroi]

    # Cria inimigos com pouca vida
    inimigo1 = Personagem("Goblin", "Criatura", 1.30, 20, "Ladrão", 0, 1)
    inimigo2 = Personagem("Orc", "Criatura", 2.00, 100, "Bruto", 0, 1)
    inimigos = {"Goblin": inimigo1, "Orc": inimigo2}

    monkeypatch.setattr('builtins.input',lambda _: "1")

    turno_combate(grupo,inimigos)

    saida = capsys.readouterr().out

    assert "Rodada 1 " in saida
    assert "Seu grupo venceu!" in saida

def test_turno_combate_inimigos_venceram(monkeypatch,capsys):
    heroi = Personagem("Herói", "Anão", 1.80, 50, "Guerreiro", 1, 1)  # Ataque muito alto
    grupo = [heroi]

    # Cria inimigos com pouca vida
    inimigo1 = Personagem("Goblin", "Criatura", 1.30, 20, "Ladrão", 50, 100)
    inimigo2 = Personagem("Orc", "Criatura", 2.00, 100, "Bruto", 100, 100)
    inimigos = {"Goblin": inimigo1, "Orc": inimigo2}

    monkeypatch.setattr('builtins.input',lambda _: "1")

    turno_combate(grupo,inimigos)

    saida = capsys.readouterr().out

    assert "Rodada 1 " in saida
    assert "Seu grupo foi derrotado!" in saida

def test_turno_combate_limite_de_rodadas(monkeypatch, capsys):
    heroi = Personagem("Herói", "Anão", 1.80, 50, "Guerreiro", 1, 1000)
    grupo = [heroi]

    inimigo = Personagem("Dragão", "Criatura", 10.0, 1000, "Boss", 1, 1000)
    inimigos = {"Dragão": inimigo}

    monkeypatch.setattr('builtins.input', lambda _: "1")

    turno_combate(grupo, inimigos)

    saida = capsys.readouterr().out
    assert "Rodada 10" in saida


def test_escolhendo_a_opcao_errada_e_perdendo_o_turno(capsys, monkeypatch,grupo_de_teste,inimigos_teste):
    monkeypatch.setattr('builtins.input', lambda _: "5")

    turno_jogador(grupo_de_teste,inimigos_teste)

    capture = capsys.readouterr()

    assert "Escolha inválida. Perdendo turno." in capture.out

def test_inimigo_morreu(capsys, monkeypatch):
    vivo = Personagem("Herói", 'Anão', 1.90, 52, 'Mago', 60, 1000)

    grupo = [vivo]
    inimigos = {"Eliot": Personagem("Eliot", "Humano", 1.70, 30, "Guerreiro", 5, 1)}  # Nome e chave batendo

    monkeypatch.setattr('builtins.input', lambda _: "1")

    turno_jogador(grupo, inimigos)

    captured = capsys.readouterr()

    assert "Turno de Herói" in captured.out
    assert "Herói ataca Eliot" in captured.out
    assert "Eliot foi derrotado!"


def test_escolhando_a_primeira_escolha_ajudar_cobrando(monkeypatch,grupo_de_teste,npcs_de_testes):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    from codigo import jogo
    jogo.confronto_mercenario = lambda g, i, n: print('Combate Simulado')

    primeiro_capitulo(grupo_de_teste,npcs_de_testes)

    assert grupo_de_teste[0].nome == 'Luna'
    assert npcs_de_testes["Thorne"].nome == 'Thorne'



def test_escolhendo_a_segunda_escolha_Ajudar_por_honra(monkeypatch,grupo_de_teste, npcs_de_testes):
    monkeypatch.setattr('builtins.input', lambda _: '2')

    from codigo import jogo
    jogo.confronto_mercenario = lambda g, i, n: print('Combate Simulado')

    primeiro_capitulo(grupo_de_teste, npcs_de_testes)

    assert grupo_de_teste[0].nome == 'Luna'
    assert npcs_de_testes["Thorne"].nome == 'Thorne'


def test_escolhendo_a_terceira_escolha_ignorar_e_voltar_a_beber(monkeypatch,grupo_de_teste, npcs_de_testes):
    monkeypatch.setattr('builtins.input', lambda _: '3')

    from codigo import jogo
    jogo.confronto_mercenario = lambda g, i, n: print('Combate Simulado')

    primeiro_capitulo(grupo_de_teste, npcs_de_testes)

    assert grupo_de_teste[0].nome == 'Luna'
    assert npcs_de_testes["Thorne"].nome == 'Thorne'


def test_combate_iniciado(monkeypatch,capsys,grupo_de_teste,npcs_de_testes):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    from codigo import jogo
    jogo.turno_combate = lambda g, i: print("Combate simulado")

    jogo.iniciar_combate(grupo_de_teste, list(npcs_de_testes.values())[:2])

    saida = capsys.readouterr().out

    assert "COMBATE INICIADO" in saida
    assert "Seu grupo enfrenta os mercenários em um confronto feroz!" in saida
    assert "--- Seu Grupo ---" in saida
    assert "--- Inimigos ---" in saida

def test_confronto_negociar_oferecer_ouro(monkeypatch, capsys, grupo_de_teste, inimigos_teste, npcs_de_testes):
    entradas = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    confronto_mercenario(grupo_de_teste, inimigos_teste, npcs_de_testes)

    saida = capsys.readouterr().out.lower()
    assert "levanta as mãos" in saida
    assert "talvez isso convença vocês" in saida or "temos ouro" in saida
    assert grupo_de_teste[0].mochila["ouro"] < 50 + 50

def test_confronto_atacar(monkeypatch, capsys, grupo_de_teste, inimigos_teste, npcs_de_testes):
    monkeypatch.setattr("builtins.input", lambda _: "2")
    from codigo import jogo
    jogo.iniciar_combate = lambda g, i: print("COMBATE SIMULADO")

    confronto_mercenario(grupo_de_teste, inimigos_teste, npcs_de_testes)
    saida = capsys.readouterr().out
    assert "puxa as armas" in saida.lower()
    assert "combate simulado" in saida.lower()

def test_confronto_fugir(monkeypatch, capsys, grupo_de_teste, inimigos_teste, npcs_de_testes):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    from codigo import jogo
    jogo.iniciar_combate = lambda g, i: print("COMBATE SIMULADO")

    confronto_mercenario(grupo_de_teste, inimigos_teste, npcs_de_testes)
    saida = capsys.readouterr().out
    assert "enviados do lorde varkan" in saida.lower()
    assert "combate simulado" in saida.lower()

def test_primeiro_capitulo_escolha_1_mensagem_final(monkeypatch, capsys, grupo_de_teste, npcs_de_testes):
    from codigo import jogo

    # Forçar escolha "1"
    entradas = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    # Criar inimigos já mortos
    mercenarios = [npcs_de_testes[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]
    for m in mercenarios:
        m.hp = 0

    # Evitar combate real: simular confronto_mercenario e pular direto
    monkeypatch.setattr(jogo, "confronto_mercenario", lambda g, i, n: None)

    jogo.primeiro_capitulo(grupo_de_teste, npcs_de_testes)

    capturado = capsys.readouterr().out
    assert "Após derrotar todos os mercenários" in capturado
    assert "vamos falar do pagamento" in capturado

def test_primeiro_capitulo_esolha_2_mensagem_final(monkeypatch, capsys, grupo_de_teste, npcs_de_testes):
    from codigo import jogo

    # Forçar escolha "2"
    entradas = iter(["2"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    # Criar inimigos já mortos
    mercenarios = [npcs_de_testes[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]
    for m in mercenarios:
        m.hp = 0

    # Evitar combate real: simular confronto_mercenario e pular direto
    monkeypatch.setattr(jogo, "confronto_mercenario", lambda g, i, n: None)

    jogo.primeiro_capitulo(grupo_de_teste, npcs_de_testes)

    capturado = capsys.readouterr().out
    assert "Após derrotar todos os mercenários" in capturado
    assert "vamos falar do pagamento" in capturado

def test_primeiro_capitulo_esolha_3_mensagem_final(monkeypatch, capsys, grupo_de_teste, npcs_de_testes):
    from codigo import jogo

    # Forçar escolha "3"
    entradas = iter(["3"])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    # Criar inimigos já mortos
    mercenarios = [npcs_de_testes[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]
    for m in mercenarios:
        m.hp = 0

    # Evitar combate real: simular confronto_mercenario e pular direto
    monkeypatch.setattr(jogo, "confronto_mercenario", lambda g, i, n: None)

    jogo.primeiro_capitulo(grupo_de_teste, npcs_de_testes)

    capturado = capsys.readouterr().out
    assert "Após derrotar todos os mercenários" in capturado
    assert "vamos falar do pagamento" in capturado

def test_iniciar_jogo(monkeypatch, capsys, grupo_de_teste, npcs_de_testes):
    # Mock para carregar_npcs
    def mock_carregar_npcs():
        return npcs_de_testes

    # Mock para primeiro_capitulo
    def mock_primeiro_capitulo(grupo, npcs):
        print(">>> Primeiro capítulo chamado!")

    # Substitui as funções reais pelos mocks
    monkeypatch.setattr("codigo.jogo.carregar_npcs", mock_carregar_npcs)
    monkeypatch.setattr("codigo.jogo.primeiro_capitulo", mock_primeiro_capitulo)

    # Evita travar no input()
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Executa a função
    iniciar_jogo(grupo_de_teste)

    # Captura saída
    saida = capsys.readouterr().out

    # Verifica se todos os personagens foram listados
    for personagem in grupo_de_teste:
        assert f"Personagem: {personagem.nome}" in saida

    # Verifica se o primeiro capítulo foi chamado
    assert ">>> Primeiro capítulo chamado!" in saida


def test_criar_personagem():
    p = Npc("Legolas", "Elfo", "Arqueiro", fala_inicial="O destino nos chama", hostil=False)

    assert p.nome == "Legolas"
    assert p.raca == "Elfo"
    assert p.classe == "Arqueiro"
    assert p.fala_inicial == "O destino nos chama"
    assert p.hostil is False
    assert p.hp == 100  # valor padrão
    assert p.ataque == 30  # valor padrão

def test_criar_npcs():
    npcs = carregar_npcs()

    # verifica se criou todos
    assert set(npcs.keys()) == {"Alric", "Thorne", "Gisa", "Hloddoviko", "Wilfred"}

    # verifica um NPC específico
    alric = npcs["Alric"]
    assert alric.nome == "Alric"
    assert alric.classe == "Mensageiro"
    assert alric.hostil is False

    thorne = npcs["Thorne"]
    assert thorne.hostil is True

