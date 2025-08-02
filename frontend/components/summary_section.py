import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from datetime import datetime
import requests
from components.summary_tools import render_summary_tools, generate_pdf

def render_summary_section(api_url):
    """Render the summary section with AI-generated summaries and visualizations"""
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.header("Financial Summary & Visualizations")
    
    # Check if user profile exists
    if not st.session_state.profile:
        st.warning("Please create a profile to generate financial summaries and visualizations.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Create tabs for different summary types
    summary_tab1, summary_tab2, summary_tab3 = st.tabs(["Expense Analysis", "Savings Projection", "Budget Recommendations"])
    
    # Tab 1: Expense Analysis
    with summary_tab1:
        st.subheader("Expense Breakdown")
        
        # Generate expense visualization
        if st.session_state.profile and "expenses" in st.session_state.profile:
            expenses_data = st.session_state.profile["expenses"]
            if expenses_data and sum(expenses_data.values()) > 0:
                # Create expense visualization
                fig, summary_text = create_expense_visualization(expenses_data, st.session_state.profile["income"])
                
                # Display the visualization
                st.pyplot(fig)
                
                # Display the summary text
                st.markdown("### Expense Analysis")
                st.markdown(summary_text)
                
                # Add download options
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download visualization
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    buf.seek(0)
                    st.download_button(
                        label="📊 Download Chart",
                        data=buf,
                        file_name=f"expense_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
                
                with col2:
                    # Download summary as PDF
                    pdf_content = f"""# Expense Analysis Summary

## User Information
Name: {st.session_state.profile['name']}
Monthly Income: ₹{st.session_state.profile['income']:,.2f}

## Expense Breakdown
{summary_text}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    
                    pdf_bytes = generate_pdf(pdf_content)
                    st.download_button(
                        label="📄 Download Summary",
                        data=pdf_bytes,
                        file_name=f"expense_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.info("No expense data available. Please update your profile with expense information.")
    
    # Tab 2: Savings Projection
    with summary_tab2:
        st.subheader("Savings Projection")
        
        # Calculate current savings
        if st.session_state.profile:
            income = st.session_state.profile["income"]
            total_expenses = sum(st.session_state.profile["expenses"].values()) if "expenses" in st.session_state.profile else 0
            monthly_savings = income - total_expenses
            
            # Create savings projection inputs
            st.markdown("### Current Monthly Savings")
            st.markdown(f"₹{monthly_savings:,.2f} per month")
            
            st.markdown("### Projection Settings")
            projection_years = st.slider("Projection Period (Years)", 1, 30, 5)
            interest_rate = st.slider("Annual Interest Rate (%)", 1.0, 15.0, 7.0, 0.1)
            
            # Generate savings projection
            fig, projection_data, summary_text = create_savings_projection(monthly_savings, projection_years, interest_rate)
            
            # Display the visualization
            st.pyplot(fig)
            
            # Display the summary text
            st.markdown("### Savings Projection Analysis")
            st.markdown(summary_text)
            
            # Add download options
            col1, col2 = st.columns(2)
            
            with col1:
                # Download visualization
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                buf.seek(0)
                st.download_button(
                    label="📊 Download Chart",
                    data=buf,
                    file_name=f"savings_projection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
            
            with col2:
                # Download summary as PDF
                pdf_content = f"""# Savings Projection Summary

## User Information
Name: {st.session_state.profile['name']}
Monthly Income: ₹{st.session_state.profile['income']:,.2f}
Monthly Savings: ₹{monthly_savings:,.2f}

## Projection Parameters
Projection Period: {projection_years} years
Annual Interest Rate: {interest_rate}%

## Projection Results
{summary_text}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                pdf_bytes = generate_pdf(pdf_content)
                st.download_button(
                    label="📄 Download Summary",
                    data=pdf_bytes,
                    file_name=f"savings_projection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
    
    # Tab 3: Budget Recommendations
    with summary_tab3:
        st.subheader("Budget Recommendations")
        
        if st.session_state.profile:
            # Generate budget recommendations
            if st.button("Generate Budget Recommendations"):
                with st.spinner("Generating budget recommendations..."):
                    try:
                        # Request budget summary from backend
                        response = requests.post(
                            f"{api_url}/summary",
                            json={"user_id": st.session_state.user_id}
                        )
                        
                        if response.status_code == 200:
                            budget_summary = response.json()["summary"]
                            
                            # Display the summary
                            st.markdown("### AI-Generated Budget Recommendations")
                            st.markdown(budget_summary)
                            
                            # Create ideal budget allocation chart
                            fig = create_ideal_budget_chart(st.session_state.profile["income"])
                            st.pyplot(fig)
                            
                            # Add download options
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                # Copy to clipboard
                                st.button("📋 Copy Text", on_click=set_clipboard_data, args=(budget_summary,))
                            
                            with col2:
                                # Download visualization
                                buf = io.BytesIO()
                                fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                                buf.seek(0)
                                st.download_button(
                                    label="📊 Download Chart",
                                    data=buf,
                                    file_name=f"ideal_budget_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                                    mime="image/png"
                                )
                            
                            with col3:
                                # Download summary as PDF
                                pdf_content = f"""# Budget Recommendations

## User Information
Name: {st.session_state.profile['name']}
Monthly Income: ₹{st.session_state.profile['income']:,.2f}

## AI-Generated Budget Recommendations
{budget_summary}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                                
                                pdf_bytes = generate_pdf(pdf_content)
                                st.download_button(
                                    label="📄 Download Summary",
                                    data=pdf_bytes,
                                    file_name=f"budget_recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf"
                                )
                        else:
                            st.error(f"Failed to generate budget recommendations: {response.text}")
                    except Exception as e:
                        st.error(f"Error generating budget recommendations: {str(e)}")
            else:
                st.info("Click the button above to generate AI-powered budget recommendations based on your financial profile.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_expense_visualization(expenses, income):
    """Create a visualization of expenses"""
    # Filter out zero values
    expenses = {k: v for k, v in expenses.items() if v > 0}
    
    if not expenses:
        return None, "No expense data available."
    
    # Calculate percentages
    total_expenses = sum(expenses.values())
    expense_percentages = {k: (v/income)*100 for k, v in expenses.items()}
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('#1E1E1E')
    
    # Pie chart for expense breakdown
    labels = list(expenses.keys())
    sizes = list(expenses.values())
    
    # Add a bit of explode to each slice for visual effect
    explode = [0.05] * len(labels)
    
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, textprops={'color': 'white'})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.set_title('Expense Breakdown', color='white', fontsize=14)
    ax1.set_facecolor('#1E1E1E')
    
    # Bar chart for expense vs. income percentage
    categories = list(expense_percentages.keys())
    percentages = list(expense_percentages.values())
    
    # Add 'Savings' category
    savings_percentage = max(0, 100 - sum(percentages))
    categories.append('Savings')
    percentages.append(savings_percentage)
    
    # Sort by percentage (descending)
    sorted_indices = np.argsort(percentages)[::-1]
    sorted_categories = [categories[i] for i in sorted_indices]
    sorted_percentages = [percentages[i] for i in sorted_indices]
    
    # Create horizontal bar chart
    bars = ax2.barh(sorted_categories, sorted_percentages, color='#6B73FF')
    
    # Highlight savings bar
    for i, category in enumerate(sorted_categories):
        if category == 'Savings':
            bars[i].set_color('#4CAF50' if savings_percentage > 20 else '#FF5252')
    
    ax2.set_xlabel('Percentage of Income (%)', color='white')
    ax2.set_title('Expense vs. Income Percentage', color='white', fontsize=14)
    ax2.set_facecolor('#1E1E1E')
    ax2.tick_params(axis='both', colors='white')
    ax2.grid(axis='x', linestyle='--', alpha=0.3)
    
    # Add percentage labels to the bars
    for i, v in enumerate(sorted_percentages):
        ax2.text(v + 1, i, f'{v:.1f}%', color='white', va='center')
    
    # Set x-axis limit to ensure labels are visible
    ax2.set_xlim(0, max(percentages) * 1.2)
    
    # Adjust layout
    plt.tight_layout()
    
    # Generate summary text
    summary_text = f"""
    Your total monthly expenses are ₹{total_expenses:,.2f}, which is {(total_expenses/income)*100:.1f}% of your income.
    
    Your largest expense categories are:
    1. {sorted_categories[0]}: ₹{expenses.get(sorted_categories[0], 0):,.2f} ({sorted_percentages[0]:.1f}% of income)
    2. {sorted_categories[1] if len(sorted_categories) > 1 else 'N/A'}: ₹{expenses.get(sorted_categories[1], 0) if len(sorted_categories) > 1 else 0:,.2f} ({sorted_percentages[1] if len(sorted_percentages) > 1 else 0:.1f}% of income)
    
    Your monthly savings are approximately ₹{income - total_expenses:,.2f}, which is {savings_percentage:.1f}% of your income.
    """
    
    return fig, summary_text

def create_savings_projection(monthly_savings, years, interest_rate):
    """Create a visualization of savings projection"""
    # Calculate projection data
    months = years * 12
    monthly_rate = interest_rate / 100 / 12
    
    # Initialize arrays
    savings_without_interest = np.zeros(months + 1)
    savings_with_interest = np.zeros(months + 1)
    
    # Calculate savings over time
    for i in range(1, months + 1):
        savings_without_interest[i] = monthly_savings * i
        savings_with_interest[i] = savings_with_interest[i-1] * (1 + monthly_rate) + monthly_savings
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    
    # Create x-axis labels (years)
    x_labels = np.arange(0, months + 1, 12)
    x_values = np.arange(0, years + 1)
    
    # Plot data
    ax.plot(savings_without_interest, label='Without Interest', color='#6B73FF', linestyle='--')
    ax.plot(savings_with_interest, label='With Interest', color='#4CAF50', linewidth=2)
    
    # Fill area between curves
    ax.fill_between(np.arange(months + 1), savings_without_interest, savings_with_interest, 
                   color='#4CAF50', alpha=0.3)
    
    # Set labels and title
    ax.set_xlabel('Years', color='white')
    ax.set_ylabel('Savings Amount (₹)', color='white')
    ax.set_title(f'Savings Projection Over {years} Years at {interest_rate}% Interest', color='white', fontsize=14)
    
    # Set x-axis ticks to show years
    ax.set_xticks(x_labels)
    ax.set_xticklabels(x_values)
    
    # Customize grid and spines
    ax.grid(linestyle='--', alpha=0.3)
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Customize ticks
    ax.tick_params(axis='both', colors='white')
    
    # Add legend
    ax.legend(facecolor='#1E1E1E', edgecolor='#555555', labelcolor='white')
    
    # Format y-axis labels with commas for thousands
    import matplotlib.ticker as ticker
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Add annotations for final values
    final_without_interest = savings_without_interest[-1]
    final_with_interest = savings_with_interest[-1]
    interest_earned = final_with_interest - final_without_interest
    
    ax.annotate(f'₹{final_without_interest:,.2f}', 
                xy=(months, final_without_interest),
                xytext=(5, 0), textcoords='offset points',
                ha='left', va='center', color='white')
    
    ax.annotate(f'₹{final_with_interest:,.2f}', 
                xy=(months, final_with_interest),
                xytext=(5, 0), textcoords='offset points',
                ha='left', va='center', color='white')
    
    # Adjust layout
    plt.tight_layout()
    
    # Create projection data for summary
    projection_data = {
        'years': years,
        'interest_rate': interest_rate,
        'monthly_savings': monthly_savings,
        'final_without_interest': final_without_interest,
        'final_with_interest': final_with_interest,
        'interest_earned': interest_earned
    }
    
    # Generate summary text
    summary_text = f"""
    With your current monthly savings of ₹{monthly_savings:,.2f}:
    
    * After {years} years without interest, you would save ₹{final_without_interest:,.2f}
    * With a {interest_rate}% annual interest rate, you would accumulate ₹{final_with_interest:,.2f}
    * The interest earned would be ₹{interest_earned:,.2f}
    
    This represents a {(interest_earned/final_without_interest)*100:.1f}% increase due to compound interest.
    """
    
    return fig, projection_data, summary_text

def create_ideal_budget_chart(income):
    """Create an ideal budget allocation chart based on the 50/30/20 rule"""
    # Calculate ideal budget allocation
    needs = income * 0.5  # 50% for needs
    wants = income * 0.3  # 30% for wants
    savings = income * 0.2  # 20% for savings
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#1E1E1E')
    ax.set_facecolor('#1E1E1E')
    
    # Create data
    categories = ['Needs', 'Wants', 'Savings']
    amounts = [needs, wants, savings]
    colors = ['#6B73FF', '#FF5252', '#4CAF50']
    
    # Create bar chart
    bars = ax.bar(categories, amounts, color=colors)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'₹{height:,.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, color='white')
    
    # Add percentage labels below category names
    for i, category in enumerate(categories):
        ax.annotate(f'{[50, 30, 20][i]}%',
                   xy=(i, 0),
                   xytext=(0, -15),  # 15 points vertical offset below axis
                   textcoords="offset points",
                   ha='center', va='top',
                   fontsize=12, color='white')
    
    # Set labels and title
    ax.set_ylabel('Amount (₹)', color='white')
    ax.set_title('Ideal Budget Allocation (50/30/20 Rule)', color='white', fontsize=14)
    
    # Customize grid and spines
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Customize ticks
    ax.tick_params(axis='both', colors='white')
    
    # Format y-axis labels with commas for thousands
    import matplotlib.ticker as ticker
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def set_clipboard_data(text):
    """Set text to clipboard using JavaScript"""
    # Create a JavaScript function to copy text to clipboard
    js_code = f"""
    <script>
    function copyToClipboard() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text).then(() => {{
            // Show a success message
            const div = document.createElement('div');
            div.textContent = 'Copied to clipboard!';
            div.style.position = 'fixed';
            div.style.top = '10px';
            div.style.right = '10px';
            div.style.padding = '10px';
            div.style.background = 'rgba(0, 200, 0, 0.8)';
            div.style.color = 'white';
            div.style.borderRadius = '5px';
            div.style.zIndex = '9999';
            document.body.appendChild(div);
            
            // Remove the message after 2 seconds
            setTimeout(() => {{
                document.body.removeChild(div);
            }}, 2000);
        }}).catch(err => {{
            console.error('Failed to copy text: ', err);
        }});
    }}
    
    // Call the function
    copyToClipboard();
    </script>
    """
    
    # Display the JavaScript code
    st.components.v1.html(js_code, height=0)