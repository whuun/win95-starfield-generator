import cv2
import numpy as np
import math
import random
import os

#lenght of animation in amount of frames
LENGHT_FRAMES = 30 * 10

#params of animation
SPEED = 1.0
STARS_AMOUNT = 250
STAR_SCALE = 1.0

#params of your screen
FPS = 30
WIDTH = 1920
HEIGHT = 1080

ABSOLUTE_SPEED = 200
ABSOLUTE_ACCELERATION = 400

class Star:
    def __init__(self, x, y):
        self.initial_x = x
        self.initial_y = y

        self.x = x
        self.y = y

        dx = x - WIDTH * 0.5 
        dy = y - HEIGHT * 0.5

        hypot = math.hypot(dx, dy) 
        canvas_hypot = math.hypot(WIDTH * 0.5, HEIGHT * 0.5) 

        self.distance_from_center = hypot / canvas_hypot        
        self.angle = math.atan2(dy, dx)

        self.initial_speed = ABSOLUTE_SPEED * self.distance_from_center
        self.speed = self.initial_speed
        self.acceleration = ABSOLUTE_ACCELERATION * (1 - self.distance_from_center)

    def update(self, lasted):
        self.speed += self.acceleration * lasted * SPEED
        distance = self.speed * lasted * SPEED

        self.x = self.x + distance * math.cos(self.angle)
        self.y = self.y + distance * math.sin(self.angle)

        avarage = (HEIGHT + WIDTH) * 0.5
        size = (self.speed / ABSOLUTE_SPEED) * avarage / 750
        size = min(size, avarage // 250) * STAR_SCALE

        return self.x, self.y, int(size) 


def create_black_mask(frame):
    lower = np.array([0, 0, 0])
    upper = np.array([50, 50, 50])
    mask = cv2.inRange(frame, lower, upper)
    return mask


def main():
    filename = 'tempoutput.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(filename, cv2.CAP_FFMPEG, fourcc, FPS, (WIDTH, HEIGHT))

    Milkyway = []

    run = True
    generate = True
    c = 0
    spawn_accumulator = 0.0

    while (run):
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        if c >= LENGHT_FRAMES:
            generate = False

        spawn_accumulator += STARS_AMOUNT / 1.5 / FPS

        while spawn_accumulator >= 1.0 and generate:
            difference = STARS_AMOUNT - len(Milkyway)
            if difference != 0:
                rand_x = random.randint(0, WIDTH)
                rand_y = random.randint(0, HEIGHT)
                Milkyway.append(Star(rand_x, rand_y))
            spawn_accumulator -= 1.0

        lasted = 1 / FPS

        index = 0
        for star in Milkyway:
            result = star.update(lasted)
            center = (int(result[0]), int(result[1]))
            diameter = result[2]

            if center[0] < 0 or center[0] >= WIDTH or center[1] < 0 or center[1] >= HEIGHT:
                Milkyway.pop(index)

            top_left = (center[0] - diameter // 2, center[1] - diameter // 2)
            bottom_right = (center[0] + diameter // 2, center[1] + diameter // 2)

            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), thickness=-1)
            index += 1

        out.write(frame)
        c += 1
        print("\r", end="")
        print(f"doing frame {c} out of {LENGHT_FRAMES}", end="")
        
        if len(Milkyway) == 0:
            run = False

    print("")

    out.release()

    print("post processing...")

    offset = c - LENGHT_FRAMES

    temp1 = cv2.VideoCapture('tempoutput.avi')
    temp2 = cv2.VideoCapture('tempoutput.avi')

    fps = temp1.get(cv2.CAP_PROP_FPS)
    frame_width = int(temp1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(temp1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter('output.avi', cv2.CAP_FFMPEG, fourcc, fps, (frame_width, frame_height))

    temp2.set(cv2.CAP_PROP_POS_FRAMES, offset)

    c = 0
    while True:
        ret, frame2 = temp2.read()
        if not ret:
            break

        if c >= LENGHT_FRAMES - offset:
            _, frame1 = temp1.read()
            mask = create_black_mask(frame1)
            inverted_mask = cv2.bitwise_not(mask)

            frame1_with_alph = cv2.bitwise_and(frame1, frame1, mask=inverted_mask)
            frame2_with_alph = cv2.bitwise_and(frame2, frame2, mask=mask)

            blend_frame = cv2.add(frame1_with_alph, frame2_with_alph)
            output.write(blend_frame)
        else:
            output.write(frame2)
        c += 1
        print("\r", end="")
        print(f"post processed frame {c} out of {LENGHT_FRAMES}", end="")

    print("")

    os.remove("tempoutput.avi")
    output.release()


main()
