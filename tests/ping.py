import netifaces # For getting the network interfaces

import platform    # For getting the operating system name
import subprocess  # For executing a shell command

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '4', host]

    # Pinging
    return subprocess.call(command) == 0

def main():
    while True:
        teste = 1;
        print("teste" + str(teste))
        teste = teste + 1
        

if __name__ == "__main__":
    main()

