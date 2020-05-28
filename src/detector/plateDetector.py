import cv2
import numpy as np
import os
from PIL import Image
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class PlateDetector:
    def __init__(self):
        pass

    def detect(self, img_path):
        image = cv2.imread(img_path)
        cnts, edge_img = self.process_img(img_path)
        plate = None
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            edges = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            if len(edges) == 4:
                x, y, w, h = cv2.boundingRect(c)
                plate = edge_img[y:y+h, x:x+w]
                plate = cv2.resize(plate, (180, 40))
                cv2.imwrite('./test/resources/plate.png', plate)
                # print(edges)
                # print(f'x:{x} y:{y} w:{w} h:{h}')
                break

        text = pytesseract.image_to_string(plate, lang='eng', config='--dpi 120')
        return text

    def __itHasContoursInit(self, cnt_edge, edges):
        for i in cnt_edge:
            print(i)
        return True
    def __contoursToEdges(self, contour):
        perimeter = cv2.arcLength(contour, True)
        return cv2.approxPolyDP(contour, 0.02 * perimeter, True)

    def process_img(self, img_path):
        image = cv2.imread(img_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.bilateralFilter(gray, 11, 90, 90)
        edges = cv2.Canny(blur, 30, 200)
        cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return (sorted(cnts, key=cv2.contourArea, reverse=True), edges)