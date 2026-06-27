"""
CS6476 Problem Set 3 imports. Only Numpy and cv2 are allowed.
"""
import cv2
import numpy as np
#import time
import math


def euclidean_distance(p0, p1):
    """Gets the distance between two (x,y) points

    Args:
        p0 (tuple): Point 1.
        p1 (tuple): Point 2.

    Return:
        float: The distance between points
    """

    raise NotImplementedError
def order_points_new(pts):
    
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # if use Euclidean distance, it will run in error when the object
    # is trapezoid. So we should use the same simple y-coordinates order method.

    # now, sort the right-most coordinates according to their
    # y-coordinates so we can grab the top-right and bottom-right
    # points, respectively
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")

def find_coord(loc,w,h):


          
    pt = []
    for pts in zip(*loc[::-1]):
        pt.append((pts[0],pts[1]))

 #   print(pt)
        
 #       cv2.rectangle(image, pts, (pts[0] + w, pts[1] + h), (0,255,255), 2)

 #   cv2.imshow('template',image)
 #   cv2.waitKey(0)

    coor_1 = []
    coor_2 = []
    coor_3 = []
    coor_4 = []
    i = 0

    if(len(pt)>4):
        pt1 = pt
        coor_1.append(pt1[0])
        for i in range(len(pt1)):
            if((pt1[i][0]-4 <= coor_1[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_1[0][1] <=pt1[i][1]+4)):
                coor_1.append(pt1[i])
                
            i += 1

        pt1 = [x for x in pt1 if x not in coor_1]
        coor_2.append(pt1[0])
        for i in range(len(pt1)):
            if((pt1[i][0]-4 <= coor_2[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_2[0][1] <=pt1[i][1]+4)):
                coor_2.append(pt1[i])
                
            i += 1



        pt1 = [x for x in pt1 if x not in coor_2]

            
        coor_3.append(pt1[0])
        for i in range(len(pt1)):
            if((pt1[i][0]-4 <= coor_3[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_3[0][1] <=pt1[i][1]+4)):
                coor_3.append(pt1[i])
                
            i += 1

        pt1 = [x for x in pt1 if x not in coor_3]
        coor_4.append(pt1[0])
        for i in range(len(pt1)):
            if((pt1[i][0]-4 <= coor_4[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_4[0][1] <=pt1[i][1]+4)):
                coor_4.append(pt1[i])
                
            i += 1
        
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        x3 = 0
        y3 = 0
        x4 = 0
        y4 = 0

        pt = []
        
        for i in range(len(coor_1)):
                x1 = coor_1[i][0] + x1
                y1 = coor_1[i][1] + y1
                
        pt.append((int(x1/len(coor_1)),int(y1/len(coor_1))))

        for i in range(len(coor_2)):
                x2 = coor_2[i][0] + x2
                y2 = coor_2[i][1] + y2
                  
        pt.append((int(x2/len(coor_2)),int(y2/len(coor_2))))

        for i in range(len(coor_3)):
                x3 = coor_3[i][0] + x3
                y3 = coor_3[i][1] + y3
        pt.append((int(x3/len(coor_3)),int(y3/len(coor_3))))

        for i in range(len(coor_4)):
                x4 = coor_4[i][0] + x4
                y4 = coor_4[i][1] + y4
        pt.append((int(x4/len(coor_4)),int(y4/len(coor_4))))

    final = [[pt[0][0]+int(w/2),pt[0][1]+int(h/2)],[pt[3][0]+int(w/2),pt[3][1]+int(h/2)],[pt[1][0]+int(w/2),pt[1][1]+int(h/2)],[pt[2][0]+int(w/2),pt[2][1]+int(h/2)]] 

    return final


def get_corners_list(image):
    """Returns a ist of image corner coordinates used in warping.

    These coordinates represent four corner points that will be projected to
    a target image.

    Args:
        image (numpy.array): image array of float64.

    Returns:
        list: List of four (x, y) tuples
            in the order [top-left, bottom-left, top-right, bottom-right].
    """

    raise NotImplementedError


def find_markers(image, template=None):
    """Finds four corner markers.

    Use a combination of circle finding, corner detection and convolution to
    find the four markers in the image.

    Args:
        image (numpy.array): image array of uint8 values.
        template (numpy.array): template image of the markers.

    Returns:
        list: List of four (x, y) tuples
            in the order [top-left, bottom-left, top-right, bottom-right].
    """

    sift = cv2.SIFT()
    blockSize = 3
    apertureSize = 3
    img_gray1 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    mask = np.zeros(img_gray1.shape, dtype=np.uint8)

    
    img_gray = np.float32(img_gray1)

    
    kernel = np.ones((4,4), np.uint8)
    closing = cv2.morphologyEx(img_gray1, cv2.MORPH_CLOSE, kernel)

 #   dst  =  cv2.cornerHarris(closing,3,3,0.245)
    dst  =  cv2.cornerHarris(closing,3,3,0.245)
    image[dst>0.035 *dst.max()]=[0,0,255]
    ret, dst = cv2.threshold(dst,0.039*dst.max(),255,0)
    dst = np.uint8(dst)
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    
    mask[dst>0.035*dst.max()] = 255
#    mask[dst>0.035*dst.max()] = 255

#    cv2.imshow('dst',dst)
#    cv2.waitKey(0)
    

    coor = np.argwhere(mask)
    
    coor_list = [l.tolist() for l in list(coor)]
    coor_tuples = [tuple(l) for l in coor_list]
    print(len(coor_tuples))
    print(coor_tuples)

 #   print(coor_tuples)
    



    coor_tuples_copy = coor_tuples
    coor_1 = []
    coor_1.append(coor_tuples_copy[0])
    coor_2 = []
    coor_3 = []
    coor_4 = []

    thres = 30
    for i, val in enumerate(coor_tuples):

        if( ((coor_1[0][0]-thres) <=val[0]<=(coor_1[0][0]+thres)) & ((coor_1[0][1]-thres) <=val[1]<=(coor_1[0][1]+50)) ):
            coor_1.append(val)
 
    #print(coor_1)
    x1 = 0
    y1 = 0
    for i, val in enumerate(coor_1):
        #print(val[1])
        x1 = x1 + val[0]
        y1 = y1 + val[1]

    x1 = int(x1/len(coor_1))
    y1 = int(y1/len(coor_1))



    #print(coor_tuples_copy)

    new_coor2 = [x for x in coor_tuples_copy if x not in coor_1]

    
    coor_2.append(new_coor2[0])
    #print(coor_2)

    for i, val in enumerate(new_coor2):

        if( ((coor_2[0][0]-thres) <=val[0]<=(coor_2[0][0]+thres)) & ((coor_2[0][1]-thres) <=val[1]<=(coor_2[0][1]+thres)) ):
            coor_2.append(val)
 
    #print(coor_1)
    x2 = 0
    y2 = 0
    for i, val in enumerate(coor_2):
        #print(val[1])
        x2 = x2 + val[0]
        y2 = y2 + val[1]

    x2 = int(x2/len(coor_2))
    y2 = int(y2/len(coor_2))

    

    new_coor3 = [x for x in new_coor2 if x not in coor_2]

    
    coor_3.append(new_coor3[0])

    for i, val in enumerate(new_coor3):

        if( ((coor_3[0][0]-thres) <=val[0]<=(coor_3[0][0]+thres)) & ((coor_3[0][1]-thres) <=val[1]<=(coor_3[0][1]+thres)) ):
            coor_3.append(val)
 
    #print(coor_1)
    x3 = 0
    y3 = 0
    for i, val in enumerate(coor_3):
        #print(val[1])
        x3 = x3 + val[0]
        y3 = y3 + val[1]

    x3 = int(x3/len(coor_3))
    y3 = int(y3/len(coor_3))

    

    new_coor4 = [x for x in new_coor3 if x not in coor_3]

    
    coor_4.append(new_coor4[0])

    for i, val in enumerate(new_coor4):

        if( ((coor_4[0][0]-thres) <=val[0]<=(coor_4[0][0]+thres)) & ((coor_4[0][1]-thres) <=val[1]<=(coor_4[0][1]+thres)) ):
            coor_4.append(val)
 
    #print(coor_1)
    x4 = 0
    y4 = 0
    for i, val in enumerate(coor_4):
        #print(val[1])
        x4 = x4 + val[0]
        y4 = y4 + val[1]

    x4 = int(x4/len(coor_4))
    y4 = int(y4/len(coor_4))

    final = [[y1,x1]]
    final.append([y4,x4])
    final.append([y2,x2])
    final.append([y3,x3])

    final_f = order_points_new(np.array(final))


    final1 = []
    final1.append((int(final_f[0][0]),int(final_f[0][1])))
    final1.append((int(final_f[3][0]),int(final_f[3][1])))
    final1.append((int(final_f[1][0]),int(final_f[1][1])))
    final1.append((int(final_f[2][0]),int(final_f[2][1])))

    


    print(final1)
        

    return final1
    #raise NotImplementedError


def draw_box(image, markers, thickness=1):
    """Draws lines connecting box markers.

    Use your find_markers method to find the corners.
    Use cv2.line, leave the default "lineType" and Pass the thickness
    parameter from this function.

    Args:
        image (numpy.array): image array of uint8 values.
        markers(list): the points where the markers were located.
        thickness(int): thickness of line used to draw the boxes edges.

    Returns:
        numpy.array: image with lines drawn.
    """
    color = (0, 255, 0)
    image = cv2.line(image, markers[0], markers[1], color, thickness)
    image = cv2.line(image, markers[1], markers[3], color, thickness)
    image = cv2.line(image, markers[2], markers[3], color, thickness)
    image = cv2.line(image, markers[2], markers[0], color, thickness)
    
    
    #print(markers)
    
    return image

 #   raise NotImplementedError


def project_imageA_onto_imageB(imageA, imageB, homography):
    """Projects image A into the marked area in imageB.

    Using the four markers in imageB, project imageA into the marked area.

    Use your find_markers method to find the corners.

    Args:
        imageA (numpy.array): image array of uint8 values.
        imageB (numpy.array: image array of uint8 values.
        homography (numpy.array): Transformation matrix, 3 x 3.

    Returns:
        numpy.array: combined image
    """

    raise NotImplementedError


def find_four_point_transform(src_points, dst_points):
    """Solves for and returns a perspective transform.

    Each source and corresponding destination point must be at the
    same index in the lists.

    Do not use the following functions (you will implement this yourself):
        cv2.findHomography
        cv2.getPerspectiveTransform

    Hint: You will probably need to use least squares to solve this.

    Args:
        src_points (list): List of four (x,y) source points.
        dst_points (list): List of four (x,y) destination points.

    Returns:
        numpy.array: 3 by 3 homography matrix of floating point values.
    """

    raise NotImplementedError


def video_frame_generator(filename):
    """A generator function that returns a frame on each 'next()' call.

    Will return 'None' when there are no frames left.

    Args:
        filename (string): Filename.

    Returns:
        None.
    """
    # Todo: Open file with VideoCapture and set result to 'video'. Replace None
    video = cv2.VideoCapture(filename)

    # Do not edit this while loop
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            yield frame
        else:
            break
    video.release()
    yield None

    # Todo: Close video (release) and yield a 'None' value. (add 2 lines)
 #   raise NotImplementedError


def find_aruco_markers(image, aruco_dict=cv2.aruco.DICT_5X5_50):
    """Finds all ArUco markers and their ID in a given image.

    Hint: you are free to use cv2.aruco module

    Args:
        image (numpy.array): image array.
        aruco_dict (integer): pre-defined ArUco marker dictionary enum.

        For aruco_dict, use cv2.aruco.DICT_5X5_50 for this assignment.
        To find the IDs of markers, use an appropriate function in cv2.aruco module.

    Returns:
        numpy.array: corner coordinate of detected ArUco marker
            in (X, 4, 2) dimension when X is number of detected markers
            and (4, 2) is each corner's x,y coordinate in the order of
            top-left, bottom-left, top-right, and bottom-right.
        List: list of detected ArUco marker IDs.
    """

    raise NotImplementedError


def find_aruco_center(markers, ids):
    """Draw a bounding box of each marker in image. Also, put a marker ID
        on the top-left of each marker.

    Args:
        image (numpy.array): image array.
        markers (numpy.array): corner coordinate of detected ArUco marker
            in (X, 4, 2) dimension when X is number of detected markers
            and (4, 2) is each corner's x,y coordinate in the order of
            top-left, bottom-left, top-right, and bottom-right.
        ids (list): list of detected ArUco marker IDs.

    Returns:
        List: list of centers of ArUco markers. Each element needs to be
            (x, y) coordinate tuple.
    """

    raise NotImplementedError
