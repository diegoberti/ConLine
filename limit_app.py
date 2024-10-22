import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import sympy as sp


def symbolic_to_callable(symbolic_str):
    """Convert a symbolic function (string) into a Python callable function."""
    x = sp.symbols('x')  # Define the symbols
    symbolic_expr = sp.sympify(symbolic_str)  # Convert the input string to a sympy expression
    func = sp.lambdify((x), symbolic_expr, modules='numpy')  # Convert sympy expression to callable
    return func

# Define a set of possible functions to choose from
def f_poly(x):
    return x**2 - 3*x + 2

def f_sin(x):
    return np.sin(x)

def f_cos(x):
    return np.cos(x)

def f_exp(x):
    return np.exp(x)

def f_log(x):
    # Use np.where to avoid log of negative numbers
    return np.where(x > 0, np.log(x+1), np.nan)

def f_tan(x):
    return np.tan(x)

def f_H(x):
    return np.heaviside(x, 0)


# Dictionary mapping function names to their implementations
functions = {
    "Polinomio: x^2 - 3x + 2": f_poly,
    "Seno: sin(x)": f_sin,
    "Coseno: cos(x)": f_cos,
    "Esponenziale: exp(x)": f_exp,
    "Logaritmo: log(x+1)": f_log,
    "Tangente: tan(x)": f_tan,
    "Salto": f_H
}

st.title("Visualizzazione grafica limiti e continuità")

insert_f = st.selectbox("Scegli la funzione", ['casualmente', 'inserendola'])


if insert_f == "casualmente":
    # Add a button for restarting the function
    if 'selected_function_name' not in st.session_state:
        st.session_state.selected_function_name, st.session_state.selected_function = random.choice(list(functions.items()))

    # When the "Restart Function" button is clicked, a new random function is selected
    if st.button("Restart"):
        st.session_state.selected_function_name, st.session_state.selected_function = random.choice(list(functions.items()))

    # Get the currently selected function and its name
    selected_function_name = st.session_state.selected_function_name
    selected_function = st.session_state.selected_function

    # Randomly select a function
    #selected_function_name, selected_function = random.choice(list(functions.items()))

    # Create the Streamlit app
    # Display the randomly selected function name
    st.write(f"Funzione selezionata: {selected_function_name}")

else:
    string_f = st.text_input(
        r"Inserisci $f(x)$ (e.g., scrivi x**2 -1 per la curva $f(x)=x^2-1$", 
        #r"Inserisci una funzione $g$ tale che è visualizzato il vincolo $g(x,y)^{-1}(\{0\})$  (e.g., scrivi x**2 + y ** 2-1 per la curva $x^2+y^2=1$)", 
        value="x**2-1"
    )
    selected_function = symbolic_to_callable(string_f)
    selected_function_name = string_f
    # Define the function for plotting and computation
    #def f(x):
    #   return np.sin(x)  # Example function, you can replace it with any function.

    # Create the Streamlit app
    #st.title("Understanding Limit and Continuity Graphically")

# Input section: user selects x0, epsilon, r
x0 = st.number_input(r"Inserisci $x_0$:", value=0.0)
epsilon = st.number_input(r"Scegli epsilon $(\varepsilon > 0)$:", min_value=0.01, value=0.5, step=0.01)
r = st.number_input(r"Segli $r$ $(r > 0)$:", min_value=0.01, value=1.0, step=0.01)

f0=selected_function(x0)

# Plot function over a wide range
if selected_function_name == f_log:

    x1 = np.linspace(x0 - 0.8, x0 + 3.2, 500)  # Wide range for plotting
    y1 = selected_function(x1)

    x2 = np.linspace(x0 - 0.8*r, x0 + 3.2*r, 500)  # Wide range for plotting
    y2 = selected_function(x2)
    
elif selected_function_name == f_tan:
    x1 = np.linspace(x0 - np.pi/2, x0 + np.pi/2, 500)  # Wide range for plotting
    y1 = selected_function(x1)

    x2 = np.linspace(x0 - r*np.pi/2, x0 + r*np.pi/2, 500)  # Wide range for plotting
    y2 = selected_function(x2)

else:
    x1 = np.linspace(x0 - 2, x0 + 2, 500)  # Wide range for plotting
    y1 = selected_function(x1)

    x2 = np.linspace(x0 - 2 * r, x0 + 2 * r, 500)  # Wide range for plotting
    y2 = selected_function(x2)



# Plot the interval (x0 - r, x0 + r)
x_zoom = np.linspace(x0 - r, x0 + r, 100)
y_zoom = selected_function(x_zoom)

# Calculate f(x0) and define the epsilon neighborhood
f0 = selected_function(x0)
f_low, f_high = f0 - epsilon, f0 + epsilon

# Plotting with Matplotlib
fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10,10))

ax1.plot(x1, y1, label=f'Grafico di f(x)', color='blue')
ax1.scatter(x0,f0, marker='x')

if selected_function_name == "Tangente: tan(x)":
    ax1.set_ylim(-100,100)
    ax1.set_xlim(x0-np.pi/2,x0+np.pi/2)

    ax2.set_ylim(-100,100)
    ax2.set_ylim(x0-r*np.pi/2,x0+r*np.pi/2)


# Plot the main graph of the function
ax2.plot(x2, y2, label=f'Grafico di f(x)', color='blue')

# Highlight the segment (x0-r, x0+r)
ax2.plot(x_zoom, y_zoom, color='orange', label=f'Segmento attorno x0')

# Highlight the neighborhood (f(x0)-epsilon, f(x0)+epsilon) on y-axis
ax2.hlines([f_low, f_high], x0 - 2 * r, x0 + 2 * r, colors='green', linestyles='dashed', label='ε-intorno')

# Mark the point x0 and its corresponding f(x0)
ax2.scatter([x0], [f0], color='red', zorder=5, label=f'f(x0) = {f0}')


# Add labels and legends
ax2.set_xlabel('x')
ax2.set_ylabel('f(x)', rotation = 'horizontal')
ax2.axvline(x0, color='red', linestyle='--', label='x = x0')
ax2.legend(bbox_to_anchor=(1.1, 1.05))



# Show the graph
st.pyplot(fig)

# Add explanation about the limit and continuity
st.markdown(f"""
### Spiegazione:
Il grafico mostra la funzione `f(x)` disegnata su un range attorno al punto `x0 = {x0}`. 
Scegliamo un intorno di `{epsilon}`, i.e., l'intervallo `({f_low}, {f_high})` sull'asse y.

Il segmento aranciano sull'asse x corrisponde all'intervallo `({x0 - r}, {x0 + r})`. 

Per visualizzare il concetto di continuità, vediamo come `x` si avvicina a `x0`, il valore di `f(x)` sta entro le linee verdi (the ε-neighborhood) 
attorno a `f(x0)`. Questo dimostra come possiamo rendere `f(x)` vicino quanto vogliamo a `f(x0)` restringendo `x` ad un intervallo piccolo a sufficienza di `x0`.

Questa è una rappresentazione visuale della definzione di continuità: Per ogni ε > 0, esiste un δ > 0 tale che se`|x - x0| < δ`, 
allora `|f(x) - f(x0)| < ε`.
""")
