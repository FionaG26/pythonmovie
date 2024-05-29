from moviepy.editor import VideoClip
import numpy as np
import cv2


def make_background():
    # Create an image for a sunny day background
    background = np.ones((480, 640, 3), dtype=np.uint8) * 255
    # Blue sky
    background[:320, :] = [135, 206, 235]
    # Green ground
    background[320:, :] = [34, 139, 34]
    # Draw the sun
    cv2.circle(background, (560, 80), 50, (0, 255, 255), -1)
    # Draw the sun's smile
    cv2.ellipse(background, (560, 80), (25, 25), 0, 180, 360, (0, 0, 0), 2)
    return background


def make_frame(t):
    background = make_background()

    # Character parameters
    character_color = (255, 0, 0)  # Red color in BGR
    character_width, character_height = 20, 40
    character_x = int(100 + 200 * t)  # Move character horizontally
    character_y = 360

    # Draw the character
    cv2.rectangle(background, (character_x, character_y),
                  (character_x + character_width, character_y + character_height),
                  character_color, -1)

    return background


# Create the animation
animation_clip = VideoClip(make_frame, duration=5)

# Write the video to a file
animation_clip.write_videofile("walking_cartoon.mp4", fps=24)
