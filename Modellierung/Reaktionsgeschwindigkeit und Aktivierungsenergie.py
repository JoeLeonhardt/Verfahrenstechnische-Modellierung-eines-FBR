#das hier ist noch nicht fertig ich hatte überlegt mir mal die kinetischen Daten auftragen zu lassen
import numpy as np
import matplotlib.pyplot as plt
import Parameter.Parameter as params
# Umrechnung
L_to_m3 = 1e-3   # L -> m3
atm_to_Pa = 101325
T_arr = np.linspace(300, 1000, 100)

k_vals = [params.k_ref * np.exp(-params.E_A / params.R * (1/T - 1/450)) for T in T_arr]
K_vals = [params.K_ref * np.exp(-params.Delta_R_H / params.R * (1/T - 1/450)) for T in T_arr]

plt.plot(T_arr, k_vals, label='k(T) (Geschwindigkeitskonstante)')
plt.plot(T_arr, K_vals, label='K(T) (Gleichgewichtskonstante)')
plt.xlabel('Temperatur (K)')
plt.legend()
plt.yscale('log')
plt.show()
