# plane_wave_addition
Python3 code to generate a set of random, focusing, complex plane waves from a restricted set of angles, sum them, and then output their sum intensity in 3D.

NOTE: this code WILL run forever if you let it, generating a more and more accurate PSF with each iteration. It leaves "bread crumbs" in the form of 
sums at each power of 2 number of waves. Remember to stop the code with CTRL+C in IDLE (or whatever other environment you run your python code in).

User-defined parameters:

theda_d_max: the maximum angular range of the focusing device to simulate. If you're a microscopist, you can think of this as the half-angle of your 
collection cone from your objective lens. This value can be derived from the equation NA = n*sin(theta), where NA is the numerical aperture of your
lens, n is the refractive index of the fluid that sits on top of your lens, and theta is the half angle of the lens (in degrees).

wavelength: the wavelength (in a vacuum!) of the waves to simulate (meters). 

n_medium: the refractive index of the medium that your waves will be focusing into (dimensionless).

voxel_size: the length of a voxel along one dimension. Note: he code assumes isotropic (square) voxels. (meters/pixel)

n_voxels: the number of voxels along one axis of the 3D volume to simulate. Note: the code assumes a cubic 3D volume, with all sides having the same number
of pixels. (pixels)

Outputs:

Output folder: titled "output" in the same directory as the python script

n_waves.txt: a text file containing the latest integer number of plane waves that it has summed in wave_sum.tif. This file is updated on each loop.

wave_sum.tif: a 32-bit TIF file containing the latest square of the sum (i.e. intensity) of all complex plane waves generated in the current and all previous
for loops. The TIF has dimensions voxel_size-by-voxel_size-by-voxel_size. The number of waves summed is saved in n_waves.txt

wave_sum_2eN.tif: A series of TIFs, each with the same dimensionality as wave_sum.tif. The number of waves that it has summed is always a power of 2, represented
in the filename.

