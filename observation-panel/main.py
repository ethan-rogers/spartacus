import pygame


from remote_serial import *
from calibration import *

background_color = (144, 144, 144)

box_color = (60, 60, 60)
stick_color = (255, 0, 0)

knob_radius = 10

width = 600
height = 430

pygame.init()
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Spartacus Observation Panel')

screen.fill(background_color)

pygame.display.flip()
running = True

box_thickness = 5
box_size = 120

text_spacing = 25
text_proportion_spacing = 10

box_x = 70
box_y = 200

box_spacing = 80

power_x = box_x
power_y = 390


motor_x = box_x + 40
motor_y = 60
motor_spacing = 100
motor_bar_height = 80

motor_width = 6

level_color = stick_color
level_length = 20
level_height = 8

max_level_height = motor_y + motor_bar_height




font = pygame.font.Font(None, 24)

spinner_motor_label = font.render(f"Spinner", False, box_color)
left_motor_label = font.render(f"Left", False, box_color)
right_motor_label = font.render(f"Right", False, box_color)
speed_motor_label = font.render(f"Speed", False, box_color)
angle_motor_label = font.render(f"Turn Rate", False, box_color)

calculated_speed = 0
calculated_turn_speed = 0

connect()

lv, rh, lh, rv = 1500, 1500, 1500 ,1500
spinner_power, left_power, right_power = 0,0,0

connected = False

l_x = box_x + box_size/2
l_y = box_y + box_size/2

r_x = box_x  + box_size*1.5 + box_spacing 
r_y = box_y + box_size/2

l_x_proportion = (lh - lh_center) /  lh_deviation
l_y_proportion = (lv - lv_center) /  lv_deviation

r_x_proportion = (rh - rh_center) /  rh_deviation
r_y_proportion = (rv - rv_center) /  rv_deviation



while running:
    screen.fill(background_color)

    data = read_data()

    if data != None:
        print(data)
        connected, spinner_power, left_power, right_power, lv, rh, lh, rv = data.split()

        spinner_power, left_power, right_power = float(spinner_power), float(left_power), float(right_power)
        lv, rh, lh, rv = int(lv), int(rh), int(lh), int(rv)
        connected = int(connected)

        calculated_speed = (left_power + right_power) / 2
        calculated_turn_speed = (left_power - right_power) / 2


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
        r_x += box_x  + box_size*1.5 + box_spacing 



    text_surface = font.render(str(lv), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x - text_spacing, box_y + box_size/2 + text_proportion_spacing)))

    text_surface = font.render(f"{l_y_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x - text_spacing, box_y + box_size/2 - text_proportion_spacing)))

    text_surface = font.render(str(lh), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size/2, box_y + box_size + text_spacing + text_proportion_spacing)))

    text_surface = font.render(f"{l_x_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size/2, box_y + box_size + text_spacing - text_proportion_spacing)))

    text_surface = font.render(str(rv), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size + box_spacing - text_spacing, box_y + box_size/2 + text_proportion_spacing)))

    text_surface = font.render(f"{r_y_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size + box_spacing - text_spacing, box_y + box_size/2 - text_proportion_spacing)))

    text_surface = font.render(str(rh), False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size*1.5 + box_spacing, box_y + box_size + text_spacing + text_proportion_spacing)))

    text_surface = font.render(f"{r_x_proportion:.2f}", False, box_color)
    screen.blit(text_surface, text_surface.get_rect(center=(box_x + box_size*1.5 + box_spacing, box_y + box_size + text_spacing - text_proportion_spacing)))

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
    pygame.draw.rect(screen, box_color, (box_x + box_size + box_spacing, box_y, box_size, box_size), width=box_thickness) 

    # motor power
    motor_pos_x = motor_x
    for config in ((spinner_power, spinner_motor_label), (left_power, left_motor_label), (right_power, right_motor_label), (calculated_speed, speed_motor_label), (calculated_turn_speed, angle_motor_label)):
        power, name = config

        pygame.draw.line(screen, box_color, (motor_pos_x, motor_y), (motor_pos_x, motor_y + motor_bar_height), width=motor_width)

        screen.blit(name, name.get_rect(center=(motor_pos_x, motor_y - text_spacing)))

        text_surface = font.render(f"{int(power * 100)}%", False, box_color)
        screen.blit(text_surface, text_surface.get_rect(center=(motor_pos_x, motor_y + motor_bar_height + text_spacing)))

        level_x = motor_pos_x - (level_length)/2
        level_y = motor_y + (motor_bar_height / 2) * (1-power)

        pygame.draw.line(screen, level_color, (level_x, level_y), (level_x + level_length, level_y), width=level_height)

        motor_pos_x += motor_spacing    
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_port()
            running = False

    pygame.display.flip()
    
