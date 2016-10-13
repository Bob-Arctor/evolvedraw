from PIL import Image, ImageDraw 
import evolver, math, sys, time, os, numpy as np

w = 100
h = 100
opacity = 200

controls = [[0,w],[0,h],[0,w/6],[0,h/6],[0,255],[0,255],[0,255]]
population = 40
parents = 20
mrate = 0.05
figures = 300
generations = 10

# moments = photos.get_albums()
# asset = photos.pick_asset(moments[4], title='Pick your image', multi=False)
# img = asset.get_image()
img = Image.open(sys.argv[1])
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
    img = img.resize((width, height),Image.LANCZOS)
img.show()
# convert to floats for fitness calculations
imarray = np.asfarray(img)

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
    # convert to float
    paintarr = np.asfarray(painting)
    # error = distance between pixels
    err = (imarray - paintarr)**2
    # sum 3 coords
    err = np.array([ [sum(y) for y in x] for x  in err])
    err = np.sqrt(err)/(imarray.shape[0]*imarray.shape[1])
    # total
    err = sum(sum(err))
    return err
    """
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = img.getpixel((i, j))    
            rp, gp, bp = painting.getpixel((i,j))
            err = err + math.sqrt( (r-rp)**2 + (g-gp)**2 + (b-bp)**2 )
    """

def makepic(dude, showimage = False, filename = None):
    drawer = ImageDraw.Draw(painting, 'RGBA')
    drawer.rectangle([0,0,w,h],(255,255,255))
    for f in dude:
        drawer.ellipse([f[0],f[1],f[0]+f[2],f[1]+f[3]],(int(f[4]), int(f[5]), int(f[6]), opacity))
    if showimage is True:
        painting.show()
    if filename is not None:
        painting.save(filename)
    
        
ev = evolver.Evolver(population, parents, mrate, controls, figures)

print('-'*50)
print('starting evolution image matching for %s'%sys.argv[1])
print('total generations planned: %d'%generations)

# create logfile
now = time.strftime("%c")
newpath = r'Log %s'%now 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    
filename = os.path.join(newpath,"evolution log %s"%now)
logfile = open(filename, 'w+')

# name for temp image file
tmp = os.path.join(newpath,"result_tmp.jpg")

for i in range(generations):
    ev.evolve(fitfunc)
    print('generation %d error:  %3.2f%% (%.2f)'%(i, ev.errors[-1][0],ev.errors[-1][1]))
    logfile.write('%s : generation %d error:  %3.2f%% (%.2f)\n'%(now,i,ev.errors[-1][0],ev.errors[-1][1]))
    # save temporary best fit file
    makepic(ev.fittest_curgen[0], False, tmp)

logfile.close()

filename = os.path.join(newpath,"result.jpg")    
makepic(ev.fittest[0], True, filename)
print('result file was saved to %s'%filename)


    
        
                                        

