import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import sympy as sp
import io
import plotly.graph_objects as go

def symbolic_to_callable(symbolic_str):
    """Convert a symbolic function (string) into a Python callable function."""
    x, y = sp.symbols('x y')  # Define the symbols
    symbolic_expr = sp.sympify(symbolic_str)  # Convert the input string to a sympy expression
    func = sp.lambdify((x, y), symbolic_expr, modules='numpy')  # Convert sympy expression to callable
    return func

def alg_vinc(f, g, x0=0,y0=0, d=1, e=0.01, cl=True, center=True, col='viridis', Blevel=False, level=0, dplot=False, cplot=False):
    x = np.arange(x0-d, x0+d, 2*d/500)
    y = np.arange(y0-d, y0+d, 2*d/500)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    Z2 = g(X, Y)

    fig1, ax1 = plt.subplots(figsize=(7,7))
    im2 = ax1.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max(), cmap=col)
    im = ax1.pcolormesh(X, Y, Z, norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=Z.min(), vmax=Z.max(), base=10), cmap=col)
    fig1.colorbar(im2, extend='both', orientation='horizontal', shrink=0.8)
    ax1.set_xlabel(r"$x$", loc='center')
    ax1.set_ylabel(r"$y$", loc='center', rotation='horizontal')

    CS1 = ax1.contour(X, Y, Z2, [0], linewidths=1.5, alpha=0.5)

    if center:
        ax1.plot(x0, y0, marker='x', color='black')

    if Blevel:
        ax1.contour(X, Y, Z, [level], linewidths=3)

    fig2 = fig1
    fig3 = None

    if dplot:
        fig3 = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.6)])
        z2_contour = np.zeros_like(Z)
        z2_contour[Z2 == 0] = Z[Z2 == 0]
        fig3.add_trace(go.Surface(z=z2_contour, x=X, y=Y, showscale=False, colorscale='Reds', opacity=1))
        fig3.update_layout(title='Grafico 3D interattivo',
                           scene=dict(
                               xaxis_title='X axis',
                               yaxis_title='Y axis',
                               zaxis_title='Z axis'
                           ))
        
    

    return fig1, fig2, fig3

def alg(f, x0=0, y0=0, d=1, e=0.01, cl=True, center=True, col='viridis', level=0, Blevel=False, dplot=False, cplot=False):
    x = np.arange(x0 - d, x0 + d, 2 * d / 500)
    y = np.arange(y0 - d, x0 + d, 2 * d / 500)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig1, ax1 = plt.subplots(figsize=(7, 7))
    im2 = ax1.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max(), cmap=col)
    im = ax1.pcolormesh(X, Y, Z, norm=colors.SymLogNorm(linthresh=0.5, linscale=1, vmin=Z.min(), vmax=Z.max(), base=10), cmap=col)
    fig1.colorbar(im2, extend='both', ax=ax1, orientation='horizontal', shrink=0.8)
    ax1.set_xlabel(r"$x$", loc='center')
    ax1.set_ylabel(r"$y$", loc='center', rotation='horizontal')

    fig2, ax2 = plt.subplots(figsize=(7,7))
    f0 = f(x0, y0)
    CS1 = ax2.contour(X, Y, Z, [f0 + 2 * e * k for k in np.arange(1, 16)], linewidths=1.5, cmap='Reds')
    ax2.contour(X, Y, Z, [f0], linewidths=1.5, colors='black')
    CS2 = ax2.contour(X, Y, Z, [f0 + 2 * e * k for k in np.arange(-15, 0)], linewidths=1.5, cmap='Blues_r')
    fig2.colorbar(CS1, extend='both', ax=ax2, orientation='horizontal', location='top')
    fig2.colorbar(CS2, extend='both', ax=ax2, orientation='horizontal', location='bottom')

    ax2.set_xlabel(r"$x$", loc='center')
    ax2.set_ylabel(r"$y$", loc='center', rotation='horizontal')

    if center:
        ax1.plot(x0, y0, marker='x', color='black')
        ax2.plot(x0, y0, marker='x', color='black')

    if Blevel:
        ax2.contour(X, Y, Z, [level], linewidths=3)

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')

    fig3 = None

    if dplot:
        fig3 = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.6)])
        f0_contour = np.zeros_like(Z)
        f0_contour[Z == f0] = Z[Z == f0]
        #fig3.add_trace(go.Surface(z=f0_contour, x=X, y=Y, showscale=False, colorscale='Reds', opacity=1))
        fig3.update_layout(title='Interactive 3D Surface Plot',
                           scene=dict(
                               xaxis_title='X axis',
                               yaxis_title='Y axis',
                               zaxis_title='Z axis'
                           ))
        
    if cplot:

        #fig3, ax3 = plt.figure().add_subplot(projection='3d')
        fig4 = plt.figure(figsize=(10, 7)) 
        ax4 = fig4.add_subplot(111, projection='3d')

        vmin = Z.min()
        vmax = Z.max()
        f0 = f(x0,y0)
        #levels = [f0 + e * k for k in np.arange(-15, 15)]
        ax4.contour(X, Y, Z, [f0 + 2 * e * k for k in np.arange(1, 16)], linewidths=1.5, cmap='Reds')
        ax4.contour(X,Y,Z, [f0], linewidths=1.5, colors='black')
        ax4.contour(X, Y, Z, [f0 + 2 * e * k for k in np.arange(-15, 0)], linewidths=1.5, cmap='Blues_r')

        #if vmax > 0:
         #   ax3.contour(X, Y, Z, c_range, cmap='Reds', linewidths=1.5)

        #if vmin < 0:
         #   ax3.contour(X, Y, Z, c_range2, cmap='Blues_r', linewidths=1.5)

        #ax2.contour(X,Y,Z, [0], linewidths=1.5)
        ax4.plot_surface(X, Y, Z, cmap="coolwarm", rstride=1, cstride=1, alpha=0.2)
    
    if cplot == False:
        fig4 = fig2

    return fig1, fig2, fig3, fig4

# Streamlit interface
st.title("Generatore di grafico dei livelli in 2D con input simbolico")

func_str_f = st.text_input(r"Inserisci una funzione $f(x,y)$ secondo le operazioni in codice Python (e.g., scrivi exp(x*y+x**2) per la funzione $f(x,y) \, = \,e^{x\,y+x^2}$)", value="exp(x*y+x**2)")

col1, col2 = st.columns(2)
with col1:
    str_x0 = st.text_input(r"Scegli $x_0$ (default 0):", value=0.0)
    x0 = float(sp.sympify(str_x0))
with col2:
    str_y0 = st.text_input(r"Scegli $y_0$ (default 0):", value=0.0)
    y0 = float(sp.sympify(str_y0))
    
center = st.checkbox(r"Mostra $(x_0,y_0)$", value=False)

lato = st.number_input(
    r"Scegli la lunghezza del lato del quadrato centrato in $(x_0, y_0)$ visualizzato (default 1):", 
    value=1.00, 
    step=0.01,
    format ="%f"
)

colormap = st.selectbox(r"Scegli un colorset per i livelli di $f$:", ['viridis', 'Greys', 'autumn', 'coolwarm'])

passo_attorno_f_0 = st.number_input(
    label=r"Scegli il passo con cui visualizzare le curv di livello, con livelli attorno a $f_0=f(x_0,y_0)$ (default 0.01):",
    min_value=0.0000000,
    step=0.0000001,
    max_value=10.0000,
    value=0.01,
    format="%f"
)

vincolo = st.checkbox("Aggiungi il vincolo 👇", value=False)
if vincolo:
    func_str_g = st.text_input(
        r"Inserisci $g(x,y)$ (e.g., scrivi x**2 + 2*y-1 per la curva $x^2+2\,y=1$), per il vincolo $g(x,y)^{-1}(\{0\})$", 
        value="x**2+y**2-1"
    )

#st.subheader(r"Scegli un eventuale livello di $f$ che vuoi visualizzare nel quadrato scelto")
curva_livello_f = st.checkbox(r"Scegli se visualizzare una curva di livello di $f$ 👇", value=False)
if curva_livello_f:
    liv_f_str = st.text_input("Scegli il livello:", value=0.0)
    livello_f = float(sp.sympify(liv_f_str))
else:
    livello_f=0
    #st.write("Seleziona la checkbox per inserire il livello che vuoi visualizzare")

dplot_f = st.checkbox(r"Scegli se visualizzare il grafico interattivo in 3D", value=False)

cplot_f = st.checkbox(r"Scegli se visualizzare il grafico statico in 3D con i livelli", value=False)



# When the user clicks the button, generate the plot
if st.button("Genera i grafici"):
    try:
        # Convert the input function to a callable function
        f = symbolic_to_callable(func_str_f)
        if vincolo:
            g = symbolic_to_callable(func_str_g)

        # Generate and display the contour plot
        if vincolo == False:
            fig1, fig2, fig3, fig4 = alg(f, x0, y0, lato, passo_attorno_f_0, center=center, col=colormap, level=livello_f, Blevel=curva_livello_f, dplot = dplot_f, cplot = cplot_f)
            if not dplot_f and not cplot_f:
                st.pyplot(fig1)
                st.pyplot(fig2)
            if cplot_f and not dplot_f:
                st.pyplot(fig2)
                st.pyplot(fig4)
            if dplot_f and not cplot_f:
                st.pyplot(fig1)
                st.plotly_chart(fig3)
            if cplot_f and dplot_f:
                st.pyplot(fig1)
                st.plotly_chart(fig3)
                st.pyplot(fig2)
                st.pyplot(fig4)

        if vincolo:
            fig1, fig2 = alg_vinc(f, g, x0, y0, lato, passo_attorno_f_0, center=center, col=colormap, level=livello_f, Blevel=curva_livello_f)
            if dplot_f:
                st.pyplot(fig1)
                st.pyplot(fig2)
            if dplot_f == False:
                st.pyplot(fig1)
        
    except Exception as ex:
        st.error(f"Error in function input: {ex.__class__.__name__} - {ex}")
