import streamlit as st
# Main page configuration
st.set_page_config(page_title="📈 Trading Guide App",page_icon=":heavy_dollar_sign:", layout="wide")

# Page Header
st.markdown("<h1 style='text-align: center;'>📈 Trading Guide App</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>We provide the best platform to gather all essential insights before investing in stocks.</h4>", unsafe_allow_html=True)
st.markdown("## 🔑 Key Features")

# Custom CSS for better card visuals
# st.markdown("""
#     <style>
#     .card {
#         background-color: #f9f9f9;
#         border-radius: 15px;
#         padding: 20px;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.1);
#         transition: transform 0.2s ease, box-shadow 0.2s ease;
#         height: 200px;
#     }
#     .card:hover {
#         transform: scale(1.02);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.15);
#     }
#     .card h4 {
#         margin-top: 0;
#         margin-bottom: 10px;
#         font-size: 20px;
#     }
#     .card p {
#         margin: 0;
#         font-size: 15px;
#         color: #444;
#     }
#     </style>
# """, unsafe_allow_html=True)

# === ROW 1 ===
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Stock Analysis")
    st.write("Through this page, you can see all the information about a stock.")
    st.page_link("pages/Stock_Analysis.py", label="Open ➜", icon="📈")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🔮 Stock Prediction")
    st.write("Explore predicted closing prices for the next 30 days using historical stock data and forecasting models.")
    st.page_link("pages/Stock_Prediction.py", label="Open ➜", icon="🧠")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📐 CAPM Return")
    st.write("Discover how CAPM calculates expected return based on stock risk and market performance.")
    st.page_link("pages/CAPM_Return.py", label="Open ➜", icon="📏")
    st.markdown('</div>', unsafe_allow_html=True)

# === ROW 2 ===
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚖️ CAPM Beta")
    st.write("Calculate Beta and Expected Return for individual stocks to assess volatility.")
    st.page_link("pages/CAPM_Beta.py", label="Open ➜", icon="⚙️")
    st.markdown('</div>', unsafe_allow_html=True)

with col5:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🤖 Model Comparison")
    st.write("Compare forecasting models like ARIMA, LSTM, Prophet, and more.")
    st.page_link("pages/Model_Comparison.py", label="Open ➜", icon="🔍")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💼 Portfolio Analysis")
    st.write("Analyze your portfolio's performance and visualize asset correlation.")
    st.page_link("pages/Portfolio_Analysis.py", label="Open ➜", icon="📊")
    st.markdown('</div>', unsafe_allow_html=True)

# === IMAGE SECTION ===
st.markdown("---")
#st.image("2app.png", caption="Trading Guide App Visual", use_column_width=True)

# ===== Footer Styling and Content =====
st.markdown("""
<style>
.footer {
    position: relative;
    bottom: 0;
    width: 100%;
    background-color:#E1EFFF;
    padding: 30px 10px;
    color: black;
    text-align: center;
    border-radius: 12px;
    margin-top: 50px;
}
.footer a {
    color: #58a6ff;
    text-decoration: none;
}
.footer a:hover {
    text-decoration: underline;
}
</style>

<div class="footer">
    <h4>👨‍💻 About the Developer</h4>
    <p>This app is developed by <strong>Vaibhav Chendake</strong>.</p>
    <p>📧 <a href="mailto:vaibhavchendake62@gmail.com">vaibhavchendake62@gmail.com</a> | 
       💼 <a href="https://www.linkedin.com/in/vaibhav_chendake-355908256" target="_blank">LinkedIn</a> | 
       💻 <a href="https://github.com/yourgithubprofile" target="_blank">GitHub</a></p>
    <hr style="border: 0.5px solid #444; width: 60%; margin: 20px auto;">
    <h5>⚠️ Disclaimer</h5>
    <p>This app is for <strong>educational purposes only</strong> and does not constitute financial advice. Always do your own research before making investment decisions.</p>
    <hr style="border: 0.5px solid #444; width: 60%; margin: 20px auto;">
    <p>© 2025 Trading Guide App. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
