from moviepy.editor import ImageSequenceClip

# List of rendered animation frames (replace with actual file paths)
frames = ["frame1.png", "frame2.png", "frame3.png", ...]

# Create a video clip from the frames
animation_clip = ImageSequenceClip(frames, fps=24)

# Write the video to a file
animation_clip.write_videofile("3d_cartoon_animation.mp4", fps=24)
