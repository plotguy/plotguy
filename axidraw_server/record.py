import time
from pseyepy import Camera, Display, Stream
from moviepy.editor import *


fn = 'naveen'

c = Camera()
s = Stream(c, file_name=fn)

time.sleep(2)

s.end()


clip = VideoFileClip(f"{fn}_0.avi")

clip.write_gif("naveen.gif")
