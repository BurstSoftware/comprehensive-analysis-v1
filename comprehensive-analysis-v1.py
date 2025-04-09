import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Competitive Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for inputs
st.sidebar.header("Competitor Data Input")

# Initialize session state for storing data
if 'competitors' not in st.session_state:
    st.session_state.competitors = {}

# Function to add competitor data
def add_competitor(name):
    if name and name not in st.session_state.competitors:
        st.session_state.competitors[name] = {
            'revenue': 0,
            'market_share': 0,
            'growth_rate': 0,
            'employees': 0,
            'customer_satisfaction': 0,
            'product_count': 0
        }

# Input for adding new competitor
new_competitor = st.sidebar.text_input("Add New Competitor")
if st.sidebar.button("Add Competitor"):
    add_competitor(new_competitor)

# Main content
st.title("Competitive Analysis Dashboard")
st.write(f"Current Date: {datetime.now().strftime('%B %d, %Y')}")

# Competitor data input section
st.header("Enter Competitor Metrics")

if st.session_state.competitors:
    # Create tabs for each competitor
    tabs = st.tabs(list(st.session_state.competitors.keys()))
    
    for tab, competitor in zip(tabs, st.session_state.competitors.keys()):
        with tab:
            col1, col2 = st.columns(2)
            with col1:
                revenue = st.number_input(
                    "Annual Revenue ($M)",
                    min_value=0.0,
                    value=float(st.session_state.competitors[competitor]['revenue']),
                    key=f"rev_{competitor}"
                )
                market_share = st.number_input(
                    "Market Share (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(st.session_state.competitors[competitor]['market_share']),
                    key=f"ms_{competitor}"
                )
                growth_rate = st.number_input(
                    "Growth Rate (%)",
                    min_value=-100.0,
                    value=float(st.session_state.competitors[competitor]['growth_rate']),
                    key=f"gr_{competitor}"
                )
            
            with col2:
                employees = st.number_input(
                    "Number of Employees",
                    min_value=0,
                    value=int(st.session_state.competitors[competitor]['employees']),
                    key=f"emp_{competitor}"
                )
                satisfaction = st.number_input(
                    "Customer Satisfaction (1-100)",
                    min_value=0,
                    max_value=100,
                    value=int(st.session_state.competitors[competitor]['customer_satisfaction']),
                    key=f"cs_{competitor}"
                )
                products = st.number_input(
                    "Number of Products",
                    min_value=0,
                    value=int(st.session_state.competitors[competitor]['product_count']),
                    key=f"pc_{competitor}"
                )
            
            # Update session state
            st.session_state.competitors[competitor].update({
                'revenue': revenue,
                'market_share': market_share,
                'growth_rate': growth_rate,
                'employees': employees,
                'customer_satisfaction': satisfaction,
                'product_count': products
            })

    # Visualizations
    st.header("Competitive Analysis Visualizations")
    
    # Convert data to DataFrame
    df = pd.DataFrame(st.session_state.competitors).T
    
    # Create various charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Comparison
        fig1 = px.bar(df, x=df.index, y='revenue', title="Revenue Comparison ($M)")
        st.plotly_chart(fig1, use_container_width=True)
        
        # Market Share Pie Chart
        fig2 = px.pie(df, values='market_share', names=df.index, title="Market Share Distribution")
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        # Growth Rate Comparison
        fig3 = px.bar(df, x=df.index, y='growth_rate', title="Growth Rate Comparison (%)")
        st.plotly_chart(fig3, use_container_width=True)
        
        # Customer Satisfaction
        fig4 = px.bar(df, x=df.index, y='customer_satisfaction', 
                     title="Customer Satisfaction (1-100)")
        st.plotly_chart(fig4, use_container_width=True)
    
    # Additional Visualizations
    st.subheader("Additional Metrics")
    
    # Scatter plot: Employees vs Revenue
    fig5 = px.scatter(df, x='employees', y='revenue', size='product_count',
                     hover_name=df.index, title="Employees vs Revenue (size = Product Count)")
    st.plotly_chart(fig5, use_container_width=True)
    
    # Data Table
    st.subheader("Raw Data")
    st.dataframe(df.style.format({
        'revenue': '${:,.2f}',
        'market_share': '{:.1f}%',
        'growth_rate': '{:.1f}%',
        'employees': '{:,.0f}',
        'customer_satisfaction': '{:.0f}',
        'product_count': '{:.0f}'
    }))

    # Export functionality
    st.subheader("Export Data")
    csv = df.to_csv()
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='competitive_analysis.csv',
        mime='text/csv',
    )

else:
    st.write("Please add at least one competitor using the sidebar to begin analysis.")

# Sidebar additional features
st.sidebar.header("Analysis Settings")
chart_type = st.sidebar.selectbox(
    "Preferred Chart Style",
    ["Bar", "Line", "Area"]
)
show_grid = st.sidebar.checkbox("Show Gridlines", value=True)

# Instructions
with st.sidebar.expander("How to Use"):
    st.write("""
    1. Add competitors using the input field above
    2. Enter metrics for each competitor in their respective tabs
    3. View automatically generated visualizations
    4. Download the data as CSV for further analysis
    """)
