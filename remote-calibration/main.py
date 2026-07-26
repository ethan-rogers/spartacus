import pygame


from remote_serial import connect, read_data

background_color = (144, 144, 144)

box_color = (60, 60, 60)
stick_color = (255, 0, 0)



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



while running:
    screen.fill(background_color)

    read_data()

    # left stick
    pygame.draw.rect(screen, box_color, (box_x, box_y, box_size, box_size), width=box_thickness)  

    # right stick
    pygame.draw.rect(screen, box_color, (width - box_x - box_size, box_y, box_size, box_size), width=box_thickness) 
  
    for event in pygame.event.get():     
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    
