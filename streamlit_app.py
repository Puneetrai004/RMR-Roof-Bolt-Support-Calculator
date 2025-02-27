import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from PIL import Image, ImageDraw

# Set page configuration
st.set_page_config(
    page_title="Rock Mass Rating (RMR) Calculator",
    page_icon="⛏️",
    layout="wide"
)

# Main title and description
st.title("⛏️ Rock Mass Rating (RMR) Calculator")
st.markdown("""
This application calculates the Rock Mass Rating (RMR) based on Bieniawski's classification system
and determines appropriate roof bolt support requirements for mining and tunneling operations.
""")

# Create tabs for different sections of the app
tab1, tab2, tab3 = st.tabs(["RMR Calculator", "Support Recommendations", "About RMR"])

with tab1:
    st.header("RMR Calculation")
    
    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    
    # Parameter A1: Uniaxial Compressive Strength (UCS)
    st.sidebar.subheader("A1: Strength of Intact Rock Material")
    ucs_options = [
        "> 250 MPa (15 points)", 
        "100-250 MPa (12 points)", 
        "50-100 MPa (7 points)", 
        "25-50 MPa (4 points)", 
        "5-25 MPa (2 points)", 
        "1-5 MPa (1 point)", 
        "< 1 MPa (0 points)"
    ]
    ucs_option = st.sidebar.selectbox("Select rock strength:", ucs_options, index=2)
    ucs_ratings = [15, 12, 7, 4, 2, 1, 0]
    ucs_values = [">250 MPa", "100-250 MPa", "50-100 MPa", "25-50 MPa", "5-25 MPa", "1-5 MPa", "<1 MPa"]
    ucs_index = ucs_options.index(ucs_option)
    a1_rating = ucs_ratings[ucs_index]
    ucs_value = ucs_values[ucs_index]
    
    # Parameter A2: Rock Quality Designation (RQD)
    st.sidebar.subheader("A2: Rock Quality Designation (RQD)")
    rqd_options = [
        "90-100% (20 points)", 
        "75-90% (17 points)", 
        "50-75% (13 points)", 
        "25-50% (8 points)", 
        "< 25% (3 points)"
    ]
    rqd_option = st.sidebar.selectbox("Select RQD value:", rqd_options, index=2)
    rqd_ratings = [20, 17, 13, 8, 3]
    rqd_values = ["90-100%", "75-90%", "50-75%", "25-50%", "<25%"]
    rqd_index = rqd_options.index(rqd_option)
    a2_rating = rqd_ratings[rqd_index]
    rqd_value = rqd_values[rqd_index]
    
    # Parameter A3: Spacing of Discontinuities
    st.sidebar.subheader("A3: Spacing of Discontinuities")
    spacing_options = [
        "> 2 m (20 points)", 
        "0.6-2 m (15 points)", 
        "200-600 mm (10 points)", 
        "60-200 mm (8 points)", 
        "< 60 mm (5 points)"
    ]
    spacing_option = st.sidebar.selectbox("Select discontinuity spacing:", spacing_options, index=2)
    spacing_ratings = [20, 15, 10, 8, 5]
    spacing_values = [">2 m", "0.6-2 m", "200-600 mm", "60-200 mm", "<60 mm"]
    spacing_index = spacing_options.index(spacing_option)
    a3_rating = spacing_ratings[spacing_index]
    spacing_value = spacing_values[spacing_index]
    
    # Parameter A4: Condition of Discontinuities
    st.sidebar.subheader("A4: Condition of Discontinuities")
    condition_options = [
        "Very rough, not continuous, no separation, unweathered (30 points)",
        "Slightly rough, separation < 1 mm, slightly weathered (25 points)",
        "Slightly rough, separation < 1 mm, highly weathered (20 points)",
        "Slickensided/gouge < 5 mm, or separation 1-5 mm (10 points)",
        "Soft gouge > 5 mm, or separation > 5 mm (0 points)"
    ]
    condition_option = st.sidebar.selectbox("Select discontinuity condition:", condition_options, index=2)
    condition_ratings = [30, 25, 20, 10, 0]
    condition_values = [
        "Very rough, not continuous, no separation, unweathered",
        "Slightly rough, separation < 1 mm, slightly weathered",
        "Slightly rough, separation < 1 mm, highly weathered",
        "Slickensided/gouge < 5 mm, or separation 1-5 mm",
        "Soft gouge > 5 mm, or separation > 5 mm"
    ]
    condition_index = condition_options.index(condition_option)
    a4_rating = condition_ratings[condition_index]
    condition_value = condition_values[condition_index]
    
    # Parameter A5: Groundwater Conditions
    st.sidebar.subheader("A5: Groundwater Conditions")
    water_options = [
        "Completely dry (15 points)",
        "Damp (10 points)",
        "Wet (7 points)",
        "Dripping (4 points)",
        "Flowing (0 points)"
    ]
    water_option = st.sidebar.selectbox("Select groundwater condition:", water_options, index=1)
    water_ratings = [15, 10, 7, 4, 0]
    water_values = ["Completely dry", "Damp", "Wet", "Dripping", "Flowing"]
    water_index = water_options.index(water_option)
    a5_rating = water_ratings[water_index]
    water_value = water_values[water_index]
    
    # Add an excavation parameters section to the sidebar
    st.sidebar.header("Excavation Parameters")
    excavation_width = st.sidebar.number_input("Excavation Width (m):", min_value=1.0, max_value=30.0, value=5.0, step=0.5)
    excavation_height = st.sidebar.number_input("Excavation Height (m):", min_value=1.0, max_value=30.0, value=3.5, step=0.5)
    tunnel_length = st.sidebar.number_input("Tunnel Length (m):", min_value=1.0, max_value=1000.0, value=100.0, step=10.0)
    
    # Calculate the total RMR value
    rmr_value = a1_rating + a2_rating + a3_rating + a4_rating + a5_rating
    
    # Determine rock mass class and description
    if rmr_value >= 81 and rmr_value <= 100:
        rock_class = "I"
        description = "Very good rock"
        class_color = "green"
    elif rmr_value >= 61 and rmr_value <= 80:
        rock_class = "II"
        description = "Good rock"
        class_color = "lightgreen"
    elif rmr_value >= 41 and rmr_value <= 60:
        rock_class = "III"
        description = "Fair rock"
        class_color = "yellow"
    elif rmr_value >= 21 and rmr_value <= 40:
        rock_class = "IV"
        description = "Poor rock"
        class_color = "orange"
    else:
        rock_class = "V"
        description = "Very poor rock"
        class_color = "red"
    
    # Create columns for displaying results
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display results in a table
        st.subheader("RMR Calculation Results")
        
        results_df = pd.DataFrame({
            "Parameter": ["A1: Rock Strength", "A2: RQD", "A3: Spacing of Discontinuities", "A4: Condition of Discontinuities", "A5: Groundwater Conditions", "TOTAL RMR", "Rock Mass Class"],
            "Condition": [ucs_value, rqd_value, spacing_value, condition_value, water_value, "", f"{rock_class} - {description}"],
            "Rating": [a1_rating, a2_rating, a3_rating, a4_rating, a5_rating, rmr_value, ""]
        })
        
        st.dataframe(results_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Display a gauge chart for the RMR
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rmr_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Rock Mass Rating (RMR)"},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': class_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 20], 'color': 'red'},
                    {'range': [20, 40], 'color': 'orange'},
                    {'range': [40, 60], 'color': 'yellow'},
                    {'range': [60, 80], 'color': 'lightgreen'},
                    {'range': [80, 100], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': rmr_value
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a simple visualization of the rock class
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; background-color: {class_color}; border-radius: 5px; margin-top: 10px;">
            <h3 style="margin: 0; color: black;">Class {rock_class}: {description}</h3>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("Support Recommendations")
    
    # Support recommendations based on RMR class
    if rock_class == "I":  # RMR 81-100
        bolt_length = max(2.0, excavation_width/5)
        bolt_spacing = 2.0
        bolt_pattern = "Spot bolting only where necessary"
        bolt_type = "Friction or Fully Grouted Bolts"
        bolt_capacity = "Low capacity (10-15 tons)"
        additional_support = "Generally no additional support required"
        
    elif rock_class == "II":  # RMR 61-80
        bolt_length = max(2.5, excavation_width/4)
        bolt_spacing = 1.5
        bolt_pattern = "Systematic bolting at 1.5-2.0m spacing"
        bolt_type = "Fully Grouted Rebar or Friction Bolts"
        bolt_capacity = "Medium capacity (15-20 tons)"
        additional_support = "Spot mesh in crown where needed"
        
    elif rock_class == "III":  # RMR 41-60
        bolt_length = max(3.0, excavation_width/3)
        bolt_spacing = 1.2
        bolt_pattern = "Systematic bolting at 1.0-1.5m spacing in crown and walls"
        bolt_type = "Fully Grouted Rebar"
        bolt_capacity = "Medium-high capacity (20-25 tons)"
        additional_support = "Wire mesh in crown; spot fiber-reinforced shotcrete (50mm)"
        
    elif rock_class == "IV":  # RMR 21-40
        bolt_length = max(4.0, excavation_width/2.5)
        bolt_spacing = 1.0
        bolt_pattern = "Systematic bolting at 1.0m spacing with wire mesh in crown and walls"
        bolt_type = "Fully Grouted Rebar or Cable Bolts"
        bolt_capacity = "High capacity (25-30 tons)"
        additional_support = "Wire mesh in crown and walls; fiber-reinforced shotcrete (100-150mm)"
        
    else:  # RMR < 21
        bolt_length = max(4.5, excavation_width/2)
        bolt_spacing = 0.6
        bolt_pattern = "Systematic bolting at 0.5-0.8m spacing with wire mesh and straps"
        bolt_type = "Fully Grouted Cable Bolts and Rebar"
        bolt_capacity = "Very high capacity (>30 tons)"
        additional_support = "Wire mesh with straps in crown and walls; fiber-reinforced shotcrete (150-200mm); light steel sets"
    
    # Calculate number of bolts required
    if rock_class == "I":
        bolts_per_row = max(2, round(excavation_width / bolt_spacing))
        rows_per_meter = 0.5  # Spot bolting only
    else:
        bolts_per_row = max(3, round(excavation_width / bolt_spacing))
        rows_per_meter = 1 / bolt_spacing
    
    bolt_density = bolts_per_row * rows_per_meter  # bolts per meter of tunnel length
    total_bolts = bolt_density * tunnel_length
    total_bolt_length = total_bolts * bolt_length
    
    # Create columns for displaying support recommendations and visualization
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Display support recommendations in a table
        st.subheader("Roof Bolt Support Recommendations")
        
        support_df = pd.DataFrame({
            "Support Parameter": [
                "Bolt Length", "Bolt Spacing", "Pattern", "Recommended Bolt Type", 
                "Required Bolt Capacity", "Additional Support", "Bolts per Row",
                "Rows per Meter", "Bolt Density", "Total Bolts Required", "Total Bolt Length"
            ],
            "Recommendation": [
                f"{bolt_length:.2f} m", f"{bolt_spacing:.2f} m", bolt_pattern, bolt_type,
                bolt_capacity, additional_support, f"{bolts_per_row}",
                f"{rows_per_meter:.2f}", f"{bolt_density:.2f} bolts/m", f"{total_bolts:.0f} bolts",
                f"{total_bolt_length:.0f} m"
            ]
        })
        
        st.dataframe(support_df, use_container_width=True, hide_index=True)
    
    with col2:
        # Create a visualization of the bolt pattern
        st.subheader("Bolt Pattern Visualization")
        
        # Create a function to generate a bolt pattern visualization
        def generate_bolt_pattern_image(width, height, spacing, length, rock_class):
            # Scale for visualization (pixels per meter)
            scale = 50
            padding = 20
            img_width = int(width * scale) + 2 * padding
            img_height = int(height * scale) + 2 * padding
            
            # Create image and drawing context
            img = Image.new('RGB', (img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw excavation profile
            draw.rectangle(
                [padding, padding, padding + int(width * scale), padding + int(height * scale)],
                outline='black', width=3
            )
            
            # Calculate bolt positions based on rock class and spacing
            bolt_positions = []
            
            if rock_class == "I":  # Spot bolting only
                # Just a few bolts in the crown
                x_positions = [width/4, width/2, 3*width/4]
                for x in x_positions:
                    bolt_positions.append((x, 0.5))
            else:
                # Systematic pattern based on spacing
                rows = int(height / spacing) if rock_class in ["IV", "V"] else max(2, int(height / spacing))
                cols = max(3, int(width / spacing))
                
                # Place bolts in a grid pattern
                for row in range(rows):
                    for col in range(cols):
                        # Adjust for even spacing
                        x = (col + 0.5) * (width / cols)
                        
                        # For better classes, focus bolts more on the crown
                        if rock_class in ["II", "III"] and row > 1:
                            continue
                        
                        # Calculate y position (from top down)
                        y = (row + 0.5) * (height / rows)
                        
                        bolt_positions.append((x, y))
            
            # Draw bolts
            bolt_radius = 5
            for x, y in bolt_positions:
                # Calculate pixel coordinates
                px = padding + int(x * scale)
                py = padding + int(y * scale)
                
                # Draw bolt head
                draw.ellipse(
                    [px - bolt_radius, py - bolt_radius, px + bolt_radius, py + bolt_radius],
                    fill='blue', outline='black'
                )
                
                # Draw bolt length line (simplified vertical representation)
                if rock_class != "I":
                    draw.line(
                        [px, py, px, py + int(length * scale * 0.75)],
                        fill='blue', width=2
                    )
            
            # Add title and legend
            return img
        
        # Generate the bolt pattern image
        bolt_pattern_img = generate_bolt_pattern_image(
            excavation_width, excavation_height, bolt_spacing, bolt_length, rock_class
        )
        
        # Display the image
        st.image(bolt_pattern_img, caption=f"Roof Bolt Pattern - Rock Class {rock_class}", use_column_width=True)
        
        # Add a legend
        st.markdown("""
        **Legend:**
        - Black rectangle: Excavation profile
        - Blue circles: Bolt heads
        - Blue lines: Approximate bolt length
        """)

with tab3:
    st.header("About Rock Mass Rating (RMR)")
    
    st.markdown("""
    ## What is Rock Mass Rating (RMR)?
    
    The Rock Mass Rating (RMR) system is a geomechanical classification system developed by Z.T. Bieniawski between 1972 and 1973. It provides a method for estimating the quality of rock masses based on several parameters, and it helps in determining appropriate support systems for underground excavations.
    
    ## Parameters of RMR
    
    The RMR system considers five main parameters:
    
    1. **Uniaxial Compressive Strength (UCS) of intact rock material** - Measures the strength of the rock when subjected to uniaxial compression.
    
    2. **Rock Quality Designation (RQD)** - An index that quantifies the degree of jointing or fracturing in a rock mass, measured as the percentage of intact core pieces longer than 10 cm in the total length of core.
    
    3. **Spacing of discontinuities** - The distance between adjacent discontinuities (joints, bedding planes, faults, etc.).
    
    4. **Condition of discontinuities** - Characteristics like roughness, separation, weathering, and infilling of the discontinuities.
    
    5. **Groundwater conditions** - The presence and pressure of water in the rock mass.
    
    ## RMR Classification
    
    Based on the total RMR value (0-100), rock masses are classified into five categories:
    
    - **Class I (RMR 81-100)**: Very good rock
    - **Class II (RMR 61-80)**: Good rock
    - **Class III (RMR 41-60)**: Fair rock
    - **Class IV (RMR 21-40)**: Poor rock
    - **Class V (RMR < 21)**: Very poor rock
    
    ## Applications of RMR
    
    The RMR system is widely used in:
    
    - Underground mining
    - Tunnel construction
    - Foundation design
    - Slope stability analysis
    - Determination of rock mass properties
    - Design of support systems for underground excavations
    
    ## Limitations
    
    While RMR is a widely used system, it has some limitations:
    
    - It does not adequately account for stress conditions
    - It may not be suitable for very weak or highly weathered rock masses
    - It does not directly consider the influence of water pressure
    - It may not be applicable to all types of rock masses or geological conditions
    
    ## References
    
    - Bieniawski, Z.T. (1973). "Engineering classification of jointed rock masses"
    - Bieniawski, Z.T. (1989). "Engineering Rock Mass Classifications"
    """)

# Add credits at the bottom
st.sidebar.markdown("---")
st.sidebar.info("RMR Calculator v1.0 | Developed with Streamlit")
st.sidebar.markdown("GitHub: [Repository Link]")
