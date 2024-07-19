import torch
import cv2
import numpy as np

template_path = 'images/remove_video_logo/logo_to_remove.png'
image_path = 'images/remove_video_logo/single_frame.png'

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # 'yolov5s' is a small version; you can use 'yolov5m' or 'yolov5l' for larger models

# Load images
img = cv2.imread(image_path)
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
template_w, template_h = template.shape[::-1]

# Convert the main image to grayscale for template matching
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect objects using YOLOv5
results = model(img)

# Process detections
for *box, conf, cls in results.xyxy[0]:
    x1, y1, x2, y2 = map(int, box)
    detected_region = gray_img[y1:y2, x1:x2]

    # Apply template matching
    res = cv2.matchTemplate(detected_region, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, (x1 + pt[0], y1 + pt[1]), (x1 + pt[0] + template_w, y1 + pt[1] + template_h), (0, 0, 255), 2)
        print(f"Detected Logo at X: {x1 + pt[0]}, Y: {y1 + pt[1]}")

cv2.imshow('Detected Objects and Logo - YOLOv5 & Template Matching', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
