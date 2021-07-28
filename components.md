
# openMVG

## Misc

- https://stackoverflow.com/questions/5171502/c-vs-cc-vs-cpp-vs-hpp-vs-h-vs-cxx
- https://stackoverflow.com/questions/152555/h-or-hpp-for-your-class-definitions

## /src/dependencies

- [cereal](https://uscilab.github.io/cereal/assets/doxygen/index.html): is a header-only C++11 serialization library. cereal takes arbitrary data types and reversibly turns them into different representations, such as compact binary encodings, XML, or JSON. cereal was designed to be fast, light-weight, and easy to extend - it has no external dependencies and can be easily bundled with other code or used standalone.
- [glfw](https://www.glfw.org/): an Open Source, multi-platform library for OpenGL, OpenGL ES and Vulkan development on the desktop. It provides a simple API for creating windows, contexts and surfaces, receiving input and events.
openMVG uses the [OSI] and the [CLP] solver in order to solve linear programs [LP].
- [osi](https://openmvg.readthedocs.io/en/latest/dependencies/osi_clp/): Osi (Open Solver Interface) provides an abstract base class to a generic linear programming (LP) solver, along with derived classes for specific solvers. Many applications may be able to use the Osi to insulate themselves from a specific LP solver. (CLP and MOSEK backend are supported in openMVG).
- [clp](https://openmvg.readthedocs.io/en/latest/dependencies/osi_clp/): CLP has been choosen because it is known to support problems of up to 1.5 million constraints. Clp (Coin-or linear programming) is an open-source linear programming solver written in C++.

## /src/nonFree

- [sift/vl](https://www.vlfeat.org/) (should check the C API): The VLFeat C library implements common computer vision algorithms, with a special focus on visual features, as used in state-of-the-art object recognition and image matching applications. VLFeat strives to be clutter-free, simple, portable, and well documented. They implement many feature detectors and descriptors, and many others, especially the handcrafted. 

## /src/openMVG

- ```cameras```: List of usable camera Intrinsics: PINHOLE_CAMERA, PINHOLE_CAMERA_RADIAL1, PINHOLE_CAMERA_RADIAL3, PINHOLE_CAMERA_BROWN, PINHOLE_CAMERA_FISHEYE
  - ```PinholeCamera.hpp```: There is a command about computing depth: compute the depth of the X point. R*X[2]+t[2].
- ```clustering```: K-means
  - ```kmeans_test.cpp```: 
    - initialize clusters/centroids with random points
    - check whether points are labelled to valid cluster ids
  - ```kmeans_trait.hpp```:
    - some math operations
    - vector/matrix info and manipulation, ...
  - ```kmeans.hpp```:
    - Compute minimum distance to any center
    - Compute Nearest center Id of a given point
    - Compute center of mass of a set a points
    - Compute simple kmeans clustering on specified data
- ```color_harmonization```:
  - ```global_quantile_gain_offset_aligment_test.cpp```: Try to solve the color consistency between the two histograms. We are looking for gain and offet parameter for each image {g;o} and the upper bound precision found by Linfinity minimization. OSI_CLP is in this file.
- ```exif```:
  - ```sensor_width_database```:
    - ```sensor_width_camera_database.txt```: store the sensor width information of many types/models of phones and digital cameras (Asus, Benq, Microsoft Lumina, Panasonic)
  - ```exif_IO_EasyExif.cpp```: 
    - Remove all leading and trailing spaces from the input. The result is a trimmed copy of the input
    - Read the file into buffer
    - There are a lot of IO information: Camera make, camera model, software, bits per sample, image width, image height, image description, image orientation, image date/time, Exposure bias, flash used?, metering mode, focal length, GPS lattitude/longitude/altitude.
- ```features```:
  - ```akaze```: implemented by Romuald PERROT, Pierre MOULON
//- [1] "Fast Explicit Diffusion for Accelerated Features in Nonlinear Scale Spaces."
//- Authors: Pablo F. Alcantarilla, Jesús Nuevo and Adrien Bartoli.
//- Date: September 2013.
//- Conference : BMVC.

See more at ```AKAZE.hpp```
  - ```dipole```: implemented by Pierre MOULON
//- [1] "New local descriptor based on dissociated dipoles"
//- Authors: Alexis Joly.
//- Date: December 2007.
//- Conference: CIVR.

See more at ```dipole_descriptor.hpp```
  - ```fast```: implemented by Pierre MOULON
// Bibliography
//
// [1] Machine learning for high-speed corner detection
// Authors: Edward Rosten and Tom Drummond
// Conference: ECCV 2006, European Conference on Computer Vision.

See more at fast_detector.cpp
  - ```liop```: implemented by Pierre MOULON
//-- Bibliography --
//------------------
//- [1] "Local Intensity Order Pattern for Feature Description"
//- Authors: Zhenhua Wang, Bin Fan and Fuchao Wu
//- Date: 2011, ICCV, IEEE International Conference on Computer Vision

See more at liop_descriptor.cpp
  - ```mser```: implemented by Romuald PERROT
//-- Bibliography --
//------------------
//- [1] "Linear Time Maximally Stable Extremal Regions"
//- Authors: David Nistér, Henrik Stewénius
//- Date: 2008.
//- Conference: ECCV.

See more at mser.hpp
  - ```sift```: implemented by Pierre MOULON
[2] "Method and apparatus for identifying scale invariant features in an image."
David G. Lowe
Patent number: 6711293
Filing date: Mar 6, 2000
Issue date: Mar 23, 2004
Application number: 09/519,89

The implementation is based on:
[1] "Anatomy of the SIFT Method."
I. Rey Otero  and  M. Delbracio
Image Processing Online, 2013.
http://www.ipol.im/pub/algo/rd_anatomy_sift/

See more at ```SIFT_Anatomy_Image_Describer.hpp```
  - ```tbmr```: implemented by Pierre MOULON
//-- Bibliography --
//------------------
//- [1] "Tree-Based Morse Regions: A Topological Approach to Local Feature Detection"
//- Authors: Yongchao Xu, Pascal Monasse, Thierry Géraud, Laurent Najman
//- Date: 2014
//- IEEE Transactions on Image Processing, Institute of Electrical and Electronics Engineers (IEEE)

See more at tbmr.hpp

- 