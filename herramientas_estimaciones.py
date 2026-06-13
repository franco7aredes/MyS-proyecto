import numpy as np
from scipy import stats

from simulacion_centro_ej1 import programa


def generar_intervalo_de_confianza(media, scuad, alpha, n):
    z_alpha_2 = stats.norm.ppf(1-alpha/2)
    std = np.sqrt(scuad/n)
    izq = media - z_alpha_2 * std
    der = media + z_alpha_2 * std
    intervalo = f"[{izq:.4f}, {der:.4f}]"
    return intervalo


def estimar_media_muestral(programa, d, N):
    res = programa(N)
    media = np.mean(res[6])
    scuad, n = 0, 1
    while n < 100 or np.sqrt(scuad / n) > d:
        n += 1
        res = programa(N)
        nueva = np.mean(res[6])
        mediaAnt = media
        media = mediaAnt + (nueva - mediaAnt) / n
        scuad = scuad * (1 - 1 / (n-1)) + n * (media - mediaAnt) ** 2

    return media, scuad, n


def estimador_p(programa, d, N):
    p, n = 0, 0
    while n <= 100 or np.sqrt(p * (1 - p) / n) > d:
        n += 1
        res = programa(N)
        temp = np.array(res[3])
        X = np.sum(temp > T)
        if X > 0:
            X = 1
        p = p + (X - p) / n

    return p

def prob_esperar_mas_de_x(tiempos, x_minutos):
    x_horas = x_minutos / 60.0
    arr_tiempos = np.array(tiempos)

    p = np.mean(arr_tiempos > x_horas)

    return p


print("====/ Ejercicio 1b /====")
media, scuad, simulaciones = estimar_media_muestral(programa, 0.1, 10000)
print(f"El tiempo promedio de permanencia es: {media:.4f}")
intervalo = generar_intervalo_de_confianza(media, scuad, 0.05, simulaciones)
print(
    f"El intervalo de confianza del %95 para {simulaciones} simulaciones es de {intervalo}")
