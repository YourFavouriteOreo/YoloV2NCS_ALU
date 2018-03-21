import sys,os,time,csv,getopt,argparse
import numpy as np
from datetime import datetime
from PIL import Image
from ObjectWrapper import *
#from Visualize import *
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import picamera



LastPerson = ""
bIsTracking = False


TRACK_MODE = True

def identify_person():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', dest='graph', type=str,
                        default='graph', help='MVNC graphs.')
    parser.add_argument('--image', dest='image', type=str,
                        default='./images/dog.jpg', help='An image path.')
    parser.add_argument('--video', dest='video', type=str,
                        default='./videos/car.avi', help='A video path.')
    args = parser.parse_args()

    network_blob=args.graph
    imagefile = args.image
    videofile = args.video

    detector = ObjectWrapper(network_blob)
    stickNum = ObjectWrapper.devNum
    
    if sys.argv[1] == '--video':
        plt.ion()
        plt.show()

        camera = picamera.PiCamera()
        camera.hflip = False
        camera.vflip = True
        start_time = datetime.now()

        stream = io.BytesIO()
        camera.resolution = (320,180)
        time.sleep(2)

        
        elapsedTime = datetime.now()-start_time
        start_time = datetime.now()

        print ('total time is %d milliseconds' % int(elapsedTime.total_seconds()*1000))

        count +=1


        filename = 'images/image_%d.jpg'%count
        start = time.time()

        stream.seek(0)
        camera.capture(stream, format='jpeg')
        stream.seek(0)
        convert = time.time()
        pil_image = Image.open(stream)
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        duration = time.time() - start
        convert_duration = time.time() - convert
        #print("Image sampling time %d ms including %d ms to convert the image." % (int(duration * 1000), int(convert_duration * 1000)))

        start = time.time()
        results = detector.Detect(open_cv_image)
        duration = time.time() - start
        #print("Network Calculation time %d ms" % int(duration * 1000))

        # Find the strongest match for "person"
        max_confidence = 0.0
        person_index = None

        print ( "Track Mode : "+ str(TRACK_MODE) )
        PersonList = []

        for index, r in enumerate(results):
            print("Found %s with confidence %g at Left: %g, Right %g, Top %g, Bottom %g" %(r.name, r.confidence, r.left, r.right, r.top, r.bottom))
            if r.name == "person" and r.confidence > max_confidence:
                PersonList.append(r)
                max_confidence = r.confidence
                person_index = index 
                print("Name is person. index is %d" % person_index)
            else:
                print("%s is not person" % r.name)
    return PersonList
            
                
def biggestbbox(PersonList):
    biggestIndex = None
    if (PersonList == []):
                bIsTracking = False   
    else:
        for person in PersonList:
            if biggestIndex is None:
                biggestIndex = person
            elif (person != biggestIndex):
                biggestIndex_width = abs(biggestIndex.right - biggestIndex.left)
                person_width = abs(person.right - person.left)
                if (biggestIndex_width < person_width):
                    biggestIndex = person
        bIsTracking = True
    return biggestIndex

def movementctrl(PersonTracking):
    print("Person width is " + (PersonTracking.right - PersonTracking.left))
    
    # while bIsTracking:
    #     width_2person = int (biggestIndex.right - biggestIndex.left)
    #     center_person = int(width_person/2)
    #     center_screen = 208
    #     width_screen = 416

        # if abs(center_person - center_screen) > 15:     #center - screen width /2
        #     while center_screen != center_person:
        #         if center_screen < center_person:
        #             move right
        #         else
        #             move left
            
        # if width_person/width_screen*100 >= 80:
        #     move back
        # else if width_person/width_screen *100 < 20:
        #     move forward
        #     moveRobotBy x


def FindPerson():
    print("IS palce holder")

def main():
    count = 0
    if((len(sys.argv)>1) is False):
            print("No parameters passed . Please pass in image or video")
            return

    while True:
        CurrentPerson = biggestbbox(identify_person())
        if CurrentPerson == None:
            break
        else:
            movementctrl(CurrentPerson)
            print("Movement Control reached")
    


if __name__ == '__main__':
    main()
