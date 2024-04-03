from OpenGL.GL import *
from OpenGL.GLUT import *

import time
import random

W_Width = 800
W_Height = 800
char_x = 400
char_y = 500 # 50  
char_radius = 20

prev_time = time.time()
char_accY = -50
char_velY = 0
char_velX = 0
char_speedX = 20
jump_power = 40
frictionX = 0.95
frictionY = 0.95
canJump = False

platform_gap = 120
vanishing_weight = 30
vanishing_time = 2

left_key = b'a'
right_key = b'd'
jump_key = b' '

keyState = {
    left_key: False,
    right_key: False,
    jump_key: False
}



class Platform:
    def __init__(self, x, y, vanishing = False):
        self.x = x
        self.y = y
        self.vanishing = vanishing
        self.collision_time = 0
        self.collided = False
        self.colors = [1,0,0] if self.vanishing == True else [1,1,1]

        self.width = 150

        self.x1 = int(self.x - self.width/2)
        self.x2 = int(self.x + self.width/2)

platforms = []
platforms.append(Platform(400, 300))
for i in range(7):
    if random.uniform(1,100) <= vanishing_weight:
        v = True
    else:
        v = False
    platforms.append(Platform(random.uniform(50, W_Width-50), platforms[-1].y + platform_gap, vanishing = v))


def draw_points(x, y):
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                return 0  
            else:
                return 7  
        else:
            if dy >= 0:
                return 3  
            else:
                return 4  
    else:
        if dx >= 0:
            if dy >= 0:
                return 1  
            else:
                return 6  
        else:
            if dy >= 0:
                return 2  
            else:
                return 5 
        
def convertZone(x1, y1, zone):
    if zone == 1:
        return y1, x1
    elif zone == 2:
        return -y1, x1
    elif zone == 3:
        return -x1, y1
    elif zone == 4:
        return -x1, -y1
    elif zone == 5:
        return -y1, -x1
    elif zone == 6:
        return y1, -x1
    elif zone == 7:
        return x1, -y1
    
    return x1, y1


def lineAlgo(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    y = y1
    points = []

    for x in range(x1, x2 + 1):
        points.append((x, y))  

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE

    return points

def drawLine(x1, y1, x2, y2, c1=1, c2=1, c3=1):
    glColor3f(c1, c2, c3)
    line_zone = findZone(x1, y1, x2, y2)
    a, b = convertZone(x1, y1, line_zone)
    c, d = convertZone(x2, y2, line_zone)
    points = lineAlgo(a, b, c, d)
    temp = []
    for point in points:
        x, y = point[0], point[1]
        old_x, old_y = convertZone(x, y, line_zone)
        temp.append((old_x, old_y))
    for point in temp:
        e, f = point[0], point[1]
        draw_points(e, f)

def draw_circle(center_x, center_y, radius):
    x, y = 0, radius
    d = 1 - radius

    while x <= y:
        draw_points(x + center_x, y + center_y)
        draw_points(y + center_x, x + center_y)
        draw_points(-y + center_x, x + center_y)
        draw_points(-x + center_x, y + center_y)
        draw_points(-x + center_x, -y + center_y)
        draw_points(-y + center_x, -x + center_y)
        draw_points(y + center_x, -x + center_y)
        draw_points(x + center_x, -y + center_y)

        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * (x - y) + 5
            x += 1
            y -= 1

def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(x, y)

def keyListener(key, x, y):
    global keyState, platforms

    for k in keyState.keys():
        if key == k:
            keyState[k] = True
            # print(k)

    # if key == b'f':
    #     platforms.append(Platform(random.uniform(50, W_Width-50), platforms[-1].y + platform_gap, vanishing = bool(random.getrandbits(1))))


def keyUpListener(key, x, y):
    global keyState

    for k in keyState.keys():
        if key == k:
            keyState[k] = False
            # print(k)

def handleKeyPress():
    global char_velY, char_velX, char_speedX, jump_power, keyState, canJump

    if keyState[left_key]:
        char_velX = -char_speedX * 10
    if keyState[right_key]:
        char_velX = char_speedX * 10
    if keyState[jump_key] and canJump == True:
        char_velY = jump_power * 10
        canJump = False

def drawShapes():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()


    glColor3f(0.96, 0.537, 0.8)
    draw_circle(char_x, char_y, char_radius)
    drawLine(0, 25, 800, 25)

    for obj in platforms:
        drawLine(obj.x1, obj.y, obj.x2, obj.y, *obj.colors)

    glutSwapBuffers()

def display():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

def poolObjects(obj):
    pooled_obj = platforms.pop(platforms.index(obj))
    y = platforms[-1].y + platform_gap
    x = random.uniform(50, W_Width-50)

    if random.uniform(1,100) <= vanishing_weight:
        v = True
    else:
        v = False
    
    new_obj = Platform(x, y, vanishing=v)

    del pooled_obj
    platforms.append(new_obj)

def update():
    global char_x, char_y, prev_time, char_velY, char_accY, frictionX, char_velX, platforms, canJump
    
    handleKeyPress()


    # Delta Time
    current_time = time.time()
    dt = current_time - prev_time
    prev_time = current_time

    # Gravity
    char_velY += (char_accY * 10) * dt
    char_y += (char_velY * dt)

    # Charecter X Movement
    char_x += (char_velX * dt)

    char_velX *= frictionX 

    for obj in platforms:
        
        # Platform Collision Checks
        # X collision
        if char_x > obj.x1 - char_radius and char_x < obj.x2 + char_radius:
            # Y Collision
            if char_y <= obj.y + char_radius and char_y >= obj.y - char_radius:
                # Colliding while falling down only
                if char_velY < 0:
                    char_velY = 0
                    char_y = obj.y + char_radius
                    canJump = True

                    if not obj.collided and obj.vanishing:
                        obj.collision_time = time.time()
                        obj.collided = True
        
        # Falling Platform
        obj.y -= 1

        # Vanishing Platform
        if obj.vanishing and obj.collided:
            elapsed_time = time.time() - obj.collision_time
            obj.colors[0] = 1 - (elapsed_time/vanishing_time)
            if elapsed_time >= vanishing_time:
                poolObjects(obj)
            

        # Platform Pooling
        if obj.y < -5:
            poolObjects(obj)

    glutPostRedisplay()

def main():
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow(b"Project 423")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W_Width, 0, W_Height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutDisplayFunc(drawShapes)
    glutMouseFunc(mouseListener)
    glutKeyboardFunc(keyListener)
    glutKeyboardUpFunc(keyUpListener)
    glutIdleFunc(update)
    # glutSpecialFunc(specialKeyListener)
    glutMainLoop()

if __name__ == "__main__":
    main()