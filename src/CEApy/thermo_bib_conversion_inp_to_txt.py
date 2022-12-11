thermo_library = open('cea-exec/thermo.txt', 'r')
lines = thermo_library.readlines()
cont = 0
species = []
for linha in lines:
    if linha[0].isalpha():
        palavras = linha.split()
        primeira_palavra_linha = palavras[0]
        if (primeira_palavra_linha != 'END') and (primeira_palavra_linha != 'thermo'):
            species.append(primeira_palavra_linha)
            cont = cont + 1
with open('cea-exec/thermo.txt', 'w') as file:
    for valor in species:
        file.write(str(valor) + '\n')
