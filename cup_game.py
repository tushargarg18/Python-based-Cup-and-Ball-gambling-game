import numpy as np
import cv2
import math
import time
#returns the distance between two coordinates
def distance(a1,b1,a2,b2):
    return(math.sqrt((a2-a1)*(a2-a1)+(b2-b1)*(b2-b1)))
flag=0
flag1=0
flag2=0
x=0
y=0
timem=2
times=60
#inital colour of the object here yellow
lower=np.array([20, 100, 100])
upper=np.array([30, 255, 255])
#colour of the cup here green
upper1=np.array([102,255,255])
lower1=np.array([33,80,40])
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
cap=cv2.VideoCapture(0)
while 1:
    ret,frame=cap.read(0)
    img=cv2.resize(frame,(340,220))
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #masking the given coloured object only
    mask=cv2.inRange(hsv,lower,upper) 
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    maskFinal=maskClose
    #finding the closed contours in the masked image
    image,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #if any contour is found that means intial object is detected
    if(conts):
        flag=1
        maxm=0
        #finding the contour no. with highest area
        for i in range (0,len(conts)):
            if((cv2.contourArea(conts[i]))>maxm):
                maxm=cv2.contourArea(conts[i])
                now=i
        #finding the radius and center of the detected object
        (x,y),radius = cv2.minEnclosingCircle(conts[now])
        center = (int(x),int(y))
        radius = int(radius)
        #drawing a circle on the actuall image using the radius and center
        cv2.circle(img,center,radius,(0,255,0),2)
        cv2.imshow("cam",img)
        cv2.waitKey(1)
    else:
        cv2.destroyAllWindows()
        #after the intial object is detected the game begins when the object is disappeared
        if(flag==1):
            x2=x
            y2=y
            radius2=radius
            center2=center
            elaps=120
            while (elaps):
                font=cv2.FONT_HERSHEY_SIMPLEX
                dis1=100
                elaps=60-int(time.clock())
                print(elaps)
                ret,frame1=cap.read()
                img1=cv2.resize(frame1,(340,220))
                hsv1=cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)
                mask1=cv2.inRange(hsv1,lower1,upper1)
                maskOpen1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,kernelOpen)
                maskClose1=cv2.morphologyEx(maskOpen1,cv2.MORPH_CLOSE,kernelClose)
                maskFinal1=maskClose1
                image1,conts1,h1=cv2.findContours(maskFinal1.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                if(conts1):
                    for i in range (len(conts1)):
                        (x1,y1),radius1 = cv2.minEnclosingCircle(conts1[i])
                        dis2=distance(x,y,x1,y1)
                        if(dis2<dis1):
                            dis1=dis2
                            x2=x1
                            y2=y1
                            radius2=int(radius1)
                    center2 = (int(x2),int(y2))
                    cv2.circle(img1,center2,5,(255,0,0),15)
                    cv2.putText(img1,"TRACK",(int(x2),int(y2)),font,0.8,(0,0,255),2,cv2.LINE_AA)  
                    cv2.imshow("cam1",img1)
                    cv2.waitKey(1)
                    x=x2
                    y=y2
            font=cv2.FONT_HERSHEY_SIMPLEX
            img2=cv2.resize(frame1,(340,220))
            cv2.circle(img2,center2,5,(255,0,0),15)
            cv2.putText(img2,"I'm Here !",(int(x2),int(y2)),font,0.6,(0,0,255),2,cv2.LINE_AA) 
            cv2.imshow("cam2",img2)
            cv2.waitKey(10)
            flag1=1
        if(flag1==1):
            break
while(1):
    ret,frame4=cap.read(0)
    img4=cv2.resize(frame4,(340,220))
    cv2.imshow('check',img4)
    if(cv2.waitKey(1)==27):
        cap.release()
        cv2.destroyAllWindows()
        break
