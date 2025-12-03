from codigo.personagem import personagens

def criar_grupo():

    while True:
        if not personagens:
            print("Nenhum personagem foi criado. Crie pelo menos um antes de continuar.")
            return None

        print("\n=== Grupo de Aventura Criado ===")
        for p in personagens:
            p.exibir_info()
        return personagens