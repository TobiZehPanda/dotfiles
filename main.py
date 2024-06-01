import os
import streamlit as st

st.set_page_config(
  page_title="Hello",
  page_icon="👋"
)

st.markdown(
  """
  # 👋 Welcome to Tobi's Configurator 👋
  I created this to help configure **Linux**!
  """
)
st.divider()
st.markdown(
  """
  ### Environment Variables
  """
)
col1, col2 = st.columns(2)

with col1:
  for var in [ "DISPLAY", "EDITOR", "HOME", "LANG", "SHELL"]:
    st.write(f"{var}: :orange[{os.environ[var]}]")

with col2:
  for var in ["TERM", "XDG_SESSION_TYPE", "XDG_BACKEND", "XDG_CURRENT_DESKTOP", "XDG_CONFIG_HOME"]:
    st.write(f"{var}: :orange[{os.environ[var]}]")

