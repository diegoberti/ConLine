import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import sympy as sp
import io

def symbolic_to_callable(symbolic_str):
    """Convert a symbolic function (string) into a Python callable function."""
    x, y = sp.symbols('x y')  # Define the symbols
    symbolic_expr = sp.sympify(symbolic_str)  # Convert the input string to a sympy expression
    func = sp.lambdify((x, y), symbolic_expr, modules='numpy')  # Convert sympy expression to callable
    return func

def alg(f, x0=0, y0=0, d=1, e=0.01, cl=True, center=True, col='Greys'):
    x = np.arange(x0 - d, x0 + d, 2 * d / 500)
    y = np.arange(y0 - d, y0 + d, 2 * d / 500)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(7, 7))
    im2 = ax1.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max(), cmap=col)
    im = ax1.pcolormesh(X, Y, Z, norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=Z.min(), vmax=Z.max(), base=10), cmap=col)
    fig.colorbar(im2, extend='both', ax=ax1, orientation='horizontal', shrink=0.8)
    ax1.tick_params(axis='x', labelbottom=False)

    levels = [f(x0, y0) + e * k for k in np.arange(-15, 15)]
    CS1 = ax2.contour(X, Y, Z, [f(x0, y0) + 2 * e * k for k in np.arange(-1, 15)], linewidths=1.5, cmap='Reds')
    ax2.contour(X,Y,Z, [0], lw=1.5, colors='black')
    CS2 = ax2.contour(X, Y, Z, [f(x0, y0) + 2 * e * k for k in np.arange(-15, 0)], linewidths=1.5, cmap='Blues_r')

    ax2.clabel(CS1)
    ax2.clabel(CS2)

    fig.colorbar(CS1, extend='both', ax=ax2, orientation='horizontal', location='top')
    fig.colorbar(CS2, extend='both', ax=ax2, orientation='horizontal', location='bottom')

    if center:
        ax1.plot(x0, y0, marker='o', color='black')
        ax2.plot(x0, y0, marker='o', color='black')

    return fig

# Streamlit interface
st.title("Contour Plot Generator with Symbolic Input")

# Collect user input
func_str = st.text_input("Enter a function of x and y (e.g., sin(x) + cos(y))", value="sin(x) + cos(y)")
x0 = st.number_input("x0 (default 0):", value=0.0, step=0.1)
y0 = st.number_input("y0 (default 0):", value=0.0, step=0.1)
d = st.number_input("d (default 1):", value=1.0, step=0.1)
e = st.number_input("e (default 0.01):", value=0.01, step=0.01)
center = st.checkbox("Show center point", value=True)

# Colormap selection
colormap = st.selectbox("Choose a colormap:", ['Greys', 'autumn', 'coolwarm', 'viridis'])

# When the user clicks the button, generate the plot
if st.button("Generate Plot"):
    try:
        # Convert the input function to a callable function
        f = symbolic_to_callable(func_str)

        # Generate and display the contour plot
        fig = alg(f, x0, y0, d, e, center=center, col=colormap)
        st.pyplot(fig)
    except Exception as ex:
        st.error(f"Error in function input: {ex.__class__.__name__} - {ex}")
