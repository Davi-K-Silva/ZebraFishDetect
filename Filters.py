from cv2 import cv2

class Filters:

    def __init__(self):
        pass

    def filters(self,ret,grayMedianFrame,cap):
        # Read frame
        ret, frame = cap.read()
        # Convert current frame to grayscale
        gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Calculate absolute difference of current frame and 
        # the median frame
        dframe = cv2.absdiff(gframe, grayMedianFrame)
        # Treshold to binarize
        th, dframe = cv2.threshold(dframe, 30, 255, cv2.THRESH_BINARY)
        # th = cv2.dilate(th, None, iterations=2)
        cnts,hierarchy = cv2.findContours(dframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return ret,frame,gframe,dframe,th,cnts,hierarchy