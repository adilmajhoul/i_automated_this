import cv2
import numpy as np
from PIL import Image

class VideoLogoReplacer:
    def __init__(self, template_path, logo_path, video_path, output_path):
        self.template_path = template_path
        self.logo_path = logo_path
        self.video_path = video_path
        self.output_path = output_path
        self.template = cv2.imread(template_path, 0)
        if self.template is None:
            print(f"Error: Could not open or read the image file '{template_path}'")
            exit()
        self.w, self.h = self.template.shape[::-1]
        self.your_logo = Image.open(logo_path).convert("RGBA")
        self.cap = cv2.VideoCapture(video_path)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fps = int(self.cap.get(5))
        self.out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.frame_width, self.frame_height))

    def process_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(gray_frame, self.template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            top_left = max_loc
            bottom_right = (top_left[0] + self.w, top_left[1] + self.h)

            resized_logo = self.your_logo.resize((self.w, self.h), Image.LANCZOS)

            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frame_pil.paste(resized_logo, (top_left[0], top_left[1]), resized_logo)
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

            self.out.write(frame)

        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()

# Usage:
template_path = 'images/remove_video_logo/logo_to_remove.png'
logo_path = 'images/remove_video_logo/image_to_add.png'

video_path = 'images/remove_video_logo/input_video_large.mp4'
output_path = 'images/remove_video_logo/output_video.mp4'

video_replacer = VideoLogoReplacer(template_path, logo_path, video_path, output_path)
video_replacer.process_video()
