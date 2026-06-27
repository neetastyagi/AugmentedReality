"""
CS6476 Problem Set 3 imports. Only Numpy and cv2 are allowed.
"""
import cv2
import numpy as np
#import time
import math
from scipy import ndimage
import time




def euclidean_distance(p0, p1):
    """Gets the distance between two (x,y) points

    Args:
        p0 (tuple): Point 1.
        p1 (tuple): Point 2.

    Return:
        float: The distance between points
    """

    raise NotImplementedError

def avg_coord(pts):
    
    x1 = 0
    y1 = 0

    for i in range(len(pts)):
        x1 = pts[i][0] + x1
        y1 = pts[i][1] + y1
                
    #print('x1,y1',x1,y1)
    return (int(x1/len(pts)),int(y1/len(pts)))

def distance(p1,p2):
    d = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    return d



def order_points_new(pts):
    
    #print(pts)
    xSorted = pts[np.argsort(pts[:, 0]), :]

    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    (tr, br) = rightMost


    return np.array([tl, bl, tr, br], dtype="float32")



def find_coord(image,loc,w,h):

 #   print(loc)
    pt = []
    for pts in zip(*loc[::-1]):
        pt.append((pts[0],pts[1]))
##
 #       cv2.rectangle(image, pts, (pts[0] + w, pts[1] + h), (0,255,255), 2)
##    
##
 #   cv2.imshow('template',image)
 #   cv2.waitKey(0)
 #   experiment.save_image('badfile.png',image)

    if(len(pt)<=200):

        coor_new = []
        coor_final = []
        pt_1 = pt
        pt_2 = pt
        for i in range(len(pt_1)):
            coor_new = []
            
            for j in range(len(pt_2)):
                
                if((pt_2[j][0]-50 <= pt_1[i][0] <= pt_2[j][0]+50) & (pt_2[j][1]-50 <= pt_1[i][1] <= pt_2[j][1]+50)):
                    
                    #print('before',coor_new)
                    coor_new.append(pt_2[j])
                    #print('after',coor_new)
                
                    
                j +=1

            if(len(coor_new)>0):
              # print('coor_new',coor_new)
               coor_final.append(avg_coord(coor_new))
 #              print('coor_final',coor_final)
                
             
                
            i += 1
            
        coor_final = [t for t in (set(tuple(i) for i in coor_final))]

 #       print('Lengthof coord',len(coor_final))
    else:
        coor_final = [(0,0)]

        
    if(len(coor_final) == 4):
        print('List of coord',coor_final)

        f = coor_final

        output_c = [[f[0][0],f[0][1]],[f[3][0],f[3][1]],[f[1][0],f[1][1]],[f[2][0],f[2][1]]]
        f_f = order_points_new(np.array(output_c))

        o1 = []
        o1.append((int(f_f[0][0]),int(f_f[0][1])))
        o1.append((int(f_f[1][0]),int(f_f[1][1])))
       
        o1.append((int(f_f[2][0]),int(f_f[2][1])))
        o1.append((int(f_f[3][0]),int(f_f[3][1])))

        coor_final = o1
    

    return coor_final 


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

    h = image.shape[0]
    w = image.shape[1]

    final = [(0,0),(0,h-1),(w-1,0),(w-1,h-1)]

    return final
    #raise NotImplementedError

def find_center(image,template):

    w, h = template.shape[::-1]
    thres = 0.8
    l = 0
    get_coord = []
    final = []
    flag = 0
    s_final = []
    for angle in np.arange(0,360,10):


        
        template_new = ndimage.rotate(template,angle,reshape = False)
        res = cv2.matchTemplate(image,template_new,cv2.TM_CCOEFF_NORMED)
        
       
#        t_1 = [0.75,0.7,0.58,0.55,0.54,0.539,0.538,0.537,0.536,0.535,0.534,0.533,0.532,0.531,0.53,0.529,0.528,0.527,0.523,0.52,0.51,0.5,0.49,0.47,0.45,0.448,0.446,0.444,0.442,0.44,0.43,0.428,0.426,0.424,0.422,0.42,0.40,0.39,0.38,0.37,0.36,0.35,0.3]

       
        t_1 = [0.75,0.7,0.65,0.6,0.5,0.58,0.55,0.548,0.546,0.544,0.542,0.54,0.539,0.538,0.537,0.536,0.535,0.534,0.533,0.532,0.531,0.53,
               0.529,0.528,0.527,0.523,0.52,0.51,0.505,0.5,0.49,0.47,0.46,0.458,0.454,0.45,0.448,0.446,0.444,0.442,0.44,0.435,0.43,
               0.428,0.426,0.424,0.422,0.42,0.415,0.41,0.405,0.40,0.398,0.396,0.393,0.39,0.385,0.38,0.375,0.37,0.36,0.355,0.35,0.34,0.33,0.32,
               0.31,0.3]
      #       for t in range(80,30,-2):
        for t in t_1:
 #           thres = (t*0.01)
            thres = t
            

            flag = 0
 
            loc = np.where( res >= thres)

            if(len(loc[0])<=150):

                final = find_coord(image,loc,w,h)


            if(len(final) == 4 ):

                d1 = distance(final[0],final[1])
                d2 = distance(final[1],final[3])
                d3 = distance(final[2],final[3])
                d4 = distance(final[2],final[0])
                r1 = d2/d1
                r2 = d4/d3

                print('length ratio',round(r1/r2,2))
                print('angle,t,thres',angle,t,t*0.01)
                print('d1,d2,d3,d4',d1,d2,d3,d4)

                if(d1>100 and d2> 100 and d3>100 and d4>100):
                    # 1.2,1.26,1.38(part5)
                    # 0.75 to 0.7(part5)
 #                      print('angle,t,thres',angle,t,t*0.01)
                    if(0.7 <= round(r1/r2,2) <= 1.39):
 #                       print('length is more than 100')
 #                       print('final doe thres and loc',final)
 #                       print('angle,t,thres',angle,t,t*0.01)

                        flag = 1
                   
 #               print('found match')
                break

            else:
                final = []
        

        if(flag == 1):
            break
        
    print('find_center',final)

    return final,s_final
        
def add_noise(img_gray):
    r, c = img_gray.shape
    x = np.random.rand(r, c)
    ids = x < 0.02 /2
    img_gray[ids] = 0
    ids = 0.02 / 2 <= x
    ids &= x < 0.02
    img_gray[ids] = 255
    return img_gray

def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang
    
          
    
    


def find_markers(image, template):
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
 

     
    img_marker = image.copy()
    t_marker = template.copy()
    img_gray = cv2.cvtColor(img_marker,cv2.COLOR_BGR2GRAY)


    g_template = cv2.cvtColor(t_marker, cv2.COLOR_BGR2GRAY)
    r_template = cv2.rotate(g_template, cv2.cv2.ROTATE_90_CLOCKWISE)
    r_rotated_new = ndimage.rotate(g_template, 351.3, reshape = False)
    r_rotated_15 = ndimage.rotate(g_template, 210 ,reshape = False)
    r_rotated_10 = ndimage.rotate(g_template, 10 ,reshape = False)
    f_image = cv2.flip(g_template, 0)

    noise_img = add_noise(img_gray)
    noise_template = add_noise(g_template)

##    cv2.imshow('noise_img',noise_img)
##    cv2.imshow('noise_template',noise_template)
##    cv2.waitKey(0)

    w, h = g_template.shape[::-1]
    w1, h1 = img_gray.shape[::-1]

    res = cv2.matchTemplate(img_gray,g_template,cv2.TM_CCOEFF_NORMED)


    loc = np.where( res >= 0.8)
    thres = 0.8
    l = 0
    get_coord = []
    final = []
    flag = 0
    s_final = []

    if(loc[0].size <=20):
        loc = np.where(res >= 0.7)


    if (loc[0].size == 0):
        loc = np.where( res >= 0.49)

        if(loc[0].size > 0):
            max_x = int(max(loc[0]))
            min_x = int(min(loc[0]))
            new_x = max_x - min_x
            if(new_x <= 10):
                print('setting loc empty')
            
                loc = (np.array([]),np.array([]))



    rotate = 0

    if (loc[0].size == 0):
        res = cv2.matchTemplate(img_gray,r_template,cv2.TM_CCOEFF_NORMED)

        loc = np.where( res >= 0.5)
        print('rotated 90')
        
    if (loc[0].size == 0):
        res = cv2.matchTemplate(img_gray,r_rotated_new,cv2.TM_CCOEFF_NORMED)

        loc = np.where( res >= 0.45)
        print('rotated 350')



    if (loc[0].size == 0):
        res = cv2.matchTemplate(img_gray,r_rotated_15,cv2.TM_CCOEFF_NORMED)
        
        loc = np.where( res >= 0.43)
       # print(loc[1])
##        for i in range(len(loc[1])):
##            loc[1][i] = loc[1][i]-16
       # print(loc[1])
        
        
 #       loc = np.where( res >= 0.356)
        print('rotated 15')

    if (loc[0].size == 0):
        loc = np.where( res >= 0.3)
        print('noisy')
        #print(loc)

    if(loc[0].size == 0):
        noise_img = add_noise(img_gray)
        res = cv2.matchTemplate(img_gray,r_rotated_15,cv2.TM_CCOEFF_NORMED)
       
        loc = np.where( res >= 0.39)        



    coor_1 = []
    coor_2 = []
    coor_3 = []
    coor_4 = []
    i = 0

    pt = []
    for pts in zip(*loc[::-1]):
        pt.append((pts[0],pts[1]))
 #       cv2.rectangle(image, pts, (pts[0] + w, pts[1] + h), (0,255,255), 2)
    

 #   cv2.imshow('template',image)
 #   cv2.waitKey(0)

    print(len(pt))
        
    if(100>=len(pt)>=4):
        pt1 = pt
        
        coor_1.append(pt1[0])
        for i in range(len(pt1)):
            if((pt1[i][0]-4 <= coor_1[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_1[0][1] <=pt1[i][1]+4)):
                coor_1.append(pt1[i])
                
            i += 1
        pt1 = [x for x in pt1 if x not in coor_1]

        if(len(pt1) > 0): 
            
            coor_2.append(pt1[0])
            for i in range(len(pt1)):
                if((pt1[i][0]-4 <= coor_2[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_2[0][1] <=pt1[i][1]+4)):
                    coor_2.append(pt1[i])
                    
                i += 1



            pt1 = [x for x in pt1 if x not in coor_2]

        if(len(pt1) > 0):           
            coor_3.append(pt1[0])
            for i in range(len(pt1)):
                if((pt1[i][0]-4 <= coor_3[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_3[0][1] <=pt1[i][1]+4)):
                    coor_3.append(pt1[i])
                    
                i += 1

            pt1 = [x for x in pt1 if x not in coor_3]
            
        if(len(pt1) > 0):
            coor_4.append(pt1[0])
            for i in range(len(pt1)):
                if((pt1[i][0]-4 <= coor_4[0][0] <=pt1[i][0]+4) & (pt1[i][1]-4 <= coor_4[0][1] <=pt1[i][1]+4)):
                    coor_4.append(pt1[i])
                    
                i += 1

        print('coor_1',coor_1)
        print('coor_2',coor_2)
        print('coor_3',coor_3)
        print('coor_4',coor_4)


        
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        x3 = 0
        y3 = 0
        x4 = 0
        y4 = 0

        pt = []
        if(len(coor_1)>0 and len(coor_2)>0 and len(coor_3)>0 and len(coor_4)>0):
            
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

            final = pt #[[pt[0][0]+int(w/2),pt[0][1]+int(h/2)],[pt[3][0]+int(w/2),pt[3][1]+int(h/2)],[pt[1][0]+int(w/2),pt[1][1]+int(h/2)],[pt[2][0]+int(w/2),pt[2][1]+int(h/2)]] 

        else:
            final = []



    
    c = 0


    if(len(final) == 0):
        print('insert here')
        c = 1

 
        final,s_final = find_center(img_gray,g_template)

        if(len(final)< 4):
            final = []
            final,s_final = find_center(noise_img,noise_template)


    if(len(final)==0):
        final = [(0,0),(110,120),(120,120),(130,130)]
     
    output_f = [[final[0][0]+int(w/2),final[0][1]+int(h/2)],[final[3][0]+int(w/2),final[3][1]+int(h/2)],[final[1][0]+int(w/2),final[1][1]+int(h/2)],[final[2][0]+int(w/2),final[2][1]+int(h/2)]]

    
    

    print('output_f',output_f)


    final_f = order_points_new(np.array(output_f))

 #   print('final_f',final_f)


    final1 = []
    final1.append((int(final_f[0][0]),int(final_f[0][1])))
    final1.append((int(final_f[1][0]),int(final_f[1][1])))
    
    final1.append((int(final_f[2][0]),int(final_f[2][1])))
    final1.append((int(final_f[3][0]),int(final_f[3][1])))

    d1 = distance(final1[0],final1[1])
    d2 = distance(final1[1],final1[3])
    d3 = distance(final1[2],final1[3])
    d4 = distance(final1[2],final1[0])

    print('d1,d2,d3,d4',d1,d2,d3,d4)
    d_final_f = []
    d_final1 = []
    if(d1>100 and d2> 100 and d3>50 and d4>100):
        print('good')
    else:
        print('insert here2')
        d_final = []
        d_final,s_final = find_center(img_gray,g_template)

        if(len(d_final)< 4):
            d_final = []
            d_final,s_final = find_center(noise_img,noise_template)


    
        output_f = [[d_final[0][0]+int(w/2),d_final[0][1]+int(h/2)],[d_final[3][0]+int(w/2),d_final[3][1]+int(h/2)],[d_final[1][0]+int(w/2),d_final[1][1]+int(h/2)],[d_final[2][0]+int(w/2),d_final[2][1]+int(h/2)]]
        print('output_f',output_f)
        d_final_f = order_points_new(np.array(output_f))

        print('final_f',d_final_f)



        d_final1.append((int(d_final_f[0][0]),int(d_final_f[0][1])))
        d_final1.append((int(d_final_f[1][0]),int(d_final_f[1][1])))
        print('here')
        d_final1.append((int(d_final_f[2][0]),int(d_final_f[2][1])))
        d_final1.append((int(d_final_f[3][0]),int(d_final_f[3][1])))

        final1 = d_final1

        if(len(final1)==0):
           final1 = [(0,0),(110,120),(120,120),(130,130)]


    

##    timestr = time.strftime("%Y%m%d-%H%M%S")
##
##    draw_box(image,final1,1)
##    experiment.save_image('output_images/badfile-'+timestr+'.png',image)
    

    #final1= [(final1[0][0]-1,final1[0][1]-1),(final1[1][0]-1,final1[1][1]-1),(final1[2][0]-1,final1[2][1]-1),(final1[3][0]-1,final1[3][1]-1)]
   
 #   print('final1',final1)
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
    #raise NotImplementedError


def apply_homography(src, H):
    dst = []
    H = H.flatten()
    if src.ndim==1:
        src = np.array([src])
    for pt in src:    
        if pt.ndim == 1:
            pt = np.array([pt])

        Z = 1./(H[6]*pt[0,0] + H[7]*pt[0,1] + H[8])
        px = (H[0]*pt[0,0] + H[1]*pt[0,1] + H[2])*Z
        py = (H[3]*pt[0,0] + H[4]*pt[0,1] + H[5])*Z
        dst.append([px,py])
    dst = np.array(dst,dtype=int)
    return dst

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


##    mask = np.ones(imageB.shape, dtype=np.uint8)
##    mask.fill(255)
##    roi = np.array([[(dp[0][0],dp[0][1]),(dp[2][0],dp[2][1]),(dp[3][0],dp[3][1]),(dp[1][0],dp[1][1])]],dtype=np.int32)
##    cv2.fillPoly(mask, roi, 0)
##    masked_image = imageB | mask
##
##    cv2.imshow('masked_image',masked_image)
##    cv2.waitKey(0)

    
    src_img = imageA
    dst = imageB
    height = imageB.shape[0]
    width = imageB.shape[1]
    hA = imageA.shape[0]
    wA = imageA.shape[1]
    H = homography
    H_inv = np.linalg.inv(H)
    arr = []

    gray = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    grayT = gray.T
    itr = np.nditer(grayT, flags=['multi_index'], order='C')
    for val in itr:
        x, y = itr.multi_index
        arr.append([x, y, 1])
    arr = (np.array(arr)).T
    temp = np.dot(H_inv, arr)
    arr_x = temp[0, :]
    arr_y = temp[1, :]
    arr_w = temp[2, :]
    arr_sx = arr_x /arr_w
    arr_sy = arr_y /arr_w

    i = 0
    itr = np.nditer(grayT, flags=['multi_index'], order='C')
    for val in itr:
        y, x = itr.multi_index
        sx = int(arr_sx[i])
        sy = int(arr_sy[i])
        if((sx <= width) & (sy <= height) &  (wA > sx >= 0) & (hA > sy >= 0)):
            dst[x,y] = src_img[sy,sx]
        i += 1
        

##    
##    l = []
##
##
##    for x in range(width):
##        for y in range(height):
##            l.append([x, y, 1])
##    l = np.array(l)
##    l = l.T
##    
##
##    res = np.dot(H_inv, l)
##
##    for k in range(height*width):
##        px = int(res[0][k] / res[2][k])
##        py = int(res[1][k] / res[2][k])
##        x = l[0][k]
##        y = l[1][k]
##        if((px <= width) & (py <= height) &  (wA > px >= 0) & (hA > py >= 0)):
##               dst[y,x] = src_img[py,px]
##
##        


    return dst
    #raise NotImplementedError


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
    p1 = src_points
    p2 = dst_points
    A = []
    for i in range(0, len(p1)):
        x, y = p1[i][0], p1[i][1]
        u, v = p2[i][0], p2[i][1]
        A.append([x, y, 1, 0, 0, 0, -u*x, -u*y, -u])
        A.append([0, 0, 0, x, y, 1, -v*x, -v*y, -v])
    A = np.asarray(A)
    U, S, Vh = np.linalg.svd(A)
    L = Vh[-1,:] / Vh[-1,-1]
    H = L.reshape(3, 3)
 #   print(H)


    
    return H
    #raise NotImplementedError


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
    print(image.size)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.Dictionary_get(aruco_dict)

    
    arucoParams = cv2.aruco.DetectorParameters_create()

    (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, dictionary = aruco_dict,parameters=arucoParams)


    final = corners
    final_id = ids

    labels = []

    if ids is None:
        print('Empty')
    else:

        for i in range(len(ids)):
     
            if(ids[i][0] == 10):
                print('10')

                a = []
                (x1,y1) = (corners[i][0][0][0],corners[i][0][0][1])
                (x2,y2) = (corners[i][0][1][0],corners[i][0][1][1])
                (x3,y3) = (corners[i][0][2][0],corners[i][0][2][1])
                (x4,y4) = (corners[i][0][3][0],corners[i][0][3][1])
                a.append((x1,y1))
                a.append((x2,y2))
                a.append((x3,y3))
                a.append((x4,y4))
                

                final = [[a[0][0],a[0][1]],[a[3][0],a[3][1]],[a[1][0],a[1][1]],[a[2][0],a[2][1]]]

                final = np.array(final)    
        
                final_f = order_points_new(np.array(final))
     #           print(np.asarray(final_f))
     #           print(type(final_f))

                labels.append(np.asarray(final_f))



        for i in range(len(ids)):
        
            if(ids[i][0] == 20):
                print('20')

                a = []
                (x1,y1) = (corners[i][0][0][0],corners[i][0][0][1])
                (x2,y2) = (corners[i][0][1][0],corners[i][0][1][1])
                (x3,y3) = (corners[i][0][2][0],corners[i][0][2][1])
                (x4,y4) = (corners[i][0][3][0],corners[i][0][3][1])
                a.append((x1,y1))
                a.append((x2,y2))
                a.append((x3,y3))
                a.append((x4,y4))
                

                final = [[a[0][0],a[0][1]],[a[3][0],a[3][1]],[a[1][0],a[1][1]],[a[2][0],a[2][1]]]

                final = np.array(final)    
        
                final_f = order_points_new(np.array(final))


                labels.append(np.asarray(final_f))
                

        for i in range(len(ids)):

            if(ids[i][0] == 30):
                print('30')

                a = []
                (x1,y1) = (corners[i][0][0][0],corners[i][0][0][1])
                (x2,y2) = (corners[i][0][1][0],corners[i][0][1][1])
                (x3,y3) = (corners[i][0][2][0],corners[i][0][2][1])
                (x4,y4) = (corners[i][0][3][0],corners[i][0][3][1])
                a.append((x1,y1))
                a.append((x2,y2))
                a.append((x3,y3))
                a.append((x4,y4))
                

                final = [[a[0][0],a[0][1]],[a[3][0],a[3][1]],[a[1][0],a[1][1]],[a[2][0],a[2][1]]]

                final = np.array(final)    
        
                final_f = order_points_new(np.array(final))

                labels.append(np.asarray(final_f))


        for i in range(len(ids)):

            if(ids[i][0] == 40):
                print('40')

                a = []
                (x1,y1) = (corners[i][0][0][0],corners[i][0][0][1])
                (x2,y2) = (corners[i][0][1][0],corners[i][0][1][1])
                (x3,y3) = (corners[i][0][2][0],corners[i][0][2][1])
                (x4,y4) = (corners[i][0][3][0],corners[i][0][3][1])
                a.append((x1,y1))
                a.append((x2,y2))
                a.append((x3,y3))
                a.append((x4,y4))
                

                final = [[a[0][0],a[0][1]],[a[3][0],a[3][1]],[a[1][0],a[1][1]],[a[2][0],a[2][1]]]

                final = np.array(final)    
        
                final_f = order_points_new(np.array(final))
                labels.append(np.asarray(final_f))




    return labels, [10,20,30,40]

   # raise NotImplementedError


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
    center = []

    
    for i in range(len(markers)):
         x = int((markers[i][0][0]+markers[i][1][0]+markers[i][2][0]+markers[i][3][0])/4)
         y = int((markers[i][0][1]+markers[i][1][1]+markers[i][2][1]+markers[i][3][1])/4)
         center.append((x,y))

 
    return center
#    raise NotImplementedError
