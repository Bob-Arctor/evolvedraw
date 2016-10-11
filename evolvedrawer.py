from scene import *
import photos, Image, ImageDraw, evolver, math

w = 254
h = 254
opacity = 125

controls = [[0,w],[0,h],[0,w/4],[0,h/4],[0,255],[0,255],[0,255]]
population = 40
parents = 20
mrate = 0.05
figures = 300

moments = photos.get_albums()
asset = photos.pick_asset(moments[4], title='Pick your image', multi=False)
img = asset.get_image()
img = img.convert('RGB')

#scale photo to fit half the screen
width = img.size[0]
height = img.size[1]
widthratio = width/(w)
heightratio = height/h
if widthratio > heightratio:
	scale = widthratio
else:
	scale = heightratio
if scale != 1:
	width = int(width/scale)
	height = int(height/scale)
	img = img.resize((width, height))
img.show()

imgw = img.size[0]
imgh = img.size[1]
painting = Image.new("RGB", (imgw, imgh), 'white')

# fitness function
def fitfunc(dude):
	#will draw all objects and calculate distance for every pixel	
	# every figure has 4 numeric params, and 3 rgb params 
	drawer = ImageDraw.Draw(painting, 'RGBA')
	drawer.rectangle([0,0,w,h],(255,255,255,255))
	for f in dude:
		drawer.ellipse([f[0],f[1],f[0]+f[2],f[1]+f[3]],(int(f[4]), int(f[5]), int(f[6]), opacity))
	# calculate error
	err = 0
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			r, g, b = img.getpixel((i, j))	
			rp, gp, bp = painting.getpixel((i,j))
			err = err + math.sqrt( (r-rp)**2 + (g-gp)**2 + (b-bp)**2 )
	return err
	

def makepic(dude):
	drawer = ImageDraw.Draw(painting, 'RGBA')
	drawer.rectangle([0,0,w,h],(255,255,255))
	for f in dude:
		drawer.ellipse([f[0],f[1],f[0]+f[2],f[1]+f[3]],(int(f[4]), int(f[5]), int(f[6]), opacity))
	painting.show()
	filename = "my_drawing.jpg"
	painting.save(filename)
	
		
ev = evolver.Evolver(population, parents, mrate, controls, figures)
for i in range(10000):
	ev.evolve(fitfunc)
	makepic(ev.fittest[-1])



	
		
										

