import re
import os
import pandas as pd
import streamlit as st

st.set_page_config(
  page_title="SSH",
  page_icon="🖥️"
)

def absolute_path(path):
  return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

def parse_line(line):
  for key, rx in rx_dict.items():
    match = rx.search(line)
    if match:
      return key, match
  return None, None

def parse_file(filepath):
  df = []
  df = pd.DataFrame(df, columns=['Host', 'HostName', 'User', 'Port', 'IdentityFile', 'LogLevel', 'Compression'])
  counter = -1
  with open(filepath, 'r', encoding='UTF-8') as file:
    line = file.readline()
    while line:
      key, match = parse_line(line)
      if key == 'host':
        counter += 1
        host = match.group('host')
        df.at[counter, 'Host'] = host
      if key == 'hostname':
        hostname = match.group('hostname')
        df.at[counter, 'HostName'] = hostname
      if key == 'user':
        user = match.group('user')
        df.at[counter, 'User'] = user
      if key == 'port':
        port = match.group('port')
        df.at[counter, 'Port'] = port
      if key == 'identity':
        identity = match.group('identity')
        df.at[counter, 'IdentityFile'] = identity
      if key == 'log':
        log = match.group('log')
        df.at[counter, 'LogLevel'] = log
      if key == 'compression':
        compression = match.group('compression')
        df.at[counter, 'Compression'] = compression
      line = file.readline()
  return df

def write_data(df):
  with open(FILE, 'w', encoding='UTF-8') as f:
    for counter in range(0, len(df.index)):
      for key, value in zip(df.columns.tolist(), df.loc[counter].tolist()):
        if not pd.isnull(value):
          f.write(f"{key} {value}\n")

        if re.search(r'.*', key):
          f.write("\t")
      f.write("\n")

FILE = absolute_path("~/.ssh/config")
rx_dict = {
  'host': re.compile(r'Host (?P<host>.*)\n'),
  'hostname': re.compile(r'HostName (?P<hostname>.*)\n'),
  'user': re.compile(r'User (?P<user>.*)\n'),
  'port': re.compile(r'Port (?P<port>\d+)\n'),
  'identity': re.compile(r'IdentityFile (?P<identity>.*)\n'),
  'log': re.compile(r'LogLevel (?P<log>.*)\n'),
  'compression': re.compile(r'Compression (?P<compression>.*)\n')
}

tab1, tab2, tab3 = st.tabs(['Show', 'Add', 'Delete'])

with tab1:
  data = parse_file(FILE)
  st.dataframe(data, use_container_width=True, hide_index=True)
  refresh = st.button("Refresh")
  if refresh:
    st.rerun()

with tab2:
  data = parse_file(FILE)
  data = st.data_editor(data, use_container_width=True, hide_index=True)
  data = data.replace([''], [None])
  write_data(data)
  add = st.button("Add")
  if add:
    data.loc[len(data.index)] = ['TEMP', None, None, None, None, None, None]
    write_data(data)
    st.rerun()

with tab3:
  data = parse_file(FILE)
  st.dataframe(data, use_container_width=True)
  with st.form("delete", clear_on_submit=True):
    delete_input = st.text_input("Delete Index:")
    delete = st.form_submit_button("Delete", type="primary")
    if delete:
      data = data.drop([int(delete_input)])
      write_data(data)
      st.rerun()

