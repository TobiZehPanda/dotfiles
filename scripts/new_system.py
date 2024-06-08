import os
import argparse

def parse_pacman():
  with open("/etc/pacman.conf", "r", encoding="UTF-8") as file:
    data = file.readlines()
    for i, line in enumerate(data):
      if line.startswith("#Color"):
        data.pop(i)
        data.insert(i, "Color\n")
      elif line.startswith("#Parallel"):
        data.pop(i)
        data.insert(i, "Parallel Downloads = 5\nILoveCandy\n")

  with open("/etc/pacman.conf", "w", encoding="UTF-8") as file:
    file.writelines(data)

def parse_sudoers():
  with open("/etc/sudoers", "r", encoding="UTF-8") as file:
    data = file.readlines()
    for i, line in enumerate(data):
      if line.startswith("# %wheel ALL=(ALL:ALL) ALL"):
        data.pop(i)
        data.insert(i, "%wheel ALL=(ALL:ALL) ALL")

  with open("/etc/sudoers", "w", encoding="UTF-8") as file:
    file.writelines(data)

def parse_hostname(hostname):
  with open("/etc/hostname", "w", encoding="UTF-8") as file:
    file.write(hostname)

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Quick setup for Archlinux')
  parser.add_argument('hostname')
  args = parser.parse_args()

  if os.geteuid() != 0:
    exit("You need root privileges to run this script!")

  os.system('timedatectl set-timezone America/Chicago')
  os.system('timedatectl set-ntp 1')
  os.system('localectl set-locale en_US.UTF-8')
  parse_pacman()
  parse_sudoers()
  parse_hostname(args.hostname)

