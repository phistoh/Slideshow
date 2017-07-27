import random
import os
import pyglet

# ============== CONFIG ==============
CYCLE_IMAGE_INTERVALL = 15.0
UPDATE_FILELIST_INTERVALL = 3600.0

# ============== FUNCTIONS ==============

# generates a list containing all filenames (strings) in ./img/
def get_filelist():
	img_path = os.path.join(os.path.dirname(__file__), "img/")
	filelist = os.listdir(img_path)
	return filelist

# cycles through a list (of filenames) and displays the next one
# if next is set to False, it'll show the previous image, else it'll show the next image
def cycle_image(dt,next=True):
	global i
	global filelist
	
	# check direction and get the next image
	if next:
		direction = 1
	else:
		direction = -1
	i = (i+direction)%len(filelist)
	current_image_path = 'img/'+filelist[i]
	
	# check if the currently selected file still exists
	# breaks if all files get deleted
	if not os.path.isfile(current_image_path):
		filelist = get_filelist()
		i = 0
		current_image_path = 'img/'+filelist[i]
	
	# update sprite, centered on the window
	current_image = pyglet.image.load(current_image_path)
	current_image.anchor_x = current_image.width//2
	current_image.anchor_y = current_image.height//2
	sprite.image = current_image
	sprite.scale = get_scale(window, current_image)
	sprite.x = window.width//2
	sprite.y = window.height//2
	
	window.clear()
	
# updates and randomizes the list
def update_filelist(dt):
	global filelist
	filelist = get_filelist()
	random.shuffle(filelist)
	
# scales the image to cover the whole window
def get_scale(window, image):
	if window.width > window.height:
		scale = float(window.width) / image.width
	else:
		scale = float(window.height) / image.height
	return scale

# ============== GLOBVARS ==============
i = 0
filelist = get_filelist()
	
# ============== MAIN ==============
# window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(640, 640)
window.set_caption('Slideshow')
icon_16 = pyglet.image.load('icon_16.png')
icon_32 = pyglet.image.load('icon_32.png')
window.set_icon(icon_16,icon_32)

@window.event
def on_draw():
	sprite.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
	if button == pyglet.window.mouse.LEFT:
		cycle_image(0, True)
	elif button == pyglet.window.mouse.RIGHT:
		cycle_image(0, False)
		
		
if __name__ == '__main__':
	current_image_path = 'img/'+filelist[i]
	
	# load the image and set its anchor to its center
	current_image = pyglet.image.load(current_image_path)
	current_image.anchor_x = current_image.width//2
	current_image.anchor_y = current_image.height//2
	
	# create a sprite, scale it and center it on the window
	sprite = pyglet.sprite.Sprite(current_image)
	sprite.scale = get_scale(window, current_image)
	sprite.x = window.width//2
	sprite.y = window.height//2
	
	
	# lower the clocks fps_limit to save resources
	main_clock = pyglet.clock
	main_clock.set_fps_limit(30)
	
	# cycle the images and update the list of files periodically
	main_clock.schedule_interval(cycle_image, CYCLE_IMAGE_INTERVALL, True)
	main_clock.schedule_interval(update_filelist, UPDATE_FILELIST_INTERVALL)
	
	pyglet.app.run()