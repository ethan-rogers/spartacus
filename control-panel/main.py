import pygame


from remote_serial import *
from calibration import *

background_color = (144, 144, 144)

box_color = (60, 60, 60)
stick_color = (255, 0, 0)

knob_radius = 10

width = 450
height = 300

pygame.init()
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Spartacus Remote Calibration')

screen.fill(background_color)

pygame.display.flip()
running = True

box_thickness = 5
box_size = 120

text_spacing = 25
text_proportion_spacing = 10

box_x = 70
box_y = 50

power_x = box_x
power_y = 250

connect()

lv, rh, lh, rv = 1500, 1500, 1500 ,1500

connected = False

l_x = box_x + box_size/2
l_y = box_y + box_size/2

r_x = width - box_x - box_size/2
r_y = box_y + box_size/2

l_x_proportion = (lh - lh_center) /  lh_deviation
l_y_proportion = (lv - lv_center) /  lv_deviation

r_x_proportion = (rh - rh_center) /  rh_deviation
r_y_proportion = (rv - rv_center) /  rv_deviation

font = pygame.font.Font(None, 24)

while running:
    screen.fill(background_color)

    data = read_data()

    if data != None:
        print(data)
        connected, lv, rh, lh, rv = map(int, data.split())

        connected = bool(connected)

        l_x_proportion = (lh - lh_center) /  lh_deviation
        l_y_proportion = (lv - lv_center) /  lv_deviation

        r_x_proportion = (rh - rh_center) /  rh_deviation
        r_y_proportion = (rv - rv_center) /  rv_deviation

        l_y = -box_size/2 * l_y_proportion
        l_y += box_y + box_size/2

        l_x = -box_size/2 * l_x_proportion
        l_x += box_x + box_size/2

        r_y = -box_size/2 * r_y_proportion
        r_y += box_y + box_size/2

        r_x = -box_size/2 * r_x_proportion
        r_x += width - box_x - box_size/2



    text_surface = font.render(str(lv), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x - text_spacing, box_y + box_size/2 + text_proportion_spacing)))

    text_surface = font.render(f"{l_y_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x - text_spacing, box_y + box_size/2 - text_proportion_spacing)))

    text_surface = font.render(str(lh), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size/2, box_y + box_size + text_spacing + text_proportion_spacing)))

    text_surface = font.render(f"{l_x_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size/2, box_y + box_size + text_spacing - text_proportion_spacing)))

    text_surface = font.render(str(rv), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(width - box_x - box_size - text_spacing, box_y + box_size/2 + text_proportion_spacing)))

    text_surface = font.render(f"{r_y_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(width - box_x - box_size - text_spacing, box_y + box_size/2 - text_proportion_spacing)))

    text_surface = font.render(str(rh), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(width - box_x - box_size/2, box_y + box_size + text_spacing + text_proportion_spacing)))

    text_surface = font.render(f"{r_x_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(width - box_x - box_size/2, box_y + box_size + text_spacing - text_proportion_spacing)))

    if (connected):
        text_surface = font.render(f"POWER: ON", False, (0, 255, 0))
    else:
        text_surface = font.render(f"POWER: OFF", False, (255, 0, 0))

    screen.blit(text_surface, (power_x,power_y))

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
            close_port()
            running = False

    pygame.display.flip()
    
