import os

def absolute_path(path):
  return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

CONFIG = "configurations.csv"
