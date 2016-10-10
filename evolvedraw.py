from scene import *
import photos, Image


#img.show()

class MyScene (Scene):
	def __init__(self, img):
		#scene.image can only display RGBA images
		self.img = img.convert('RGBA')
		#init with empty figures
		self.figures = []
		super(MyScene, self).__init__()
		
	def setup(self):
		self.background_color = 'grey'
		#scale photo to fit half the screen
		width = self.img.size[0]
		height = self.img.size[1]
		print(width, height)
		print(self.size.w, self.size.h)
		widthratio = width/(self.size.w/2-10)
		heightratio = height/self.size.h
		if widthratio > heightratio:
			scale = widthratio
		else:
			scale = heightratio
		if scale != 1:
			width = int(width/scale)
			height = int(height/scale)
			print(width, height)
			self.img.resize((width, height))
		# center the image on the left half
		self.imagelocation = [(self.size.w/2-width)/2, (self.size.h-height)/1]
		# load image for display
		self.img = load_pil_image(self.img)
	
	def draw(self):
		image(self.img, *self.imagelocation)
		ellipse(600,200,700,300)
		
asset = photos.pick_asset(title='Pick your image', multi=False)
img = asset.get_image()
run(MyScene(img))


