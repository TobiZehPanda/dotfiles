import os
import streamlit as st
import pandas as pd

FILE = "configurations.cvs"

def absolute_path(path):
  return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

def add_config(name, src, dest, *argv):
  data = pd.DataFrame({"name": [name], "src": [src], "dest":[dest], "src2":[argv[0]], "dest2":[argv[1]]})
  data.to_csv(FILE, mode="a", index=False, header=False)

def delete_config(index):
  df = pd.read_csv(FILE)
  df.drop([index]).to_csv(FILE, mode="w", index=False, header=True)

def edit_config():
  if not os.path.isfile(FILE):
    with open(FILE, "w", encoding="UTF-8") as f:
      f.write("name,src,dest,src2,dest2\n")
  df = pd.read_csv(FILE)
  df = df.astype(str)
  update_df = st.data_editor(df, use_container_width=True)
  update_df.to_csv(FILE, mode="w", index=False, header=True)

def show_config():
  if not os.path.isfile(FILE):
    with open(FILE, "w", encoding="UTF-8") as f:
      f.write("name,src,dest,src2,dest2\n")
  df = pd.read_csv(FILE)
  st.dataframe(df, use_container_width=True)

def install(app_data):
  if os.path.islink(absolute_path(app_data['dest'].to_string(index=False))):
    st.warning("Link found. Removing!")
    os.unlink(absolute_path(app_data['dest'].to_string(index=False)))
    if not app_install.isnull().values.any():
      os.unlink(absolute_path(app_data['dest2'].to_string(index=False)))
  elif os.path.isfile(absolute_path(app_data['dest'].to_string(index=False))):
    st.warning("File found. Removing!")
    os.remove(absolute_path(app_data['dest'].to_string(index=False)))
    if not app_install.isnull().values.any():
      os.remove(absolute_path(app_data['dest2'].to_string(index=False)))
  elif os.path.isdir(absolute_path(app_data['dest'].to_string(index=False))):
    st.warning("Directory found. Removing!")
    os.rmdir(absolute_path(app_data['dest'].to_string(index=False)))
    if not app_install.isnull().values.any():
      os.rmdir(absolute_path(app_data['dest22'].to_string(index=False)))
  st.info(f"Installing {app_data['name'].to_string(index=False)} links!")
  os.symlink(absolute_path(app_data['src'].to_string(index=False)), absolute_path(app_data['dest'].to_string(index=False)))
  if not app_install.isnull().values.any():
    os.symlink(absolute_path(app_data['src2'].to_string(index=False)), absolute_path(app_data['dest2'].to_string(index=False)))

tab1, tab2, tab3 = st.tabs(["Install Configs", "Add/Edit", "Delete"])

with tab1:
  dataframe = pd.read_csv(FILE)
  app_list = dataframe['name'].tolist()
  app_config = st.multiselect('Choose configs to systemlink:', app_list)
  button = st.button('Submit')

  if button and app_config:
    st.success("Installing configs....")
    for app in app_config:
      app_install = df[df['name'].str.match(app)]
      install(app_install)

with tab2:
  edit_config()
  with st.form("add", clear_on_submit=True):
    st_name = st.text_input("Name:")
    st_src = st.text_input("Source:")
    st_dest = st.text_input("Destination:")
    st_src2 = st.text_input("Source 2:")
    st_dest2 = st.text_input("Destination 2:")
    submit = st.form_submit_button("Add")
    if submit:
      add_config(st_name, st_src, st_dest, st_src2, st_dest2)
      st.rerun()

with tab3:
  show_config()
  with st.form("delete", clear_on_submit=True):
    st_delete = st.text_input("Delete Index:")
    delete = st.form_submit_button("Delete", type="primary")
    if delete:
      delete_config(int(st_delete))
      st.rerun()
