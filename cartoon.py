from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Point3
from moviepy.editor import ImageSequenceClip
from PIL import Image
import numpy as np
import os


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the default camera control to customize the camera position
        self.disableMouse()

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)

        # Scale and position the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Create a simple human-like character using basic shapes
        self.character = self.render.attachNewNode("character")

        # Body
        body = self.loader.loadModel("models/misc/rgbCube")
        body.setScale(0.5, 1, 1)
        body.reparentTo(self.character)
        body.setColor(1, 0, 0, 1)

        # Head
        head = self.loader.loadModel("models/misc/sphere")
        head.setScale(0.3)
        head.reparentTo(self.character)
        head.setPos(0, 0, 1.5)
        head.setColor(1, 0.8, 0.6, 1)

        # Left Arm
        left_arm = self.loader.loadModel("models/misc/rgbCube")
        left_arm.setScale(0.2, 0.5, 0.2)
        left_arm.reparentTo(self.character)
        left_arm.setPos(-0.7, 0, 0.5)
        left_arm.setColor(1, 0.8, 0.6, 1)

        # Right Arm
        right_arm = self.loader.loadModel("models/misc/rgbCube")
        right_arm.setScale(0.2, 0.5, 0.2)
        right_arm.reparentTo(self.character)
        right_arm.setPos(0.7, 0, 0.5)
        right_arm.setColor(1, 0.8, 0.6, 1)

        # Left Leg
        left_leg = self.loader.loadModel("models/misc/rgbCube")
        left_leg.setScale(0.2, 0.2, 0.5)
        left_leg.reparentTo(self.character)
        left_leg.setPos(-0.3, 0, -1)
        left_leg.setColor(0, 0, 1, 1)

        # Right Leg
        right_leg = self.loader.loadModel("models/misc/rgbCube")
        right_leg.setScale(0.2, 0.2, 0.5)
        right_leg.reparentTo(self.character)
        right_leg.setPos(0.3, 0, -1)
        right_leg.setColor(0, 0, 1, 1)

        # Initial character position
        self.character.setPos(-10, 0, 0)

        # Add the movement task to the task manager
        self.taskMgr.add(self.move_character, "moveCharacterTask")

        # Position the camera
        self.camera.setPos(0, -30, 6)
        self.camera.lookAt(Point3(0, 0, 2))

        # Directory to save frames
        self.frames_dir = "frames"
        os.makedirs(self.frames_dir, exist_ok=True)

        # Frame index
        self.frame_index = 0

        # Task to capture frames
        self.taskMgr.add(self.capture_frame, "captureFrameTask")

    def move_character(self, _task):
        # Calculate new position
        pos = self.character.getPos()
        pos.setX(pos.getX() + 0.1)

        # Reset position if the character moves too far to the right
        if pos.getX() > 10:
            pos.setX(-10)

        # Set the new position
        self.character.setPos(pos)

        return Task.cont

    def capture_frame(self, _task):
        # Capture the frame from the window
        dr = self.win.getDisplayRegion(0)
        tex = dr.getScreenshot()
        image = np.array(tex.getRamImageAs("RGBA")).reshape((tex.getYSize(), tex.getXSize(), 4))
        image = Image.fromarray(image, 'RGBA')

        # Save the frame as an image
        frame_filename = os.path.join(self.frames_dir, f"frame_{self.frame_index:04d}.png")
        image.save(frame_filename)
        self.frame_index += 1

        # Stop capturing after a certain number of frames
        if self.frame_index >= 240:  # Capture for 10 seconds at 24 fps
            self.taskMgr.remove("moveCharacterTask")
            self.taskMgr.remove("captureFrameTask")
            self.render_video()
            self.userExit()

        return Task.cont

    def render_video(self):
        # Compile frames into a video using MoviePy
        frame_files = [os.path.join(self.frames_dir, f"frame_{i:04d}.png") for i in range(self.frame_index)]
        clip = ImageSequenceClip(frame_files, fps=24)
        clip.write_videofile("walking_cartoon.mp4", codec='libx264')


app = MyApp()
app.run()
