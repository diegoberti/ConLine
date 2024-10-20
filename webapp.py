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

def alg_vinc(f, g, x0=0,y0=0, d=1, e=0.01, cl=True, center=True, col='viridis', Blevel=False, level=0):
    x = np.arange(x0-d, x0+d, 2*d/500)
    y = np.arange(y0-d, y0+d, 2*d/500)
    X, Y = np.meshgrid(x, y)
    Z=f(X,Y)
    Z2=g(X,Y)

    fig, ax = plt.subplots(figsize=(7,7))
    #im = ax.imshow(data2d)
    
    #im = ax.imshow(Z, extent=(x0-d, x0+d, y0-d, y0+d), norm=colors.SymLogNorm(linthresh=lnrwidth, linscale=1,
                                             # vmin=Z.min(), vmax=Z.max(), base=10))
   # im = ax.imshow(Z, extent=(x0-d, x0+d, y0-d, y0+d), vmin=Z.min(), vmax=Z.max())
    im2 = ax.pcolormesh(X,Y,Z, vmin=Z.min(), vmax = Z.max(), cmap=col)
    im = ax.pcolormesh(X,Y,Z, norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=Z.min(), vmax=Z.max(), base = 10), cmap=col)
    fig.colorbar(im2, extend='both', orientation='horizontal', shrink=0.8)
    ax.set_xlabel(r"$x$", loc='center')
    ax.set_ylabel(r"$y$", loc='center', rotation = 'horizontal')
    #ax.tick_params(axis='x', labelbottom=False)

    
    CS1 = ax.contour(X,Y, Z2, [0], linewidths=1.5, alpha=0.5)

    if center:
        ax.plot(x0, y0, marker='x', color='black')

    if Blevel==True:
        ax.contour(X,Y, Z, [level], linewidths=3)
        

    return fig 

def alg(f, x0=0, y0=0, d=1, e=0.01, cl=True, center=True, col='viridis', level=0, Blevel=False):
    x = np.arange(x0 - d, x0 + d, 2 * d / 500)
    y = np.arange(y0 - d, y0 + d, 2 * d / 500)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    #fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(7, 7))
    fig1, ax1 = plt.subplots(figsize=(7, 7))
    im2 = ax1.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max(), cmap=col)
    im = ax1.pcolormesh(X, Y, Z, norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=Z.min(), vmax=Z.max(), base=10), cmap=col)
    fig1.colorbar(im2, extend='both', ax=ax1, orientation='horizontal', shrink=0.8)
    ax1.set_xlabel(r"$x$", loc='center')
    ax1.set_ylabel(r"$y$", loc='center', rotation = 'horizontal')

    fig2, ax2 = plt.subplots(figsize=(7,7))

    #levels = [f(x0, y0) + e * k for k in np.arange(-15, 15)]
    CS1 = ax2.contour(X, Y, Z, [f(x0, y0) + 2 * e * k for k in np.arange(-1, 15)], linewidths=1.5, cmap='Reds')
    CS2 = ax2.contour(X, Y, Z, [f(x0, y0) + 2 * e * k for k in np.arange(-15, 0)], linewidths=1.5, cmap='Blues_r')

    #ax2.clabel(CS1)
    #ax2.clabel(CS2)

    fig2.colorbar(CS1, extend='both', ax=ax2, orientation='horizontal', location='top')
    fig2.colorbar(CS2, extend='both', ax=ax2, orientation='horizontal', location='bottom')

    ax2.set_xlabel(r"$x$", loc='center')
    ax2.set_ylabel(r"$y$", loc='center', rotation = 'horizontal')

    if center:
        ax1.plot(x0, y0, marker='x', color='black')
        ax2.plot(x0, y0, marker='x', color='black')

    if Blevel==True:
        ax2.contour(X,Y, Z, [level], linewidths=3)

    return fig1, fig2

# Streamlit interface
st.title("Generatore di grafico dei livelli in 2D con input simbolico")

# temp =st.number_input(
#     label="test",
#     min_value=0.0000000,
#     step=0.0000001,
#     max_value=10.0000,
#     value = 0.0000045,
#     format = "%8f"
# )

# Collect user input
func_str_f = st.text_input(r"Inserisci una funzione $f(x,y)$ secondo le operazioni in codice Python (e.g., scrivi exp(x*y+x**2) per la funzione $f(x,y) \, = \,e^{x\,y\,x^2}$)", value="exp(x*y*x**2)")
vincolo = st.checkbox("Aggiungi il vincolo", value = False)
func_str_g = st.text_input(r"Inserisci una funzione $g$ tale che è visualizzato il vincolo $g(x,y)^{-1}(\{0\})$  (e.g., x**2+y**2-1 per la curva $x^2+y^2=1$)", value="x**2+y**2-1")
x0 = st.number_input(r"$x_0$ (default 0):", value=0.0, step=0.1)
y0 = st.number_input(r"$y_0$ (default 0):", value=0.0, step=0.1)
lato = st.number_input(
    r"lato del quadrato centrato in $(x_0, y_0)$ visualizzato (default 1):", 
    value=1.00, 
    step=0.01,
    format ="%f"
)
passo_attorno_f_0 =st.number_input(
    label=r"passo attorno a $f_0=f(x_0,y_0)$ (default 0.01):",
    min_value=0.0000000,
    step=0.0000001,
    max_value=10.0000,
    value = 0.01,
    format = "%f"
)
center = st.checkbox(r"Mostra $(x_0,y_0)$", value=False)
curva_livello_f = st.checkbox(r"Scegli se visualizzare una curva di livello di $f$", value=False)
livello_f = st.number_input(
    label="Scegli il livello",
    value=0.0000,
    step=0.0001,
    format="%f"
)

# Colormap selection
colormap = st.selectbox("Scegli un colore:", ['viridis', 'Greys', 'autumn', 'coolwarm'])

# When the user clicks the button, generate the plot
if st.button("Genera i grafici"):
    try:
        # Convert the input function to a callable function
        f = symbolic_to_callable(func_str_f)
        g = symbolic_to_callable(func_str_g)

        # Generate and display the contour plot
        if vincolo == False:
            fig1, fig2 = alg(f, x0, y0, lato, passo_attorno_f_0, center=center, col=colormap, level=livello_f, Blevel=curva_livello_f)
            st.pyplot(fig1)
            st.pyplot(fig2)
        if vincolo:
            fig = alg_vinc(f, g, x0, y0, lato, passo_attorno_f_0, center=center, col=colormap, level=livello_f, Blevel=curva_livello_f)
            st.pyplot(fig)
        
    except Exception as ex:
        st.error(f"Error in function input: {ex.__class__.__name__} - {ex}")
