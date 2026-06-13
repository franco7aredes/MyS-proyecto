from random import random
import numpy as np
from simulacion_centro_ej1 import programa
# corregir: el programa va a devolver un struct


def media_muestral_x_b(programa, d, T):
    res = programa(T)
    media = np.mean(res[6])
    scuad, n = 0, 1
    while n < 100 or np.sqrt(scuad / n) > d:
        n += 1
        res = programa(T)
        nueva = np.mean(res[6])
        mediaAnt = media
        media = mediaAnt + (nueva - mediaAnt) / n
        scuad = scuad * (1 - 1 / (n-1)) + n * (media - mediaAnt) ** 2

    return media


def estimador_p(programa, d, T):
    p, n = 0, 0
    while n <= 100 or np.sqrt(p * (1 - p) / n) > d:
        n += 1
        res = programa(T)
        temp = np.array(res[3])
        X = np.sum(temp > T)
        if X > 0:
            X = 1
        p = p + (X - p) / n

    return p


media = media_muestral_x_b(programa, 0.1, 100)
print(media)
