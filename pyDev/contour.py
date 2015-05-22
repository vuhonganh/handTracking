import cv2
import numpy as np
from math import *


def appendimages(im1,im2):
    """ Return a new image that appends the two images side-by-side. """
    # select the image with the fewest rows and fill in enough empty rows
    rows1 = im1.shape[0]
    rows2 = im2.shape[0]
    if rows1 < rows2:
        im1 = np.concatenate((im1,zeros((rows2-rows1,im1.shape[1]))),axis=0)
    elif rows1 > rows2:
        im2 = np.concatenate((im2,zeros((rows1-rows2,im2.shape[1]))),axis=0)
        # if none of these cases they are equal, no filling needed.
        return np.concatenate((im1,im2), axis=1)

def append_imgs(im1, im2, im3):
    #buff = appendimages(im1,im2)
    #return appendimages(buff,im3)

    buff = np.concatenate((im1,im2), axis=1)
    return np.concatenate((buff,im3), axis=1)


#check whether the point is near edge or not
def point_not_at_edge( x, y, img_height, img_width, threshold):
    no_at_edge = ( (x > threshold) and (y > threshold) and ( fabs(x - img_width) > threshold ) and ( fabs(y - img_height) > threshold ) )
    return no_at_edge
    
#check whether two points are too near from each other    
def points_not_similar(x, y, x_neighb, y_neighb, threshold):
    no_same_point = (fabs(x - x_neighb) + fabs(y - y_neighb) > 2*threshold)
    return no_same_point  


def good_points(x, y, x_next, y_next, img_height, img_width, threshold):
    no_same_point = (fabs(x - x_next) + fabs(y - y_next) > 2*threshold)
    no_at_edge    = (x > threshold) and (y > threshold) and ( fabs(x - img_width) > threshold ) and ( fabs(y - img_height) > threshold ) 
    return (no_same_point and no_at_edge)

'''
calculate the point on wrist of the hand
by taking the average of opposites of convexity defects to the center
'''    
def find_wrist(center, contour, set_idx_convDefs):
    n = len(set_idx_convDefs)
    opposites = np.zeros((2,n))
    for i in range(n):
        opposites[0,i] = 2*center[0] - contour[set_idx_convDefs[i], 0, 0] #calcul x
        opposites[1,i] = 2*center[1] - contour[set_idx_convDefs[i], 0, 1] #calcul y
    
    total = np.sum(opposites, axis = 1)
    #print total
    x = int(total[0]/n)
    y = int(total[1]/n)
    wrist = (x, y)
    #print 'wrist = ', wrist
    return wrist

'''
simple methods to detect finger tips
by calculating the farthest points on convex hull
compared to a fixed point. This fixed point can be center or wrist
'''
def simple_detect_fingerTips(hull, img, fixedPoint, edge_thresh, neighbor_thresh):
    dist_from_fixedPoint = []
    img_height, img_width = img.shape[0:2]
    hull_nbPts = hull.shape[0]

    #calculate distance to fixed Point
    for i in range(hull_nbPts):
        dist_from_fixedPoint.append(cv2.norm(fixedPoint - hull[i], cv2.NORM_L2))
    
    #sort index from farthest to nearest
    max_indx = np.argsort(-1*np.array(dist_from_fixedPoint))

    #need to eliminate same points and points at edge
    #results stored in idx_ok, the list of candidate indices of hulls 
    idx_ok = []

    for i in range(hull_nbPts):
        idx = max_indx[i]
        if point_not_at_edge(hull[idx,0,0], hull[idx,0,1], img_height, img_width, edge_thresh):
            if(len(idx_ok) == 0):
                idx_ok.append(idx)
            else:
                not_similar = True
                for idx_neighbor in idx_ok:
                    not_similar = (points_not_similar(hull[idx,0,0], hull[idx,0,1], hull[idx_neighbor,0,0], hull[idx_neighbor,0,1],neighbor_thresh))
                    if not not_similar: #if similar break the loop 
                        break
                       
                if(not_similar):
                    idx_ok.append(idx)                    
    return idx_ok

def simple_preprocessing(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
   
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    blur = cv2.erode(blur, kernel, iterations = 2)
    blur = cv2.dilate(blur, kernel, iterations = 2)

    ret, bin_image = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_image


def simple_preprocessing2(img, backGround):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray2 = cv2.cvtColor(backGround, cv2.COLOR_BGR2GRAY)

    gray = gray-gray2
    
    blur = cv2.GaussianBlur(gray, (5,5), 0)
   
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    #blur = cv2.erode(blur, kernel, iterations = 2)
    #blur = cv2.dilate(blur, kernel, iterations = 2)

    ret, bin_image = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_image



def hsv_preprocessing(img):
    
    #define boundaries of HSV pixel intensities to be considered as 'skin'
    #H: 2-39 / 360 * 255 = 1-28
    #S: 0.15 - 0.9 / 1 * 255 = 38- 250
    #V: 0.2 - 0.95 / 1 * 255 = 
    lower = np.array([1, 38, 51])
    upper = np.array([28, 250, 242])

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #hsv = cv2.GaussianBlur(hsv, (5,5), 0)
    skinMask = cv2.inRange(hsv, lower, upper)

    #choosing a structure elements to apply noise-remove process
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)

    blur = cv2.GaussianBlur(skinMask, (5,5), 0)

    ret, bin_image = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bin_image


def find_contour_hull(binary_image):
    #find the contour
    contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #search the maximum contour in the hierachy tree of contours
    max_area = 0
    ci = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        if(area > max_area):
            max_area = area
            ci = i

    cnt = contours[ci]
    hull = cv2.convexHull(cnt)
    hull_idx = cv2.convexHull(cnt, returnPoints = False)

    return cnt, hull, hull_idx

def draws_contour_hull(img, cnt, hull):
    #draws the image with only the contour and its convex hull
    drawing = np.zeros(img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 3) 
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    return drawing


def eliminate_background(img, backGround, thres_diff):
    height, width, depth = img.shape
    for i in range(height):
        for j in range(width):
            erase = True
            for k in range(depth):
                if(fabs(img[i,j,k] - backGround[i,j,k]) > thres_diff):
                    erase = False
            if erase:
                img[i,j,:] = 0
    return img
'''
Tracking by camera
NOTE: hsv is very color and light sensitive and simple_preprocessing seems stabler
'''

 
'''
    firstSec = 0
    camera = cv2.VideoCapture(0)
    for i in range(12):
        camera.read()
    
    grabbed, backGround = camera.read()
    for i in range(12):
        grabbed, img = camera.read()
        backGround = backGround/2 + img/2
'''


def tracking():
    camera = cv2.VideoCapture(0)
    _,img = camera.read()
 
    h,w,d = img.shape

    #out = cv2.VideoWriter('video.avi',-1,1,(3*w,h))
   
    fourcc = cv2.cv.CV_FOURCC('F', 'M', 'P', '4')
    out = cv2.VideoWriter()
    success = out.open('output.avi',fourcc, 15, (3*w,h), True)
    

    waitTime = 100
    for i in range(waitTime):
        _, average = camera.read()

    #average = np.float32(average)
    index_im = 0
    while True:

        grabbed, img = camera.read()
        #alpha = 0.01 #factor of forgetting
        #cv2.accumulateWeighted(img, average, alpha)#img is src, average is dst

        img_diff = cv2.absdiff(img, average)#convert scale and do subtract these 2 images
        #cv2.imshow('img_diff', img_diff)
        
        #substract background
        #img = eliminate_background(img, backGround, 20)

        #bin_image = simple_preprocessing(img, backGround)
        bin_image = simple_preprocessing(img_diff)
        bin_image2 = bin_image.copy()
        cv2.imshow('binaire', bin_image2)
        # bin_image = hsv_preprocessing(img)

        # cv2.imshow('orig', img)
        # cv2.imshow('bin', bin_image)
        # cv2.waitKey(0)
        cnt, hull, hull_idx = find_contour_hull(bin_image)
        drawing = draws_contour_hull(img, cnt, hull)


        #search the points between each finger by using convexity defects
        #see the doc of opencv to understand implementation details

        convDefs = cv2.convexityDefects(cnt, hull_idx)
        dist_order = np.argsort((-1)*convDefs[:,0,3])
        max4dist = dist_order[0:4]
        max4points = convDefs[max4dist,0,2]

        for i in max4points:
            cv2.circle(drawing, tuple(cnt[i,0]), 5, [255,255,0], 2) 
    
        hull_nbPts = hull.shape[0]

        '''
        #draws all the points constitue the convex hull (for debugging)
        for i in range(hull_nbPts):
        cv2.circle(drawing, tuple(hull[i,0]), 4, [255,0,0], 2) 
        cv2.putText(drawing, str(i), tuple(hull[i,0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0], 1, cv2.CV_AA)
        '''

        #find and draw center of contour
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
            cx = int(moments['m10']/moments['m00']) # cx = M10/M00
            cy = int(moments['m01']/moments['m00']) # cy = M01/M00
    
        centr=(cx,cy) 
        cv2.circle(drawing, centr, 5, [0, 255, 255], 2) 

        #find and draw point represents the wrist of the hand
        wrist = find_wrist(centr, cnt, max4points)
        cv2.circle(drawing, wrist, 5, [0, 255, 255], 2) 

        edge_thresh = 20
        neighbor_thresh = 20
        fixedPoint = wrist
        idx_ok = simple_detect_fingerTips(hull, img, fixedPoint, edge_thresh, neighbor_thresh)

        #print 'list of idx_ok = ', idx_ok
        max_5hull_idx = idx_ok[0:5]
        #print 'first five of idx_ok = ', max_5hull_idx

        for i in max_5hull_idx:
            cv2.circle(drawing, tuple(hull[i,0]), 6, [0,255,0], 2)
            #print hull[i]

        #print dist_from_center
        #cv2.imshow('contour and convex hull', drawing)
      
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        drawing = cv2.cvtColor(drawing, cv2.COLOR_BGR2GRAY)
        '''
        print img.shape
        print bin_image2.shape
        print drawing.shape
        '''
        
        frame = append_imgs(img, bin_image2, drawing)
       
        #cv2.imshow('frame', frame)
        #out.write(frame)
        cv2.imwrite("store2/" + "img"+str(index_im) + ".jpg", frame)
        index_im += 1
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
    camera.release()
    out.release()
    #self.out = None
    cv2.destroyAllWindows()

def main():

    image_name = "hand_in_BG5.png"

    img = cv2.imread(image_name)

    bin_image = simple_preprocessing(img)
    #bin_image = hsv_preprocessing(img)

    cv2.imshow('orig', img)
    cv2.imshow('bin', bin_image)
    cv2.waitKey(0)
    cnt, hull, hull_idx = find_contour_hull(bin_image)
    drawing = draws_contour_hull(img, cnt, hull)


    #search the points between each finger by using convexity defects
    #see the doc of opencv to understand implementation details

    convDefs = cv2.convexityDefects(cnt, hull_idx)
    dist_order = np.argsort((-1)*convDefs[:,0,3])
    max4dist = dist_order[0:4]
    max4points = convDefs[max4dist,0,2]

    for i in max4points:
        cv2.circle(drawing, tuple(cnt[i,0]), 5, [255,255,0], 2) 
    
    hull_nbPts = hull.shape[0]

    '''
    #draws all the points constitue the convex hull (for debugging)
    for i in range(hull_nbPts):
    cv2.circle(drawing, tuple(hull[i,0]), 4, [255,0,0], 2) 
    cv2.putText(drawing, str(i), tuple(hull[i,0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,0,0], 1, cv2.CV_AA)
    '''

    #find and draw center of contour
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00
    
    centr=(cx,cy) 
    cv2.circle(drawing, centr, 5, [0, 255, 255], 2) 

    #find and draw point represents the wrist of the hand
    wrist = find_wrist(centr, cnt, max4points)
    cv2.circle(drawing, wrist, 5, [0, 255, 255], 2) 

    edge_thresh = 20
    neighbor_thresh = 20
    fixedPoint = wrist
    idx_ok = simple_detect_fingerTips(hull, img, fixedPoint, edge_thresh, neighbor_thresh)

    #print 'list of idx_ok = ', idx_ok
    max_5hull_idx = idx_ok[0:1]
    #print 'first five of idx_ok = ', max_5hull_idx

    for i in max_5hull_idx:
        cv2.circle(drawing, tuple(hull[i,0]), 6, [0,255,0], 2)
        #print hull[i]

    #print dist_from_center
    cv2.imshow('contour and convex hull', drawing)
    k = cv2.waitKey(0)


if __name__ == "__main__":
   # main()
    tracking()
