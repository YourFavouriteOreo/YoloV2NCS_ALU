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
from interruptingcow import timeout

LastPerson = ""


SHOW_GUI = False

TRACK_MODE = True

def print_spaces(num_spaces):
    print(' ' * num_spaces + '||')

def main():
    if((len(sys.argv)>1) is False):
        print("No parameters passed . Please pass in image or video")
        return

    arser = argparse.ArgumentParser()
    parser.add_argument('--graph', dest='graph', type=str,
                        default='graph', help='MVNC graphs.')
    parser.add_argument('--image', dest='image', type=str,
                        default='./images/dog.jpg', help='An image path.')
    parser.add_argument('--video', dest='video', type=str,
                        default='./videos/car.avi', help='A video path.')
    args = parser.parse_args()
    

def identify_people():
    

    network_blob=args.graph
    imagefile = args.image
    videofile = args.video

    detector = ObjectWrapper(network_blob)
    stickNum = ObjectWrapper.devNum

    if sys.argv[1] == '--image':
        # image preprocess
        #img = cv2.imread(imagefile)
        pil_image = Image.open(imagefile).convert('RGB')
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        start = datetime.now()

        results = detector.Detect(open_cv_image)

        for r in results:
            print(r.name)

        end = datetime.now()
        elapsedTime = end-start

        print ('total time is " milliseconds', elapsedTime.total_seconds()*1000)

        #imdraw = Visualize(img, results)
        #cv2.imshow('Demo',imdraw)
        #cv2.imwrite('test.jpg',imdraw)
        #cv2.waitKey(10000)
    elif sys.argv[1] == '--video':
        plt.ion()
        plt.show()

        camera = picamera.PiCamera()
        camera.hflip = False
        camera.vflip = False
        start_time = datetime.now()

        stream = io.BytesIO()
        #camera.resolution = (320,180)
        camera.resolution = (320,180)
        #camera.start_preview()
        time.sleep(2)

        for image in range(100):
            elapsedTime = datetime.now()-start_time
            start_time = datetime.now()

            print ('total time is %d milliseconds' % int(elapsedTime.total_seconds()*1000))

            filename = 'images/image_%d.jpg'%image
            #camera.capture(filename)
            #pil_image = Image.open(filename).convert('RGB')

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

            # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__',
            # '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
            # '__str__', '__subclasshook__', '__weakref__', 'bottom', 'confidence', 'left', 'name', 'objType', 'right', 'top']
            #
            # Found person at Left: 124, Right 298, Top 13, Bottom 168

            if SHOW_GUI:
                text = ""
                plt.gcf().clear()
                fig,ax = plt.subplots(1)
                imgplot = ax.imshow(pil_image)
            
            
            max_confidence = 0.0
            person_index = None

            print (TRACK_MODE)
            person_list = []
           
            for index, r in enumerate(results):
            #print("Found %s with confidence %g at Left: %g, Right %g, Top %g, Bottom %g" %(r.name, r.confidence, r.left, r.right, r.top, r.bottom))
                
                if r.name == "person" and r.confidence > max_confidence:
                    person_list.append(r)
                    max_confidence = r.confidence
                    person_index = index
                    print("Name is person. index is %d" % person_index)
                else:
                    print("%s is not person", %r.name)
                    
            if (person_list.isEmpty()):
                print("No people detected")
                return None
                # maybe call a method to move the robot
            
            else:
                closest_person = find_closest(person_list)
                closest_person_index = results(closest_person)
                print("Closest person is: " + closest_person
                       + " with index :" + closest_person_index)
                return closest_person
            
            # WHAT IS THE USE OF THIS PART
            if person_index is not None:
                r = results[person_index]
                center = int((r.right + r.left)/2)
                print_spaces(center)

            if SHOW_GUI:
                if person_index is not None:
                    r = results[person_index]
                #for r in results:
                    #print(r.name)
                    text = r.name2
                    width = r.right-r.left
                    height = r.bottom-r.top

                    print("width %d, height %d" %(width, height))
                    rect = patches.Rectangle((r.left,r.top),width, height,linewidth=1,edgecolor='r',facecolor='none')
                    ax.add_patch(rect)

                plt.text(20, -20, text)
                plt.xticks([])
                plt.yticks([])
                plt.draw()
                plt.pause(0.001)
                plt.savefig('%s.png' % filename)

# Find the strongest match for "person"
def findClosest(person_list):
    
    biggest_person = None
    biggest_person_width = 500 #screen width

    for person in person_list:
        person_width = abs(person.left - person.right)
        if (biggest_person_width < person_width):
            biggest_person = person
            biggest_person_width = person_width
    
    return biggest_person

            
def move_robot(tracked_person):
    if(tracked_person not None):
        width_person = int (tracked_person.right - tracked_person.left)
        center_person = int(width_person/2)

        center_screen = 208
        width_screen = 416
        
        
        with timeout() :
            if abs(center_person - center_screen) > 15:     #center - screen width /2
                if center_screen < center_person:
                    move right
                else
                    move left
                
                if width_person/width_screen *100 >= 80
                    # move back
                else if width_person/width_screen *100 < 20
                    # advance
            
       
    else:
        pass


if __name__ == '__main__':
    main()
