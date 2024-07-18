import cv2
import numpy as np
from PIL import Image
import os

class LogoRemover:
    def __init__(self, logo_to_remove, logo_to_add):
        self.template = cv2.imread(logo_to_remove, 0)
        self.your_logo = Image.open(logo_to_add).convert("RGBA")
        self.w, self.h = self.template.shape[::-1]

    def process_video(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fps = int(cap.get(5))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(gray_frame, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res)

            top_left = max_loc
            bottom_right = (top_left[0] + self.w, top_left[1] + self.h)

            resized_logo = self.your_logo.resize((self.w, self.h), Image.LANCZOS)
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            frame_pil.paste(resized_logo, (top_left[0], top_left[1]), resized_logo)
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def run(self, input_folder):
        for filename in os.listdir(input_folder):
            if filename.endswith('.mp4'):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(input_folder, f"output_{filename}")
                self.process_video(input_path, output_path)

# Example usage
logo_remover = LogoRemover('images/remove_video_logo/logo_to_remove.png', 'images/remove_video_logo/image_to_add.png')
logo_remover.run('images/remove_video_logo/input_videos')
