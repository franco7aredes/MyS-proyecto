import numpy as np
from scipy import stats

from simulacion_centro_ej1 import programa
from simulacion_centro_prioritarios import programa_prioritarios


def generar_intervalo_de_confianza(media, scuad, alpha, n):
    z_alpha_2 = stats.norm.ppf(1-alpha/2)
    std = np.sqrt(scuad/n)
    izq = media - z_alpha_2 * std
    der = media + z_alpha_2 * std
    intervalo = f"[{izq:.4f}, {der:.4f}]"
    return intervalo


def estimar_media_muestral(programa, d, N, metrica=6):
    res = programa(N)
    media = np.mean(res[metrica])
    scuad, n = 0, 1
    while n < 100 or np.sqrt(scuad / n) > d:
        n += 1
        res = programa(N)
        nueva = np.mean(res[metrica])
        mediaAnt = media
        media = mediaAnt + (nueva - mediaAnt) / n
        scuad = scuad * (1 - 1 / (n-1)) + n * (media - mediaAnt) ** 2

    return media, scuad, n


def calcular_metricas_permanencia(tiempos, x_minutos=60):
    arr = np.array(tiempos)
    media = np.mean(arr)
    mediana = np.median(arr)
    p25 = np.percentile(arr, 25)
    p75 = np.percentile(arr, 75)
    p90 = np.percentile(arr, 90)

    x_horas = x_minutos / 60.0
    prob_mayor_x = np.mean(arr > x_horas)

    return media, mediana, p25, p75, p90, prob_mayor_x
