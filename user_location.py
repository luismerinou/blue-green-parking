import logging
import sys

import streamlit as st
from dotenv import load_dotenv

from utils.map_utils import (
    init_session_state,
    get_location,
)
from utils.calculate_parking_lots import show_nearest_parking_lot_summary, show_nearby_parking_lots
from utils.device_utils import detect_device

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

st.set_page_config(
    page_title="Blue green parking", page_icon=":blue_car:", layout="wide"
)
# Apply Linear-like style
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
            background-color: #0E0E10;
            color: #FFFFFF;
        }
        .block-container {
            padding-top: 1rem !important;
        }
        .main {
            padding-top: 0rem !important;
        }
        .folium-map {
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(0,0,0,0.3);
        }
    </style>
""", unsafe_allow_html=True)


def main():
    detect_device()
    st.title("")
    init_session_state()
    current_latitude, current_longitude, accuracy = get_location(logger)

    is_mobile = st.session_state["is_mobile"]

    if is_mobile:
        st.markdown("""
            <h1 style='text-align: center; font-size:2.5rem; font-weight:700;'>Aparcamientos Zona SER Madrid</h1>
            <p style='text-align: center; color:#A1A1AA;'>Encuentra los aparcamientos más cercanos a ti</p>
        """, unsafe_allow_html=True)
        show_nearest_parking_lot_summary(current_latitude, current_longitude, distance_from_me=1000)
        show_nearby_parking_lots(current_latitude, current_longitude, distance_from_me=1000)

    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("""
                <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
                    <h1 style="font-size:3rem; font-weight:700; margin-bottom: 0.5rem;">Aparcamientos Zona SER Madrid</h1>
                    <p style="font-size:1.1rem; color:#A1A1AA;">Encuentra los aparcamientos más cercanos a ti</p>
                </div>
            """, unsafe_allow_html=True)
            show_nearest_parking_lot_summary(current_latitude, current_longitude, distance_from_me=1000)

        with col2:
            show_nearby_parking_lots(current_latitude, current_longitude, distance_from_me=1000)

if __name__ == "__main__":
    main()
