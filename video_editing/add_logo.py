from moviepy.editor import *
import os
import concurrent.futures


class VideoProcessor:
    def __init__(self, image_path, scale_factor, position, output_folder):

        self.image_path = image_path
        self.scale_factor = scale_factor
        self.pos = position

        self.output_folder = output_folder

    def process_video(self, video_path, iteration):
        # Load the video
        video = VideoFileClip(video_path)

        # Calculate new width as 80% of the video width
        new_width = int(video.w * 0.85)

        # Load the image and set its duration
        image = ImageClip(self.image_path).set_duration(video.duration)

        # Calculate the aspect ratio of the image
        image_aspect_ratio = image.h / image.w

        # Calculate new height while maintaining the image aspect ratio
        new_height = int(new_width * image_aspect_ratio)

        # Resize the image
        image_scaled = image.resize((new_width, new_height))

        # Calculate the new position (10% from the top)
        top_position = int(video.h * 0.1)

        # Create composite video with the updated position
        video_with_image = CompositeVideoClip([video, image_scaled.set_pos(("center", top_position))])

        # Save the output video
        output_path = os.path.join(self.output_folder, f"{iteration}_video.mp4")
        video_with_image.write_videofile(output_path, codec="libx264")

    def run(self, input_folder):
        # Ensure output folder exists
        os.makedirs(self.output_folder, exist_ok=True)

        videos = [video for video in os.listdir(input_folder) if video.endswith((".mp4", ".mov", ".avi"))]

        for i, filename in enumerate(videos):
            video_path = os.path.join(input_folder, filename)
            self.process_video(video_path, i)

        # Process 5 videos at a time
        # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #     for i, filename in enumerate(videos):
        #         video_path = os.path.join(input_folder, filename)
        #         executor.submit(self.process_video, video_path, i)


# Example usage
image_path = "images/promo.png"
scale_factor = 0.8
position = ("center", 100)

processor = VideoProcessor(image_path, scale_factor, position, "output_videos")
processor.run("input_videos")
