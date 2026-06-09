from random import random
import numpy as np

def lambda_t(t):
    tau = t % 8
    if 0 <= tau <= 4:
        return 2.5 * tau + 4
    else:
        return 24 - 2.5 * tau

def generar_llegada_poisson(t_actual,T_max):
    lambda_max = 14
    t_aux = t_actual
    while True:
        U1 = 1 - random()
        t_aux = t_aux - np.log(U1) / lambda_max
        if t_aux > T_max:
            return float('inf')
        U2 = 1 - random()
        if U2 <= lambda_t(t_aux) / lambda_max:
            return t_aux

def programa(T= 16):
    t, NA, ND = 0, 0, 0
    n1, n2 = 0, 0
    t0 = generar_llegada_poisson(t, T)
    tA = t0
    t1, t2 = float('inf'), float('inf')

    t_llegadas = []
    reg_n1 = [0]
    t_atencion = []
    t_salida_atencion = []
    t_imagen = []
    t_salidas = []
    reg_n2 = [0]

    while tA < float('inf') or t1 < float('inf') or t2 < float('inf'):
        evento = min(tA, t1, t2)

        if evento == tA:
            t = tA
            NA += 1
            n1 += 1
            t_llegadas.append(t)
            tA = generar_llegada_poisson(t, T)
            reg_n1.append(n1)
            if tA > T:
                tA = float('inf')
            if n1 == 1:
                # Y1 es el tiempo de atencion en admision
                Y1 = np.random.exponential( 1 / 15)
                t1 = t + Y1

        elif evento == t1:
            t = t1
            n1 -= 1
            t_salida_atencion.append(t)
            primero = t_llegadas.pop(0)
            t_atencion.append( t - primero)
            reg_n1.append(n1)
            if n1 = 0:
                t1 = float('inf')
            else:
                Y1 = np.random.exponential( 1 / 15)
                t1 = t + Y1
            n2 += 1
            reg_n2.append(n2)
            if n2 == 1:
                Y2 = np.random.exponential( 1 / 12)
                t2 = t + Y2


# fin de servicio en imagen
        else:
            t = t2
            ND += 1
            n2 -= 1
            primero = t_salida_atencion.pop(0)
            t_imagen.append( t - primero)
            t_salidas.append(t)
            reg_n1.append(n1)
            if n2 == 0:
                t2 = float('inf')
            else:
                Y2 = np.random.exponential( 1 / 12)
                t2 = t + Y2

    return {
        't_llegadas': t_llegadas
        't_atencion': t_atencion
        't_imagen': t_imagen
        't_salidas': t_salidas
        'reg_n1': reg_n1
        'reg_n2': reg_n2
    }

def media_muestral_x_b(programa, d, T):
    res = programa(T)
    media = np.mean(res['t_imagen'])
    scuad, n = 0, 1
    while n <= 100 or np.sqrt(scuad / n) > d:
        n += 1
        res = programa(T)
        nueva = np.mean(res['t_imagen'])
        mediaAnt = media
        media = mediaAnt + ( nueva - mediaAnt) / n
        scuad = scuad * ( 1 - 1(n-1)) + n * (media - mediaAnt) ** 2

    return media

def estimador_p(programa, d, T):
    p, n = 0 , 0
    while n <= 100 or np.sqrt(p * ( 1 - p ) / n ) > d:
        n += 1
        res = programa(T)
        temp = np.array(res['t_salidas'])
        X = np.sum(temp > T)
        if X > 0:
            X = 1
        p = p + (X - p) / n

    return p
