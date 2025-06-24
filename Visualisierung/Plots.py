#Plotten des Ergebnis der Simulation
import plotly.graph_objs as go #interaktibver Plot
from plotly.subplots import make_subplots #Mehrfachanzeige der plots
from Modellierung.Modellierung import run_fbr_simulation
import Parameter.Parameter as params
#4 geteilter Plot für das Interface

def plot_fbr_results_plotly(mcat_eval, X, T, p, c_A, c_B, p0): #nimmt nur die Ergebnisse der simulation
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "Umsatz X", "Temperatur T [K]",
            "dimensionsloser Druck (p/p₀)", "Konzentrationen [mol/m³]"
        )
    )

    # Umsatz X
    fig.add_trace(go.Scatter(
        x=mcat_eval, y=X, mode='lines+markers', name='Umsatz X',
        hovertemplate='m_cat: %{x:.2f} kg<br>X: %{y:.3f}'), row=1, col=1)

    # Temperatur
    fig.add_trace(go.Scatter(
        x=mcat_eval, y=T, mode='lines+markers', name='Temperatur',
        hovertemplate='m_cat: %{x:.2f} kg<br>T: %{y:.1f} K'), row=1, col=2)

    # Druck
    fig.add_trace(go.Scatter(
        x=mcat_eval, y=p/p0, mode='lines+markers', name='p/p0',
        hovertemplate='m_cat: %{x:.2f} kg<br>p/p₀: %{y:.3f}'), row=2, col=1)

    # Konzentrationen
    fig.add_trace(go.Scatter(
        x=mcat_eval, y=c_A, mode='lines+markers', name='A (mol/m³)',
        hovertemplate='m_cat: %{x:.2f} kg<br>c_A: %{y:.2f}'), row=2, col=2)
    fig.add_trace(go.Scatter(
        x=mcat_eval, y=c_B, mode='lines+markers', name='B (mol/m³)',
        hovertemplate='m_cat: %{x:.2f} kg<br>c_B: %{y:.2f}'), row=2, col=2)

    fig.update_layout(
        height=700, width=950,
        legend=dict(x=1.04, y=1),
        margin=dict(t=70, l=40, r=40, b=40)
    )
    fig.update_xaxes(title_text='Katalysatormasse (kg)', row=1, col=1)
    fig.update_xaxes(title_text='Katalysatormasse (kg)', row=1, col=2)
    fig.update_xaxes(title_text='Katalysatormasse (kg)', row=2, col=1)
    fig.update_xaxes(title_text='Katalysatormasse (kg)', row=2, col=2)

    fig.update_yaxes(title_text='Umsatz X', row=1, col=1)
    fig.update_yaxes(title_text='Temperatur (K)', row=1, col=2)
    fig.update_yaxes(title_text='p/p₀', row=2, col=1)
    fig.update_yaxes(title_text='Konzentration (mol/m³)', row=2, col=2)

    return fig

#def plot_kinetik_K(T_arr, k_arr, K_arr): -> WIP
    # Erzeuge Plotly-Figur für k(T) und K(T)-> WIP

    #return fig-> WIP
