import streamlit as st

class DeviceService:
    def detect_device(self):
        """Detecta el dispositivo desde el que se está usando la aplicación"""
        st.markdown("""
            <script>
            const width = window.innerWidth;
            fetch('/_stcore/streamlit.setComponentValue', {
                method: 'POST',
                body: JSON.stringify({
                    key: 'screen_width',
                    value: width,
                    type: 'int'
                }),
                headers: { 'Content-Type': 'application/json' }
            });
            </script>
        """, unsafe_allow_html=True)

        width = st.session_state.get("screen_width", 1200)
        st.session_state["is_mobile"] = width < 768
