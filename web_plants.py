from flask import Flask, render_template, redirect, url_for
import psutil
import time
import datetime
import water
import os
import threading

app = Flask(__name__)
#gets the server time for the web site
def template(title = "HELLO!", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate
# sets the server time into template data using the above function
@app.route("/")
def hello():
    templateData = template()
    return render_template('main.html', **templateData)
#last watered reads the lastwartered.txt file and sends it back to the server
@app.route("/last_watered")
def checkLastWatered():
    templateData = template(text = water.getLastWatered())
    return render_template('main.html', **templateData)
#last time the tap was turned off
@app.route("/last_tap_off")
def checkLastTap_off():
    templateData = template(text = water.getLastTimeTapOff())
    return render_template('main.html', **templateData)

#sensor reads the sensor info to send to the site
#wrong way round
@app.route("/sensor")
def action():
    status = water.getStatus()
    message = ""
    if (status == 0):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)
# waters the pants once
@app.route("/water")
def action2():
    water.pumpOn()
    water.pumpOff()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)
@app.route("/first")
def first():
    thread1.start()
    running = True
    
#turns auto water on or off

@app.route("/auto/water/<toggle>")
def autoWater(toggle):
    running = None
    if toggle == "ON":
        running = True
        templateData = template(text = "Auto Watering On")
        #water.setup_auto(running, toggle)
        water.autoWater(running)
        #for process in psutil.process_iter():
        #try: # i think this try catch block should run the command or the auto water file is incorrect
                #and is not running the command in the auto water.py file
            #if process.cmdline()[0] == 'Water/auto_water.py':
                #templateData = template(text = "Already running")
                #running = True
        #except:
            #pass
        #if not running:
            #threading.Thread(target= water.auto_water()).start
    else:
        templateData = template(text = "Auto Watering Off")
        running = False
        #water.setup_auto(running, toggle)
        water.autoWater(running)
        os.system("pkill -f Water/water.py")
        

    return render_template('main.html', **templateData)

@app.route("/shutdown")
def shutdown():
    os.system("shutdown /s /t 1")

thread1 = threading.Thread(target = water.autoWater)

if __name__ == "__main__":
    app.run(debug=True)


   