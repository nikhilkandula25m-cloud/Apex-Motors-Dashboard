import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# ==========================================
# 1. PAGE CONFIG & SESSION STATE
# ==========================================
st.set_page_config(layout="wide", page_title="Apex Motors | Network Engine", initial_sidebar_state="expanded")

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'landing'
if 'selected_dealer' not in st.session_state:
    st.session_state.selected_dealer = None
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'previous_view' not in st.session_state:
    st.session_state.previous_view = 'landing'

# ==========================================
# 2. PREMIUM ENTERPRISE CSS & SAAS BADGES
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #F3F6F9 !important; }
    
    .stApp [data-testid="stVerticalBlock"] p, .stApp [data-testid="stVerticalBlock"] h1, 
    .stApp [data-testid="stVerticalBlock"] h2, .stApp [data-testid="stVerticalBlock"] h3, 
    .stApp [data-testid="stVerticalBlock"] h4, .stApp [data-testid="stVerticalBlock"] li, 
    .stApp [data-testid="stVerticalBlock"] span, [data-testid="stMetricValue"] {
        color: #0F172A !important;
    }
    
    [data-testid="stMetricDelta"] span, [data-testid="stMetricDelta"] div, [data-testid="stMetricDelta"] svg { color: inherit !important; }

    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #0F172A !important; }
    .stSelectbox div, .stMultiSelect div, [data-baseweb="popover"] span, [data-baseweb="popover"] li { color: #0F172A !important; }

    .stButton > button, [data-testid="stDownloadButton"] > button {
        background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    .stButton > button p, [data-testid="stDownloadButton"] > button p, [data-testid="stDownloadButton"] > button span {
        color: #0F172A !important; font-weight: 600 !important;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] > button:hover {
        border-color: #0EA5E9 !important; background-color: #F8FAFC !important;
    }
    div[data-testid="stAlert"] { background-color: rgba(255, 255, 255, 0.95) !important; border: 1px solid #E2E8F0 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important; }

    .header-container { background-color: #FFFFFF; padding: 20px 30px; border-bottom: 2px solid #E2E8F0; margin-top: -60px; margin-bottom: 25px; margin-left: -3rem; margin-right: -3rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02); }
    .brand-title { font-family: 'Segoe UI', sans-serif; font-size: 2.2rem !important; font-weight: 800 !important; color: #002A5C !important; margin: 0; }
    .brand-subtitle { color: #64748B !important; font-size: 1.1rem !important; font-weight: 600 !important; margin: 0; }
    div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #FFFFFF !important; border-radius: 12px !important; box-shadow: 0 4px 10px -2px rgba(0, 0, 0, 0.05) !important; border: 1px solid #E2E8F0 !important; }
    div[data-testid="metric-container"] { background-color: #FFFFFF !important; border-left: 5px solid #00509E !important; padding: 15px 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important; border: 1px solid #E2E8F0 !important; }
    .section-title { font-size: 1.25rem !important; font-weight: 800 !important; color: #002A5C !important; margin-bottom: 15px; padding-bottom: 8px; border-bottom: 2px solid #F1F5F9; }
    
    .badge-red { background-color: #FEE2E2 !important; color: #991B1B !important; padding: 4px 14px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; border: 1px solid #FCA5A5; display: inline-block;}
    .badge-orange { background-color: #FEF3C7 !important; color: #92400E !important; padding: 4px 14px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; border: 1px solid #FCD34D; display: inline-block;}
    .badge-green { background-color: #D1FAE5 !important; color: #065F46 !important; padding: 4px 14px; border-radius: 999px; font-weight: 700; font-size: 0.85rem; border: 1px solid #6EE7B7; display: inline-block;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. BALANCED DYNAMIC DATA GENERATION
# ==========================================
@st.cache_data
def load_dynamic_data():
    base_locations = [
        ("Mumbai", "Maharashtra", 19.076, 72.877), ("Pune", "Maharashtra", 18.520, 73.856), 
        ("Nagpur", "Maharashtra", 21.145, 79.088), ("Nashik", "Maharashtra", 19.997, 73.789),
        ("Delhi", "Delhi", 28.613, 77.209), ("Gurugram", "Haryana", 28.459, 77.026),
        ("Noida", "Uttar Pradesh", 28.535, 77.391), ("Lucknow", "Uttar Pradesh", 26.846, 80.946),
        ("Kanpur", "Uttar Pradesh", 26.449, 80.331), ("Agra", "Uttar Pradesh", 27.176, 78.008),
        ("Bangalore", "Karnataka", 12.971, 77.594), ("Mysore", "Karnataka", 12.295, 76.639),
        ("Hubli", "Karnataka", 15.364, 75.123), ("Mangalore", "Karnataka", 12.914, 74.856),
        ("Chennai", "Tamil Nadu", 13.082, 80.270), ("Coimbatore", "Tamil Nadu", 11.016, 76.955),
        ("Madurai", "Tamil Nadu", 9.925, 78.119), ("Trichy", "Tamil Nadu", 10.790, 78.704),
        ("Ahmedabad", "Gujarat", 23.022, 72.571), ("Surat", "Gujarat", 21.170, 72.831),
        ("Vadodara", "Gujarat", 22.307, 73.181), ("Rajkot", "Gujarat", 22.303, 70.802),
        ("Kolkata", "West Bengal", 22.572, 88.363), ("Siliguri", "West Bengal", 26.727, 88.395),
        ("Jaipur", "Rajasthan", 26.912, 75.787), ("Jodhpur", "Rajasthan", 26.238, 73.024),
        ("Hyderabad", "Telangana", 17.385, 78.486), ("Warangal", "Telangana", 17.968, 79.594),
        ("Kochi", "Kerala", 9.931, 76.267), ("Trivandrum", "Kerala", 8.524, 76.936),
        ("Chandigarh", "Punjab", 30.733, 76.779), ("Ludhiana", "Punjab", 30.901, 75.857),
        ("Bhopal", "Madhya Pradesh", 23.259, 77.412), ("Indore", "Madhya Pradesh", 22.719, 75.857),
        ("Patna", "Bihar", 25.594, 85.137), ("Bhubaneswar", "Odisha", 20.296, 85.824),
        ("Guwahati", "Assam", 26.144, 91.736), ("Ranchi", "Jharkhand", 23.344, 85.309),
        ("Jamshedpur", "Jharkhand", 22.804, 86.202), ("Dhanbad", "Jharkhand", 23.795, 86.430),
        ("Visakhapatnam", "Andhra Pradesh", 17.686, 83.218), ("Vijayawada", "Andhra Pradesh", 16.506, 80.648),
        ("Raipur", "Chhattisgarh", 21.251, 81.629), ("Dehradun", "Uttarakhand", 30.316, 78.032)
    ]
    
    data = []
    random.seed(101) # Seed for stability
    
    # Generate 150 Dealers with Weighted Tiering for Realistic Balance
    for i in range(1, 151):
        city, state, lat, lon = random.choice(base_locations)
        lat += random.uniform(-0.06, 0.06) 
        lon += random.uniform(-0.06, 0.06)
        
        # Roll a die to determine dealer tier: 45% Green, 35% Orange, 20% Red
        tier_roll = random.random()
        
        if tier_roll < 0.45: # HEALTHY (Green bias)
            sales = random.uniform(0.90, 1.25)
            service = random.uniform(0.85, 0.99)
            complaints = random.uniform(0.5, 3.0)
            inv_aging = random.uniform(0.02, 0.12)
            delays = int(random.uniform(0, 5))
        elif tier_roll < 0.80: # WARNING (Orange bias)
            sales = random.uniform(0.75, 1.10)
            service = random.uniform(0.65, 0.85)
            complaints = random.uniform(2.5, 5.5)
            inv_aging = random.uniform(0.10, 0.22)
            delays = int(random.uniform(4, 12))
        else: # CRITICAL (Red bias)
            sales = random.uniform(0.50, 1.15)
            service = random.uniform(0.40, 0.65)
            complaints = random.uniform(5.0, 9.5)
            inv_aging = random.uniform(0.20, 0.45)
            delays = int(random.uniform(10, 25))
            
        data.append({
            "Dealer_ID": f"D{i:04d}",
            "Dealer_Name": f"Apex {city} {random.choice(['Prime', 'Central', 'Motors', 'Auto', 'Elite'])}",
            "City": city, "State": state, "Latitude": lat, "Longitude": lon,
            "Sales_vs_Target_Pct": sales,
            "Service_Performance_Pct": service,
            "Complaints_per_100": complaints,
            "Inventory_Aging_Pct": inv_aging,
            "Payment_Delays_Days": delays
        })
        
    df = pd.DataFrame(data)
    
    # Calculate Core Health Score
    comp_service = df['Service_Performance_Pct'] * 100 * 0.4
    comp_complaints = ((10 - df['Complaints_per_100']) * 10).clip(lower=0) * 0.3
    comp_inventory = ((30 - (df['Inventory_Aging_Pct'] * 100)) / 30 * 100).clip(lower=0) * 0.3
    df['Operational_Health_Index'] = (comp_service + comp_complaints + comp_inventory).clip(lower=0, upper=100)
    
    # ==========================================
    # HYPER-DYNAMIC DIAGNOSTIC GENERATOR
    # ==========================================
    def dynamic_diagnose(row):
        health = row['Operational_Health_Index']
        inv_pct = row['Inventory_Aging_Pct'] * 100
        sales_pct = row['Sales_vs_Target_Pct'] * 100
        srv_pct = row['Service_Performance_Pct'] * 100
        delays = row['Payment_Delays_Days']
        complaints = row['Complaints_per_100']
        
        ap_liquidity = ["Freeze Wholesale Dispatch", "Mandate 90-Day Stock Liquidation Event", "Initiate Floorplan Restructuring", "Audit Dealership Bank Balances", "Halt Dealer Incentive Payouts"]
        ap_brand = ["Suspend Volume Target Bonuses", "Mandate Customer Experience (CX) Retraining", "Deploy Mystery Shopper Audit", "Review Pre-Delivery Inspection (PDI) Logs", "Change Dealership General Manager"]
        ap_ops = ["Conduct 30-Day Pipeline Review", "Fast-track Spare Parts Allocation", "Dispatch Regional Fix Team", "Subsidize Local Lead Gen Campaign", "Audit Workshop Bay Utilization"]
        ap_growth = ["Fast-Track Top Tier Allocations", "Consider for Territory Expansion", "Nominate for Regional Dealer of the Year", "Invite to OEM Strategic Advisory Board", "Co-Fund Flagship Showroom Upgrade"]
        
        if health < 60:
            color = 'red'
            if inv_pct > 22 and delays > 10:
                diag = random.choice(["Liquidity Crisis", "Capital Gridlock", "Insolvency Risk"])
                rc_templates = [
                    f"Critical cash flow bottleneck. With {inv_pct:.1f}% of inventory severely aged, capital is locked, directly causing {delays} days of OEM payment delays.",
                    f"Working capital is paralyzed. The dealer is holding {inv_pct:.1f}% stale metal, making it impossible to service debt, resulting in a {delays}-day default on floorplan financing.",
                    f"Financial red flag: {delays} days behind on payments due to complete inability to turn inventory. {inv_pct:.1f}% of current stock is highly aged."
                ]
                rc = random.choice(rc_templates)
                ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_liquidity, 3))])
                
            elif complaints > 5.5 and sales_pct > 95:
                diag = random.choice(["Brand Equity Erosion", "Aggressive Mis-selling", "CX Failure"])
                rc_templates = [
                    f"Dealer is artificially inflating throughput (hitting {sales_pct:.1f}% of target) at the severe cost of brand reputation, generating {complaints:.1f} complaints per 100 vehicles.",
                    f"A dangerous push-marketing environment. Sales are high ({sales_pct:.1f}%), but post-sale SLAs are collapsing with an unacceptable complaint rate of {complaints:.1f}.",
                    f"Volume targets ({sales_pct:.1f}%) are being met through predatory tactics or skipped PDIs. {complaints:.1f} customer complaints per 100 units indicates severe local brand damage."
                ]
                rc = random.choice(rc_templates)
                ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_brand, 3))])
                
            else:
                diag = random.choice(["Systemic Collapse", "Margin Compression", "Multi-Point Failure"])
                rc_templates = [
                    f"An across-the-board operational breakdown. Service performance is critically low at {srv_pct:.1f}%, leading to negative fixed-absorption and systemic unprofitability.",
                    f"Fundamental business failure. {srv_pct:.1f}% service efficiency combined with {sales_pct:.1f}% sales attainment means the dealer cannot cover operational overhead.",
                    f"A multi-metric collapse. With sales languishing at {sales_pct:.1f}% and service efficiency dropping to {srv_pct:.1f}%, the business is fundamentally unviable without OEM intervention."
                ]
                rc = random.choice(rc_templates)
                ap = "1. Place under OEM Administration\n2. Appoint Turnaround GM\n3. Halt all CapEx Projects"
                
        elif health < 78:
            color = 'orange'
            if inv_pct > 18:
                diag = random.choice(["Inventory Bloat", "Pipeline Friction"])
                rc = random.choice([
                    f"A pipeline mismatch is causing vehicle accumulation. Currently holding {inv_pct:.1f}% aged stock, which threatens future cash flow.",
                    f"Sales pacing does not match wholesale intake. With {inv_pct:.1f}% of inventory aging rapidly, a targeted liquidation strategy is required."
                ])
                ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_ops + [ap_liquidity[1]], 3))])
                
            elif srv_pct < 75:
                diag = random.choice(["Service Bottleneck", "Workshop Inefficiency"])
                rc = random.choice([
                    f"Workshop efficiency has dropped to {srv_pct:.1f}%, causing long customer wait times and threatening high-margin service revenue.",
                    f"Fixed-ops friction detected. A service performance score of {srv_pct:.1f}% indicates underutilized bays or significant parts delays."
                ])
                ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_ops, 3))])
                
            else:
                diag = random.choice(["Operational Drift", "Performance Plateau"])
                rc = f"While core sales are functional, creeping operational inefficiencies are creating friction. Minor delays in collections ({delays} days) require close monitoring."
                ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_ops, 3))])
                
        else:
            color = 'green'
            diag = random.choice(["Optimal Operation", "Exemplary Performance", "Network Benchmark"])
            rc = random.choice([
                f"This dealer exhibits robust financial discipline. Hitting {sales_pct:.1f}% of target while maintaining a stellar {srv_pct:.1f}% service efficiency.",
                f"A highly optimized retail engine. Outstanding service retention ({srv_pct:.1f}%) combined with highly disciplined inventory turnaround.",
                f"Setting the regional benchmark. They maintain {sales_pct:.1f}% sales velocity with minimal aged inventory ({inv_pct:.1f}%) and excellent cash flow."
            ])
            ap = "\n".join([f"{i+1}. {act}" for i, act in enumerate(random.sample(ap_growth, 3))])
            
        return pd.Series([color, diag, rc, ap])
            
    df[['Status_Color', 'Diagnosis', 'Root_Cause', 'Action_Plan']] = df.apply(dynamic_diagnose, axis=1)
    
    def calc_bleed(row):
        if row['Inventory_Aging_Pct'] > 0.15:
            aged_cars = max(0, int(50 * row['Inventory_Aging_Pct']))
            return int(aged_cars * ((1000000 * 0.10) / 365) * 15)
        return 0
    df['Simulated_Capital_Bleed'] = df.apply(calc_bleed, axis=1)
    
    return df

df_master = load_dynamic_data()

# ==========================================
# 4. GLOBAL SIDEBAR (CLEAN WHITE THEME)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #0F172A; margin-bottom: 0px;'>Control Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 0.9rem;'>Executive Filters</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color: #E2E8F0; margin: 10px 0px;'>", unsafe_allow_html=True)
    
    state_filter = st.multiselect("📍 Filter by State", options=sorted(df_master['State'].dropna().unique()), placeholder="All States")
    status_filter = st.multiselect("🚨 Filter by Risk Tier", options=['red', 'orange', 'green'], format_func=lambda x: "Critical" if x == 'red' else ("Warning" if x == 'orange' else "Healthy"), placeholder="All Risk Tiers")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset View", use_container_width=True):
        st.session_state.current_view = 'landing'
        st.session_state.selected_dealer = None
        st.rerun()

# Apply filters
df = df_master.copy()
if state_filter: df = df[df['State'].isin(state_filter)]
if status_filter: df = df[df['Status_Color'].isin(status_filter)]


# ==========================================
# PAGE 1: THE MACRO LANDING PAGE
# ==========================================
if st.session_state.current_view == 'landing':
    st.markdown("""
        <div class="header-container">
            <p class="brand-title">APEX MOTORS</p>
            <p class="brand-subtitle">National Network Intelligence Command</p>
        </div>
    """, unsafe_allow_html=True)
    
    macro_health = df['Operational_Health_Index'].mean() if not df.empty else 0
    macro_bleed = df['Simulated_Capital_Bleed'].sum()
    total_dealers = len(df)
    
    st.markdown("<div class='section-title'>Executive Summary</div>", unsafe_allow_html=True)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Active Dealerships", f"{total_dealers}", "0% vs Last Month")
    mc2.metric("Network Health Index", f"{macro_health:.1f} / 100", "+1.4% vs Last Month", delta_color="normal")
    mc3.metric("Simulated Capital at Risk", f"₹ {(macro_bleed / 100000):,.1f} L", "-3% Exposure", delta_color="inverse")
    mc4.metric("Q3 Target Attainment", "93.2%", "+1.8% YTD")
    st.markdown("<br>", unsafe_allow_html=True)

    col_map, col_panel = st.columns([2.3, 1.2], gap="large")
    
    with col_map:
        with st.container(border=True):
            st.markdown('<div class="section-title">📍 Geospatial Risk Map</div>', unsafe_allow_html=True)
            
            def get_marker_size(row):
                if row['Status_Color'] == 'red': return 25
                elif row['Status_Color'] == 'orange': return 12
                else: return 5

            df['Visual_Size'] = df.apply(get_marker_size, axis=1)

            fig_map = px.scatter_map(
                df, lat="Latitude", lon="Longitude", color="Status_Color",
                color_discrete_map={'red': 'rgba(220, 38, 38, 1.0)', 'orange': 'rgba(245, 158, 11, 0.8)', 'green': 'rgba(16, 185, 129, 0.4)'},
                size="Visual_Size", hover_name="Dealer_Name", custom_data=["Dealer_Name"],
                zoom=4.0, center={"lat": 22.0, "lon": 79.0}, map_style="carto-positron", height=580
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            map_event = st.plotly_chart(fig_map, on_select="rerun", selection_mode="points", width="stretch")
            
            if len(map_event.selection.points) > 0:
                st.session_state.selected_dealer = map_event.selection.points[0]["customdata"][0]
                st.session_state.previous_view = 'landing'
                st.session_state.current_view = 'dashboard'
                st.rerun()

    with col_panel:
        with st.container(border=True):
            st.markdown('<div class="section-title">📊 Network Composition</div>', unsafe_allow_html=True)
            
            status_counts = df['Status_Color'].value_counts().reset_index()
            status_counts.columns = ['Status_Color', 'Count']
            
            # Ensure proper ordering in donut chart
            color_order = {'green': 1, 'orange': 2, 'red': 3}
            status_counts = status_counts.sort_values(by="Status_Color", key=lambda x: x.map(color_order))
            
            fig_donut = px.pie(
                status_counts, values='Count', names='Status_Color', hole=0.7,
                color='Status_Color', color_discrete_map={'red': '#DC3545', 'orange': '#FFC107', 'green': '#28A745'}
            )
            fig_donut.update_traces(textinfo='value', textfont_size=16)
            
            fig_donut.update_layout(
                showlegend=False, height=180, margin={"r":0,"t":0,"l":0,"b":0},
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                annotations=[dict(text=f"{total_dealers}", x=0.5, y=0.53, font_size=28, showarrow=False, font_color="#0F172A"),
                             dict(text="Total", x=0.5, y=0.35, font_size=12, showarrow=False, font_color="#64748B")]
            )
            st.plotly_chart(fig_donut, width="stretch", theme=None)
            
            critical = len(df[df['Status_Color'] == 'red'])
            warning = len(df[df['Status_Color'] == 'orange'])
            healthy = len(df[df['Status_Color'] == 'green'])
            
            st.markdown("<hr style='margin: 10px 0px;'>", unsafe_allow_html=True)
            if st.button(f"🔴 View {critical} Critical Dealers", use_container_width=True, key="btn_red", disabled=(critical==0)):
                st.session_state.selected_category = 'red'
                st.session_state.current_view = 'list_view'
                st.rerun()
            if st.button(f"🟡 View {warning} Warning Dealers", use_container_width=True, key="btn_yellow", disabled=(warning==0)):
                st.session_state.selected_category = 'orange'
                st.session_state.current_view = 'list_view'
                st.rerun()
            if st.button(f"🟢 View {healthy} Healthy Dealers", use_container_width=True, key="btn_green", disabled=(healthy==0)):
                st.session_state.selected_category = 'green'
                st.session_state.current_view = 'list_view'
                st.rerun()

        with st.container(border=True):
            st.markdown('<div class="section-title">⚡ Live Alerts Feed</div>', unsafe_allow_html=True)
            st.info("🕒 **10 mins ago:** Routine allocations dispatched to Northern Region.")
            st.warning("🕒 **1 hr ago:** 2 Warning Dealers flagged for inventory review.")
            if critical > 0:
                st.error("🕒 **2 hrs ago:** Immediate OEM intervention required for Critical nodes.")

# ==========================================
# PAGE 2: THE CATEGORY LIST VIEW
# ==========================================
elif st.session_state.current_view == 'list_view':
    cat = st.session_state.selected_category
    title_map = {'red': '🔴 Critical Interventions', 'orange': '🟡 Operational Warnings', 'green': '🟢 Healthy Operations'}
    
    st.markdown(f"""
        <div class="header-container">
            <p class="brand-title">{title_map[cat]}</p>
            <p class="brand-subtitle">Category Roster & Quick Diagnostics</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ Back to Network Map"):
        st.session_state.current_view = 'landing'
        st.session_state.selected_category = None
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    filtered_df = df[df['Status_Color'] == cat].reset_index(drop=True)
    cols = st.columns(3, gap="large")
    
    for idx, row in filtered_df.iterrows():
        with cols[idx % 3]:
            with st.container(border=True):
                badge_class = f"badge-{row['Status_Color']}"
                st.markdown(f"#### {row['Dealer_Name']} <br><span class='{badge_class}' style='margin-top: 8px;'>{row['Diagnosis']}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: #64748B;'>📍 {row['City']}, {row['State']}</span>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 10px 0px;'>", unsafe_allow_html=True)
                
                health_score = int(row['Operational_Health_Index'])
                st.write(f"**Health Score:** {health_score} / 100")
                st.progress(health_score / 100)
                st.write(f"**Sales vs Target:** {int(row['Sales_vs_Target_Pct']*100)}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"🔍 Diagnose Dealer", key=f"diag_{row['Dealer_ID']}", use_container_width=True):
                    st.session_state.selected_dealer = row['Dealer_Name']
                    st.session_state.previous_view = 'list_view'
                    st.session_state.current_view = 'dashboard'
                    st.rerun()

# ==========================================
# PAGE 3: THE MICRO BI DASHBOARD
# ==========================================
elif st.session_state.current_view == 'dashboard':
    dealer = df_master[df_master['Dealer_Name'] == st.session_state.selected_dealer].iloc[0]
    
    badge_class = f"badge-{dealer['Status_Color']}"
    st.markdown(f"""
        <div class="header-container" style="display: flex; justify-content: space-between; align-items: center;">
            <div style="width: 100%;">
                <p class="brand-title">{dealer["Dealer_Name"]}</p>
                <p class="brand-subtitle">{dealer["City"]}, {dealer["State"]} &nbsp;|&nbsp; <span class='{badge_class}'>{dealer["Diagnosis"].upper()}</span></p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_back, col_head = st.columns([1.5, 8.5])
    with col_back:
        button_text = "⬅️ Back to Map" if st.session_state.previous_view == 'landing' else "⬅️ Back to List"
        if st.button(button_text):
            st.session_state.current_view = st.session_state.previous_view
            st.session_state.selected_dealer = None
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sales vs Target", f"{int(dealer['Sales_vs_Target_Pct'] * 100)}%", "-4% vs Prev Qtr", delta_color="inverse" if dealer['Status_Color']=='red' else "normal")
    c2.metric("Operational Health", f"{int(dealer['Operational_Health_Index'])} / 100", "+1.2 Points", delta_color="normal")
    c3.metric("Payment Delays", f"{dealer['Payment_Delays_Days']} Days", "+3 Days" if dealer['Status_Color']=='red' else "-1 Day", delta_color="inverse")
    c4.metric("Aging Inventory", f"{int(dealer['Inventory_Aging_Pct'] * 100)}%", "-2% Cleared")
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">📈 6-Month Performance Trend (Sales vs Target)</div>', unsafe_allow_html=True)
        months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct (Current)']
        base_val = int(dealer['Sales_vs_Target_Pct'] * 100)
        if dealer['Status_Color'] == 'red':
            trend_data = [105, 102, 95, 88, 80, base_val]
            line_color = '#DC3545'
        elif dealer['Status_Color'] == 'orange':
            trend_data = [90, 85, 88, 92, 85, base_val]
            line_color = '#FFC107'
        else:
            trend_data = [92, 95, 98, 99, 101, base_val]
            line_color = '#28A745'
            
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=months, y=trend_data, mode='lines+markers', fill='tozeroy', 
                                      marker=dict(size=8, color=line_color), line=dict(width=3, color=line_color),
                                      fillcolor=f"rgba({px.colors.hex_to_rgb(line_color)[0]}, {px.colors.hex_to_rgb(line_color)[1]}, {px.colors.hex_to_rgb(line_color)[2]}, 0.1)"))
        
        fig_line.update_layout(
            height=250, margin={"r":20,"t":20,"l":60,"b":50}, 
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
            font=dict(color="black", size=13), 
            yaxis=dict(range=[0, 120], gridcolor='#E2E8F0', title=dict(text="Target %", font=dict(color="black"), standoff=15), automargin=True), 
            xaxis=dict(showgrid=False, automargin=True, title=dict(text="Month", font=dict(color="black"), standoff=15))
        )
        st.plotly_chart(fig_line, width="stretch", theme=None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_bar, col_quad = st.columns(2, gap="large")
    
    with col_bar:
        with st.container(border=True):
            st.markdown('<div class="section-title">📉 Dealer vs. National Average</div>', unsafe_allow_html=True)
            categories = ['Sales Volume', 'Service Quality', 'Inventory Turn', 'CX/Complaints', 'Cash Flow']
            dealer_vals = [
                min(100, dealer['Sales_vs_Target_Pct']*100), dealer['Service_Performance_Pct']*100, 
                max(0, 100 - (dealer['Inventory_Aging_Pct']*100)), max(0, 100 - (dealer['Complaints_per_100']*10)), max(0, 100 - (dealer['Payment_Delays_Days']*3))
            ]
            avg_vals = [95, 85, 88, 80, 94]
            
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(y=categories, x=avg_vals, name='National Average', orientation='h', marker=dict(color='#64748B')))
            fig_bar.add_trace(go.Bar(y=categories, x=dealer_vals, name=dealer['Dealer_Name'], orientation='h', marker=dict(color='#0EA5E9' if dealer['Status_Color']!='red' else '#EF4444')))
            
            fig_bar.update_layout(
                barmode='group', height=360, margin={"r":20,"t":60,"l":60,"b":60}, 
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="black", size=13),
                legend=dict(orientation="h", yanchor="bottom", y=1.20, xanchor="right", x=1, font=dict(color="black")),
                xaxis=dict(range=[0,100], gridcolor='#E2E8F0', title=dict(text="Performance Score", font=dict(color="black"), standoff=15), automargin=True),
                yaxis=dict(automargin=True)
            )
            st.plotly_chart(fig_bar, width="stretch", theme=None)

    with col_quad:
        with st.container(border=True):
            st.markdown('<div class="section-title">🎯 Network Matrix Positioning</div>', unsafe_allow_html=True)
            fig_quad = go.Figure()
            
            fig_quad.add_shape(type="rect", x0=70, x1=100, y0=1.0, y1=1.5, fillcolor="rgba(16, 185, 129, 0.1)", line_width=0, layer="below")
            fig_quad.add_shape(type="rect", x0=0, x1=70, y0=1.0, y1=1.5, fillcolor="rgba(245, 158, 11, 0.1)", line_width=0, layer="below")
            fig_quad.add_shape(type="rect", x0=70, x1=100, y0=0, y1=1.0, fillcolor="rgba(245, 158, 11, 0.1)", line_width=0, layer="below")
            fig_quad.add_shape(type="rect", x0=0, x1=70, y0=0, y1=1.0, fillcolor="rgba(239, 68, 68, 0.1)", line_width=0, layer="below")

            fig_quad.add_trace(go.Scatter(x=df_master['Operational_Health_Index'], y=df_master['Sales_vs_Target_Pct'], mode='markers', marker=dict(color='#94A3B8', size=6, opacity=0.7), hoverinfo='skip'))
            fig_quad.add_trace(go.Scatter(x=[dealer['Operational_Health_Index']], y=[dealer['Sales_vs_Target_Pct']], mode='markers', marker=dict(color='#0F172A', size=16, line=dict(color='#10B981' if dealer['Status_Color']=='green' else '#EF4444', width=3))))
            
            fig_quad.update_layout(
                showlegend=False, height=360, margin={"r":20,"t":40,"l":60,"b":60}, 
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="black", size=12),
                xaxis=dict(title=dict(text="Operational Health Score", font=dict(color="black"), standoff=15), range=[0, 100], showgrid=False, zeroline=False, tickfont=dict(color="black"), automargin=True),
                yaxis=dict(title=dict(text="Sales vs Target", font=dict(color="black"), standoff=15), range=[0.4, 1.5], showgrid=False, zeroline=False, tickfont=dict(color="black"), automargin=True)
            )
            fig_quad.add_hline(y=1.0, line_dash="dash", line_color="#CBD5E1")
            fig_quad.add_vline(x=70, line_dash="dash", line_color="#CBD5E1")
            st.plotly_chart(fig_quad, width="stretch", theme=None)

    st.markdown("<br>", unsafe_allow_html=True)
    col_cause, col_action = st.columns(2, gap="large")
    
    with col_cause:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">🔍 Root Cause Analysis</div>', unsafe_allow_html=True)
            st.write(f"{dealer['Root_Cause']}")
            
    with col_action:
        with st.container(border=True):
            st.markdown(f'<div class="section-title">⚡ Immediate Action Plan</div>', unsafe_allow_html=True)
            actions = dealer['Action_Plan'].split('\n')
            for action in actions:
                st.write(f"- {action}")
                
            memo_text = f"APEX MOTORS EXECUTIVE BRIEF\n" + "="*30 + "\n"
            memo_text += f"DEALER: {dealer['Dealer_Name']}\nLOCATION: {dealer['City']}, {dealer['State']}\nSTATUS: {dealer['Diagnosis'].upper()}\n\n"
            memo_text += f"ROOT CAUSE ANALYSIS:\n{dealer['Root_Cause']}\n\n"
            memo_text += f"MANDATED ACTION PLAN:\n{dealer['Action_Plan']}"
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Executive Brief",
                data=memo_text,
                file_name=f"{dealer['Dealer_ID']}_Strategic_Brief.txt",
                mime="text/plain",
                use_container_width=True
            )
                
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f'<div class="section-title">💸 Working Capital Bleed Simulator</div>', unsafe_allow_html=True)
        days = st.slider("Forecast Days to Liquidate Aged Stock:", min_value=1, max_value=30, value=15, key="bleed_slider")
        
        total_inventory = 50
        aged_cars = max(0, int(total_inventory * dealer['Inventory_Aging_Pct']))
        daily_bleed_per_car = (1000000 * 0.10) / 365
        total_bleed = int(aged_cars * daily_bleed_per_car * days)
        
        if aged_cars > 0:
            st.error(f"**Financial Exposure:** If this dealer's **{aged_cars} aged units** sit on the lot for another **{days} days**, the floorplan interest bleed will reach **₹ {total_bleed:,.0f}**, severely eroding OEM repayment capacity.")
        else:
            st.success("This dealer currently maintains a highly efficient inventory turnover with zero critically aged units.")