#################################################
#########           Desafio             #########
#################################################

# Utilize a biblioteca python requests para o consumo das API's
# Considere a PokéAPI (api com dados dos pokemons)
# https://pokeapi.co/docs/v2
# Não se esque de incluir tratativas de exceções.

# Questões
# Parte 1: Crie uma função que dado o nome ou id de um pokemon
# retorne um dicionário com seus atributos da forma:
# {
#     "abilities": [nome_de_todas_as_habilidades],
#     "forms": [nome_de_todas_as_formas],
#     "height": <numero>,
#     "id": pokemon_id,
#     "name": name,
#     "weight": peso_do_pokemon
# }
# Exemplos:
#   - consultar o pokemon bulbasaur: https://pokeapi.co/api/v2/pokemon/bulbasaur
#   - consultar o pokemon ivysaur: https://pokeapi.co/api/v2/pokemon/ivysaur
#   - consultar o pokemon charmander: https://pokeapi.co/api/v2/pokemon/charmander
#
# Caso haja um erro, como pokemon inexistente,
# gere uma exceção CUSTOMIZADA com a mensagem correspondente
# Exemplo de erro: https://pokeapi.co/api/v2/pokemon/10000 => retorna 404



# Parte 2: Crie uma função que dado uma string,
# valide se essa string corresponde a um CPF válido.
# As regras para validação de um CPF são:
# - Conter 11 dígitos
# - Validar os dígitos verificadores,
#       como descrito em: https://www.calculadorafacil.com.br/computacao/validar-cpf
# Você ainda deverá aceitar os formatos:
# - Com pontos e traços (xxx.xxx.xxx-xx)
# - Sem pontos e traços (xxxxxxxxxxx)
#
# Caso o CPF seja inválido, gere uma exceção CUSTOMIZADA, com a mensagem correspondente.
#   Casos obrigatórios:
#       - Exceção para formato inválido
#           - deverá contemplar os casos de caracteres não permitidos,
#               além do tamanho (número de dígitos) menor ou maior que o especificado.
#       - Exceção para dígitos inválidos
#           - deverá ocorrer quando não obedecer a regra de validação.
# Exemplo de CPF inválido: 111.111.111-11
# Exemplo de CPF válido:   377.136.110-96


# Parte 3: Crie uma função que calcule o Pokemon id de uma pessoa, dado um CPF VÁLIDO:
# O Pokemón id será calculado utilizando a seguinte função de hash:

#def poke_hash(cpf: int) -> int:
    # Note que a variável cpf deverá ter sido convertida para inteiro
    # ANTES de chamar a função poke_hash
#    return cpf % 97

# Utilize a validação de CPF.
# Sua função deverá ser robusta a erros da função de validação de CPF,
# tratando exceções, mas não às escondendo.
# Dica:
#try:
#    raise Exception("oi, eu sou o Goku")
#except Exception as e:
#    print("\nHouve um exception.\n")
#    raise e


# Parte 4: crie um Menu que ofereça ao usuário as opções:
# - Opção 1: Consultar os dados de um Pokemon
#   -> solicite o id ou nome do pokemon
#   -> nesta opção, utilize a biblioteca pprint para a impressão no terminal
#       Dica: pprint.pprint(TEXTO)
#
# - Opção 2: Consultar qual seu pokemon
#   -> nesta opção, peça o CPF do usuário
#       e reutilize as funções desenvolvidas nas questões 2 e 3.
#   -> imprima os dados com pprint, assim como no item anterior.
#
# - Opção 3: Encerrar ou continuar a execução, para isso:
#   -> utilize um loop infinito
#   -> solicite a confirmação com s/N:
#         -> aceite diferentes casos como: "sim", "s", "Sim", "n", etc...
#
# Você deverá tratar todas as execeções que possam ser geradas dentro das funções anteriores



"""Primeira questão!"""
import requests
import re
import pprint

class PokemonNotFoundError(Exception):
    pass
class InvalidCPFError(Exception):
    pass
def pokedex(nome_ou_id):
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nome_ou_id}")
        response.raise_for_status()
        info_pokemon = response.json()
        habilidades = [ability['ability']['name'] for ability in info_pokemon['abilities']]
        forms = [form['name'] for form in info_pokemon['forms']]
        return {
            "abilities": habilidades,
            "forms": forms,
            "height": info_pokemon['height'],
            "id": info_pokemon['id'],
            "name": info_pokemon['name'],
            "weight": info_pokemon['weight']
        }
    except requests.exceptions.RequestException:
        raise PokemonNotFoundError(f"Pokémon '{nome_ou_id}' não encontrado")
    except KeyError:
        raise PokemonNotFoundError(f"Pokémon '{nome_ou_id}' não encontrado")

"""Segunda questão!"""
def validar_cpf(cpf):
    # Remove pontos e traços
    cpf = re.sub(r'\D', '', cpf)
    if not cpf.isdigit() or len(cpf) != 11:
        raise InvalidCPFError("O CPF deve conter exatamente 11 dígitos")
    # Calcula os dígitos verificadores
    digito = [int(c) for c in cpf]
    total = sum(a * b for a, b in zip(digito[:9], range(10, 1, -1)))
    total = (total * 10) % 11
    if total == 10:
        total = 0
    if total != digito[9]:
        raise InvalidCPFError("CPF invalido")
    total = sum(a * b for a, b in zip(digito[:10], range(11, 1, -1)))
    total = (total * 10) % 11
    if total == 10:
        total = 0
    if total != digito[10]:
        raise InvalidCPFError("CPF invalido")

"""Terceira questão!"""
def poke_hash(cpf):
    try:
        validar_cpf(cpf)
        cpf_int = int(re.sub(r'\D', '', cpf))
        return cpf_int % 97
    except InvalidCPFError as e:
        raise e

"""Quarta questão!"""
def main():
    while True:
        print("Menu:")
        print("1. Consultar os dados de um Pokemon")
        print("2. Consultar qual seu pokemon")
        print("3. Encerrar")

        option = input("Escolha uma opção (1/2/3): ")

        if option == '1':
            nome_ou_id = input("Digite o nome ou id do Pokemon: ")
            try:
                pokedex_info = pokedex(nome_ou_id)
                pprint.pprint(pokedex_info)
            except PokemonNotFoundError as e:
                print(e)
        elif option == '2':
            cpf = input("Digite seu CPF: ")
            try:
                validar_cpf(cpf)
                pokemon_id = poke_hash(cpf)
                print(f"Seu Pokémon ID é: {pokemon_id}")
                try:
                    pokedex_info = pokedex(pokemon_id)
                    pprint.pprint(pokedex_info)
                except PokemonNotFoundError as e:
                    print(e)
            except InvalidCPFError as e:
                print(e)
        elif option == '3':
            confirmation = input("Deseja encerrar (s/N)? ").strip().lower()
            if confirmation in ('s', 'sim', 'S', 'SIM'):
                break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida (1/2/3).")


if __name__ == "__main__":
    main()
