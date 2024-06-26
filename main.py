import os
import streamlit as st
from streamlit_extras.badges import badge

st.set_page_config(
  page_title="Hello",
  page_icon="❤️"
)

st.markdown(
  """
  # Welcome to Configurator-Inator
  I created this to help configure **Linux**!
  """
)
badge(type="github", name="TobiZehPanda/dotfiles")

st.divider()
with st.expander("Environment Variables"):
  col1, col2 = st.columns(2)

  with col1:
    for var in [ "DISPLAY", "EDITOR", "HISTFILE", "HOME", "LANG", "SHELL"]:
      if var in os.environ:
        st.write(f"{var}: :orange[{os.environ[var]}]")

  with col2:
    for var in ["TERM", "USER", "XDG_BACKEND", "XDG_CONFIG_DIR", "XDG_CURRENT_DESKTOP", "XDG_SESSION_TYPE"]:
      if var in os.environ:
        st.write(f"{var}: :orange[{os.environ[var]}]")

