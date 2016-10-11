from scene import *
import photos, Image, ImageDraw


#img.show()
w = 500
h = 500
opacity = 125

asset = photos.pick_asset(title='Pick your image', multi=False)
img = asset.get_image()
img = img.convert('RGBA')
#init with empty figures

figures = []

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

figures.append([10,20,100,200,0,50,10])
figures.append([30,15,300,100,70,170,20])
figures.append([40,10,150,250,10,10,160])

# every figure has 4 numeric params, and 3 rgb params 
drawer = ImageDraw.Draw(painting, 'RGBA')
#drawer.rectangle([0,0,self.imgw,self.imgh], (255,255,255,255))
for f in figures:
	drawer.ellipse([f[0],f[1],f[2],f[3]],(f[4], f[5], f[6], opacity))
painting.show()
	
#filename = "my_drawing.jpg"
#self.painting.save(filename)
		
#rgb_im = image1.convert('RGB')
#r, g, b = rgb_im.getpixel((1, 1))	
#print(r, g, b)


	
		
										

