import re
import os
import sys
import utils.global_var
import pandas as pd
import streamlit as st
from streamlit_extras.grid import grid
from loguru import logger

st.set_page_config(
  page_title="SSH",
  page_icon="🔗"
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
  df.index = range(len(df))
  with open(FILE, 'w', encoding='UTF-8') as f:
    for counter in range(0, len(df.index)):
      st.write(df.loc[counter])
      for key, value in zip(df.columns.tolist(), df.loc[counter].tolist()):
        if not pd.isnull(value):
          f.write(f"{key} {value}\n")

        if re.search(r'.*', key):
          f.write("\t")
      f.write("\n")

FILE = absolute_path("~/.ssh/config")
DIR = absolute_path("~/.ssh")
rx_dict = {
  'host': re.compile(r'Host (?P<host>.*)\n'),
  'hostname': re.compile(r'HostName (?P<hostname>.*)\n'),
  'user': re.compile(r'User (?P<user>.*)\n'),
  'port': re.compile(r'Port (?P<port>\d+)\n'),
  'identity': re.compile(r'IdentityFile (?P<identity>.*)\n'),
  'log': re.compile(r'LogLevel (?P<log>.*)\n'),
  'compression': re.compile(r'Compression (?P<compression>.*)\n')
}

if not os.path.exists(DIR):
  os.mkdir(DIR)
if not os.path.exists(FILE):
  open(FILE, 'a').close()

tab1, tab2, tab3 = st.tabs(['Show', 'Add', 'Delete'])

with tab1:
  data = parse_file(FILE)
  st.dataframe(data, use_container_width=True, hide_index=True)
  refresh = st.button("Refresh")
  if refresh:
    st.rerun()

with tab2:
  data = parse_file(FILE)
  with st.form("add", clear_on_submit=True):
    st_grid = grid(2, 2, 1, 2)
    st_host = st_grid.text_input("Name*")
    st_hostname = st_grid.text_input("IP Address/Hostname*")
    st_user = st_grid.text_input("User")
    st_port = st_grid.text_input("Port")
    st_identity = st_grid.text_input("Identity Path")
    st_log = st_grid.selectbox("Log Level", ("", "INFO", "VERBOSE"))
    st_compression = st_grid.selectbox("Compression", ("", "Yes", "No"))
    st_grid.caption(r':red[_\* is required_]')
    st_add = st.form_submit_button("Add")

  if st_add:
    if len(st_host) == 0:
      st.error("Name is required!")
      st.stop()
    if len(st_hostname) == 0:
      st.error("IP/Hostname is required!")
      st.stop()
    data.loc[len(data.index)] = [st_host, st_hostname, st_user, st_port, st_identity, st_log, st_compression]
    data = data.replace([''], [None])
    write_data(data.sort_values(by='Host'))
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
