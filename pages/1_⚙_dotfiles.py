import os
import time
import utils.global_var
from utils.global_var import absolute_path
import streamlit as st
from streamlit_extras.grid import grid
import pandas as pd

CONFIG = utils.global_var.CONFIG

st.set_page_config(
  page_title="dotfiles",
  page_icon="⚙️"
)


def add_config(name, src, dest, *argv):
  if not argv[0] and not argv[1]:
    data = pd.DataFrame({"name": [name], "src": [src], "dest":[dest], "extra":[False], "src2":[argv[0]], "dest2":[argv[1]]})
  else:
    data = pd.DataFrame({"name": [name], "src": [src], "dest":[dest], "extra":[True], "src2":[argv[0]], "dest2":[argv[1]]})
  data.to_csv(CONFIG, mode="a", index=False, header=False)

def check_exists(path):
  exist = False
  if os.path.isfile(path):
    exist = True
  elif os.path.isdir(path):
    exist = True
  elif os.path.islink(path):
    exist = True
  return exist

def check_installed(app_names, app_data):
  app_not_installed = app_names[:]
  counter = 0
  for name in app_names[:]:
    if check_exists(absolute_path(app_data['dest'][counter])):
      app_names.remove(name)
    else:
      app_not_installed.remove(name)
    counter += 1
  return app_names, app_not_installed

def delete_config(index):
  df = pd.read_csv(CONFIG)
  df.drop([index]).to_csv(CONFIG, mode="w", index=False, header=True)

def edit_config():
  if not os.path.isfile(CONFIG):
    with open(CONFIG, "w", encoding="UTF-8") as f:
      f.write("name,src,dest,extra,src2,dest2\n")
  df = pd.read_csv(CONFIG)
  df['name'] = df['name'].astype(str)
  df['src'] = df['src'].astype(str)
  df['dest'] = df['dest'].astype(str)
  df['src2'] = df['src2'].astype(str)
  df['dest2'] = df['dest2'].astype(str)
  df['extra'] = df['extra'].astype(bool)
  update_df = st.data_editor(df, use_container_width=True, hide_index=True).sort_values(by=['name'])
  update_df.to_csv(CONFIG, mode="w", index=False, header=True)

def install(app_data):
  if os.path.islink(absolute_path(app_data['dest'])):
    st.warning(f"Link found at {app_data['dest']}.. Removing!")
    os.unlink(absolute_path(app_data['dest']))
    if app_install['extra'].item() and os.path.islink(absolute_path(app_data['dest2'])):
      st.warning(f"Link found at {app_data['dest2']}.. Removing!")
      os.unlink(absolute_path(app_data['dest2']))
  elif os.path.isfile(absolute_path(app_data['dest'])):
    st.warning(f"File found at {app_data['dest']}.. Removing!")
    os.remove(absolute_path(app_data['dest']))
    if app_install['extra'].item() and os.path.isfile(absolute_path(app_data['dest2'])):
      st.warning(f"File found at {app_data['dest2']}.. Removing!")
      os.remove(absolute_path(app_data['dest2']))
  elif os.path.isdir(absolute_path(app_data['dest'])):
    st.warning(f"Directory found at {app_data['dest']}.. Removing!")
    os.rmdir(absolute_path(app_data['dest']))
    if app_install['extra'].item() and os.path.isdir(absolute_path(app_data['dest2'])):
      st.warning(f"Directory found at {app_data['dest2']}.. Removing!")
      os.rmdir(absolute_path(app_data['dest2']))
  st.info(f"Installing {app_data['name']} links! ({app_data['dest']})")
  os.symlink(absolute_path(app_data['src']), absolute_path(app_data['dest']))
  if app_install['extra'].tolist():
    st.info(f"Installing {app_data['name']} links! ({app_data['dest2']})")
    os.symlink(absolute_path(app_data['src2']), absolute_path(app_data['dest2']))

def remove(app_data):
  st.info(f"Removing {app_data['name']} ({app_data['dest']})")
  os.unlink(absolute_path(app_data['dest']))
  if app_data['extra'].item():
    st.info(f"Removing {app_data['name']} ({app_data['dest2']})")
    os.unlink(absolute_path(app_data['dest2']))

def init_config():
  if not os.path.isfile(CONFIG):
    with open(CONFIG, "w", encoding="UTF-8") as f:
      f.write("name,src,dest,extra,src2,dest2\n")

tab1, tab2, tab3, tab4 = st.tabs(["Install Configs", "Remove Configs", "Add/Edit", "Delete"])

init_config()

with tab1:
  dataframe = pd.read_csv(CONFIG)
  app_list, app_not_installed_list = check_installed(dataframe['name'].tolist(), dataframe)
  app_config = st.multiselect('Choose configs to systemlink:', app_list)
  button = st.button('Submit')

  if button and app_config:
    st.success("Installing configs....")
    for app in app_config:
      app_install = dataframe[dataframe['name'].str.match(app)]
      install(app_install.iloc[0])
    st.success("Done! :3")
    time.sleep(2)
    st.rerun()

with tab2:
  app_remove_list = st.multiselect('Choose configs to remove:', app_not_installed_list)
  button = st.button('Remove', type="primary")

  if button and app_remove_list:
    for app in app_remove_list:
      app_remove = dataframe[dataframe['name'].str.match(app)]
      remove(app_remove.iloc[0])
    st.success("Done :3")
    time.sleep(2)
    st.rerun()

with tab3:
  edit_config()
  with st.form("add", clear_on_submit=True):
    st_grid = grid(1, 2, 2)
    st_name = st_grid.text_input("Name*:")
    st_src = st_grid.text_input("Source*:")
    st_dest = st_grid.text_input("Destination*:")
    st_src2 = st_grid.text_input("Source 2:")
    st_dest2 = st_grid.text_input("Destination 2:")
    st_grid.caption(r':red[_\* is required_]')
    submit = st_grid.form_submit_button("Add")
    if submit:
      if len(st_name) == 0:
        st.error("Name is empty!")
        st.stop()
      if len(st_src) == 0:
        st.error("Source is empty!")
        st.stop()
      if len(st_dest) == 0:
        st.error("Destination is empty!")
        st.stop()
      add_config(st_name, st_src, st_dest, st_src2, st_dest2)
      st.rerun()

with tab4:
  dataframe = pd.read_csv(CONFIG)
  st.dataframe(dataframe, use_container_width=True)
  with st.form("delete", clear_on_submit=True):
    st_delete = st.text_input("Delete Index:")
    delete = st.form_submit_button("Delete", type="primary")
    if delete:
      delete_config(int(st_delete))
      st.rerun()
