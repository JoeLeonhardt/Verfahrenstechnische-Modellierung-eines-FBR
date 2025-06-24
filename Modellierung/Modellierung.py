import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import Parameter.Parameter as params

# allgemeine Gleichungen
# <<< Diese Funktionen berechnen die Temperaturabhängigkeit von k, K und die mittlere Wärmekapazität cp
def k_arrhenius(T):
    T = np.clip(T, 100, 2000)
    # <<< Arrhenius-Gleichung für die Geschwindigkeitskonstante (reagiert exponentiell auf Temperatur)
    return params.k_ref * np.exp(-params.E_A / params.R * (1/T - 1/params.T_ref))

def K_eq(T):
    T = np.clip(T, 100, 2000)
    # <<< Van't Hoff-Gleichung für die Gleichgewichtskonstante (abhängig von Temperatur und Reaktionsenthalpie)
    return params.K_ref * np.exp(-params.Delta_R_H / params.R * (1/T - 1/params.T_ref))

def cp_mixture(X):
    X = np.clip(X, 0, 1)
    # <<< Gemischte Wärmekapazität, gewichtet nach Umsatz X
    return params.cP_A * (1 - X) + params.cP_B * X

# Differenzialgleichungssystem wie in Doku definiert
# <<< Diese Funktion beschreibt das System von DGLs für den Festbettreaktor.
# <<< Sie gibt für einen kleinen Schritt d(m_cat) zurück, wie sich Umsatz, Temperatur und Druck ändern.
def dgls(m_cat, y, nA0, kDa, Tk, debug=False):
    X, T, p = y
    nA = nA0 * (1 - X)      # <<< aktueller Molenstrom A
    nB = nA0 * X / 2        # <<< aktueller Molenstrom B (Stöchiometrie: 2A -> B)
    n_total = nA + nB       # <<< aktueller Gesamt-Molenstrom
    p_Pa = p * params.atm_to_Pa   # <<< Druck in Pascal
    V_dot = n_total * params.R * T / p_Pa  # <<< Volumenstrom nach idealem Gasgesetz
    c_A = nA / V_dot        # <<< Konzentration A im Reaktor (mol/m³)
    c_B = nB / V_dot        # <<< Konzentration B im Reaktor (mol/m³)
    c_A_L = c_A * 1e-3      # <<< Konzentration A in mol/L für die Kinetik
    c_B_L = c_B * 1e-3      # <<< Konzentration B in mol/L für die Kinetik
    k = k_arrhenius(T)      # <<< Temperaturabhängige Geschwindigkeitskonstante
    K = K_eq(T)             # <<< Temperaturabhängige Gleichgewichtskonstante
    r_A = k * (c_A_L ** 2 - c_B_L / K)  # <<< Reaktionsrate (reversibel!)
    dX_dm = r_A / nA0       # <<< Änderung des Umsatzes pro kg Katalysator
    dT_dm = (-params.Delta_R_H * r_A - kDa * (T - Tk)) / (nA0 * cp_mixture(X))  # <<< Energiebilanz
    dp_dm = -params.alpha / (2 * p)   # <<< Druckverlust nach Ergun-Gleichung (vereinfacht)
    if debug and m_cat < 0.5:
        print(f"...")
    return [dX_dm, dT_dm, dp_dm]

#Simulation mit definierten Wertebereichen
# Funktion übernimmt die initialen Bedingungen, löst das DGLS numerisch (mit solve_ivp)
#und berechnet anschließend aus dem Ergebnis die wichtigsten Größen (Umsatz, Konzentrationen, ..)
def run_fbr_simulation(T0, p0, nA0, kDa, Tk, mcat_max=20, n_points=200):
    y0 = [0.0, params.T0, p0]                      # Startwerte für Umsatz X, Temperatur T, Druck p
    mcat_span = (0, mcat_max)                        #Integrationsbereich für Katalysatormasse [kg]
    mcat_eval = np.linspace(0, mcat_max, n_points)  #Auswertepunkte entlang der Katalysatormasse

    # Lösung Differentialgleichungssystems
    sol = solve_ivp(
        lambda m_cat, y: dgls(m_cat, y, nA0, kDa, Tk, debug=False),
        mcat_span, y0, dense_output=True, max_step=0.1
    )
    X, T, p = sol.sol(mcat_eval)            # <<< Extrahiere Lösungen für alle Auswertepunkte

    #Weitere Größen aus dem Umsatz berechnen (wie oben)
    nA = nA0 * (1 - X)
    nB = nA0 * X / 2
    n_total = nA + nB
    V_dot = n_total * params.R * T / (p * params.atm_to_Pa)
    c_A = nA / V_dot
    c_B = nB / V_dot

    return mcat_eval, X, T, p, c_A, c_B #weitergabe der berechneten Werte für die anderen Module
