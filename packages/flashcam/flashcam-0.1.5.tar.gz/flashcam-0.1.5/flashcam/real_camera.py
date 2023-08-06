import cv2
from flashcam.base_camera2 import BaseCamera

from flashcam.usbcheck import recommend_video
# import base_camera  #  Switches: slowrate....

import datetime
import time
import socket

import glob

import subprocess as sp
import numpy as np

import flashcam.config as config


class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def init_cam():
        """
        should return videocapture device
        but also sould set Camera.video_source
        """
        res = "640x480"
        print("D... init_cam caleld with:", res)
        print("i... init_cam caleld with:", res)
        print("\n\ni... IS  is ALREADY init ?????????:",  config.CONFIG["camera_on"],"\n\n\n")

        #if config.CONFIG["camera_on"]:
        #    print("i... init_cam is ALREADY ON:" )
        #    return cap

        vids = recommend_video( config.CONFIG["recommended"]  )
        if len(vids)>0:
            vidnum = vids[0]
            cap = cv2.VideoCapture(vidnum,  cv2.CAP_V4L2)

            # config.CONFIG["camera_on"] = True

            # - with C270 - it showed corrupt jpeg
            # - it allowed to use try: except: and not stuck@!!!
            #cap = cv2.VideoCapture(vidnum)
            #   70% stucks even with timeout
            pixelformat = "MJPG"
            w,h =  int(res.split("x")[0]), int(res.split("x")[1])
            fourcc = cv2.VideoWriter_fourcc(*pixelformat)
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,   w )
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  h )
            return cap
        return None


    @staticmethod
    def frames():
        """
        vidnum = number; res 640x480;
        recommended= ... uses the recommend_video to restart the same cam
        """
        print("i... frames enterred")

        cap = Camera.init_cam(  )
        nfrm = 0
        if config.CONFIG["recommended"]:
            wname = "none "
        else:
            wname = config.CONFIG["recommended"]
        frame_prev = None
        while True:

            timeoutok = False
            ret = False
            frame = None
            if (cap is None) or (not cap.isOpened()):
                print("X... camera None or not Opened)")
                ret = False
            else:
                try: #----this catches errors of libjpeg with cv2.CAP_V4L2
        #            with timeout(3): #--- this may help when no CAP_V4L2; MAYNOT
                    print(f"i... frame {nfrm:8d}   ", end="\r" )
                    ret, frame = cap.read()
                    BaseCamera.nframes+=1

                    #wname = f"res {frame.shape[1]}x{frame.shape[0]}"
                    nfrm+=1
                    print(f"D... got frame (frames iter)   ret={ret}  {frame.shape}")
        #        except TimeoutError:
        #            timeoutok = True
        #            nfrm = 0
                except Exception as ex:
                    print("D... SOME OTHER EXCEPTION ON RECV...", ex)
                    config.CONFIG["camera_on"] = False

    #        if  timeoutok:
    #            print("X... timout")

            if not ret:
                time.sleep(0.5)
                #vids = recommend_video(recommended) # try to re-init the same video
                #if len(vids)>0:
                #    vidnum = vids[0]
                config.CONFIG["camera_on"] = False

                cap = Camera.init_cam( )
                nfrm = 0

                # create gray + moving lines BUT prev_frame is bad sometimes
                try:
                    print("D... trying to gray frame")
                    frame = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
                    height, width = frame.shape[0] , frame.shape[1]

                    skip = 10
                    startl = 2*(nfrm % skip) # moving lines
                    for il in range(startl,height,skip):
                        x1, y1 = 0, il
                        x2, y2 = width, il
                        #image = np.ones((height, width)) * 255
                        line_thickness = 1
                        cv2.line(frame, (x1, y1), (x2, y2), (111, 111, 111),
                                 thickness=line_thickness)
                except:
                    print("X... prev_frame was bad, no gray image")

            #print("D... ret==", ret)
            if ret:
                frame_prev = frame
                if datetime.datetime.now().second %2 == 0:
                    cv2.circle(frame, (10,10), 10, (0,0,255), -1 )
                else:
                    cv2.circle(frame, (10,10), 10, (0,255,0), -1 )

            #if not(ret): # i will send gray or crap. Not None
            #    frame = None
            #    print("D... yielding ok")
            yield frame
                # cv2.namedWindow( wname, cv2.WINDOW_KEEPRATIO)
                # cv2.resizeWindow(wname, frame.shape[1], frame.shape[0] )
                # cv2.imshow( wname , frame );
                # k = cv2.waitKey(1)
                # if k == ord("q"):
                #     break

    @staticmethod
    def set_video_source(source):

        print("D... set_video_source: source=", source)
        camera = cv2.VideoCapture( source,  cv2.CAP_V4L2)
        print("D... ",camera)
        print("D... setting MJPG writer....FMP4 works too")
        # camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('F','M','P','4'))
        print("D... first camera read ....")
        ok = False
        try:
            _, img = camera.read()
            print(img.size) # this can fail and reset to DEV 0
            ok = True
        except Exception as ex:
            print("X... CAMERA read ... FAILED",ex)

        if ok:
            return camera
        return None



    @staticmethod
    def nonoframes():
        """
        INIT CAMERA
        YIELD FRAMES
        """
        print("D............ FRAMES .... first entry")

        camera = Camera.set_video_source( 1 )

        if (camera is None) or (not camera.isOpened()):
            print("X... cannot start the camera")
            yield ""
            # raise error will not help - neither for killing all
            # quit will not help neither
            raise RuntimeError('Could not start camera.')

        while True:
            # time.sleep(0.002)
            _, img = camera.read()
            # time.sleep(0.002)

            BaseCamera.nframes+=1

            #====================== historically here I did changes ========

            # encode as a jpeg image and return it
            #

            if datetime.datetime.now().second %2 == 0:
                cv2.circle(img, (10,10), 10, (0,0,255), -1 )
            else:
                cv2.circle(img, (10,10), 10, (0,255,0), -1 )


            try:
                pic=img # img is ntuple; i can send tuple
                #pic=cv2.imencode('.jpg', img)[1]  # [1] is ndarray
                #pic=cv2.imencode('.jpg', img)[1].tobytes()
            except:
                print("X... yieldin None ... camera off?")
                time.sleep(0.2)
                pic=""
                pic=None
            #print( type(pic) , len(pic)) # pic hight
            yield pic
            ###########################################   OK
