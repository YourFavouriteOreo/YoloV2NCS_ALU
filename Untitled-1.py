
def identify_person():
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
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                dura8tion = time.time() - start
                conve8rt_duration = time.time() - convert
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

                print ( "Track Mode : "+TRACK_MODE)
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
                
                
def biggestbbox():
    biggestIndex = None
    if (PersonList == []):
                print("No people detected")
                bIsTracking = False
                       
            else:
                for x in PersonList:
                    if biggestIndex is None:2
                        biggestIndex = x
                    elif (x != biggestIndex):
                        biggestIndex_width = abs(biggestIndex.left - biggestIndex.right)
                        x_width = abs(x.left - x.right)
                        if (biggestIndex_width < x_width):
                            biggestIndex = x
                bIsTracking = True

def movementctrl():

    while bIsTracking:
        width_person = int (biggestIndex.right + biggestIndex.left)
        center_person = int(width_person/2)
        center_screen = 208
        width_screen = 416

        if abs(center_person - center_screen) > 15:     #center - screen width /2
            while center_screen != center_person:
                if center_screen < center_person:
                    move right
                else
                move left
            
        if width_person/width_screen*100 >= 80:
            move back
        else if width_person/width_screen *100 < 20:
            move forward
            moveRobotBy x

movementctrl(biggestbbox(identify_person()))