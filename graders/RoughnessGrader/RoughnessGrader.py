
import cv2
import numpy as np
import math
from ResourceManager import ResourceManager

class RoughnessGrader:
    def get_perimeter(self, contours):
        perimeter = 0
        for c in contours:
            perimeter += cv2.arcLength(c, True)
        return perimeter
    
    def get_area(self, contours):
        area = 0
        for c in contours:
            area += cv2.contourArea(c)
        return area
    
    def get_score(self, image, binary_grid, do_show_contours=False):
        # Turn image grey for higher accuracy
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set a threshold
        thresh = 1

        # Get threshold image
        ret, thresh_img = cv2.threshold(image_grey, thresh, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate perimeter
        perimeter = self.get_perimeter(contours)

        if perimeter == 0:
            return 0

        # Calculate measured area
        measured_area = self.get_area(contours)

        # Calculate maximum roughness
        radius = math.sqrt(measured_area / math.pi)
        maximum_roughness = radius / 2

        # Calculate actual roughness
        roughness = measured_area / perimeter

        # Calculate score
        score = 1 - (roughness / maximum_roughness)

        if(do_show_contours):
            self.show_counters(image, contours)
        
        # return round(score, ResourceManager().FLOAT_PRECISION)
        return score
    
    def show_counters(self, image, contours):
        # Create an empty image for contours
        image_contours = np.zeros(image.shape)

        perimeter = self.get_perimeter(contours)

        # Draw contours on empty image
        for c in contours:
            approx = cv2.approxPolyDP(c, 0.0001 * perimeter, True)
            cv2.drawContours(image_contours, [approx], -1, (0, 0, 255), 1)

        # Show image
        cv2.imshow('Output', image_contours)
        cv2.waitKey(0)