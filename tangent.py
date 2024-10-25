import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Funzione per interpretare l'input dell'utente e restituire una funzione compatibile con numpy
def parse_function(input_str):
    x = sp.symbols('x')
    try:
        # Interpreta l'espressione inserita
        symbolic_expr = sp.sympify(input_str)
        # Converte in una funzione compatibile con numpy
        func = sp.lambdify(x, symbolic_expr, 'numpy')
        return func, symbolic_expr
    except Exception as e:
        st.error(f"Errore nell'interpretazione della funzione: {e}")
        return None, None

# Funzione per tracciare la curva e le secanti
def plot_tangent_secant(func, symbolic_expr, x_point, h_value, lato):
    # Definisci i valori di x per la curva
    x_values = np.linspace(x_point - lato, x_point + lato, 500)
    y_values = func(x_values)

    # Calcola i punti della secante e la pendenza della tangente
    x_secant = x_point + h_value
    y_secant = func(x_secant)
    y_point = func(x_point)

    # Calcolo della derivata (pendenza della tangente) usando sympy
    x = sp.symbols('x')
    tangent_slope_expr = sp.diff(symbolic_expr, x)
    tangent_slope_func = sp.lambdify(x, tangent_slope_expr, 'numpy')
    tangent_slope = tangent_slope_func(x_point)

    # Valori della secante
    secant_slope = (y_secant - y_point) / h_value
    secant_line = y_point + secant_slope * (x_values - x_point)
    tangent_line = y_point + tangent_slope * (x_values - x_point)

    # Tracciamento della curva, delle secanti e della tangente
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label=f"Curva (y = {symbolic_expr})", color="blue")
    plt.scatter([x_point, x_secant], [y_point, y_secant], color="red", zorder=5)
    plt.plot(x_values, secant_line, '--', label=f"Secante (h = {h_value:.4f})", color="orange")
    plt.plot(x_values, tangent_line, ':', label="Tangente (limite delle secanti con h → 0)", color="green")

    # Etichette e legenda
    plt.title("Tangente come limite delle secanti")
    plt.xlabel("x")
    plt.ylabel("f(x)", rotation='horizontal')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt.gcf())
    plt.close()

# App Streamlit
st.title("Visualizzazione della tangente come limite delle secanti")
st.write("Inserisci una funzione qui sotto per vedere come la retta tangente si avvicina alla curva come limite delle secanti.")

# Input per la funzione
input_function = st.text_input("Inserisci una funzione di x, ad esempio 'x**2' o 'sin(x)':", value="x**2")

lato_str = st.text_input("Inserisci la lunghezza del lato della visualizzazione", value = 1.0)
lato = float(lato_str)

# Interpreta la funzione e crea una funzione compatibile con numpy
func, symbolic_expr = parse_function(input_function)

if func is not None:
    # Input per il punto x0 per la tangente
    x_point = st.text_input("Inserisci il punto x0 dove vuoi calcolare la tangente:", "1.0")
    try:
        x_point = float(x_point)  # Converte l'input in float
    except ValueError:
        st.error("Per favore, inserisci un numero valido per x0.")

    # Input per il valore di h per la secante
    h_value = st.slider("Scegli la distanza h per la retta secante", min_value=0.01, max_value=lato, value=lato/2, step=0.01)

    # Traccia la curva, la secante e la tangente
    plot_tangent_secant(func, symbolic_expr, x_point, h_value, lato)
