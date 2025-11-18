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

def generate_heatmap(f, g, x0, y0, d, colormap, center=True, level=0, show_level=False, with_constraint=False):
    """Generate heatmap with optional constraint."""
    # Adaptive resolution
    n_points = min(500, max(100, int(500 * d)))
    x = np.linspace(x0 - d, x0 + d, n_points)
    y = np.linspace(y0 - d, y0 + d, n_points)
    X, Y = np.meshgrid(x, y)
    
    Z = f(X, Y)
    
    fig, ax = create_base_plot(X, Y, Z, colormap)
    
    # Add constraint contour if requested
    if with_constraint and g is not None:
        Z2 = g(X, Y)
        ax.contour(X, Y, Z2, [0], linewidths=1.5, alpha=0.5, colors='white')
    
    if center:
        ax.plot(x0, y0, marker='x', color='black', markersize=10, markeredgewidth=2)
    
    if show_level:
        ax.contour(X, Y, Z, [level], linewidths=3, colors='lime')
    
    return fig

def generate_contour(f, x0, y0, d, passo, center=True, level=0, show_level=False):
    """Generate contour plot."""
    # Adaptive resolution
    n_points = min(500, max(100, int(500 * d)))
    x = np.linspace(x0 - d, x0 + d, n_points)
    y = np.linspace(y0 - d, y0 + d, n_points)
    X, Y = np.meshgrid(x, y)
    
    Z = f(X, Y)
    f0 = f(x0, y0)
    
    # Create contour plot
    fig, ax = create_contour_plot(X, Y, Z, f0, passo)
    
    if center:
        ax.plot(x0, y0, marker='x', color='black', markersize=10, markeredgewidth=2)
    
    if show_level:
        ax.contour(X, Y, Z, [level], linewidths=3, colors='lime')
    
    return fig

def fig_to_bytes(fig):
    """Convert matplotlib figure to bytes for download."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return buf

# Streamlit interface
st.title("Esplora le curve di livello")

# Domain selection
st.subheader(r"$\bullet$ Scegli il quadrato $Q$ centrato in $(x_0, y_0)$ e di lato $2\ell$")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    str_x0 = st.text_input(r"Scegli $x_0$:", value="0")

with col2:
    str_y0 = st.text_input(r"Scegli $y_0$:", value="0")

with col3:
    center = st.checkbox(r"Mostra $(x_0, y_0)$", value=False)

with col4:
    lato_str = st.text_input(r"Scegli $\ell$:", value="1")

# Function input
st.subheader(r"$\bullet$ Scegli la funzione $f$")

col_func, col_help = st.columns([1, 1])

with col_func:
    func_str_f = st.text_input(
        r"Inserisci $f(x,y)$ secondo la sintassi Python",
        value="exp(x*y+x**2)"
    )

with col_help:
    # Help expander
    st.write("")
    st.write("")
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

# Section 1: Generate contour plot
st.subheader(r"$\bullet$ Genera curve di livello attorno a $f(x_0,y_0)$")

passo_str = st.text_input(
    label=r"Scegli la differenza tra i valori dei livelli partendo da $f_0=f(x_0,y_0)$:",
    value="0.01",
    key="passo_contour"
)

curva_livello_contour = st.checkbox(r"Visualizza una curva di livello specifica", value=False, key="level_contour")
liv_contour_str = None
if curva_livello_contour:
    liv_contour_str = st.text_input("Scegli il livello:", value="0", key="level_value_contour")

if st.button("Genera curve di livello"):
    try:
        # Parse and validate inputs
        x0 = float(sp.sympify(str_x0))
        y0 = float(sp.sympify(str_y0))
        lato = float(sp.sympify(lato_str))
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
        
        # Show function value at center with minimal decimal places
        if f0_val == int(f0_val):
            f0_display = f"{int(f0_val)}"
        else:
            f0_display = f"{f0_val:.6g}"
        
        st.info(f"$f(x_0, y_0) = {f0_display}$")
        
        # Parse level if specified
        livello_contour = 0
        if curva_livello_contour and liv_contour_str:
            livello_contour = float(sp.sympify(liv_contour_str))
        
        # Generate contour plot
        fig = generate_contour(f, x0, y0, lato, passo, 
                              center=center, level=livello_contour,
                              show_level=curva_livello_contour)
        
        st.subheader("Curve di livello di $f$ in $Q$")
        st.pyplot(fig)
        
        buf = fig_to_bytes(fig)
        st.download_button(
            label="📥 Scarica curve di livello (PNG)",
            data=buf,
            file_name=f"contours_{x0}_{y0}.png",
            mime="image/png",
            key="download_contour"
        )
        
    except ValueError as ve:
        st.error(f"❌ Errore di validazione: {ve}")
    except Exception as ex:
        st.error(f"❌ Errore: {ex.__class__.__name__} - {ex}")


# Section 2: Generate heatmap
st.subheader(r"$\bullet$ Genera la mappa dei valori di $f$ in $Q$")

colormap_heat = st.selectbox(
    r"Scegli un colorset:", 
    ['viridis', 'Greys', 'autumn', 'coolwarm'],
    key="colormap_heat"
)

vincolo_heat = st.checkbox("Aggiungi il vincolo", value=False, key="vincolo_heat")
func_str_g_heat = None
if vincolo_heat:
    func_str_g_heat = st.text_input(
        r"Inserisci $g(x,y)$ per il vincolo $g(x,y)=0$:", 
        value="x**2+y**2-1",
        key="constraint_heat"
    )

curva_livello_heat = st.checkbox(r"Visualizza una curva di livello specifica", value=False, key="level_heat")
liv_heat_str = None
if curva_livello_heat:
    liv_heat_str = st.text_input("Scegli il livello:", value="0", key="level_value_heat")

if st.button("Genera mappa di calore"):
    try:
        # Parse and validate inputs
        x0 = float(sp.sympify(str_x0))
        y0 = float(sp.sympify(str_y0))
        lato = float(sp.sympify(lato_str))
        
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
        
        # Show function value at center with minimal decimal places
        if f0_val == int(f0_val):
            f0_display = f"{int(f0_val)}"
        else:
            f0_display = f"{f0_val:.6g}"
        
        st.info(f"$f(x_0, y_0) = {f0_display}$")
        
        # Parse constraint if specified
        g = None
        if vincolo_heat and func_str_g_heat:
            g = symbolic_to_callable(func_str_g_heat)
        
        # Parse level if specified
        livello_heat = 0
        if curva_livello_heat and liv_heat_str:
            livello_heat = float(sp.sympify(liv_heat_str))
        
        # Generate heatmap
        fig = generate_heatmap(f, g, x0, y0, lato, colormap_heat, 
                              center=center, level=livello_heat, 
                              show_level=curva_livello_heat, with_constraint=vincolo_heat)
        
        st.subheader("Mappa dei valori di $f$ in $Q$")
        st.pyplot(fig)
        
        buf = fig_to_bytes(fig)
        st.download_button(
            label="📥 Scarica mappa (PNG)",
            data=buf,
            file_name=f"heatmap_{x0}_{y0}.png",
            mime="image/png",
            key="download_heat"
        )
        
    except ValueError as ve:
        st.error(f"❌ Errore di validazione: {ve}")
    except Exception as ex:
        st.error(f"❌ Errore: {ex.__class__.__name__} - {ex}")

