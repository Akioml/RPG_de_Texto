from codigo.jogo import iniciar_jogo
from codigo.grupo import criar_grupo
from codigo.personagem import menu

def main():
    # Primeiro criar personagens se não existirem
    menu()
    grupo = criar_grupo()
    if grupo:  # só inicia se tiver personagens
        iniciar_jogo(grupo)

if __name__ == "__main__":
    main()
