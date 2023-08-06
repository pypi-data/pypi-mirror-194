# FEBID
Simulation of the FEBID process written in Python.  
FEBID stands for Focused Electron Beam Induced Deposition, which is a variation of a CVD (chemical vapor deposition) process.
It uses volative organo-metallic molecules (precursor) as material and a controlled electron beam (typically in a SEM)
to selectively deposit material on a substrate.  

The simulation is build based on a continuum model.
Features:
1. Enabled diffusion, FTCS approach
2. Electron-matter interaction is implemented via a Monte Carlo simulaton submodule
3. No gas dynamics implications
4. Process can be observed live while simulation is running
5. 3D models produced by the simulation can be viewed with the shipped scripts

## Installation

1. Clone the repository and choose virtual environment.
2. In the virtual environment execute `pip install .` to install the package and it's dependencies.

Alternatively, it can be installed as a package via pip if an access token is avalable:  
`pip install git+https://{token}@github.com/MrCheatak/FEBID_py.git#febid`

**Note**: Cython modules utilize OpenMP for parallel computations. You may need to install it in order to run the simulation.

On Mac OSX it can be installed together with *LLVM/clang* using *brew*:
	
In Terminal: `brew install llvm`

On Linux/Ubuntu it is available through *apt-get* and is compatible with the standard gcc compiler:

In Terminal: `sudo apt-get install libomp-dev`

On Windows it should be shipped with standard gcc compiler, so no actions are required from the user.

## Usage:

If using an IDE like PyCharm the entry point is the source/start.py file.  
Alternatively, it can be run from the console with `python -m febid` once installed.

1. The simulation setup is done via the control pannel.
2. Define simulation volume by specifying a prepared .vtk file or create an empty volume from parameters
 or automatically, if you intend to print from a stream-file.
3. Create a printing path from a number of simple shapes or load a more complex path from a stream-file.
4. Choose Settings file, that includes surface flux, beam parameters and substrate material.
5. Choose Precursor file, that contains properties of the precursor and its expected deponat.
6. Statistics from the simulation as well as current states of the simulation volume (snapshots) can be saved 
with the desired intervals. The program will create a folder with the specified name and put all the files 
inside
7. The deposition process can be observed visually when Show process is checked.

Control pannel:

* VTK file – allows specifying a VTK-type file (.vtk) that contains a predefined structure to be used in the simulation.
* Parameters – create a fresh simulation volume with specified dimensions and voxel(cell) size with a substrate at the bottom. 
* Auto – to be used only when using a stream-file. The dimensions of the simulation volume will be defined automatically to encapsulate the printing path with a sufficient margin.
* Simple pattern – allows generation of a path with one of the available shapes.
* x, y – parameters of the selected shape. Position for a point, length for a line, edge length for a square and rectangle, radius for a circle. Except for the point, all shapes are placed in the center. Keep in mind, that the printing path should be inside the borders of the simulation volume.
* Dwell time – the shape contour is divided into discrete points, which a beam visits in a sequence. This parameter sets the amount of time the beam sits or dwells at a single position along the path. 
* Pitch – the distance between two consequent positions of the beam along it's path.
* Repeats – the number of times the pattern defined by shape, dwell time and pitch has to be repeated.
* Stream file – allows specifying a special stream-file, that defines a more complex printing path. It represents a sequence of beam positions with dwell times.
* Beam parameters – a YAML (.yml) file with beam parameters to be specified here. A mandatory field.
* Precursor parameters – a YAML (.yml) file with precursor(printing material) and deponat(printed material) properties. A mandatory field.
* Save simulation data – check to regularly save statistical data of the simulation including time passed, simulation intrinsic time passed and number of cells filled. The save interval is specified in the next field.
* Save structure snapshots – check to regularly save the state of the deposition process. The save interval is specified in the next field.

**VTK file option**: read the volume with a structure from a .vtk file. The file can be a regular .vtk file with a structure in it
   or it can be a file produced by the simulation (by checking Save structure snapshots). If a regular .vtk file is specified, it
   has to be a UniformGrid, have a cubic cell (equal spacings) and have a one cell array.

**Graphical**: when 'Show the process' is checked to view the simulation process in real-time, a window with a 3D scene will open. Refresh rate is set to 0.5 s, thus it may slow to interact with. 
The scene is interactive, meaning it can be zoomed by scrolling, rotated  with a mouse, moved around (with Shift pressed) and focused at the cursor by pressing 'f'. 
The coloring and the corresponding scale represents the concentration of the precursor at the surface. Thus, the 3D object displayed is not the solid structure itself, but it's whole surface, that follows the shape of the solid 3D object.
   
**Viewing simulation results**: There are two options to inspect a structure deposited by FEBID. The first one is viewing a specific snapshot with all the corresponding data layers. It can be done via running the source/libraries/vtk_rendering/show_file.py script and specifying a .vtk file. 
The Second option is to view the process based on a series of structure snapshots. It can be done via source/libraries/vtk_rendering/show_animation_new.py script. Unlike viewing a single file, only one data layer can be 'animated'. Surface deposit or precursor density data is currently supported, it can be set up inside the scripts.  
These scripts can also be run from the console:  
`python -m febid show_file`
`python -m show_animation`