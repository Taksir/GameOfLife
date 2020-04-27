import numpy as np
import os, shutil
from PIL import Image
import imageio
from time import time
import webbrowser
import sys

class gameOfLife:
    def __init__(self, n, userSeed = -1, imageDimensionX = 300, imageDimensionY = 300):
        if userSeed >= 0:
            np.random.seed(userSeed)
        self.ndim = n # set dimension here
#         self.grid = np.random.randint(0,2, size = (n+2,n+2)) # 2-D grid for simulatiom
        if n > 100:
            self.grid = np.random.choice(2, size=((n+2)*(n+2)), p=[0.98, 0.02]).reshape(n+2, n+2)
        elif n > 20:
            self.grid = np.random.choice(2, size=((n+2)*(n+2)), p=[0.8, 0.2]).reshape(n+2, n+2)
        else:
            self.grid = np.random.choice(2, size=((n+2)*(n+2)), p=[0.75, 0.25]).reshape(n+2, n+2)
        self.grid[0, :] = 0
        self.grid[n+1,:]= 0
        self.grid[:, 0] = 0
        self.grid[:,n+1]= 0
        self.counter = 0 # works as counter for the stored images
        self.imageDimensionX = imageDimensionX # height of stored images
        self.imageDimensionY = imageDimensionY # width of stored images
        
        # PREPARE DIRECTORY 
        self.folder = os.getcwd() + '/temp'
        # Create target Directory if don't exist
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        else:
            for filename in os.listdir(self.folder):
                file_path = os.path.join(self.folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                    
    def takeSnapshot(self, showImage = False):  
        img = Image.fromarray(self.grid * 255, 'L')
        # img = img.resize((self.imageDimensionX, self.imageDimensionY), Image.ANTIALIAS)
        img.save(self.folder + '/' + str(self.counter) + '.png')
        self.counter += 1
        if showImage == True:
            img.show()
            
    def makeGif(self, duration = 0.25):
        image_folder = os.fsencode(self.folder+'/')
        filenames = []
        for file in os.listdir(image_folder):
            filename = os.fsdecode(file)
            if filename.endswith( ('.jpeg', '.png') ):
                filenames.append(filename)
        filenames.sort() # this iteration technique has no built in order, so sort the frames
        images = list(map(lambda filename: imageio.imread(self.folder+'/'+filename), filenames)) 
        imageio.mimsave(os.getcwd() + '/GameOfLife.gif', images, duration = 0.25)

    def printGrid(self):
        temp_grid = np.empty_like(self.grid, dtype=str)
        temp_grid[self.grid == 0] = '-'
        temp_grid[self.grid == 1] = 'X'
        print(temp_grid[1:-1, 1:-1], sep='\n')
        
    def computeNeighbors(self,x,y):
        x += 1
        y += 1
        return np.sum(self.grid[x-1:x+2, y-1:y+2]) - self.grid[x,y]  
    
    def updateToNextGen(self):
        temp_grid = np.zeros_like(self.grid)
        for i in range(0, self.ndim):
            for j in range(0, self.ndim):
                count = self.computeNeighbors(i,j)
                if count == 2 or count == 3:
                    temp_grid[i+1,j+1] = 1
        self.grid = np.copy(temp_grid)
        
    def simulate(self, no_of_iterations, showImage = False, print_grid = False):
        for i in range(no_of_iterations):
            self.takeSnapshot()
            self.updateToNextGen()
            if print_grid == True:
                print("After Generation {}:".format(i+1))
                self.printGrid()
        self.takeSnapshot()   
    
    def viewGif(self):
        webbrowser.open(os.getcwd() + '/GameOfLife.gif')
        
if __name__ == "__main__":
    start = time()
    if len(sys.argv[1:]) > 0:
        dimension = int(sys.argv[1])
        no_of_iterations = int(sys.argv[2])
        duration = float(sys.argv[3])
    else:
        dimension = 100
        no_of_iterations = 20
        duration = 0.5
    if dimension < 3 or no_of_iterations < 1 or duration < 0.1 or duration > 2.0:
         sys.exit('dimension should be atleast 3. No of iterations should be sensible, not idiotic. 0.1 <= duration <= 2.0' ) 
    
    game = gameOfLife(dimension)
    
    print("Initial State of game:")
    game.printGrid()
    game.simulate(no_of_iterations)
    game.makeGif(duration)
    print("It took %.3f secs to do the whole simulation and generate GameOfLife.gif" %(time() - start))
    game.viewGif()
