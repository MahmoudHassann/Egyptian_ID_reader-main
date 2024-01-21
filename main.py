
from matplotlib import pyplot

from pytesseract import *
from tkinter import *
from PIL import ImageTk,Image
import cv2
import re
import numpy as np
import argparse
import imutils

def main():
    pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # img = capture_image()

    img=cv2.imread("data_set/14.jpg")

    cv2.imshow("Original Image", img)
    cv2.waitKey(0)
    #save_images()
    ara_num_res = extract_ara_num(img)
    print("ara_num_res: ",ara_num_res)

def extract_ara_num(img):
    #num=3

    # focus on the number section
    #img = cv2.imread("test/7.jpg")

    # Apply preprocessing
    img_preprocessed = preprocess_image(img)



    # Edge detection
    # edges = edge_detection(img_preprocessed)

    # Morphological transformations
    # img_morph = morphological_transformations(edges)

    # Find contours
    contours = find_contours(img_preprocessed)

    # Filter contours based on area
    min_area_threshold = 500  # Adjust as needed
    filtered_contours = filter_contours(contours, min_area_threshold)

    # Crop background
    cropped_background = crop_background(img, filtered_contours)

    # Display results (you may want to adapt this to your GUI)
    cv2.imshow("Original Image", img)
    cv2.imshow("Preprocessed Image", img_preprocessed)
    # cv2.imshow("Edge Detection", edges)
    # cv2.imshow("Morphological Transformations", img_morph)
    cv2.imshow("Cropped Background", cropped_background)
    cv2.waitKey(0)

    #
    #     # Improved error handling
    #
    # img = resize_ara_num(cropped_background)
    # h,w,ch=img.shape
    # img = img[int(h/1.8):int(h/1.08), int(w/2.8):int(w/1)]
    copy=cropped_background

    ##############################

    count = 0
    # in the loop untill reading the number
    while (True):
        count = count + 1
        # cv2.imshow('image0', img)
        # cv2.waitKey(500)

        # img = gray(img)
        # cv2.imshow('image01', img)
        # cv2.waitKey(500)
        # img = gaussian_blur(img)
        # cv2.imshow('image02', img)
        # cv2.waitKey(1000)
        # img=remove_noise(img)
        # cv2.imshow('image03', img)
        # cv2.waitKey(1000)
        # img=canny(img)
        # cv2.imshow('image04', img)
        # cv2.waitKey(3000)
        # img = threshold_ara_num(img)
        # cv2.imshow('image05', img)
        # cv2.waitKey(500)
        #
        # img= remove_noise(img)
        # cv2.imshow('image06', img)
        # cv2.waitKey(3000)
        #
        #cv2.imwrite("test_croped/"+str(1)+".jpg", img)
        #
        # cv2.imshow("img", img)
        # cv2.waitKey(0)

        res = pytesseract.image_to_string(img, lang="ara_number_id").split()
        print(res)
        if res != []:
            for i in res:
                if len(i) > 13 and len(i) < 15:
                    return i

        f_res=""
        for i in range(1,len(res)+1):
            if i >1:
                temp=res[len(res) - i]
                temp+=f_res
                f_res = temp
            else:
                f_res+= res[len(res) - i]

            if len(f_res)==14:
                return f_res


        img = increase_contrast(copy)
        cv2.imshow("img0",img)
        cv2.waitKey(0)
        if count > 1:
            img = increase_contrast(img)
        if count == 3:
            return "please re-capture the image"
        continue
    ################################################


def save_images():
    for i in range(1, 53):
        img = cv2.imread("nn/" + str(i) + ".jpg")
        img = resize_ara_num(img)
        h, w, ch = img.shape
        img = img[int(h / 1.8):int(h / 1.08), int(w / 3):int(w / 1)]
        cv2.imwrite("test_croped/" + str(i) + ".jpg", img)

##//////////////////////internet scource code //////////////////////////////////

def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def splitting_the_image(img):
    h, w, c = img.shape
    boxes = pytesseract.image_to_boxes(img)
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

    #img = cv2.imread('invoice-sample.jpg')

    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    print(d.keys())

    n_boxes = len(d['text'])
    for i in range(n_boxes):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)


# def detect_oriantation(img):
#     r'\nRevision: (\d+)\n'
#     osd = pytesseract.image_to_osd(img)
#     angle = re.search('(?<=Rotate: )(\d+)\n', osd).group(0)
#     script = re.search('(?<=Script: )(\d+)\n', osd).group(0)
#     print("angle: ", angle)
#     print("script: ", script)

def detect_digit_only(img):
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    res=pytesseract.image_to_string(img, config=custom_config)
    return res

def detect_custome(img):
    custom_config = r'-c tessedit_char_whitelist=0123456789 --psm 6'
    print(pytesseract.image_to_string(img, config=custom_config))
##////////////////////////////////////////////////////////##



def increase_contrast(img):
    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #cv2.imshow("lab", lab)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    #cv2.imshow('l_channel', l)
    #cv2.imshow('a_channel', a)
    #cv2.imshow('b_channel', b)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    #cv2.imshow('CLAHE output', cl)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    #cv2.imshow('limg', limg)

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    #cv2.imshow('final', final)
    return final


def extract_objects(img):
    image = img
    original = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    canny = cv2.Canny(blurred, 120, 255, 1)
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv2.dilate(canny, kernel, iterations=1)

    # Find contours
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # Iterate thorugh contours and filter for ROI
    image_number = 0
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        ROI = original[y:y + h, x:x + w]
        cv2.imwrite("ROI/ROI_{}.jpg".format(image_number), ROI)
        image_number += 1

    cv2.imshow('canny', canny)
    cv2.imshow('image', image)
    cv2.waitKey(0)

def remove_shadow(img):
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    #cv2.imwrite('shadows_out.png', result)
    #cv2.imwrite('shadows_out_norm.png', result_norm)
    return result_norm


def capture_image():
    img = cv2.VideoCapture()
    # The device number might be 0 or 1 depending on the device and the webcam
    img.open(0, cv2.CAP_DSHOW)
    while (True):
        ret, frame = img.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    img.release()
    cv2.destroyAllWindows()

    return frame


def sharpen(img):

    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    image_sharp = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    return image_sharp


def gaussian_blur(img):
    img = cv2.GaussianBlur(img, (3, 3), 1)
    return img

def decrease_brightness(img):
    img = np.int16(img)
    img=img-100
    img = np.clip(img, 0, 255)
    img = np.uint8(img)

    return img


def increase_brightness(img,value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def color_raise(img):
    boundaries = [
        ([0, 0, 0], [70, 70, 70])
    ]

    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        # show the images
        cv2.imshow("images", np.hstack([img, output]))
        cv2.waitKey(0)
    return output

def erode(img):
    img = cv2.erode(img.copy(), None,iterations=2)
    return img

def dilate(img):
    img = cv2.dilate(img.copy(), None,iterations=2)
    return img

def gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def threshold_eng_num(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img

def threshold_ara_num(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img

def threshold_word(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img

def resize_eng_num(img):
    #scale_percent = 50  # percent of original size
    width = 712
    height = 512
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

# def resize_ara_num(img):
#     #scale_percent = 50  # percent of original size
#     if len(img.shape) == 2:
#         # Grayscale image, convert to 3 channels for resizing
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#
#     width = 712
#     height = 512
#     dim = (width, height)
#     img2 = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
#     cv2.imshow("image1",img2)
#     cv2.waitKey(3000)
#     cv2.destroyAllWindows()
#     return img2
def resize_ara_num(img, target_width=712):
    if img is None:
        print("Error: Input image is None.")
        return None

    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    original_height, original_width, _ = img.shape
    aspect_ratio = original_height / original_width
    target_height = int(target_width * aspect_ratio)

    dim = (target_width, target_height)
    img_resized = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)

    return img_resized



def preprocess_image(img):
    #Gaussian blur
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray",gray)
    # cv2.waitKey(1000)

    # Dynamic thresholding
    _, img1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    img = cv2.bitwise_or(img1, img2)
    # cv2.imshow('thre', img)
    # cv2.waitKey(1000)

    # Apply histogram equalization
    equalized = cv2.equalizeHist(img)
    # cv2.imshow("eq", equalized)
    # cv2.waitKey(1000)

    return equalized

def find_contours(img):
    # Find contours
    contours, _ = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return contours

def filter_contours(contours, min_area_threshold):
    # Filter contours based on area
    filtered_contours = [
        cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold
    ]

    return filtered_contours

def crop_background(img, contours):
    if not contours:
        return None  # No contours found

    # Find the largest contour after filtering
    largest_contour = max(contours, key=cv2.contourArea)

    # Smooth the contour using convex hull
    hull = cv2.convexHull(largest_contour)

    # Create a mask for the convex hull
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [hull], 0, (255, 255, 255), thickness=cv2.FILLED)

    # Bitwise AND operation to obtain the cropped background
    cropped_background = cv2.bitwise_and(img, mask)

    return cropped_background
#IMP************************
# def preprocess_image(img):
#     #Gaussian blur
#     img = cv2.GaussianBlur(img, (5, 5), 0)
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # cv2.imshow("gray",gray)
#     # cv2.waitKey(1000)
#
#     # Dynamic thresholding
#     _, img1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     img2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
#     img = cv2.bitwise_or(img1, img2)
#     # cv2.imshow('thre', img)
#     # cv2.waitKey(1000)
#
#     # Apply histogram equalization
#     equalized = cv2.equalizeHist(img)
#     # cv2.imshow("eq", equalized)
#     # cv2.waitKey(1000)
#
#     return equalized
#
# def edge_detection(img):
#     edges = cv2.Canny(img, 50, 150)
#     return edges
#
# def morphological_transformations(img):
#     kernel = np.ones((5, 5), np.uint8)
#     img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
#     img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
#     return img
#
# def find_contours(img):
#     contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     return contours
#
# def filter_contours(contours, min_area_threshold):
#     filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]
#     return filtered_contours
#
# def crop_background(img, contours):
#     if len(contours) == 0:
#         return None  # No contours found
#
#     # Filter contours based on area
#     min_area_threshold = 500  # Adjust as needed
#     filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area_threshold]
#
#     if not filtered_contours:
#         return None  # No valid contours found after filtering
#
#     # Find the largest contour after filtering
#     largest_contour = max(filtered_contours, key=cv2.contourArea)
#
#     # Fit a bounding rectangle around the largest contour
#     x, y, w, h = cv2.boundingRect(largest_contour)
#
#     # Create a mask for the bounding rectangle
#     mask = np.zeros_like(img)
#     cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), thickness=cv2.FILLED)
#
#     # Bitwise AND operation to obtain the cropped background
#     cropped_background = cv2.bitwise_and(img, mask)
#
#     return cropped_background


def Canny(img):
    img = cv2.Canny(img, 120, 255)
    return img

def fill(img):
    im_floodfill = img.copy()

    h, w = img.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255);
    im_floodfill_inv  = cv2.bitwise_not(im_floodfill)
    im_out = img | im_floodfill_inv
    return im_out


if __name__ == '__main__':
    #form = Tk()
    #canvas = Canvas(form, width=1200, height=650)
    #canvas.pack()
    main()


