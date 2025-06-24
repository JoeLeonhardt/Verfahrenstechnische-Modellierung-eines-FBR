#hier werden alle module importiert
import gradio as gr #UI Modul
import numpy as np #Modul fürs rechnen (wird hier nicht aktiv genutzt stört aber auch nicht, da es Modellierung genutzt wird)
import matplotlib.pyplot as plt #Plots erstellen (interaktiv) (wird hier nicht aktiv genutzt stört aber auch nicht, da es in Plots.py genutzt wird)
import Parameter.Parameter as params #eigenes Modukl mit den gegebenen Parametern
import Visualisierung.Plots as plots #eigenes Modul was die plots erstellt
from Modellierung.Modellierung import run_fbr_simulation #mein Modellierungsmodul
import pandas as pd #Modul für wertetabellen

# Parameterkopplung in Gradio (WIP) von cA0, T0, p0 -> ermöglicht Veränderung der Parameter im UI mit Rückgabe der Werte in die Simulation

def gasgesetz_update(cA0, T0, p0, calc_mode):

    if calc_mode == "Berechne Druck":
        p0_new = cA0 * params.R * T0 / params.atm_to_Pa
        return f"{p0_new:.2f} atm", gr.update()
    elif calc_mode == "Berechne Eintrittskonzentration":
        cA0_new = p0 * params.atm_to_Pa / (params.R * T0)
        return f"{cA0_new:.2f} mol/m³", gr.update()
    elif calc_mode == "Berechne Eintrittstemperatur":
        T0_new = p0 * params.atm_to_Pa / (cA0 * params.R)
        return f"{T0_new:.2f} K", gr.update()
    return "-", gr.update()

#eigntlicher Start der Simulation aus dem Modul Modellierung, mit Berücksichtigung der veränderbaren Parameter aus dem UI, 
# stellt sicher, dass alle gekoppelten Werte intern nochmal neu berechnet werden -> notwendiger Workaround
# gibt dann die Plots, Tabellen, und Infotexte für die UI zurück
def run_simulation(cA0, T0, p0, Tk, kDa, kref, show_table, calc_mode):

    if calc_mode == "Berechne Druck":
        p0 = cA0 * params.R * T0 / params.atm_to_Pa
    elif calc_mode == "Berechne Eintrittskonzentration":
        cA0 = p0 * params.atm_to_Pa / (params.R * T0)
    elif calc_mode == "Berechne Eintrittstemperatur":
        T0 = p0 * params.atm_to_Pa / (cA0 * params.R)

    p0_Pa = p0 * params.atm_to_Pa
    Vdot0 = params.R * T0 / p0_Pa
    nA0 = cA0 * Vdot0  # [mol/min]

    #Simulation mit den endgültigen Werten aus dem UI starten
    mcat_eval, X, T, p, c_A, c_B = run_fbr_simulation(T0, p0, nA0, kDa, Tk)

    #Plots erzeugen aus aktuellen Simulationsdaten
    fig = plots.plot_fbr_results_plotly(mcat_eval, X, T, p, c_A, c_B, p0)

    # k(T), K(T)-Plot (WIP)
    #k_vals = [k_arrhenius(Ti) for Ti in T]
    #K_vals = [K_eq(Ti) for Ti in T]
    #kK_fig = plots.plot_kinetik_K(T, k_vals, K_vals)

    #Wertetabelle (Anzeige und download option)

    value_table = pd.DataFrame({
        "m_cat [kg]": mcat_eval,
        "X": X,
        "T [K]": T,
        "p [atm]": p,
        "c_A [mol/m³]": c_A,
        "c_B [mol/m³]": c_B
    }) if show_table else None

    # 5. UI Parameter die für die aktuelle simulation genutzt werden
    info = f"""
    **Aktuelle Startparameter:**  
    $c_{{A,0}}$ = {cA0:.2f} mol/m³, $T_0$ = {T0:.2f} K, $p_0$ = {p0:.2f} atm  
    $T_K$ = {Tk:.2f} K, $k_{{Da}}$ = {kDa:.2f}, $k_{{ref}}$ = {kref:.2f}
    """
    return fig, value_table, info
    #return fig, kK_fig, value_table, info -> nur für k(T), K(T)-Plot (WIP))

#launch des Interface über gradio mit den Designelementen
with gr.Blocks() as demo:
    gr.Markdown("# Festbettreaktor – Interaktive Simulation")
    # Slider und ein Dropdown für die Kopplung dr abhängigen Parameter (hier bin ich noch nicht zufrieden), was im Dropdown ausgewählt ist wird durch die anderen 2 Parameter berechnet

    with gr.Row():

        cA0_slider = gr.Slider(10, 500, value=271, label="Eintrittskonzentration A [mol/m³]")
        T0_slider = gr.Slider(300, 700, value=450, label="Eintrittstemperatur [K]")
        p0_slider = gr.Slider(1, 30, value=10, label="Eintrittsdruck [atm]")
        calc_mode = gr.Dropdown(["Berechne Druck", "Berechne Eintrittskonzentration", "Berechne Eintrittstemperatur"], value="Berechne Druck", label="Zu berechnender Parameter")

        # Das Ergebnisfeld für den gekoppelten Parameter (soll read only sein WIP)
        gekoppelter_parameter = gr.Textbox(label="Gekoppelter Parameter", interactive=False)

    with gr.Row():
        Tk_slider = gr.Slider(300, 700, value=500, label="Kühlmitteltemperatur [K]")
        kDa_slider = gr.Slider(0.1, 2.0, value=0.8, step=0.05, label="Wärmeabfuhrkoeffizient $k_{Da}$")
        kref_slider = gr.Slider(0.05, 2.0, value=0.5, step=0.01, label="Kinetikkonstante $k_{ref}$")
    #Optionsfeld für Wertetabelle
    show_table = gr.Checkbox(label="Wertetabelle anzeigen/downloaden")

    #Update des gekoppelten Parameters (WIP)
    # <<< Die .change()-Methoden sorgen dafür, dass das UI-Feld bei Änderung eines Parameters immer neu berechnet wird
    cA0_slider.change(gasgesetz_update, [cA0_slider, T0_slider, p0_slider, calc_mode], [gekoppelter_parameter])
    T0_slider.change(gasgesetz_update, [cA0_slider, T0_slider, p0_slider, calc_mode], [gekoppelter_parameter])
    p0_slider.change(gasgesetz_update, [cA0_slider, T0_slider, p0_slider, calc_mode], [gekoppelter_parameter])
    calc_mode.change(gasgesetz_update, [cA0_slider, T0_slider, p0_slider, calc_mode], [gekoppelter_parameter])

    sim_btn = gr.Button("Simulation starten")

    gr.Markdown("### Ergebnisdiagramme")
    #anzeige des hauptplots
    plot_output = gr.Plot(label="Reaktorprofile (Umsatz, T, p, Konzentration)")
    #kK_output = gr.Plot(label="Kinetik- und Gleichgewichtskon_
    gr.Markdown("### Ergebnisdiagramme") #Zeigt plot mit allen Reaktorprofilen (Umsatz, Temperatur, Druck, Konzentrationen)
    plot_output = gr.Plot(label="Reaktorprofile (Umsatz, T, p, Konzentration)")
    #kK_output = gr.Plot(label="Kinetik- und Gleichgewichtskonstante $k(T), K(T)$") -> WIP
    #Tabelle mit allen Simulationsergebnissen (optional, je nach Checkbox)
    table_output = gr.Dataframe(label="Wertetabelle")
    #Infotext aktuelle Parameter und Startbedingungen
    info_output = gr.Markdown()
    # Download CSV
    download_btn = gr.DownloadButton("Tabelle herunterladen (CSV)")

    sim_btn.click(
        run_simulation,
        inputs=[cA0_slider, T0_slider, p0_slider, Tk_slider, kDa_slider, kref_slider, show_table, calc_mode],
        outputs=[plot_output, table_output, info_output]
    )

# Bilanzgleichungen als Infofeld
gr.Markdown(r"""
    **Bilanzgleichungen:**
    $$
    \begin{aligned}
      \frac{dX}{dm_\mathrm{cat}} &= \frac{r_A}{n_{A,0}} \\
      \frac{dT}{dm_\mathrm{cat}} &= \frac{-\Delta_R H \cdot r_A - k_{Da}(T-T_K)}{n_{A,0} \cdot \bar{c}_P} \\
      \frac{dp}{dm_\mathrm{cat}} &= -\frac{\alpha}{2p}
    \end{aligned}
    $$
    """)

demo.launch(share=False)