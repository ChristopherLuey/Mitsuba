Blobby Shape Dataset
Micah K. Johnson
6/20/2011

This package contains scripts and files used to create the synthetic dataset in
the paper "Shape Estimation in Natural Illumination" by Micah K. Johnson and
Edward H. Adelson, CVPR 2011. 

= data =
Normal maps and masks for 10 blobby shapes.

= images =
Rendered images of each shape in ten different lighting environments.

= obj =
These files were rendered to normal maps using "debug" mode in pbrt. 

= pbrt =

Rendering the obj files as normal maps requires several modifications to pbrt
(at least when the dataset was created in 2010). 

First, add the wavefront and debug files into the appropriate directories in the
pbrt-v2 src tree. Then modify api.cpp to call these functions. 

changes to api.cpp
	added include statements for integrators/debug.h and shapes/wavefront.h

	added these lines at the appropriate places:
     else if (name == "wavefront")
         s = CreateWavefrontShape(object2world, world2object, reverseOrientation
                              paramSet);

     else if (name == "debug")
         si = CreateDebugIntegrator(paramSet);

	
Once the modified files are compiled, the pbrt files can be rendered as follows:
for file in *.pbrt; do pbrt $file; done

