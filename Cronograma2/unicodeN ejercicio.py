def normalize(texto):
    acentos = {"á":"a", "é":"e", "í": "i", "ó": "o", "ú": "u"}
    resultado = []
    for letra in texto.lower():
        if letra in acentos:
            resultado.append(acentos[letra])
        else:
            resultado.append(letra)
    return "".join(resultado)
print(normalize("poción de vida"))