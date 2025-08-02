import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_tax_comparison(visualization_data):
    """Render a tax comparison graph"""
    # Extract data
    labels = visualization_data.get("labels", ["Old Regime", "New Regime"])
    values = visualization_data.get("values", [0, 0])
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set bar positions
    x = np.arange(len(labels))
    width = 0.6
    
    # Create bars
    bars = ax.bar(x, values, width, color=['#6B73FF', '#000DFF'])
    
    # Add labels and title
    ax.set_xlabel('Tax Regime', fontsize=12, color='white')
    ax.set_ylabel('Tax Amount (₹)', fontsize=12, color='white')
    ax.set_title('Tax Regime Comparison', fontsize=14, fontweight='bold', color='white')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, color='white')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'₹{height:,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, color='white')
    
    # Highlight the better regime
    better_index = 0 if values[0] < values[1] else 1
    bars[better_index].set_color('#4CAF50')  # Green color for better option
    
    # Calculate savings
    savings = abs(values[0] - values[1])
    savings_text = f"Savings with {labels[better_index]}: ₹{savings:,.2f}"
    
    # Add savings text
    ax.text(0.5, -0.15, savings_text, transform=ax.transAxes, ha='center', fontsize=12, color='white')
    
    # Set background color
    ax.set_facecolor('#1E1E1E')
    fig.patch.set_facecolor('#1E1E1E')
    
    # Customize grid and spines
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Customize ticks
    ax.tick_params(axis='both', colors='white')
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig)
    
    # Add download button for the graph
    st.download_button(
        label="Download Graph",
        data=None,  # In a real implementation, we would save the figure to a BytesIO object
        file_name="tax_comparison.png",
        mime="image/png",
        disabled=True  # Disabled for now as we're not implementing the actual download
    )