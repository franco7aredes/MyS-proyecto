from random import random
import numpy as np


def lambda_t(t):
    return 8 + 4 * np.sin(np.pi * t / 12)


def generar_llegada_poisson(t_actual, T_max):
    lambda_max = 12
    t_aux = t_actual
    while True:
        U1 = 1 - random()
        t_aux = t_aux - np.log(U1) / lambda_max
        if t_aux > T_max:
            return float('inf')
        U2 = 1 - random()
        if U2 <= lambda_t(t_aux) / lambda_max:
            return t_aux

# fijarse lo del T, si corresponde


def programa(T=16):
    t, NA, ND = 0, 0, 0
    n1, n2 = 0, 0
    t0 = generar_llegada_poisson(t, T)
    tA = t0
    t1, t2 = float('inf'), float('inf')

    t_llegadas = []
    t_recepcion = []
    t_validacion = []
    t_salida_recepcion = []
    t_salidas = []
    reg_n1 = [0]
    reg_n2 = [0]
    # Para registrar un tiempo total en sistema
    t_servicio_sistema = []
    t_llegada_sistema = []

    while tA < float('inf') or t1 < float('inf') or t2 < float('inf'):
        evento = min(tA, t1, t2)

        if evento == tA:
            t = tA
            NA += 1
            n1 += 1
            t_llegadas.append(t)
            t_llegada_sistema.append(t)
            tA = generar_llegada_poisson(t, T)
            reg_n1.append(n1)
            if tA > T:
                tA = float('inf')
            if n1 == 1:
                Y1 = np.random.exponential(1 / 4)
                t1 = t + Y1

        # Fin de servicio en Recepción
        elif evento == t1:
            t = t1
            n1 -= 1
            t_salida_recepcion.append(t)
            primero = t_llegadas.pop(0)
            t_recepcion.append(t - primero)
            reg_n1.append(n1)
            if n1 == 0:
                t1 = float('inf')
            else:
                Y1 = np.random.exponential(1 / 4)
                t1 = t + Y1
            n2 += 1
            reg_n2.append(n2)
            if n2 == 1:
                Y2 = np.random.exponential(1 / 6)
                t2 = t + Y2

        # Fin de servicio en Validación
        else:
            t = t2
            ND += 1
            n2 -= 1
            primero = t_salida_recepcion.pop(0)
            t_validacion.append(t - primero)
            t_salidas.append(t)
            reg_n1.append(n1)

            # Registramos el tiempo total en el sistema
            llegada = t_llegada_sistema.pop(0)
            t_servicio_sistema.append(t - llegada)
            if n2 == 0:
                t2 = float('inf')
            else:
                Y2 = np.random.exponential(1 / 6)
                t2 = t + Y2

    return (
        t_llegadas,
        t_recepcion,
        t_validacion,
        t_salidas,
        reg_n1,
        reg_n2,
        t_servicio_sistema
    )
