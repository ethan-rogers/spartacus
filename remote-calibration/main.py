import pygame


from remote_serial import connect, read_data
from calibration import *

background_color = (144, 144, 144)

box_color = (60, 60, 60)
stick_color = (255, 0, 0)

knob_radius = 10

width = 400
height = 300

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Spartacus Remote Calibration')

screen.fill(background_color)

pygame.display.flip()
running = True

box_thickness = 5
box_size = 120

box_x = 50
box_y = height / 2 - box_size / 2

connect()

l_x = box_x + box_size/2
l_y = box_y + box_size/2

r_x = width - box_x - box_size/2
r_y = box_y + box_size/2

while running:
    screen.fill(background_color)

    data = read_data()

    if data != None:
        print(data)
        lv, rh, lh, rv = map(int, data.split())

        l_y =  (lv - lv_center) /  lv_deviation
        l_y *= -box_size/2
        l_y += box_y + box_size/2

        l_x =  (lh - lh_center) /  lh_deviation
        l_x *= -box_size/2
        l_x += box_x + box_size/2

        r_y =  (rv - rv_center) /  rv_deviation
        r_y *= -box_size/2
        r_y += box_y + box_size/2

        r_x =  (rh - rh_center) /  rh_deviation
        r_x *= -box_size/2
        r_x += width - box_x - box_size/2

    # left knob
    pygame.draw.circle(screen, stick_color, (l_x, l_y), knob_radius, width=0)

    # right knob
    pygame.draw.circle(screen, stick_color, (r_x, r_y), knob_radius, width=0)


    # left stick
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_size, box_size), width=box_thickness)  

    # right stick
    pygame.draw.rect(screen, box_color, (width - box_x - box_size, box_y, box_size, box_size), width=box_thickness) 
  
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    
