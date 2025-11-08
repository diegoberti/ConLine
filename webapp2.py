import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import sympy as sp
import io

def symbolic_to_callable(symbolic_str):
    """Convert a symbolic function (string) into a Python callable function with validation."""
    x, y = sp.symbols('x y')
    try:
        symbolic_expr = sp.sympify(symbolic_str)
        # Check that only x, y are used
        if not symbolic_expr.free_symbols.issubset({x, y, sp.S.EmptySet}):
            raise ValueError("La funzione deve contenere solo le variabili x e y")
        func = sp.lambdify((x, y), symbolic_expr, modules='numpy')
        return func
    except Exception as e:
        raise ValueError(f"Funzione non valida: {str(e)}")

def create_base_plot(X, Y, Z, colormap, figsize=(7, 7)):
    """Create the base heatmap plot with logarithmic scaling."""
    fig, ax = plt.subplots(figsize=figsize)
    
    # Regular colormap for colorbar
    im2 = ax.pcolormesh(X, Y, Z, vmin=Z.min(), vmax=Z.max(), cmap=colormap)
    # Logarithmic scaling for actual plot
    im = ax.pcolormesh(X, Y, Z, 
                       norm=colors.SymLogNorm(linthresh=0.5, linscale=1, 
                                             vmin=Z.min(), vmax=Z.max(), base=10), 
                       cmap=colormap)
    
    fig.colorbar(im2, extend='both', orientation='horizontal', shrink=0.8)
    ax.set_xlabel(r"$x$", loc='center')
    ax.set_ylabel(r"$y$", loc='center', rotation='horizontal')
    ax.set_aspect('equal')
    
    return fig, ax

def create_contour_plot(X, Y, Z, f0, passo, figsize=(7, 7)):
    """Create the contour plot with level curves around f0."""
    fig, ax = plt.subplots(figsize=figsize)
    
    # Positive levels (red)
    CS1 = ax.contour(X, Y, Z, [f0 + 2 * passo * k for k in np.arange(1, 16)], 
                     linewidths=1.5, cmap='Reds')
    # Level at f0 (black)
    ax.contour(X, Y, Z, [f0], linewidths=1.5, colors='black')
    # Negative levels (blue)
    CS2 = ax.contour(X, Y, Z, [f0 + 2 * passo * k for k in np.arange(-15, 0)], 
                     linewidths=1.5, cmap='Blues_r')
    
    fig.colorbar(CS1, extend='both', ax=ax, orientation='horizontal', location='top')
    fig.colorbar(CS2, extend='both', ax=ax, orientation='horizontal', location='bottom')
    
    ax.set_xlabel(r"$x$", loc='center')
    ax.set_ylabel(r"$y$", loc='center', rotation='horizontal')
    ax.set_aspect('equal')
    
    return fig, ax

def plot_with_constraint(f, g, x0, y0, d, colormap, center=True, level=0, show_level=False):
    """Generate plot with constraint visualization."""
    # Adaptive resolution
    n_points = min(500, max(100, int(500 * d)))
    x = np.linspace(x0 - d, x0 + d, n_points)
    y = np.linspace(y0 - d, y0 + d, n_points)
    X, Y = np.meshgrid(x, y)
    
    Z = f(X, Y)
    Z2 = g(X, Y)
    
    fig, ax = create_base_plot(X, Y, Z, colormap)
    
    # Add constraint contour
    ax.contour(X, Y, Z2, [0], linewidths=1.5, alpha=0.5, colors='white')
    
    if center:
        ax.plot(x0, y0, marker='x', color='black', markersize=10, markeredgewidth=2)
    
    if show_level:
        ax.contour(X, Y, Z, [level], linewidths=3, colors='lime')
    
    return fig

def plot_without_constraint(f, x0, y0, d, passo, colormap, center=True, level=0, show_level=False):
    """Generate heatmap and contour plots without constraint."""
    # Adaptive resolution
    n_points = min(500, max(100, int(500 * d)))
    x = np.linspace(x0 - d, x0 + d, n_points)
    y = np.linspace(y0 - d, y0 + d, n_points)
    X, Y = np.meshgrid(x, y)
    
    Z = f(X, Y)
    f0 = f(x0, y0)
    
    # Create heatmap
    fig1, ax1 = create_base_plot(X, Y, Z, colormap)
    
    if center:
        ax1.plot(x0, y0, marker='x', color='black', markersize=10, markeredgewidth=2)
    
    if show_level:
        ax1.contour(X, Y, Z, [level], linewidths=3, colors='lime')
    
    # Create contour plot
    fig2, ax2 = create_contour_plot(X, Y, Z, f0, passo)
    
    if center:
        ax2.plot(x0, y0, marker='x', color='black', markersize=10, markeredgewidth=2)
    
    if show_level:
        ax2.contour(X, Y, Z, [level], linewidths=3, colors='lime')
    
    return fig1, fig2

def fig_to_bytes(fig):
    """Convert matplotlib figure to bytes for download."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf

# Streamlit interface
st.title("Esplora le curve di livello")

# Domain selection
st.markdown(
    r"<span style='color:#1f4e79'>$\bullet$ Scegli il quadrato $Q$ centrato in $(x_0, y_0)$ e di lato $2\ell$</span>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    str_x0 = st.text_input(r"Scegli $x_0$ (default 0):", value="0")

with col2:
    str_y0 = st.text_input(r"Scegli $y_0$ (default 0):", value="0")

with col3:
    lato = st.number_input(
        r"Scegli $\ell$ (default 1):",
        value=1.00,
        min_value=0.01,
        step=0.01,
        format="%f"
    )

center = st.checkbox(r"Mostra $(x_0, y_0)$", value=False)

# Function input
st.markdown(
    r"<span style='color:#1f4e79'>$\bullet$ Scegli la funzione $f$</span>",
    unsafe_allow_html=True
)
func_str_f = st.text_input(
    r"Inserisci una funzione $f(x,y)$ secondo le operazioni in codice Python",
    value="exp(x*y+x**2)"
)

# Help expander
with st.expander("📖 Mostra la guida per la sintassi Python"):
    st.markdown("""
    **Sintassi per scrivere funzioni matematiche in Python:**

    - **Potenze**: `x**2` per $x^2$, `x**3` per $x^3$, `x**(1/3)` per $x^{1/3}$
    - **Moltiplicazioni**: `3*x` per $3x$, `x*y` per $xy$
    - **Esponenziale**: `exp(x)` per $e^{x}$ 
    - **Trigonometriche**: `sin(x)`, `cos(x)`, `tan(x)`, `sin(x + y)`
    - **Logaritmi**: `log(x)`, `log10(x)` per logaritmi naturali e base 10
    - **Radici quadrate**: `sqrt(x)` per $\sqrt{x}$
    - **Altre funzioni comuni**: `abs(x)` per $|x|$
    
    **Esempi:**
    - `exp(x*y + x**2)` per $e^{xy + x^2}$
    - `sin(x + y)` per $\sin(x + y)$
    - `log(x**2 + y**2 + 1)` per $\log(x^2 + y^2+1)$
    """)

# Colormap selection
colormap = st.selectbox(
    r"Scegli un colorset per i livelli di $f$:", 
    ['viridis', 'Greys', 'autumn', 'coolwarm']
)

# Step size input
passo_str = st.text_input(
    label=r"Scegli il passo con cui visualizzare le curve di livello attorno a $f_0=f(x_0,y_0)$ (default 0.01):",
    value="0.01"
)

# Constraint option
vincolo = st.checkbox("Aggiungi il vincolo 👇", value=False)
func_str_g = None
if vincolo:
    func_str_g = st.text_input(
        r"Inserisci $g(x,y)$ per il vincolo $g(x,y)=0$ (e.g., x**2 + y**2 - 1 per il cerchio unitario)", 
        value="x**2+y**2-1"
    )

# Level curve option
curva_livello_f = st.checkbox(r"Visualizza una curva di livello specifica di $f$ 👇", value=False)
liv_f_str = None
if curva_livello_f:
    liv_f_str = st.text_input("Scegli il livello:", value="0")

# Generate plots button
if st.button("Genera i grafici"):
    try:
        # Parse and validate inputs
        x0 = float(sp.sympify(str_x0))
        y0 = float(sp.sympify(str_y0))
        passo = float(sp.sympify(passo_str))
        
        if passo <= 0:
            st.error("Il passo deve essere positivo")
            st.stop()
        
        if lato <= 0:
            st.error("Il lato deve essere positivo")
            st.stop()
        
        # Convert function
        f = symbolic_to_callable(func_str_f)
        
        # Test function at center
        f0_val = f(x0, y0)
        if not np.isfinite(f0_val):
            st.warning(f"⚠️ La funzione non è definita o è infinita in ({x0}, {y0})")
            st.stop()
        
        # Show function value at center
        st.info(f"✓ $f({x0}, {y0}) = {f0_val:.6f}$")
        
        # Parse level if specified
        livello_f = 0
        if curva_livello_f and liv_f_str:
            livello_f = float(sp.sympify(liv_f_str))
        
        # Generate plots
        if vincolo:
            g = symbolic_to_callable(func_str_g)
            fig = plot_with_constraint(f, g, x0, y0, lato, colormap, 
                                      center=center, level=livello_f, 
                                      show_level=curva_livello_f)
            st.pyplot(fig)
            
            # Download button
            buf = fig_to_bytes(fig)
            st.download_button(
                label="📥 Scarica il grafico (PNG)",
                data=buf,
                file_name=f"level_curves_constraint_{x0}_{y0}.png",
                mime="image/png"
            )
        else:
            fig1, fig2 = plot_without_constraint(f, x0, y0, lato, passo, colormap,
                                                center=center, level=livello_f,
                                                show_level=curva_livello_f)
            
            st.subheader("Mappa di calore")
            st.pyplot(fig1)
            buf1 = fig_to_bytes(fig1)
            st.download_button(
                label="📥 Scarica mappa di calore (PNG)",
                data=buf1,
                file_name=f"heatmap_{x0}_{y0}.png",
                mime="image/png",
                key="download1"
            )
            
            st.subheader("Curve di livello")
            st.pyplot(fig2)
            buf2 = fig_to_bytes(fig2)
            st.download_button(
                label="📥 Scarica curve di livello (PNG)",
                data=buf2,
                file_name=f"contours_{x0}_{y0}.png",
                mime="image/png",
                key="download2"
            )
        
    except ValueError as ve:
        st.error(f"❌ Errore di validazione: {ve}")
    except Exception as ex:
        st.error(f"❌ Errore: {ex.__class__.__name__} - {ex}")
