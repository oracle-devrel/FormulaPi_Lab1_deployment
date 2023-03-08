import os
import subprocess, re
import psutil
import yaml
import time
import json

from flask import Flask, render_template, url_for, redirect, request

# global config
# global devicename
# global gamehost
# global f1fwd
# global f1store
# global dburl

app = Flask(__name__)

storeyml = os.environ['F1SIM_HOME'] + "/f1store.yaml" 

def load_f1store():
    global config
    global devicename
    global gamehost
    global f1fwd
    global f1store
    global dburl
    global rmqusername
    global rmqpassword
    global storetxt
    global hometrack
    global gameversion
    global leaderboardurl
    global registrationurl
    global runningguideurl

    with open(storeyml, 'r') as f:
        storetxt = f.read()
        config = yaml.safe_load(storetxt)
    devicename = config['devicename']
    gamehost = config['gamehost']
    f1fwd = config['forward']
    f1store = config['store']
    dburl = config['oracledb']['properties']['dburl']
    rmqusername = config['rabbitmq']['properties']['rmqusername']
    rmqpassword = config['rabbitmq']['properties']['rmqpassword']
    hometrack = config['hometrack']
    gameversion = config['version']
    leaderboardurl = config['leaderboard']
    registrationurl = config['registration']
    runningguideurl = config['runningguide']

def save_f1store():
    with open(storeyml, 'w') as f:
        f.write(storetxt)

# initial load of f1store.yaml
load_f1store()

@app.route('/')
def index():
    return render_template('index.html', dname=devicename, ghost=gamehost)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/circuit')
def circuit():
    data = {'hometrack': hometrack, 'packetformat': gameversion}
    return render_template('livemap.html', data=data)

@app.route('/telemetry')
def telemetry():
    data = {'rmqusername': rmqusername, 'rmqpassword': rmqpassword, 'hometrack': hometrack, 'packetformat': gameversion}
    return render_template('f1telemetry.html', data=data)

@app.route('/leaderboard')
def leaderboard():
    return redirect(leaderboardurl)

@app.route('/registration')
def registration():
    return redirect(registrationurl)

@app.route('/runningguide')
def runningguide():
    return redirect(runningguideurl)

@app.route('/jetDB')
def jet():
    return render_template('f1Jet.html')

@app.route('/chart')
def charting():
    return render_template('chart.html')

@app.route('/rbr/<car>')
def modelviewer(car):

    modelURL = url_for('static', filename='images/RB_18_Max_v05')

    if car == "rb16":
        modelURL = url_for('static', filename='images/F1RB16B_v44')

    return render_template('f1Model.html', model=modelURL)

@app.route('/api/services')
def s_stats():
    processes = []

    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            processes.append((processName , ' ::: ', processID))
            # print(processName , ' ::: ', processID)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    proc = {'running': ' '.join(str(e) for e in processes)}

    stream = os.popen('python3 web/info.py') 
    output = stream.read()

    info = {'status': 'true', 'output': output}

    f1prod = read_status('f1sim-producer')
    f1cons = read_status('f1sim-consumer')

    f1param = {'store': f1store, 'forward': f1fwd, 'db': dburl}

    body = {'process': proc, 'info': info, 'f1prod': f1prod, 'f1cons': f1cons, 'f1store': f1param}

    return body

@app.route('/service')
def services():
    f1cons = read_status('f1sim-consumer')
    if (("status" in f1cons) == False) or (("running" in f1cons['status']) == False):
        f1consbtn = 'Start Consumer'
    else:
        f1consbtn = 'Stop Consumer'
    f1prod = read_status('f1sim-producer')
    if (("status" in f1prod) == False) or (("running" in f1prod['status']) == False):
        f1prodbtn = 'Start Producer'
    else:
        f1prodbtn = 'Stop Producer'
    return render_template('service-status.html', dname=devicename, ghost=gamehost, f1consbtn=f1consbtn, f1prodbtn=f1prodbtn)

@app.route('/yaml')
def f1config():
    return render_template('f1yaml.html', storetxt = storetxt)

@app.route('/yaml/load')
def f1config_load():
    load_f1store()
    return redirect(url_for('f1config'))

@app.route('/yaml/save', methods=['POST'])
def f1config_save():
    global storetxt
    storetxt = request.form['storetxt'].replace('\r','')
    # print(storetxt)
    save_f1store()
    return redirect(url_for('f1config'))

@app.route('/test')
def testingMQ():
    return render_template('rmq_test.html')

@app.route('/control/producer')
def control_producer():
    f1prod = read_status('f1sim-producer')
    if (("status" in f1prod) == False) or (("running" in f1prod['status']) == False):
        control = 'start'
    else:
        control = 'stop'
    p =  subprocess.Popen(['sudo', 'systemctl', control, 'f1sim-producer'], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    # print(output)
    return redirect(url_for('services'))

@app.route('/control/consumer')
def control_consumer():
    f1cons = read_status('f1sim-consumer')
    if (("status" in f1cons) == False) or (("running" in f1cons['status']) == False):
        control = 'start'
    else:
        control = 'stop'
    p =  subprocess.Popen(['sudo', 'systemctl', control, 'f1sim-consumer'], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    # print(output)
    return redirect(url_for('services'))

def read_status(service):
    p =  subprocess.Popen(["sudo", "systemctl", "status",  service], stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    print(output)

    service_regx = r"Loaded:.*\/(.*service);"
    status_regx= r"Active:(.*) since (.*);(.*)"
    service_status = {}

    for line in output.splitlines():
        service_search = re.search(service_regx, line)
        status_search = re.search(status_regx, line)

        if service_search:
            service_status['service'] = service_search.group(1)
            #print("service:", service)

        if status_search:
            service_status['status'] = status_search.group(1).strip()
            #print("status:", status.strip())
            service_status['since'] = status_search.group(2).strip()
            #print("since:", since.strip())
            service_status['uptime'] = status_search.group(3).strip()
            #print("uptime:", uptime.strip())

    service_status['output'] = output
    return service_status

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0") 
