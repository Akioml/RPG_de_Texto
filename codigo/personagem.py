class Personagem:
    def __init__(self,nome, raca, altura, idade, classe, ataque, hp=100):
        self.nome = nome
        self.raca = raca
        self.altura = altura
        self.idade = idade
        self.classe = classe
        self.ataque = ataque
        self.hp = hp
        self.mochila = {'ouro': 50}

    def exibir_info(self):
        print(f"Nome: {self.nome}")
        print(f"Raça: {self.raca}")
        print(f"Altura: {self.altura}m")
        print(f"Idade: {self.idade} anos")
        print(f"Classe: {self.classe}")
        print(f"Vida: {self.hp}")
        print(f"Ataque: {self.ataque}")
        print("-" * 20)

personagens = []

def criar_novo_personagem(**kwargs):
    print('\n=== Criar Novo Personagem ===')

    campos = ['nome', 'raca', 'altura', 'idade', 'classe', 'ataque']
    valores = {}

    for campo in campos:
        if campo in kwargs and kwargs[campo] is not None:
            valores[campo] = kwargs[campo]
        else:
            entrada = input(f'{campo.capitalize()}: ')
            valores[campo] = float(entrada) if campo == 'ataque' else entrada

        hp = 100
    novo_personagem = Personagem(
        nome=valores['nome'],
        raca=valores['raca'],
        altura=valores['altura'],
        idade=valores['idade'],
        classe=valores['classe'],
        ataque=valores['ataque']
    )   

    personagens.append(novo_personagem)

    print(f"\nPersonagem '{valores['nome']}' criado com sucesso!\n")
    return novo_personagem

def exibir_todos_personagens():
    print("\n=== Lista de Personagens Criados ===")
    if not personagens:
        print('Nenhum personagem criado! ')
        return
    for i, p in enumerate(personagens,1):
        print(f'Personagem {i}')
        p.exibir_info()

def menu():
    while len(personagens) < 4:
        print(f"\n=== Menu Principal ===")
        print(f"Personagens criados: {len(personagens)}/4")
        print("1 - Criar Novo Personagem")
        print("2 - Exibir Personagens Criados")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_novo_personagem()
        elif opcao == '2':
            exibir_todos_personagens()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()