import streamlit as st
import requests
import plotly.graph_objects as go

# MUST be the first Streamlit command
st.set_page_config(page_title="Used Car Price Predictor", layout="centered", page_icon="🚗")

# Custom CSS for professional styling
st.markdown("""
<style>
    .stButton>button {
        background: linear-gradient(to right, #2ab5a9, #0b8a7d);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #0b8a7d, #2ab5a9);
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stRadio>div {
        flex-direction: row;
        gap: 15px;
    }
    .stRadio [role=radiogroup] {
        gap: 15px;
    }
    .stHeader {
        border-bottom: 2px solid #2ab5a9;
        padding-bottom: 8px;
    }
    /* Fix for slider color */
    .stSlider [data-baseweb=slider] {
        background-color: #f0f2f6;
    }
    .stSlider [data-baseweb=slider] span {
        background-color: #2ab5a9 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚗 Used Car Price Predictor")
st.markdown("Enter your car's details below to get an estimated resale price.")

# --- SECTION 1: Basic Info ---
with st.container():
    st.subheader("🔧 Car Specifications", divider='blue')
    col1, col2 = st.columns(2)
    with col1:
        car_age = st.slider("Car Age (Years)", 0, 30, 5, help="Age of your car in years")
        engine_cc = st.number_input("Engine Capacity (cc)", min_value=600, max_value=6000, value=1300, step=100)
        owner_count = st.slider("Number of Previous Owners", 0, 5, 1)
    with col2:
        mileage_kmpl = st.number_input("Mileage (km per litre)", min_value=1.0, max_value=50.0, value=15.0, step=0.5)
        brand = st.slider("Brand Rating (0-10)", 0, 10, 5, help="0 = Economy brand, 10 = Luxury brand")
        accidents_reported = st.slider("Accidents Reported", 0, 10, 0)

# --- SECTION 2: Fuel Type ---
st.subheader("⛽ Fuel Type", divider='blue')
fuel_type = st.radio("Fuel Type", ["Electric", "Petrol", "Other"], horizontal=True, index=1)
fuel_type_Electric = 1 if fuel_type == "Electric" else 0
fuel_type_Petrol = 1 if fuel_type == "Petrol" else 0

# --- SECTION 3: Transmission Type ---
st.subheader("⚙️ Transmission", divider='blue')
transmission = st.radio("Transmission Type", ["Manual", "Automatic"], horizontal=True, index=0)
transmission_Manual = 1 if transmission == "Manual" else 0

# --- SECTION 4: Color Selection ---
st.subheader("🎨 Car Color", divider='blue')
color = st.selectbox("Choose your car's color", ["White", "Blue", "Gray", "Red", "Silver", "Other"], index=0)
color_Blue = 1 if color == "Blue" else 0
color_Gray = 1 if color == "Gray" else 0
color_Red = 1 if color == "Red" else 0
color_Silver = 1 if color == "Silver" else 0
color_White = 1 if color == "White" else 0

# --- SECTION 5: Service History ---
st.subheader("🛠️ Service History", divider='blue')
service_history = st.radio("Service History", ["None", "Partial", "Regular"], horizontal=True, index=2)
service_history_None = 1 if service_history == "None" else 0
service_history_Partial = 1 if service_history == "Partial" else 0

# --- SECTION 6: Insurance ---
st.subheader("🛡️ Insurance", divider='blue')
insurance = st.radio("Is Insurance Valid?", ["Yes", "No"], horizontal=True, index=0)
insurance_valid_Yes = 1 if insurance == "Yes" else 0

# --- Combine all features ---
input_data = {
    "car_age": car_age,
    "mileage_kmpl": mileage_kmpl,
    "engine_cc": engine_cc,
    "owner_count": owner_count,
    "brand": brand,
    "accidents_reported": accidents_reported,
    "fuel_type_Electric": fuel_type_Electric,
    "fuel_type_Petrol": fuel_type_Petrol,
    "transmission_Manual": transmission_Manual,
    "color_Blue": color_Blue,
    "color_Gray": color_Gray,
    "color_Red": color_Red,
    "color_Silver": color_Silver,
    "color_White": color_White,
    "service_history_None": service_history_None,
    "service_history_Partial": service_history_Partial,
    "insurance_valid_Yes": insurance_valid_Yes
}

# --- Predict button ---
predict_col, debug_col = st.columns([3, 1])
with predict_col:
    if st.button("🔍 Predict Resale Price", use_container_width=True):
        try:
            # res = requests.post("http://127.0.0.1:8000/predict", json=input_data)
            res = requests.post("http://backend:8000/predict", json=input_data)


            if res.status_code == 200:
                result = res.json()
                predicted_price = float(result['predicted_price'])
                
                # Price display with animation
                st.success("## 💰 Price Estimation Complete!")
                st.balloons()
                
                # Create a container for results
                with st.container():
                    st.markdown(f"""
                    <div style="text-align:center; padding:20px; border-radius:10px; 
                                background:linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
                                border:1px solid #2ab5a9;">
                        <h2 style="color:#0b8a7d;">Estimated Resale Value</h2>
                        <p style="font-size:2.5rem; font-weight:bold; color:#025b51;">
                            USD {predicted_price:,.0f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Enhanced gauge chart
                    max_val = max(50000, predicted_price * 2)  # Dynamic max range
                    
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=predicted_price,
                        title={'text': "Market Value Assessment", 'font': {'size': 18}},
                        delta={'reference': predicted_price * 0.7, 'relative': False, 'increasing': {'color': "#2ab5a9"}},
                        gauge={
                            'axis': {
                                'range': [0, max_val],
                                'tickwidth': 1,
                                'tickcolor': "#025b51",
                                'tickformat': ',.0f',
                                'tickprefix': '$'
                            },
                            'bar': {'color': "#025b51", 'thickness': 0.3},
                            'bgcolor': "white",
                            'borderwidth': 2,
                            'bordercolor': "gray",
                            'steps': [
                                {'range': [0, max_val/3], 'color': '#f8d7da'},
                                {'range': [max_val/3, 2*max_val/3], 'color': '#fff3cd'},
                                {'range': [2*max_val/3, max_val], 'color': '#d4edda'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': predicted_price
                            }
                        }
                    ))
                    
                    fig.update_layout(
                        height=300,
                        margin=dict(l=20, r=20, t=60, b=20),
                        font=dict(family="Arial", size=14, color="#025b51")
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Value breakdown visualization (FIXED PROGRESS BAR)
                    with st.expander("💡 Value Breakdown Analysis", expanded=True):
                        st.markdown("#### Key Factors Influencing Price")
                        
                        # Calculate factors with capped percentages
                        factors = {
                            "Brand Rating": min(brand * 0.8, 100),
                            "Mileage Efficiency": min(mileage_kmpl * 0.5, 100),
                            "Service History": 12.0 if service_history == "Regular" else 5.0,
                            "Accidents Reported": min(accidents_reported * 1.5, 100),
                            "Previous Owners": min(owner_count * 0.7, 100)
                        }
                        
                        # Calculate impacts (positive/negative)
                        impacts = {
                            "Brand Rating": factors["Brand Rating"],
                            "Mileage Efficiency": factors["Mileage Efficiency"],
                            "Service History": factors["Service History"],
                            "Accidents Reported": -factors["Accidents Reported"],
                            "Previous Owners": -factors["Previous Owners"]
                        }
                        
                        # Sort by absolute impact
                        sorted_impacts = dict(sorted(impacts.items(), key=lambda item: abs(item[1]), reverse=True))
                        
                        for factor, impact in sorted_impacts.items():
                            col1, col2 = st.columns([2, 3])
                            col1.markdown(f"**{factor}**")
                            
                            # Convert to percentage value (0-100) and cap at 100
                            value = min(abs(impact) / 100, 1.0)
                            col2.progress(value, 
                                         text=f"{'↑ Increases' if impact > 0 else '↓ Decreases'} value by {abs(impact):.1f}%")

            else:
                st.error(f"❌ Server Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"🔥 Connection Error: Could not reach the prediction server. Details: {str(e)}")

with debug_col:
    with st.expander("🔧 Debug Data"):
        st.json(input_data)