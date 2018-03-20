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

def main():
    if((len(sys.argv)>1) is False):
        print("No parameters passed . Please pass in image or video")
        return

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
    

        #imdraw = Visualize(img, results)
        #cv2.imshow('Demo',imdraw)
        #cv2.imwrite('test.jpg',imdraw)
        #cv22.waitKey(10000)
    if sys.argv[1] == '--video':
        plt.ion()
        plt.show()

        camera = picamera.PiCamera()
        camera.hflip = False
        camera.vflip = True
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
            print(open_cv_image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            print(open_cv_image)
            duration = time.time() - start
            convert_duration = time.time() - convert
            #print("Image sampling time %d ms including %d ms to convert the image." % (int(duration * 1000), int(convert_duration * 1000)))

            start = time.time()
            results = detector.Detect(open_cv_image)
            duration = time.time() - start
            #print("Network Calculation time %d ms" % int(duration * 1000))

            # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__',
            # '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
            # '__str__', '__subclasshook__2', '__weakref__', 'bottom', 'confidence', 'left', 'name', 'objType', 'right', 'top']
            #
            # Found person at Left: 124, Right 298, Top 13, Bottom 168

            # Find the strongest match for "person"
            max_confidence = 0.0
            person_index = None

            print (TRACK_MODE)
            PersonList = []

            for index, r in enumerate(results):
                #print("Found %s with confidence %g at Left: %g, Right %g, Top %g, Bottom %g" %(r.name, r.confidence, r.left, r.right, r.top, r.bottom))
                if r.name == "person" and r.confidence > max_confidence:
                    PersonList.append(r)
                    max_confidence = r.confidence
                    person_index = index
                    print("Name is person. index is %d" % person_index)
                else:
                    print("%s is not person" % r.name)
            
            if (PersonList == {}):
                print("No people detected")
                bIsTracking = False
            else:
                BiggestIndex = None
                for x in PersonList:
                    if BiggestIndex is None:
                        BiggestIndex = x
                    elif (x != BiggestIndex):
                        if ((BiggestIndex.left - BiggestIndex.right) < (x.left - x.right)):
                            BiggestIndex = x
                bIsTracking = True


            if person_index is not None:
                r = results[person_index]
                center = int((r.right + r.left)/2)
                print_spaces(center)

if __name__ == '__main__':
    main()
