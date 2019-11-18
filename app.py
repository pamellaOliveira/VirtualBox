from flask import Flask, render_template, request
import subprocess
import json
import threading
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

def ajeitandoListarVms(out):
    infoVMS = {}
    aux = out.decode('utf-8')
    vms = aux.split("Configured memory balloon size")
    for j in range(len(vms)-1):
        dic = {}
        a = str(vms[j])
        b = a.split("\r\n")
        for i in b:
            if "Name:" in i:
                aux2 = i.split()
                valor = str(aux2[-1])
                dic["Name"] = valor
            if "Guest OS" in i and "Windows" in i:
                aux2 = i.split()
                dic["Guest OS"] = str(aux2[-3] + aux2[-2] + aux2[-1])
            if "Guest OS" in i and "Ubuntu" in i:
                aux2 = i.split()
                dic["Guest OS"] = str(aux2[-2] + aux2[-1])
            if "Memory size" in i:
                aux2 = i.split()
                dic["Memory size"] = str(aux2[-1])
            if "Hardware UUID" in i:
                aux2 = i.split()
                dic["Hardware UUID"] = str(aux2[-1])
            if "Number of CPUs" in i:
                aux2 = i.split()
                dic["Number of CPUs"] = str(aux2[-1])
        infoVMS[j] = dic
        #print(infoVMS)
    return infoVMS


def listarVMs():
    mPath = '"C:\\Program Files\\Oracle\\VirtualBox\\VboxManage"'
    command = " list -l vms"
    junto = mPath + command
    proc = subprocess.Popen(junto,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    listaVMS = ajeitandoListarVms(out)
    return listaVMS

@app.route('/',methods = ['POST'])
def retornaValores():
    nomeNova = request.form['nomeNova']
    cpu = request.form['cpu']
    memoria = request.form['memoria']
    so = request.form['so']
    nomeVelhaVM = buscandoNomeVM(so)
    print(so)
    #clonarVM(nomeVelhaVM,nomeNova)
    #modificarMemoria(nomeNova,memoria)
    #modificarCpu(nomeNova,cpu)
    t1 = threading.Thread(target= clonarVM,args=(nomeVelhaVM,nomeNova))
    t2 = threading.Thread(target= modificarMemoria, args= (nomeNova,memoria))
    t3 = threading.Thread(target= modificarCpu, args= (nomeNova,cpu))
    t4 = threading.Thread(target= startandoVM, args= (nomeNova,))
    t1.start()
    t1.join()
    t2.start()
    t2.join()
    t3.start()
    t3.join()
    t4.start()
    t4.join()
    return listarVMs()


def buscandoNomeVM(so): 
    if str(so) == "2":
        nameVM = "win7"
    if str(so) == "1":
        nameVM = "ubuntu2"
    return nameVM

def startandoVM(nomeNova):
    mPath = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage"'
    command = " startvm " + nomeNova 
    junto = mPath + command
    proc = subprocess.Popen(junto,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("startando")
    return junto


def clonarVM(nomeVelhaVM,nomeNova):
    mPath = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage"'
    command = " clonevm " + nomeVelhaVM + " --name " + nomeNova +  " --register"
    junto = mPath + command
    print(junto)
    proc = subprocess.Popen(junto,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("clonando")
    return junto


def modificarMemoria(nomeNova,memoria):
    mPath = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage"'
    command = " modifyvm " + nomeNova + " --memory " + memoria 
    junto = mPath + command
    proc = subprocess.Popen(junto,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("memoria")
    return junto 

def modificarCpu(nomeNova,cpu):
    mPath = '"C:\\Program Files\\Oracle\\VirtualBox\\VBoxManage"'
    command = " modifyvm " + nomeNova + " --cpus " + cpu 
    junto = mPath + command
    print("cpu")
    proc = subprocess.Popen(junto,stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return junto
app.run(port=5000,debug=True)