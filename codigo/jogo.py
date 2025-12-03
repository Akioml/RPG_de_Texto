import  random
from codigo.grupo import criar_grupo
from codigo.npc import carregar_npcs


def obter_escolha(msg,opcoes_validas):
    escolha = input(msg.strip())
    return  escolha if escolha in opcoes_validas else None

def grupo_vivo(grupo):
    return  any(p.hp > 0 for p in grupo)

def mostrar_inimigos(inimigos):

    if isinstance(inimigos, dict):
        inimigos = inimigos.values()

    for i, inimigo in enumerate(inimigos):
        print(f"{i + 1} - {inimigo.nome} (HP: {inimigo.hp})")


def dialogo_personagens(grupo, indice, fala):
    personagem = grupo[indice]
    print(f'{personagem.nome}: {fala}')

def fala_npc(npcs, nome, fala):
    npc = npcs[nome]
    print(f'{npc.nome}: {fala}')


# ======== Combate ========

def turno_jogador(grupo, inimigos):
    if isinstance(inimigos, list):
        inimigos = {inimigo.nome: inimigo for inimigo in inimigos}

    for personagem in grupo:
        if personagem.hp <= 0:
            continue

        print(f'\nTurno de {personagem.nome}')
        print('Inimigos:')

        inimigos_vivos = {nome: inimigo for nome, inimigo in inimigos.items() if inimigo.hp > 0}

        if not inimigos_vivos:
            return {}

        for idx, (nome, inimigo) in enumerate(inimigos_vivos.items(), 1):
            print(f"{idx} - {nome} (HP: {inimigo.hp})")

        escolha = input('\nEscolha um inimigo para atacar: ')

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(inimigos_vivos)):
            print('\nEscolha inválida. Perdendo turno.')
            continue

        alvo_nome = list(inimigos_vivos.keys())[int(escolha) - 1]
        alvo = inimigos_vivos[alvo_nome]
        dano = personagem.ataque
        alvo.hp -= dano
        print(f"{personagem.nome} ataca {alvo.nome} causando {dano} de dano!")

        if alvo.hp <= 0:
            print(f"{alvo.nome} foi derrotado!")

    # Retorna apenas inimigos ainda vivos
    return {nome: inimigo for nome, inimigo in inimigos.items() if inimigo.hp > 0}




def turno_inimigos(grupo, inimigos):
    grupo_vivo = [p for p in grupo if p.hp > 0]

    for inimigo in inimigos.values():
        if not grupo_vivo:
            break

        alvo = random.choice(grupo_vivo)
        dano = inimigo.ataque
        alvo.hp -= dano
        print(f"{inimigo.nome} ataca {alvo.nome} causando {dano} de dano!")

        if alvo.hp <= 0:
            print(f"{alvo.nome} foi derrotado!")

        grupo_vivo = [p for p in grupo if p.hp > 0]



    return grupo



def turno_combate(grupo, inimigos):
    rodada = 1
    while rodada <= 10:
        print(f"\n=== Rodada {rodada} ===")

        inimigos = turno_jogador(grupo, inimigos)
        if not inimigos:
            print("\nSeu grupo venceu!")
            break

        grupo = turno_inimigos(grupo, inimigos)
        if not any(p.hp > 0 for p in grupo):
            print("\nSeu grupo foi derrotado!")
            break

        rodada += 1


# ===== Eventos Narrativos =====

def iniciar_combate(grupo, inimigos):
    print("\n=== COMBATE INICIADO ===")
    print("Seu grupo enfrenta os mercenários em um confronto feroz!")

    print("\n--- Seu Grupo ---")
    for personagem in grupo:
        personagem.exibir_info()

    print("\n--- Inimigos ---")
    for inimigo in inimigos:
        inimigo.exibir_info()

    turno_combate(grupo, inimigos)

def confronto_mercenario(grupo, inimigos, npcs):
    # aceitar dicionário ou lista
    if isinstance(inimigos, dict):
        inimigos_list = list(inimigos.values())
    else:
        inimigos_list = inimigos  # assume já é lista

    print("\nO grupo encara os mercenários que agora cercam o jardim da mansão.")
    print("O clima está tenso. Uma decisão precisa ser tomada...\n")

    while True:
        acao = obter_escolha("\nO que o grupo faz?\n1 - Tenta negociar\n2 - Atacar os Mercenários\n3 - Fugir\n> ",
                             {"1", "2", "3"})

        if acao == "1":
            print("\nVocê levanta as mãos e tenta falar com o líder dos mercenários...")
            print(f"{grupo[0].nome}: Não precisamos lutar. Pode haver algo que desejam mais do que sangue.")
            if inimigos_list:
                print(f"{inimigos_list[0].nome}: Tsc... Vocês acham que isso é uma feira? Falem rápido.")

            proposta = obter_escolha(
                "\nComo deseja negociar?\n"
                "1 - Oferecer ouro\n"
                "2 - Intimidar com reputação do grupo\n"
                "3 - Mentir dizendo que são emissários de um lorde poderoso\n> ",
                {"1", "2", "3"}
            )

            if proposta == "1":
                if len(grupo) > 1:
                    print(f"{grupo[1].nome}: Temos ouro.... Talvez isso convença vocês a deixar a mansão e ir embora")
                if inimigos_list:
                    print(f"{inimigos_list[0].nome}: Hmph... Dinheiro fala alto.")
                print("Os mercenários trocam olhares entre si.")
                print("Thorne sorri, mas os olhos continuam frios.")
                fala_npc(npcs, "Thorne", "Quanto ouro vocês tem a oferecer?")
                print("Você entrega parte de sua bolsa de moedas. O grupo resolve o problema, mas empobrecido.")
                grupo[0].mochila['ouro'] = max(0, grupo[0].mochila.get('ouro', 0) - 50)
                return  # termina sem combate
            elif proposta == "2":
                #CRIAR A NARAÇÃO DE SEGUNDA ESCOLHA INTIMIDAR POR REPUTAÇÃO (QUE NÃO VAI DAR CERTO NO FINALKK)
                
                if len(grupo) > 2:
                 print(f"{grupo[2].nome}: Acredito que conhecem o famoso Grupo """)
            print("Os mercenários hesitam por um segundo.")
            fala_npc(npcs, 'Gisa', "Espere... Varkan? Isso muda as coisas...")
            print("O líder Thorne rosna.")
            fala_npc(npcs, 'Thorne', "Como saberemos que vocês foram enviados por ele ?")
            print("Um clima tenso toma conta de todo o Jardim")
            if len(grupo) > 0:
                print(f"{grupo[0].nome} Temos uma carta dele aqui no bolso algum de vocês poderia vir aqui pegar ")
            print("Os mercenários hesitam por um segundo.")
            fala_npc(npcs, 'Thorne', "Vá até lá Gisa")
            print(f'Quando Gisa chega próxima o suficiente de {grupo[0].nome} uma adaga é sacada para apunhalar o mercenário, mas acaba errando dando início ao combate')
            iniciar_combate(grupo, inimigos_list)
            return

        elif acao == "2":
            print("\nSem hesitar, seu grupo puxa as armas e parte para o confronto!")
            if len(grupo) > 1:
                print(f"{grupo[1].nome}: Não temos tempo pra conversa com lixo como vocês!")
            for inimigo in inimigos_list:
                print(f"{inimigo.nome}, o {inimigo.classe}, se prepara para o combate!")
            iniciar_combate(grupo, inimigos_list)
            break

        elif acao == "3":
            if len(grupo) > 2:
                print(f"{grupo[2].nome}: Pensamos que vocês gostariam de saber... somos enviados do Lorde Varkan.")
            print("Os mercenários hesitam por um segundo.")
            fala_npc(npcs, 'Gisa', "Espere... Varkan? Isso muda as coisas...")
            print("O líder Thorne rosna.")
            fala_npc(npcs, 'Thorne', "Como saberemos que vocês foram enviados por ele ?")
            print("Um clima tenso toma conta de todo o Jardim")
            if len(grupo) > 0:
                print(f"{grupo[0].nome} Temos uma carta dele aqui no bolso algum de vocês poderia vir aqui pegar ")
            print("Os mercenários hesitam por um segundo.")
            fala_npc(npcs, 'Thorne', "Vá até lá Gisa")
            print(f'Quando Gisa chega próxima o suficiente de {grupo[0].nome} uma adaga é sacada para apunhalar o mercenário, mas acaba errando dando início ao combate')
            iniciar_combate(grupo, inimigos_list)
            return

def primeiro_capitulo(grupo, npcs):
    while True:
        escolha = obter_escolha("\nO que seu grupo faz?\n1 - Ajudar cobrando\n2 - Ajudar por honra\n3 - Ignorar\n> ",
                                {"1", "2", "3"})

        if escolha == '1':
            print(f'O primeiro a se mover foi {grupo[0].nome}, um {grupo[0].classe}')
            dialogo_personagens(grupo, 0, "Por uma boa quantia, eu e meu grupo podemos ajudar!")
            fala_npc(npcs, 'Alric',
                     'Sou apenas um mensageiro, meu mestre possui muito dinheiro! Por favor, venham comigo.')

            mercenarios_hostis = [npcs[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]

            print("""\nO portão range alto ao se abrir...""")  # Texto resumido por brevidade
            fala_npc(npcs, 'Thorne', 'O QUE EU DISSE? ERA PARA TER MATADO ESSE MENSAGEIRO!')

            confronto_mercenario(grupo, mercenarios_hostis, npcs)

            if all(m.hp <= 0 for m in mercenarios_hostis):
                print(f'Após derrotar todos os mercenários, {grupo[2].nome} se dirige ao mensageiro e diz:')
                print('-- Trabalho feito. Agora, vamos falar do pagamento!')
            break

        elif escolha == '2':
            print(f'O primeiro a se mover foi {grupo[0].nome}, um {grupo[0].classe}')
            dialogo_personagens(grupo, 0,
                                "Não buscamos ouro. Estamos aqui por honra. Proteger inocentes é nossa missão.")

            fala_npc(npcs, 'Alric',
                     'Vocês são verdadeiros heróis... Meu mestre ficará emocionado com essa coragem. Por favor, venham comigo.')

            print(
                "\nEnquanto atravessam a trilha até a fortaleza de pedra, o vento carrega o cheiro de sangue e fumaça.")
            print("Ao se aproximarem do vilarejo, veem casas queimando e corpos espalhados...")

            fala_npc(npcs, 'Gisa', 'Malditos... alguém teve coragem de nos enfrentar? ')

            mercenarios_hostis = [npcs[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]

            print("""\nAs espadas são desembainhadas e o combate se aproxima como uma tempestade...""")

            confronto_mercenario(grupo, mercenarios_hostis, npcs)

            if all(m.hp <= 0 for m in mercenarios_hostis):
                print(f'Após derrotar todos os mercenários, {grupo[2].nome} se dirige ao mensageiro e diz:')
                print('-- Trabalho feito. Agora, vamos falar do pagamento!')
            break

        elif escolha == '3':
            print(f'{grupo[0].nome}, um {grupo[0].classe}, ergue sua caneca e vira-se para os companheiros.')
            dialogo_personagens(grupo, 0, "Não nos metamos. Não é nossa luta.")

            fala_npc(npcs, 'Alric', 'Por favor... vidas estão em risco! Não façam isso...')

            print("\nO mensageiro sai correndo da taverna, com o desespero estampado no rosto.")
            print("Você volta sua atenção para a bebida, tentando ignorar a culpa...")

            # Cenas subsequentes da escolha
            print("\nHoras se passam. A madrugada cai silenciosa.")
            print("Mas o silêncio logo é rompido...")

            fala_npc(npcs, 'Wilfred', 'Achamos eles. O informante estava certo. Cortem a garganta de todos.')

            print("Você foi seguido. Mercenários entram pela porta dos fundos da taverna com armas em punho.")

            mercenarios_hostis = [npcs[nome] for nome in ["Thorne", "Gisa", "Hloddoviko", "Wilfred"]]

            print("""\nVocê se levanta com a mão na empunhadura da arma. Não há escolha agora. É lutar ou morrer.""")

            confronto_mercenario(grupo, mercenarios_hostis, npcs)

            if all(m.hp <= 0 for m in mercenarios_hostis):
                print(f'Após derrotar todos os mercenários, {grupo[2].nome} se dirige ao mensageiro e diz:')
                print('-- Trabalho feito. Agora, vamos falar do pagamento!')
            break

def iniciar_jogo(grupo):
    input("Pressione Enter para começar sua jornada...")

    print("""\nO sol se punha lentamente atrás das montanhas distantes, tingindo o céu de tons dourados e alaranjados. 
        Uma brisa fresca carregava o cheiro da terra úmida e das folhas que dançavam nas trilhas poeirentas. 
        No vilarejo de Valdora, entre colinas e florestas densas, as sombras já começavam a se alongar.""")

    print("""\nA Taverna do Javali Cansado era o coração pulsante daquele fim de tarde. 
        As velhas madeiras rangiam sob os passos dos frequentadores, e uma lareira crepitava num canto, jogando luz tremeluzente nas paredes cobertas de troféus de caça. 
        Você está sentado com seu grupo em uma mesa ao fundo, observando o movimento.\n""")

    print("""\nDe repente, a porta se abre com um estrondo. Um mensageiro entra ofegante e grita:
        — Tem algo vindo da floresta negra! Eles precisam de ajuda na Mansão dos Hollowind! Por favor, alguém!
        O jovem mensageiro mal teve tempo de recuperar o fôlego antes que quatro figuras se levantassem quase ao mesmo tempo. 
        Olhares se cruzaram na taverna. Não havia necessidade de palavras. 
        Algo os chamava — talvez a promessa de ouro, aventura, ou quem sabe, um velho senso de justiça.\n""")

    for personagem in grupo:
        print(f"Personagem: {personagem.nome}")

    npcs = carregar_npcs()
    primeiro_capitulo(grupo, npcs)