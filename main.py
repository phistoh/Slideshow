import random
import os
import pyglet
import time

# ============== CONFIG ==============
CYCLE_IMAGE_INTERVALL = 5.0
UPDATE_FILELIST_INTERVALL = 3600.0

# ============== FUNCTIONS ==============

# updates the time label to the current localtime
def update_time(dt):
	time_label.text = time.strftime("%H:%M")
	
# generates a list containing all filenames (strings) in ./img/
def get_filelist():
	img_path = os.path.join(os.path.dirname(__file__), "img/")
	filelist = os.listdir(img_path)
	return filelist

# cycles through a list (of filenames) and displays the next one
# if next is set to False, it'll show the previous image, else it'll show the next image
def cycle_image(next=True):
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

# checks if the slideshow is paused and if not calls cycle_image() to show a new image
def next_image(dt, next=True):
	global pause
	if not pause:
		cycle_image(next)
	
# updates and randomizes the list
def update_filelist(dt):
	global filelist
	filelist = get_filelist()
	random.shuffle(filelist)
	
# scales the image to cover the whole window
def get_scale(window, image):
	scale = max(float(window.width) / image.width, float(window.height) / image.height)
	return scale
	
	
# ============== GLOBVARS ==============
i = 0
filelist = get_filelist()
pause = False
	
# ============== MAIN ==============
# window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(1024, 600)
window.set_caption('Slideshow')
icon_16 = pyglet.image.load('icon_16.png')
icon_32 = pyglet.image.load('icon_32.png')
window.set_icon(icon_16,icon_32)

@window.event
def on_draw():
	sprite.draw()
	time_label.draw()

# left and right button to show the next and previous image; middle mouse button to pause/resume the slideshow	
@window.event
def on_mouse_release(x, y, button, modifiers):
	global pause
	if button == pyglet.window.mouse.LEFT:
	elif button == pyglet.window.mouse.RIGHT:
	elif button == pyglet.window.mouse.MIDDLE:
		pause = not pause
		
		
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
	
	time_label = pyglet.text.Label(time.strftime("%H:%M"), font_name='Segoe UI', font_size=48, x=window.width*0.98, y=window.height*0.03, anchor_x='right', anchor_y='baseline')
	
	# cycle the images and update the list of files periodically
	main_clock.schedule_interval(next_image, CYCLE_IMAGE_INTERVALL, True)
	main_clock.schedule_interval(update_filelist, UPDATE_FILELIST_INTERVALL)
	main_clock.schedule_interval(update_time, 30.0)
	
	pyglet.app.run()