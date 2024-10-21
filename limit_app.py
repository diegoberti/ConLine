import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

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
    "Polynomial: x^2 - 3x + 2": f_poly,
    "Sine: sin(x)": f_sin,
    "Cosine: cos(x)": f_cos,
    "Exponential: exp(x)": f_exp,
    "Logarithm: log(x+1)": f_log,
    "Tangent: tan(x)": f_tan,
    "Salto": f_H
}

# Add a button for restarting the function
if 'selected_function_name' not in st.session_state:
    st.session_state.selected_function_name, st.session_state.selected_function = random.choice(list(functions.items()))

# When the "Restart Function" button is clicked, a new random function is selected
if st.button("Restart Function"):
    st.session_state.selected_function_name, st.session_state.selected_function = random.choice(list(functions.items()))

# Get the currently selected function and its name
selected_function_name = st.session_state.selected_function_name
selected_function = st.session_state.selected_function

# Randomly select a function
#selected_function_name, selected_function = random.choice(list(functions.items()))

# Create the Streamlit app
st.title("Understanding Limit and Continuity Graphically")

# Display the randomly selected function name
st.write(f"Selected Function: {selected_function_name}")

# Define the function for plotting and computation
#def f(x):
 #   return np.sin(x)  # Example function, you can replace it with any function.

# Create the Streamlit app
#st.title("Understanding Limit and Continuity Graphically")

# Input section: user selects x0, epsilon, r
x0 = st.number_input("Enter the point x0:", value=0.0)
epsilon = st.number_input("Choose epsilon (ε > 0):", min_value=0.01, value=0.5, step=0.01)
r = st.number_input("Choose radius r (r > 0):", min_value=0.01, value=1.0, step=0.01)

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

ax1.plot(x1, y1, label=f'Graph of f(x)', color='blue')
ax1.scatter(x0,f0, marker='x')

if selected_function_name == "Tangent: tan(x)":
    ax1.set_ylim(-100,100)
    ax1.set_xlim(x0-np.pi/2,x0+np.pi/2)

    ax2.set_ylim(-100,100)
    ax2.set_ylim(x0-r*np.pi/2,x0+r*np.pi/2)


# Plot the main graph of the function
ax2.plot(x2, y2, label=f'Graph of f(x)', color='blue')

# Highlight the segment (x0-r, x0+r)
ax2.plot(x_zoom, y_zoom, color='orange', label=f'Segment around x0')

# Highlight the neighborhood (f(x0)-epsilon, f(x0)+epsilon) on y-axis
ax2.hlines([f_low, f_high], x0 - 2 * r, x0 + 2 * r, colors='green', linestyles='dashed', label='ε-neighborhood')

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
### Explanation:
The graph shows the function `f(x)` plotted over a range around the point `x0 = {x0}`. 
We have chosen an epsilon neighborhood of `{epsilon}`, i.e., the interval `({f_low}, {f_high})` on the y-axis.

The highlighted orange segment on the x-axis corresponds to the interval `({x0 - r}, {x0 + r})`. 

To visualize the concept of continuity, we see that as `x` approaches `x0`, the values of `f(x)` stay within the green dashed lines (the ε-neighborhood) 
around `f(x0)`. This demonstrates how we can make `f(x)` as close as we like to `f(x0)` by restricting `x` to a small enough interval around `x0`.

This is a visual representation of the definition of continuity: For every ε > 0, there exists a δ > 0 such that if `|x - x0| < δ`, 
then `|f(x) - f(x0)| < ε`.
""")
