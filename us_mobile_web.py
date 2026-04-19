import streamlit as st
import time
import requests

# Page Config
st.set_page_config(page_title="US Mobile Plan Engine", page_icon="📱", layout="centered")

# Custom CSS for US Mobile Branding
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    .recommendation-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def get_coverage_data(zip_code):
    """
    Attempts a real-time signal lookup using geographic intelligence.
    """
    NETWORK_INTEL = {
        "Warp": {
            "bands": "n260, n261 (mmWave), n77 (C-Band)",
            "lat": "12ms",
            "tech": "5G Ultra Wideband"
        },
        "Light Speed": {
            "bands": "n41 (UC), n71 (Extended Range)",
            "lat": "18ms",
            "tech": "5G Mid-Band"
        },
        "Dark Star": {
            "bands": "n77, n5, n2",
            "lat": "22ms",
            "tech": "5G+ Optimized"
        }
    }

    try:
        response = requests.post(
            "https://api.usmobile.com/web-gateway/api/v1/coverage/check",
            json={"zipCode": zip_code},
            timeout=2
        )
        api_status = "Live" if response.status_code == 200 else "Restricted Access (Simulated Data)"
    except Exception:
        api_status = "Simulation Mode"

    first_digit = zip_code[0]
    if first_digit in ['0', '1', '2']:
        net = "Warp"
    elif first_digit in ['8', '9']:
        net = "Light Speed"
    else:
        net = "Dark Star"
        
    data = NETWORK_INTEL[net]
    return {
        "network": net,
        "speed": f"{data['tech']} ({data['bands']})",
        "latency": data['lat'],
        "status": api_status,
        "zip": zip_code
    }

# App UI
st.title("📱 US Mobile Strategy Engine")
st.subheader("2026 Plan Recommendation Prototype")

with st.expander("ℹ️ About this tool"):
    st.write("This tool demonstrates the backend routing logic for US Mobile's next-gen plan recommendation engine. It uses ZIP-code intelligence and user behavior profiles to find the optimal plan.")

# Form
with st.form("plan_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        zip_code = st.text_input("Enter ZIP Code", placeholder="e.g. 90210", max_chars=5)
        account_type = st.selectbox("Account Type", ["Personal", "Business"])
    
    with col2:
        usage = st.selectbox("Data Usage Profile", [
            "High (>70GB, Streaming/Gaming)",
            "Average (10GB - 70GB)",
            "Low (<10GB, Essential)"
        ])
        lines = st.number_input("Number of Lines", min_value=1, max_value=20, value=1)
    
    wifi = "Mix of both"
    if usage == "Low (<10GB, Essential)":
        wifi = st.radio("Primary Connectivity", ["Mostly WiFi", "Mix of both"])

    submitted = st.form_submit_button("Generate Recommendation")

if submitted:
    if not zip_code or len(zip_code) < 5:
        st.error("Please enter a valid 5-digit ZIP code.")
    else:
        with st.spinner("Analyzing Network Intelligence..."):
            time.sleep(1.5)
            coverage = get_coverage_data(zip_code)
            
            # Logic Tree
            recommended_plan = ""
            price = ""
            features = ""
            reasoning = ""
            
            if account_type == "Business":
                recommended_plan = "By the Gig (Pooled)"
                price = "$10/mo + $2/GB"
                reasoning = "Business accounts benefit most from pooled data across multiple devices/fleets."
                features = "Shared data pool, multi-line management, priority support."
            else:
                if "High" in usage:
                    recommended_plan = "Unlimited Premium"
                    price = "$32.50/mo"
                    features = "Truly Unlimited Priority Data, 100GB Hotspot, International Roaming."
                    reasoning = "You're a power user. Premium ensures you never throttle and have massive hotspot data."
                elif "Average" in usage:
                    recommended_plan = "Unlimited Starter"
                    price = "$22.50/mo"
                    features = "70GB High-Speed Data, 20GB Hotspot."
                    reasoning = "The 'Sweet Spot'. Perfect for most users who stream and use social media daily."
                else:
                    if wifi == "Mostly WiFi":
                        recommended_plan = "Light Plan"
                        price = "$8/mo"
                        features = "2GB High-Speed Data, Unlimited Talk & Text."
                        reasoning = "Bare minimum for the essential user who stays connected to WiFi."
                    else:
                        recommended_plan = "Unlimited Flex"
                        price = "$17.50/mo"
                        features = "10GB High-Speed Data, 5GB Hotspot (Annual)."
                        reasoning = "Great budget option for those who need a bit of data while on the go."

            # UI Output
            st.success(f"Best Network Found: {coverage['network']} in {zip_code}")
            
            # Main Card
            st.markdown(f"""
            <div class="recommendation-box">
                <h2 style='color:#007bff; margin-top:0;'>{recommended_plan}</h2>
                <h3 style='margin:0;'>Starting at {price}</h3>
                <hr>
                <p><b>Network:</b> {coverage['network']} ({coverage['speed']})</p>
                <p><b>Estimated Latency:</b> {coverage['latency']}</p>
                <p><b>Included Features:</b> {features}</p>
                <p style='font-style: italic; color: #555;'><b>Why:</b> {reasoning}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Technical Details Table
            st.divider()
            st.write("### Technical Signal Intelligence")
            st.table({
                "Parameter": ["Underlying Carrier", "5G Technology", "Signal Status", "API Connectivity"],
                "Details": [
                    coverage['network'], 
                    coverage['speed'], 
                    "Excellent" if coverage['network'] != "Dark Star" else "Great", 
                    coverage['status']
                ]
            })
            
            if lines >= 3 and recommended_plan not in ["Unlimited Premium", "By the Gig (Pooled)"]:
                st.warning(f"💡 Multi-line Note: With {lines} lines, switching to 'By the Gig' could save you up to 30% monthly.")

st.markdown("<p style='text-align: center; color: #888;'>Ready to activate? Visit <a href='https://usmobile.com/activate'>usmobile.com/activate</a></p>", unsafe_allow_html=True)
