import cv2
from PIL import Image
import pytesseract
import imutils


pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class PlateDetector:
    def __init__(self):
        pass

    def detect(self, img_path: str) -> str:
        cnts, image = self.process_img(img_path)
        numberPlateCnt = None
        img1 = image.copy()
        cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)
        # cv2.imshow("Top 30 Contours", img1)
        # cv2.waitKey(0)

        count = 0
        plate_image = None

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                numberPlateCnt = approx

                x, y, w, h = cv2.boundingRect(c)
                plate_image = image[y:y + h, x:x + w]
                cv2.imwrite("test/resources/plate.png", plate_image)
                break

        # cv2.drawContours(image, [numberPlateCnt], -1, (0, 255, 0), 3)
        # cv2.imshow("Final image", image)
        # cv2.waitKey(0)

        # cv2.imshow("Plane image", plate_image)
        # cv2.waitKey(0)

        img = Image.open('./test/resources/plate.png')
        new_size = tuple(2*x for x in img.size)
        img = img.resize(new_size, Image.ANTIALIAS)

        text = pytesseract.image_to_string(img, lang='eng')
        return text

    def process_img(self, img_path: str) -> list:
        image = cv2.imread(img_path)

        # Resize image
        image = imutils.resize(image, width=500)

        # cv2.imshow("Original Image", image)
        # cv2.waitKey(0)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Grayscale", gray)
        # cv2.waitKey(0)

        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        # cv2.imshow("Bilateral Image", gray)
        # cv2.waitKey(0)

        edges = cv2.Canny(gray, 170, 200)
        # cv2.imshow("Canny", edges)
        # cv2.waitKey(0)

        cnts, new = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img = image.copy()
        cv2.drawContours(img, cnts, -1, (0, 255, 0), 3)
        # cv2.imshow("all contours", img)
        # cv2.waitKey(0)

        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        return cnts, image
