import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

class RectangleProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.output_folder = os.path.join(folder_path, "output")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def calculate_distance(self, rect1, rect2):
        x1, y1, w1, h1 = rect1[:4]
        x2, y2, w2, h2 = rect2[:4]

        left1, right1 = x1, x1 + w1
        top1, bottom1 = y1, y1 + h1
        left2, right2 = x2, x2 + w2
        top2, bottom2 = y2, y2 + h2

        if right1 < left2:
            dx = left2 - right1
        elif right2 < left1:
            dx = left1 - right2
        else:
            dx = 0

        if bottom1 < top2:
            dy = top2 - bottom1
        elif bottom2 < top1:
            dy = top1 - bottom2
        else:
            dy = 0

        return np.sqrt(dx**2 + dy**2)

    def is_overlapping(self, rect1, rect2):
        x1, y1, w1, h1 = rect1[:4]
        x2, y2, w2, h2 = rect2[:4]

        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def merge_rectangles(self, rectangles):
        merged = True
        while merged:
            merged = False
            for i in range(len(rectangles)):
                for j in range(i + 1, len(rectangles)):
                    if self.is_overlapping(rectangles[i], rectangles[j]):
                        x_min = min(rectangles[i][0], rectangles[j][0])
                        y_min = min(rectangles[i][1], rectangles[j][1])
                        x_max = max(rectangles[i][0] + rectangles[i][2], rectangles[j][0] + rectangles[j][2])
                        y_max = max(rectangles[i][1] + rectangles[i][3], rectangles[j][1] + rectangles[j][3])
                        area = (x_max - x_min) * (y_max - y_min)
                        rectangles[i] = (x_min, y_min, x_max - x_min, y_max - y_min, area)
                        del rectangles[j]
                        merged = True
                        break
                if merged:
                    break
        return rectangles

    def find_bounding_rectangles(self, image_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output_image = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        rectangles = []
        red_rectangles = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            if area > 10000:
                red_rectangles.append((x, y, w, h, area))
            else:
                rectangles.append((x, y, w, h, area))

        red_rectangles = self.merge_rectangles(red_rectangles)
        filtered_rectangles = []
        for rect in rectangles:
            overlap = False
            for red_rect in red_rectangles:
                if self.is_overlapping(rect, red_rect):
                    overlap = True
                    break
            if not overlap:
                filtered_rectangles.append(rect)

        return output_image, filtered_rectangles

    def find_adjacent_classes(self, rectangles, distance_threshold=30):
        adjacent_classes = []
        for i in range(len(rectangles)):
            for j in range(i + 1, len(rectangles)):
                if self.calculate_distance(rectangles[i], rectangles[j]) < distance_threshold:
                    found = False
                    for cls in adjacent_classes:
                        if i in cls or j in cls:
                            cls.add(i)
                            cls.add(j)
                            found = True
                            break
                    if not found:
                        adjacent_classes.append({i, j})

        merged = True
        while merged:
            merged = False
            for i in range(len(adjacent_classes)):
                for j in range(i + 1, len(adjacent_classes)):
                    if adjacent_classes[i].intersection(adjacent_classes[j]):
                        adjacent_classes[i].update(adjacent_classes[j])
                        del adjacent_classes[j]
                        merged = True
                        break
                if merged:
                    break

        return adjacent_classes

    def find_min_bounding_rect(self, rectangles, indices):
        x_min = min(rectangles[i][0] for i in indices)
        y_min = min(rectangles[i][1] for i in indices)
        x_max = max(rectangles[i][0] + rectangles[i][2] for i in indices)
        y_max = max(rectangles[i][1] + rectangles[i][3] for i in indices)
        return (x_min, y_min, x_max - x_min, y_max - y_min)

    def second_round_merge(self, min_rects, distance_threshold=1):
        merged = True
        while merged:
            merged = False
            for i in range(len(min_rects)):
                for j in range(i + 1, len(min_rects)):
                    if self.calculate_distance(min_rects[i], min_rects[j]) < distance_threshold:
                        x_min = min(min_rects[i][0], min_rects[j][0])
                        y_min = min(min_rects[i][1], min_rects[j][1])
                        x_max = max(min_rects[i][0] + min_rects[i][2], min_rects[j][0] + min_rects[j][2])
                        y_max = max(min_rects[i][1] + min_rects[i][3], min_rects[j][1] + min_rects[j][3])
                        min_rects[i] = (x_min, y_min, x_max - x_min, y_max - y_min)
                        del min_rects[j]
                        merged = True
                        break
                if merged:
                    break
        return min_rects

    def filter_small_rectangles(self, min_rects):
        filtered_rects = []
        for rect in min_rects:
            x, y, w, h = rect
            if w >= 30 and h >= 30 and w * h >= 3000:
                filtered_rects.append(rect)
        return filtered_rects

    def display_bounding_rectangles(self, output_image, rectangles, adjacent_classes, image_path):
        min_rects = []
        for cls in adjacent_classes:
            min_rect = self.find_min_bounding_rect(rectangles, cls)
            min_rects.append(min_rect)

        min_rects = self.second_round_merge(min_rects)
        filtered_min_rects = self.filter_small_rectangles(min_rects)

        for i, rect in enumerate(filtered_min_rects):
            cropped_image = output_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
            page_info = os.path.basename(image_path).split('.')[0]
            cv2.imwrite(os.path.join(self.output_folder, f"cropped_{page_info}_box_{i}.png"), cropped_image)
            cv2.rectangle(output_image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0), 2)

        plt.imshow(cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB))
        plt.title('Bounding Rectangles')
        plt.axis('off')
        plt.show()

    def process_image(self, image_path):
        output_image, rectangles = self.find_bounding_rectangles(image_path)
        adjacent_classes = self.find_adjacent_classes(rectangles)
        self.display_bounding_rectangles(output_image, rectangles, adjacent_classes, image_path)

    def process_all_images(self):
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(self.folder_path, filename)
                print(f"Processing {image_path}")
                self.process_image(image_path)