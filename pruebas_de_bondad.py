import numpy as np
import scipy.stats as stats


def prueba_bondad_ajuste(tiempos_permanencia):
    datos = np.array(tiempos_permanencia)
    N = len(datos)

    # Estimaciones
    media = np.mean(datos)
    var = np.var(datos, ddof=1)

    # Exponencial
    scale_exp = media
    loc_exp = 0

    # Log Normal
    cv2 = var / (media**2)
    shape_log = np.sqrt(np.log(1 + cv2))
    scale_log = np.exp(np.log(media / np.sqrt(1 + cv2)))
    loc_log = 0

    obs, bins = np.histogram(datos, bins=50)

    def calc_esp(dist, params, limites, N_tot, obs_arr):
        p_i = np.diff(dist.cdf(limites, *params))

        p_i[0] += dist.cdf(limites[0], *params)
        p_i[-1] += (1.0 - dist.cdf(limites[-1], *params))

        esp = p_i * N_tot
        esp = esp * (np.sum(obs_arr) / np.sum(esp))

        return esp

    esp_exp = calc_esp(stats.expon, (loc_exp, scale_exp), bins, N, obs)
    esp_log = calc_esp(
        stats.lognorm, (shape_log, loc_log, scale_log), bins, N, obs)

    _, pval_exp = stats.chisquare(f_obs=obs, f_exp=esp_exp, ddof=1)
    _, pval_log = stats.chisquare(f_obs=obs, f_exp=esp_log, ddof=2)

    return pval_exp, pval_log


