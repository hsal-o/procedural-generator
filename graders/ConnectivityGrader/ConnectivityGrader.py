import cv2
import numpy as np
import math
from ResourceManager import ResourceManager

class ConnectivityGrader:
    def get_perimeter(self, contours):
        perimeter = 0
        for c in contours:
            perimeter += cv2.arcLength(c, True)
        return perimeter
    
    def remove_dwarf_contours(self, contours):
        # Find largest contour area
        largest_contour = max(contours, key=cv2.contourArea)
        largest_area = cv2.contourArea(largest_contour)

        # Set a minimum area threshold, will be largest area * min area %
        min_area_percentage = 0.2
        min_area = largest_area * min_area_percentage

        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_area]

        return filtered_contours
    
    # Preprocess image using Opening Morphology with a custom kernal to close off "diagonal" openings
    # https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
    def preprocess_image(self, image):
        kernel = np.array([[0, 1, 0],
                        [1, 0, 1],
                        [0, 1, 0]], dtype=np.uint8)
        processed_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        
        return processed_image
    
    def get_score(self, image, binary_grid, do_show_contours=False):
        image = self.preprocess_image(image)

        # Turn image grey for higher accuracy
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set a threshold
        thresh = 1

        # Get threshold image
        ret, thresh_img = cv2.threshold(image_grey, thresh, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL  , cv2.CHAIN_APPROX_SIMPLE)

        if contours == ():
            return 0

        # Filter contours to remove dwarf contours
        contours = self.remove_dwarf_contours(contours)

        # score = len(contours)
        score = math.exp(-0.25 * math.exp(1) * (len(contours) - 1)) # e^(0.25e(x-1))

        # Debug, shows contours
        # self.show_counters(image, contours)
        
        # return round(score, ResourceManager().FLOAT_PRECISION)
        return score
    
    def show_counters(self, image, contours):
        # Interesting test cases:
        # 1132484721 // Two caves are diagonally adjacent, see difference between preprocessed image and w/o
        # 3967836191 // Two sizeable caves with three dwarf caves

        # Create an empty image for contours
        image_contours = np.zeros(image.shape)

        perimeter = self.get_perimeter(contours)

        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]

        # Draw contours on empty image
        for i, contour in enumerate(contours):
            color = colors[i % len(colors)]
            approx = cv2.approxPolyDP(contour, 0.0001 * perimeter, True)
            cv2.drawContours(image_contours, [approx], -1, color, 1)

        # Show image
        cv2.imshow('Output', image_contours)
        cv2.waitKey(0)
