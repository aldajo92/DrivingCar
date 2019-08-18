import pygame
import time

pygame.init()

pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
done = False

if __name__ == "__main__":

	while done == False:
		for event in pygame.event.get():  # User did something
			if event.type == pygame.JOYBUTTONDOWN:
				done = True
			elif event.type == pygame.JOYBUTTONUP:
				print("Joystick button released.")

		axes = joystick.get_numaxes()

		for i in range(axes):
			axis = joystick.get_axis(i)
			print("Axis {} value: {:>6.3f}".format(i, axis))
		
		time.sleep(0.01)
