def texto(texto):
    return texto.upper()

import math
def radianes_a_horas(radianes):
        radianes = radianes % (2 * math.pi) # Normalizar los radianes para estar en el rango de 0 a 2π
        horas = (radianes / (2 * math.pi)) * 12 # Convertir radianes a horas   
        horas_completas = int(horas) # Extraer las horas completas
        minutos = (horas - horas_completas) * 60 # Convertir el resto a minutos
        minutos_completos = int(minutos)
        segundos = (minutos - minutos_completos) * 60 # Convertir el resto a segundos
        segundos_completos = int(round(segundos,0))
        return horas_completas, minutos_completos, segundos_completos

