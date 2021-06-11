from cv2 import cv2

class Start:

    def __init__(self):
        pass

    #Inicia o programa e realiza operações do open cv
    def start(self):
        # Open Video
        cap = cv2.VideoCapture('video1.mp4')

        #Create tracker object

        # Set median frame
        medianFrame = cv2.imread('BaseBkg.jpg')

        # Display median frame
        cv2.imshow('Median Background Frame', medianFrame)
        cv2.waitKey(0)

        # Reset frame number to 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Convert background to grayscale
        grayMedianFrame = cv2.cvtColor(medianFrame, cv2.COLOR_BGR2GRAY)

        return cap,medianFrame,grayMedianFrame