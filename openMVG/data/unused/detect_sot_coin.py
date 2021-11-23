import os
import argparse
import math

import numpy as np
import cv2


def find_hough_circles(img):
    # img = cv2.medianBlur(img, 9)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,120,
                                param1=120,param2=80,minRadius=50,maxRadius=150)
    # print('[**] circles: ', circles, type(circles), circles.shape)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        
    return cimg

def cal_depth_map(l_img, r_img):
    # Matched block size. It must be an odd number >=1 . Normally, it should be somewhere in the 3..11 range.
    block_size = 20
    min_disp = -128
    max_disp = 128
    # Maximum disparity minus minimum disparity. The value is always greater than zero.
    # In the current implementation, this parameter must be divisible by 16.
    num_disp = max_disp - min_disp
    # Margin in percentage by which the best (minimum) computed cost function value should "win" the second best value to consider the found match correct.
    # Normally, a value within the 5-15 range is good enough
    uniquenessRatio = 5
    # Maximum size of smooth disparity regions to consider their noise speckles and invalidate.
    # Set it to 0 to disable speckle filtering. Otherwise, set it somewhere in the 50-200 range.
    speckleWindowSize = 200
    # Maximum disparity variation within each connected component.
    # If you do speckle filtering, set the parameter to a positive value, it will be implicitly multiplied by 16.
    # Normally, 1 or 2 is good enough.
    speckleRange = 2
    disp12MaxDiff = 0
    
    stereo = cv2.StereoSGBM_create(
        # minDisparity=min_disp,
        numDisparities=32,
        blockSize=block_size,
        # uniquenessRatio=uniquenessRatio,
        # speckleWindowSize=speckleWindowSize,
        # speckleRange=speckleRange,
        # disp12MaxDiff=disp12MaxDiff,
        # P1=8 * 1 * block_size * block_size,
        # P2=32 * 1 * block_size * block_size,
    )
    # stereo = cv2.StereoSGBM_create(numDisparities=32, blockSize=20)
    disparity = stereo.compute(l_img, r_img)

    return disparity

def canny_edge_detection(image, blur_ksize=5, threshold1=100, threshold2=200):
    img_gaussian = cv2.GaussianBlur(image,(blur_ksize,blur_ksize),0)

    img_canny = cv2.Canny(img_gaussian,threshold1,threshold2)

    return img_canny

def find_contours(image):
    height, width = image.shape
    ret, thresh = cv2.threshold(image,100,255,0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    blank_image = np.zeros((height, width, 3), np.uint8)
    cnt = contours[:]
    image = cv2.drawContours(blank_image, cnt, -1, (0,255,0), 1)

    return thresh, image, contours

def moments(contour):
    M = cv2.moments(contour)
    for key, val in M.items():
        print(key, ':', val)
    return M

def find_centroid(contour):
    M = cv2.moments(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    print('centroid: ', cx, cy)
    return (cx, cy)

def contour_area(contour):
    '''Contour area can also be get from M[‘m00’]'''
    area = cv2.contourArea(contour)
    print('area: ', area)
    return area

def contour_perimeter(contour):
    perimeter = cv2.arcLength(contour,True)
    print('perimeter: ', perimeter)
    return perimeter

def contour_approximation(contour, perc=0.1):
    epsilon = perc*cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,epsilon,True)
    print('contour approx: ', approx)
    return approx

def convex_hull(contour):
    hull = cv2.convexHull(contour)
    print('hull: ', hull)
    return hull

def straight_bounding_rectangle(image, contours):
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    return image

def rotated_rectangle(image, contours):
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        image = cv2.drawContours(image,[box],0,(0,0,255),2)
    return image

def minimum_enclosing_circle(image, contours): 
    for contour in contours:
        (x,y),radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        image = cv2.circle(image,center,radius,(0,255,0),2)
    return image

def fitting_an_ellipse(image, contours):
    for contour in contours:
        ellipse = cv2.fitEllipse(contour)
        image = cv2.ellipse(image,ellipse,(0,255,0),2)
    return image

def calculate_aspect_ratio(contour):
    '''
    It is the ratio of width to height of bounding rect of the object.
    '''
    x,y,w,h = cv2.boundingRect(contour)
    aspect_ratio = float(w)/h
    print('aspect ratio: ', aspect_ratio)
    return aspect_ratio

def calculate_extent(contour):
    '''
    Extent is the ratio of contour area to bounding rectangle area.
    '''
    area = cv2.contourArea(contour)
    x,y,w,h = cv2.boundingRect(contour)
    rect_area = w*h
    extent = float(area)/rect_area
    print('extent: ', extent)
    return extent

def calculate_circle_extent(contour):
    '''
    Extent is the ratio of contour area to bounding circle area.
    '''
    area = cv2.contourArea(contour)
    (x, y), radius = cv2.minEnclosingCircle(contour)
    circle_area = math.pi * (radius**2)
    extent = float(area)/circle_area
    return extent, (x, y), radius

def detect_closed_curves(image, contours):
    curves = []
    # height, width = image.shape
    # blank_image = np.zeros((height, width, 3), np.uint8)

    for contour in contours:
        circle_extent, (x, y), radius = calculate_circle_extent(contour)
        if circle_extent > 0.5:
            print("[**] circle_extent: ", circle_extent)
            curves.append(contour)

            center = (int(x),int(y))
            radius = int(radius)
            image = cv2.circle(image,center,radius,(0,255,0),2)
    # image = cv2.drawContours(blank_image, cnt, -1, (0,255,0), 1)
    return image, curves


def calculate_solidity(contour):
    '''
    Solidity is the ratio of contour area to its convex hull area.
    '''
    area = cv2.contourArea(contour)
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area)/hull_area
    print('solidity: ', solidity)
    return solidity

def calculate_equivalent_diameter(contour):
    '''
    Equivalent Diameter is the diameter of the circle whose area is same as the contour area.
    '''
    area = cv2.contourArea(contour)
    equi_diameter = np.sqrt(4*area/np.pi)
    print('equivalent diameter: ', equi_diameter)
    return equi_diameter

def calculate_orientation(contour):
    '''
    Orientation is the angle at which object is directed. Following method also gives the Major Axis and Minor Axis lengths.
    '''
    if contour.shape[0] >= 5:
        (x,y),(MA,ma),angle = cv2.fitEllipse(contour)
        print('Major axis length: ', MA)
        print('Minor axis length: ', ma)
        print('Angle: ', angle)
        return (x,y), (MA,ma), angle
    else:
        return (-1,-1), (-1,-1), -1

def increase_contrast(image):
    #-----Converting image to LAB Color model-----
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            
    #-----Splitting the LAB image to different channels-----
    l, a, b = cv2.split(lab)
            
    #-----Applying CLAHE to L-channel-----
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
            
    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----
    limg = cv2.merge((cl,a,b))
            
    #-----Converting image from LAB Color model to RGB model-----
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inp', '--input_path', type=str, required=True, help='Path to the input video')
    parser.add_argument('-oup', '--output_path', type=str, required=True, help='Path to the output folder')
    args = parser.parse_args()

    INPUT_PATH = args.input_path
    OUTPUT_DIR = args.output_path
    # filename = 'large_background_2.mp4'
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    vidcap = cv2.VideoCapture(INPUT_PATH)
    success, image = vidcap.read()
    height, width, channel = image.shape
    
    list_of_images = []
    count = 0
    while success:
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_color.jpg" % count), image) # save frame as JPEG file      
        image = increase_contrast(image)
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_color_contrast.jpg" % count), image) # save frame as JPEG file      
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        list_of_images.append(image)
        hct_image = find_hough_circles(image)
        edge_image = canny_edge_detection(image, blur_ksize=7, threshold1=10, threshold2=40)
        thresh_image, contour_image, contours = find_contours(edge_image)
        edge_then_hct_image = find_hough_circles(edge_image)
        color_edge_image = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)
        minimum_enclosing_circle_image = minimum_enclosing_circle(color_edge_image, contours)
        color_edge_image_2 = cv2.cvtColor(edge_image, cv2.COLOR_GRAY2BGR)
        closed_curve_image, curves = detect_closed_curves(color_edge_image_2, contours)
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d.jpg" % count), image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_hct.jpg" % count), hct_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_edge.jpg" % count), edge_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_thresh.jpg" % count), thresh_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_contour.jpg" % count), contour_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_edge_then_hct.jpg" % count), edge_then_hct_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_minimum_enclosing_circle.jpg" % count), minimum_enclosing_circle_image)   # save frame as JPEG file      
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_close_curve.jpg" % count), closed_curve_image)   # save frame as JPEG file      
        success, image = vidcap.read()
    
        count += 1

    for i in range(0, count-1):
        disparity = cal_depth_map(list_of_images[i+1], list_of_images[i])
        cv2.imwrite(os.path.join(OUTPUT_DIR, "frame%d_disparity.jpg" % i), disparity)