
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
    
    def filter_parent_contours(self, contours, hierarchy):
        parent_contours = []
        child_contours = []
        for i, h in enumerate(hierarchy[0]):
            if h[3] == -1:  # If the contour has no parent (its a parent contour)
                parent_contours.append(contours[i])
            else:
                child_contours.append(contours[i])
        return parent_contours, child_contours
    
    def get_score(self, image, binary_grid, do_show_contours=False):
        # Turn image grey for higher accuracy
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set a threshold
        thresh = 1

        # Get threshold image
        ret, thresh_img = cv2.threshold(image_grey, thresh, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out parent and child contours
        parent_contours, child_contours = self.filter_parent_contours(contours, hierarchy)

        # Calculate perimeter and area for parent contours
        parent_perimeter = self.get_perimeter(parent_contours)
        parent_area = self.get_area(parent_contours)

        # Calculate perimeter and area for child contours (holes)
        child_perimeter = self.get_perimeter(child_contours)
        child_area = self.get_area(child_contours)

        # Subtract hole area from parent, adding perimeter
        parent_perimeter += child_perimeter
        parent_area -= child_area

        # Calculate maximum roughness
        parent_radius = math.sqrt(parent_area / math.pi)
        parent_maximum_roughness = parent_radius / 2

        # Calculate actual roughness for parent contours
        parent_roughness = parent_area / parent_perimeter

        # Normalize complexity score
        score = 1 - (parent_roughness / parent_maximum_roughness)

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