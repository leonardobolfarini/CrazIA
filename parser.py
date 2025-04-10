import re

def extrair_medicamentos_e_horarios(texto):
    padrao = r"(?P<medicamento>\b\w+\b).*(?P<horario>\d{1,2} ?(horas|h|H))"
    matches = re.findall(padrao, texto, re.IGNORECASE)

    resultados = []
    for match in matches:
        medicamento, horario = match
        resultados.append((medicamento.strip(), horario.strip()))
    return resultados
