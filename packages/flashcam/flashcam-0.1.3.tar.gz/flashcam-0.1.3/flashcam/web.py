#!/usr/bin/env python3
'''
This is flask interface
'''
from flashcam.version import __version__
from fire import Fire
from flashcam import config

#--------------------------------------

from importlib import import_module
import os
import sys  #exit
from flask import Flask, render_template, render_template_string, Response, url_for
from flask import request
from flask import jsonify

import getpass
import datetime as dt
import time

from flask import request
#===== another auth.
from flask_httpauth import HTTPBasicAuth

import pantilthat

# block stuff depending on PC
import socket

import random

import cv2
import numpy as np

from flashcam.real_camera import Camera

app = Flask(__name__)

config.CONFIG['filename'] = "~/.config/flashcam/cfg.json"

Camera = Camera # creating the OBJECT


def logthis( ttt="Started" ):
    sss=dt.datetime.now().strftime("%Y/%m/%d %a %H:%M:%S")+" "+ttt+"\n"
    print(sss , end="")
    with open( os.path.expanduser("~/flashcam.log") ,"a+") as f:
        f.write( sss )


logthis()
remote_ip=""
auth = HTTPBasicAuth()

#---not fstring- {} would colide
index_page_refresh30 = """
 <meta http-equiv="refresh" content="30";>

<html>
<script>
function doDate()
{
    var str = "";

    var days = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
    var months = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

    var now = new Date();

    str +=  now.getHours() +":" + now.getMinutes() + ":" + now.getSeconds();
    document.getElementById("todaysDate").innerHTML = str;
}

setInterval(doDate, 200);
</script>
  <head>
    <title>Video Streaming</title>
  </head>
  <body>

<p>
<div id="todaysDate"></div>
</p>
    <!--h1>Video Streaming Demonstration</h1-->
    <img src="{{url}}">
<br>

  </body>
</html>

"""


index_page = """
 <!--meta http-equiv="refresh" content="5";-->

<html>
<script>
function doDate()
{
    var str = "";

    var days = new Array("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
    var months = new Array("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");

    var now = new Date();

    str +=  now.getHours() +":" + now.getMinutes() + ":" + now.getSeconds();
    document.getElementById("todaysDate").innerHTML = str;
}

setInterval(doDate, 200);
</script>
  <head>
    <title>Video Streaming</title>
  </head>
  <body>

<p>
<div id="todaysDate"></div>
</p>
    <!--h1>Video Streaming Demonstration</h1-->
    <img src="{{url}}">
<br>

  </body>
</html>

"""
#    <img src="{{ url_for('video') }}">



@auth.verify_password
def verify_password(username, password):
#    user = User.query.filter_by(username = username).first()
#    if not user or not user.verify_password(password):
#        return False
#    g.user = user
    config.load_config()
    config.show_config()
    u = config.CONFIG["user"]
    p = config.CONFIG["password"]
    #u=getpass.getuser()
    #p=u+u
    # try:
    #     with open( os.path.expanduser("~/.pycamfw_pass") ) as f:
    #         print("YES---> FILE  ","~/.pycamfw_pass")
    #         p=f.readlines()[0].strip()
    # except:
    #     print("NO FILE  ","~/.pycamfw_pass")

    if (username==u) and (password==p):
        logthis( "   TRUE  checking userpass (verify)"+username+"/"+password+"/")
        logthis( "   TRUE  checking userpass (real  )"+u+"/"+p+"/")
        return True
    else:
        logthis( "   FALSE checking userpass (verify)"+username+"/"+password+"/")
        logthis( "   FALSE checking userpass (real  )"+u+"/"+p+"/")
        return False




@app.route('/')
@auth.login_required
def index():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " / remote      = "+request.remote_addr )
    logthis( " / remote xreal= "+remote_ip )
    url = url_for('video')
    print(url)
    return render_template_string(index_page, url=url)

@app.route('/refresh30')
@auth.login_required
def index30():
    global remote_ip
    """Video streaming home page."""
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " / remote      = "+request.remote_addr )
    logthis( " / remote xreal= "+remote_ip )
    url = url_for('video')
    print(url)
    return render_template_string(index_page_refresh30, url=url)


#('index.html')

@app.route('/video')
@auth.login_required
def video():
    print("VIDEO")
    remote_ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    logthis( " /video remote      = "+request.remote_addr )
    logthis( " /video remote xreal= "+remote_ip )
    # i return JPG TO AXIS CAMERA....
    #---------------this is MJPEG-------------------------
    #config.CONFIG["product"] = "Webcam C270"
    return Response(gen(Camera(config.CONFIG["product"], "640x480"),remote_ip),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



#========================================= CAMERA GEN ===


def gen(camera, remote_ip, blend=False, bigtext=True):
    """ returns jpeg;
    can do modifications per USER !
    can send only some frames
    """
    print("D... gen")
    framecnt = 0
    framecnttrue = 0
    ss_time = 0

    while True:
        time.sleep(0.3)
        framecnt+=1
        print("D... get_frame (gen)")
        frame = camera.get_frame()
        print("D... got_frame (gen)")
        start = dt.datetime.now()
        blackframe = np.zeros((480,640,3), np.uint8)
        #frame = blackframe
        if blend:
            frame = 0.5*frame + 0.5*imgs[ random.randint(0,len(imgs)-1) ]

        if bigtext:
            frame = cv2.putText(
                img = frame,
                text = dt.datetime.now().strftime("%H:%M:%S"),
                org = (10, 100),
                fontFace = cv2.FONT_HERSHEY_DUPLEX,
                fontScale = 2.0,
                color = (125, 246, 55),
                thickness = 3
            )
            frame = cv2.putText(
                img = frame,
                text = f"{framecnt:6d} {ss_time:.3f}",
                org = (10, 50),
                fontFace = cv2.FONT_HERSHEY_DUPLEX,
                fontScale = 1.0,
                color = (125, 246, 55),
                thickness = 1
            )
        #----- i dont send None now, but this helped to avoid crash
        if not(frame is None):
            frame=cv2.imencode('.jpg', frame)[1].tobytes()
        else:
            continue
        stop = dt.datetime.now()
        ss_time = (stop-start).total_seconds()

        #===== MAYBE THIS IS WASTING - it should throw get_frame
        #  but with -k sync   it restarts

        # yield ( frame)  #--------- JPEG vs MJPEG
        yield (b'--frame\r\n' # ---- JPEG
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




if __name__ == '__main__':

    # very first config should know if pantilt is installed
    config.load_config()
    #if v4i.check_pantilt():
    #    config.CONFIG['pantilt'] = True
    #    config.save_config()

    app.run(host='0.0.0.0', port=config.CONFIG['port'], threaded=True)
