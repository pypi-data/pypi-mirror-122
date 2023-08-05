from adminserver.main import *

server = server()

infocommand = server.infoc
level = server.level
systeminfo = server.systeminfo
listusers = server.listusers
addnewuser = server.addnewuser
verifylogin = server.verifylogin
verifylastlogin = server.verifylastlogin
cpuprocesses = server.checkcpuprocesses
cpustrace = server.checkcpuprocessesstrace
systemprocesses = server.checksystemprocesses
destroyprocess = server.destroyprocess
networktraffic = server.checknetworktraffic
listenerports = server.checklistenerports
portslsof = server.checklistenerportslsof
rootkit = server.checkrootkit
scanweb = server.scanweb
