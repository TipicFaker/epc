import robomasterpy
import time
import cv2 as cv
from robomasterpy import framework as rmf
hub = rmf.Hub()

def display(frame, **kwargs) -> None:       
    cv.imshow("frame", frame)
    cv.waitKey(1)

print("start")

#robomasterpy.get_broadcast_ip(1)

cmd = robomasterpy.Commander()
print(cmd)

print("lol")

# enable video streaming
cmd.stream(True)
# rm.Vision is a handler for video streaming
# display is the callback function defined above

ip = cmd.get_ip()

hub.worker(rmf.Vision, 'vision', (None, ip, display))

hub.run()

print(cmd.chassis_move(x = 1, y = 0, z = 360, speed_xy=2, speed_z=180))

#cmd.do("chassis move x 1 y 1")

time.sleep(3)

print(cmd.chassis_move(x = -1, y = 0, speed_xy= 2))

time.sleep(3)

print("yes")

cmd.close()