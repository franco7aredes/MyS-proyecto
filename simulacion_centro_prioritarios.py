from random import random
import numpy as np


def lambda_t(t):
    return 8 + 4 * np.sin(np.pi * t / 12)


def generar_llegada_poisson(t_actual):
    lambda_max = 12
    t_aux = t_actual
    while True:
        U1 = 1 - random()
        t_aux = t_aux - np.log(U1) / lambda_max
        U2 = 1 - random()
        if U2 <= lambda_t(t_aux) / lambda_max:
            return t_aux


def programa_prioritarios(N=10000):
    t, NA, ND = 0, 0, 0
    n1, n2 = 0, 0
    t0 = generar_llegada_poisson(t)
    tA = t0
    t1, t2 = float('inf'), float('inf')

    # las nuevas variables
    cola1 = []
    cola2_P = []
    cola2_N = []
    cliente_en_validacion = None

    t_llegadas = []
    t_recepcion = []
    t_validacion = []
    t_salidas = []
    reg_n1 = [0]
    reg_n2 = [0]
    # Para registrar un tiempo total en sistema
    t_servicio_sistema_N = []
    t_servicio_sistema_P = []

    while tA < float('inf') or t1 < float('inf') or t2 < float('inf'):
        evento = min(tA, t1, t2)

        if evento == tA:
            t = tA
            NA += 1
            n1 += 1

            tipo = 'N' if random() < 0.8 else 'P'
            cola1.append([t, tipo, None])

            t_llegadas.append(t)
            # voy a cortar la llegada de clientes cuando llegue a N
            if NA < N:
                tA = generar_llegada_poisson(t)
            else:
                tA = float('inf')
            reg_n1.append(n1)
            if n1 == 1:
                Y1 = np.random.exponential(4 / 60)
                t1 = t + Y1

        # Fin de servicio en Recepción
        elif evento == t1:
            t = t1
            n1 -= 1

            cliente = cola1.pop(0)
            t_llegada_orig = cliente[0]

            t_recepcion.append(t - t_llegada_orig)
            reg_n1.append(n1)
            if n1 == 0:
                t1 = float('inf')
            else:
                Y1 = np.random.exponential(4 / 60)
                t1 = t + Y1
            n2 += 1
            reg_n2.append(n2)

            cliente[2] = t
            # si Validacion esta libre, pasa
            if t2 == float('inf'):
                cliente_en_validacion = cliente
                Y2 = np.random.exponential(0.1)
                t2 = t + Y2
            else:
                if cliente[1] == 'P':
                    cola2_P.append(cliente)
                else:
                    cola2_N.append(cliente)

        # Fin de servicio en Validación
        else:
            t = t2
            ND += 1
            n2 -= 1

            # vemos los datos del cliente que acaba de terminar
            t_llegada_orig, tipo_orig, t_salida_rec = cliente_en_validacion

            t_validacion.append(t - t_salida_rec)
            t_salidas.append(t)
            reg_n2.append(n2)

            tiempo_total = t - t_llegada_orig
            if tipo_orig == 'N':
                t_servicio_sistema_N.append(tiempo_total)
            else:
                t_servicio_sistema_P.append(tiempo_total)

            # regla de prioridad
            if len(cola2_P) > 0:
                cliente_en_validacion = cola2_P.pop(0)
                Y2 = np.random.exponential(0.1)
                t2 = t + Y2
            elif len(cola2_N) > 0:
                cliente_en_validacion = cola2_N.pop(0)
                Y2 = np.random.exponential(0.1)
                t2 = t + Y2
            else:
                t2 = float('inf')
                cliente_en_validacion = None

    return (
        t_llegadas,
        t_recepcion,
        t_validacion,
        t_salidas,
        reg_n1,
        reg_n2,
        t_servicio_sistema_N,
        t_servicio_sistema_P
    )
