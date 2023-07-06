import numpy as np          #so we can simulate many points in parallel
import tifffile as tf       #so we can save images
from pathlib import Path    #so we can make folders
import math                 #so we can calculate numbers 

################################################################################
#user-defined parameters

theta_d_max = 73.77 #maximum angular range of the lens to simulate (degrees)
wavelength = 509e-9 #wavelength of waves in a vacuum (m)
n_medium = 1.406    #refractive index of medium (dimensionless)
voxel_size = 32e-9  #length of voxel along one dimension (m/px)
n_voxels = 64      #number of pixels along x axis (px)

################################################################################
theta_r_max = np.deg2rad(theta_d_max)   #convert to radians because it's easier
wavelength /= n_medium #scales the vacuum wavelength to the medium
n_waves = 0     #iterative variable to count the number of plane waves added

xx = np.arange(-n_voxels//2, n_voxels-n_voxels//2).reshape(1, 1, n_voxels) #x
yy = np.arange(-n_voxels//2, n_voxels-n_voxels//2).reshape(1, n_voxels, 1) #y
zz = np.arange(-n_voxels//2, n_voxels-n_voxels//2).reshape(n_voxels, 1, 1) #z

def planewave(kx, ky, kz): #returns a plane wave given 3 k-vectors
    return np.exp(1j*(kx*xx + ky*yy + kz*zz))

wave = np.zeros((n_voxels, n_voxels, n_voxels), dtype='complex128')
    #complex matrix to store the sum of all waves

output = Path('output')         #if there isn't already an output folder...
output.mkdir(exist_ok=True)     #...then we need to make an output folder!         

print('This runs forever, so don''t forget to stop!')

print('Simulating PSF from random plane waves...', sep='', end='') #progress bar

while True: #keep adding waves until we tell the code to stop with ctrl+C
    k_xyz = np.random.uniform(-1, 1, 3) #pick random point in a cube of length 2
    if np.linalg.norm(k_xyz) > 1:   #if point is outside sphere of radius 1...
        continue                    #...ignore that point

    k_xyz /= np.linalg.norm(k_xyz)  #move point from inside to on the sphere

    theta_r = np.arccos(k_xyz[2])   #angular distance of point from optical axis
    if theta_r >= theta_r_max:      #if point is beyond angular range of lens...
        continue                    #...ignore that point

    k_xyz *= 2*np.pi/(wavelength/voxel_size)     #wavenumber of the wave (1/px)
    n_waves += 1                    #increment this to count number of added waves
    kx, ky, kz = k_xyz          #split wavenumber into component vectors
    wave += planewave(kx, ky, kz)   #add wave to the running sum

    tf.imwrite(output/'wave_sum.tif',(np.abs(wave)**2).astype('float32'))
        #save PSF intensity to disk
    
    if math.log2(n_waves).is_integer(): #if number waves added is power of 2...
        tf.imwrite(output/('wave_sum_2e' + str(int(math.log2(n_waves))) +
            '.tif'), (np.abs(wave)**2).astype('float32')) #...save that image
                                    
    if (n_waves/100).is_integer():
        print('.', end='', sep='') #print a period every 100 waves added
    
    text_file = open(output/'n_waves.txt', 'w')
    text = text_file.write(str(n_waves)) #write wave sum total to text file
    text_file.close()
