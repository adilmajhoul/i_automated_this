import cv2
import numpy as np

def multi_scale_template_matching(image, template, scales, threshold=0.95):
    found = None
    
    for scale in scales:
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        template_width, template_height = resized_template.shape[::-1]
        
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            found = (max_val, max_loc, template_width, template_height)
    
    return found

def get_logo_size(video_path, template_path):
    cap = cv2.VideoCapture(video_path)
    
    # for _ in range(10):
    #     ret, frame = cap.read()

    template_img = cv2.imread(template_path, cv2.IMREAD_COLOR)
    frame = cv2.imread('images/remove_video_logo/single_frame.png', cv2.IMREAD_COLOR)
    
    # Convert both template and frame to grayscale for template matching
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    
    # Define scales to search for the template
    # scales = np.linspace(0.5, 2.0, 20)  # Example scales, you can adjust this range
    


    # Perform template matching
    result = cv2.matchTemplate(gray_frame, gray_template, cv2.TM_CCOEFF_NORMED)

    # Locate the best match (top-left corner of the matched area)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= 0.80:
        template_width, template_height = gray_template.shape[::-1]
        return template_width, template_height
    else:
        # Return some default values or handle this case accordingly
        return 100, 100  # Example of returning default values

# Example usage

logo_to_remove = 'images/remove_video_logo/logo_to_remove_large.png'

video_path = 'images/remove_video_logo/input_video_large.mp4'


template_width, template_height = get_logo_size(video_path, logo_to_remove)
print(f"Detected template size: {template_width}x{template_height}")
