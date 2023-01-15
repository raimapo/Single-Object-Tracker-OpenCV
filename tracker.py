import cv2
import math
import keyboard
from coordinates import coordinates

rect = (0,0,0,0)
startPoint = False
endPoint = False
drawPoint = False
clear=False

tracker_types = ['CSRT', "DaSiamRPN"]
tracker_type = tracker_types[0]

if tracker_type == "CSRT":
    tracker = cv2.legacy.TrackerCSRT_create()
if tracker_type == "DaSiamRPN":
    tracker = cv2.TrackerDaSiamRPN_create()


def on_mouse(event,x,y,flags,params):
    global rect,startPoint,endPoint,drawPoint,clear
    
    if keyboard.is_pressed('q'):
      # get mouse click
      if event == cv2.EVENT_LBUTTONDOWN:
        rect = (x, y, 0, 0)
        startPoint = True
        clear=False
        if startPoint == True and endPoint == True:
            endPoint = False
                       
      if event == cv2.EVENT_MOUSEMOVE and startPoint == True and endPoint == False:
        rect = (rect[0], rect[1], x, y)
        drawPoint = True
     
      if event == cv2.EVENT_LBUTTONUP:
        rect = (rect[0], rect[1], x, y)
        endPoint = True
    else:
      if event == cv2.EVENT_LBUTTONDOWN:
        rect = (x-20, y-20, x+20, y+20)
        startPoint = True
        endPoint = True
        drawPoint = True
        clear=False

# define a video capture object
vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow('Tracker',cv2.WINDOW_KEEPRATIO)
cv2.setWindowProperty('Tracker',cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
#cv2.setWindowProperty('Tracker',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
w=vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
h=vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

while(True):
    
  # Capture the video frame
  # by frame
  ret, frame = vid.read()
 
  cv2.setMouseCallback('Tracker', on_mouse)

  if startPoint == True and endPoint == True:       
    coord=coordinates(rect)
    bbox=coord.corrected()
    ok = tracker.init(frame, bbox)
    startPoint = False
  
  timer = cv2.getTickCount()

  if endPoint == True and startPoint == False and clear==False:
        ok, bbox = tracker.update(frame)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            frame = cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            #rectcenter = ((bbox[0]+bbox[2]), (bbox[1]+bbox[3]))
            #print(rectcenter)
            frame = cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        else :
            # Tracking failure
            frame = cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
           
    #frame = cv2.putText(frame, numbers_to_strings(args.trackers) + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
    #drawing rectangle in real time
  if startPoint == True and drawPoint == True:
        frame = cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 0), 2)
  
  if keyboard.is_pressed('r'):
    clear = True
  
  cv2.imshow("Tracker", frame)
  
  k = cv2.waitKey(10) & 0xff
  if k==27:
    break

vid.release()
cv2.destroyAllWindows()