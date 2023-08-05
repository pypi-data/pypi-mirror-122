import os
import urllib.request as urllib
import platform
import requests
from colorama import init, Fore

init(autoreset=True)

# Here is the function to know the public ip, do not modify this function unless you find an error.


def GetIpPublica():
    try:
        server = 'https://www.ifconfig.me/ip'
        consulta = urllib.build_opener()
        consulta.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0')]
        url = consulta.open(server, timeout=17)
        response = url.read()
        try:
            response = response.decode('UTF-8')
        except UnicodeDecodeError:
            response = response.decode('ISO-8859-1')

        url.close()
        return response
    except:
        return None


def sysinfo():
    print('Uname:', platform.uname())
    print('Machine :', platform.machine())
    print('Node :', platform.node())
    print('Processor :', platform.processor())
    print('Release :', platform.release())
    print('System :', platform.system())
    print('Version :', platform.version())
    print('Platform :', platform.platform())

# The server class contains the components of the system menu, if you edit or add some function in the class you would be adding new content for the system.


class server:

    def __init__(self):
        pass

    def infoc(self, command):
        os.system("man {}".format(command))

    def level(self, nivel):
        os.system("init {}".format(nivel))

    def systeminfo(self):
        print(Fore.CYAN + "Machine architecture:")
        os.system("uname -m")
        print(Fore.CYAN + "Kernel version used:")
        os.system("uname -r")
        print(Fore.CYAN + "Ubuntu system specifications:")
        os.system("lshw")
        print(Fore.CYAN + "Private IP Address:")
        os.system("ifconfig wlan0")
        print(Fore.CYAN + "Public IP Address:")
        ip = GetIpPublica()
        print(ip)
        print(Fore.CYAN + "More system information:")
        os.system("inxi")
        sysinfo()
        print(Fore.CYAN + "Hardware information:")
        os.system("lscpu")
        print(Fore.CYAN + "Username:")
        os.system("whoami")

    def listusers(self):
        os.system("awk -F: '{ print $1}' /etc/passwd")

    def addnewuser(self, user):
        os.system("adduser {}".format(user))

    def verifylogin(self):
        os.system("w")

    def verifylastlogin(self):
        os.system("last")

    def checkcpuprocesses(self):
        os.system("top")

    def checkcpuprocessesstrace(self, pid):
        os.system("strace -d -p {}".format(pid))

    def checksystemprocesses(self):
        os.system("ps auxf")

    def destroyprocess(self, pip):
        os.system("kill -9 {}".format(pip))

    def checknetworktraffic(self):
        os.system("iftop")

    def checklistenerports(self):
        os.system("netstat -plunt")

    def checklistenerportslsof(self):
        os.system("lsof -p")

    def checkrootkit(self):
        os.system("chkrootkit")

    def scanweb(self, link):
        try:
            target = requests.get(url=link)
            header = dict(target.headers)
            for x in header:
                print(x + " : "+header[x])
        except:
            print(Fore.RED + "[*] Error, could not connect to server")
