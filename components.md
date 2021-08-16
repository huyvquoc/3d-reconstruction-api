
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

  - ```binary_regions.hpp```: definitions of functions for representing binary regions (what is a binary region? Is binary region of an image?)
    - Read from files the regions and their corresponding descriptors.
    - Export in two separate files the regions and their corresponding descriptors.
    - Return the number of defined regions
    - Return the squared Hamming distance between two descriptors
  - ```descriptor.hpp```: definition of a class that handles descriptor (a data container of N values of type T). 
    - For example:
      - * SiftDescriptor => <uchar,128> or <float,128>
      - * Surf 64 => <float,64>
      - * Brief 512 bits => <unsigned char,512/sizeof(unsigned char)>
    - This constructor allows you to construct Descriptor from Eigen expressions.
    - This method allows you to assign Eigen expressions to Descriptor.
    - Read descriptors from file.
    - Write descriptors to file.
    - Read descriptors from file (in binary mode).
    - Write descriptors to file (in binary mode).
  - ```feature.cpp```: main utility functions for processing point features.
    - Return the coterminal angle between [0;2*PI]. Angle value must be in Radian.
    - Read feats from file.
    - Write feats to file.
    - Export point feature based vector to a matrix [(x,y)'T, (x,y)'T].
  - ```image_describer.hpp```: A pure virtual class for image description computation
    - Use a preset to control the number of detected regions.
    - Detect regions on the image and compute their attributes (description).
  - ```regions_factory_io.hpp```: Register region type for serialization
  - ```regions_factory.hpp```:
    - Define the classic SIFT Keypoint.
    - Define the AKAZE Keypoint (with a float descriptor).
    - Define the AKAZE Keypoint (with a LIOP descriptor).
    - Define the AKAZE Keypoint (with a binary descriptor saved in an uchar array).
  - ```regions.cpp```: Init the regions_type from an image describer file (used for regions loading). 
  - ```scalar_regions.hpp```: Specialization of the abstract Regions class to handle Scalar descriptors.
    - Read from files the regions and their corresponding descriptors.
    - Export in two separate files the regions and their corresponding descriptors.
    - Return the number of defined regions.
    - Return the L2 distance between two descriptors.
    - Add the Inth region to another Region container.
  - ```svg_features.cpp```: SVG is a platform for two-dimensional graphics. It has two parts: an XML-based file format and a programming API for graphical applications. Key features include shapes, text and embedded raster graphics, with many different painting styles. It supports scripting through languages such as ECMAScript and has comprehensive support for animation.
    - Draw image.
    - Draw features.
    - Save the SVG file.
    - Display feature circles (blob circles?).
- ```geodesy```
  - ```geodesy.hpp```: namespace containing various classes and functions used to deal with geodesy transformation.
    - Convert WGS84 lon,lat,alt data to ECEF data (Earth Centered Earth Fixed).
    - Convert WGS84 lon,lat,alt data to UTM data (Universal Transverse Mercator).
    - There are some hard-set numbers for longitude and latitude in the file.
    - Convert ECEF (XYZ) to lon,lat,alt values for the WGS84 ellipsoid.
- ```geometry```
  - ```box.cpp```: 
    - Distance from center to corner (like sphere radius).
    - Top face.
    - Bottom face.
    - Defines the supporting volume thanks to 6 half_planes.
    - Define remaining supporting planes (box borders).
    - Export box points.
  - ```box.hpp```: Namespace holding various classes and methods for geometry manipulation.
    - Define a Bounding box using 6 Half Spaces. This structure is used for testing box-HalfPlaneObject intersection.
    - Points that define the bounding box.
    - Define a Square bounding box from a center position and radius (center to corner distance).
    - Define a Rectangular parallelepiped bounding box from min/max axis aligned positions.
    - Export the Box as a PLY file.
  - ```convex_hull_test.cpp```:
    - Test corner case (an empty point cloud).
    - Test corner case (point cloud with one point).
    - Test convex hull of random points
      - a. Generate some random point in a given area
      - b. Compute its convex hull
      - c. Check that all the points are inside the defined convex hull
  - ```convex_hull.cpp```:
    - Compute the 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
      - A. sort the point in lexicographic ordering (use x and then y).
      - B. Build lower hull.
      - C. Build upper hull.
  - ```convex_hull.hpp```:
    - Define an alias in order to represent a Polygon as an array of 2d floating point coordinates. Polygon must be defined as CounterClockWise polygon. In order to check if your polygon is CounterClockWise you can use the Area Function.
      - A positive area means CounterClockWise polygon.
      - A negative area means a Clockwise polygon.
    - Test if a point is inside a convex polygon.
    - Compute the area of a convex polygon using the 'determinant method' http://www.mathwords.com/a/area_convex_polygon.htm
    - Compute the convex hull of a set of 2D points.
      - Note: the last point in the returned list is the same as the first one.
      - Implements Andrew's monotone chain algorithm. O(n log n) complexity.
      - https://en.wikibooks.org/wiki/Algorithm_Implementation/Geometry/Convex_hull/Monotone_chain
  - ```frustum_box_intersection_test.cpp```: Box/Camera frustum intersection unit test
    - Test with a point that is inside the defined volume.
    - Test with a point that is outside the defined volume.
    - Test with a set of intersecting boxes.
    - Test with a set of non-intersecting boxes.
    - Test with infinite Frustum for each camera.
    - Test with truncated frustum.
  - ```frustum_intersection_test.cpp```: Camera frustum intersection unit test
    - Test with infinite Frustum for each camera.
    - Test with truncated frustum.
    - Create infinite frustum that do not share any space
      - 4 cameras on a circle that look to the same direction
      - Apply a 180° rotation to the rotation matrix in order to make the cameras don't share any visual hull
    - Build frustum with near and far plane defined by min/max depth per camera
    - Test if the frustum have an overlap
  - ```frustum.cpp```:
    - Definition of the frustum with the supporting points.
    - Definition of the supporting planes.
    - supporting point for drawing is a normalized cone, since infinity cannot be represented.
    - update near & far planes & clear set points.
    - Add Znear and ZFar half plane using the cam looking direction.
    - supporting point are the points defined by the truncated cone.
    - export to ply file.
      - Vertex count evaluation.
      - Faces count evaluation.
      - Export frustums points. 
      - Export frustums faces.
  - ```frustum.hpp```: Namespace holding various classes and methods for geometry manipulation.
    - Define a camera Frustum:
      - infinite Frustum (4 Half Spaces) (a pyramid)
      - truncated Frustum (6 Half Spaces) (a truncated pyramid)
      - This structure is used for testing frustum intersection (see if two cam can share visual content)
    - HalfPlaneObject
      - Camera centre and the 4 points that define the image plane.
      - Near clip plane distance.
      - Far clip plane distance.
      - Support points.
      - Build a frustum from the image size, camera intrinsic and pose.
      - Build a frustum from image size, camera intrinsics, pose and clip planes.
      - Tells if the Frustum is an infinite one.
      - Tells if the Frustum is truncated.
      - Return the supporting frustum points.
      - Export the Frustum as a PLY file (infinite frustum as exported as a normalized cone).
  - ```half_space_intersection.cpp```:
    - Check if it exists a point on all positive side of the half plane thanks to a Linear Program formulation [1]. => If a point exists: there is a common subspace defined and so intersections. The LP formulation consists in set the Half_plane as constraint and check if a point can fit the equations.
    - Solve in order to see if a point exists within the half spaces positive side?.
    - Concatenate the Half Planes and see if an intersection exists.
    - Compute the total number of half-planes.
  - ```half_space_intersection.hpp```:
    - Define the Half_plane equation (abcd coefficients).
    - Define a collection of Half_plane.
    - Define a plane passing through the points (p, q, r).
    - Test if half-planes defines a non empty volume.
    - Define a Volume 'object' thanks to a series of half_plane: This structure is used for testing generic HalfPlaneObject/HalfPlaneObject intersection.
    - Test if two defined 'volume' intersects.
    - Test if a point is on the positive side of the HalfPlanes.
    - Test if multiple defined 'volume' intersect
  - ```plane_estimation_kernel.hpp```: 
    - Compute a Half_plane equation from 3 points.
    - Compute a Half_plane equation from 3 points and store its centroid.
    - Compute the absolute distance of the point to the plane.
    - Compute an angular error (radians) between the direction of the point and the plane normal. The metric is biased by the distance: 
      - This cost function will prefer plane with large region support.
    - Define a kernel to be able to perform robust estimation of Half_plane. 
      - Use a half_plane Solver and a point to plane distance cost function.
      - Use a half_plane and centroid Solver and a point to plane angular cost function.
  - ```pose3.hpp```: Defines a pose in 3d space [R|C] t = -RC
    - Orientation matrix.
    - Center of rotation.
    - Get Rotation matrix.
    - Get center of rotation.
    - Get translation vector.
    - Apply pose.
    - Composition of poses.
    - Get inverse of the pose.
    - Return the pose as a single Mat34 matrix [R|t].
  - ```rigid_transformation3D_srt.cpp```:
    - Get the transformation via Umeyama's least squares algorithm. This returns a matrix of the form: [ s * R t] [ 0 1] from which we can extract the scale, rotation, and translation.
    - Extract transformation parameters.
    - convert x to rotation matrix and a translation vector and a Scale factor x = {tx,ty,tz,anglex,angley,anglez,S}.
    - Build the rotation matrix.
    - Evaluate re-projection errors.
    - convert x to rotation matrix x = {anglex,angley,anglez}.
    - Refine rotation.
  - ```rigid_transformation3D_srt.cpp```:
    - 3D rigid transformation estimation (7 dof) Compute a Scale Rotation and Translation rigid transformation. This transformation provide a distortion-free transformation using the following formulation Xb = S * R * Xa + t. "Least-squares estimation of transformation parameters between two point patterns", Shinji Umeyama, PAMI 1991, DOI: 10.1109/34.88573
    - Eigen Levemberg-Marquardt functor to refine translation, Rotation and Scale parameter.
    - Computes error given a sample.
    - Eigen LM functor to refine Rotation.
    - 3D rigid transformation refinement using LM. Refine the Scale, Rotation and translation rigid transformation using a Levenberg-Marquardt opimization.
  - ```Similarity3_Kernel.hpp```:
    - Computes the 3D similarity transform between two point cloud.
    - Return the Squared error between a collection of points (stored as column).
    - Return the Squared error between the point x2 and the transformed point S(x1).
    - Define a Kernel to solve a robust 3D similarity between point cloud.
  - ```Similarity3.hpp```:
    - Define a 3D Similarity transform encoded as a 3D pose plus a scale.
    - This define identity transformation centered at origin of a cartesian frame.
    - Apply transformation to a point.
    - Concatenation of pose.
    - Get inverse of the similarity.
- ```graph```
  - ```connectedComponent.hpp```:
    - Export node of each CC (Connected Component) in a map.
    - Computes nodeIds that belongs to the largest bi-edge connected component.
    - Create a graph from pairwise correspondences:
      - remove not biedge connected component,
      - keep the largest connected component.
    - Graph is bi-edge connected, but still many connected components can exist. Keep only the nodes belonging to the largest Bi-edge component.
    - Keep only the largest connected component
      - list all CC size
      - export node that belong to the largest CC
    - Computes nodeIds that belongs to the largest connected component.
    - Establish nodes connections (by using Union Find) on edges.
    - List the number of parent_id (the number of CCs).
  - ```graph_builder.hpp```:
    - Structure used to keep information of an image graph: Build a graph (add nodes and connection between nodes).
    - Build a graph from a list of pair.
      - A-- Compute the number of node we need.
      - B-- Create a node graph for each element of the set.
      - C-- Add weighted edges from the pairs object.
    - Create a graph from node index and pairs (edges).
      - A-- Create a node graph for each element of the set.
      - B-- Add weighted edges from the pairs object.
  - ```graph_graphviz_export.hpp```:
    - Export an Image connection graph to graphviz file format. Example :
    graph 1 {
    node [shape=circle]
    n1 --  n0
    n2 --  n0
    n2 --  n1
    }
    - Export a graph and generate it using graphviz.
    - Export the graph as a DOT (graph description language) file.
  - ```graph_stats.hpp```:
    - Export graph statistics to the console:
      - number of node
      - number of cc
      - node degree statistics (min, max, mean, median)
  - ```graph.hpp```:
    - namespace handling various methods and classes related to graph manipulation. 
  - ```triplet_finder.hpp```:
    - Simple container for a tuple of three value.
    - Indicate if an edge contains one of the element of the triplet.
    - Indicate if triplet are the same.
    - Indicate if triplet are differents.
    - Stream operation.
    - Return triplets contained in the graph build from IterablePairs.
- ```graphics```
  - ```color_gradient.hpp```:
    - Port made from http://www.andrewnoske.com/wiki/Code_-_heatmaps_and_color_gradients
      - Use c++11 style
      - Add multiple possible color gradient initialization

    - How to use the code:
      - 1. Create the object and configure the color gradient

      Color_Gradient heatMapGradient(Color_Gradient::k2BlueRedHeatMap());
      // Re-Initialize to use a gradient based on 5 colors
      //heatMapGradient = Color_Gradient(Color_Gradient::k5ColorHeatMap());

      - 2. Get the color corresponding to the % range you want

      float r,g,b;
      const float interpolated_ratio = .5f;
      heatMapGradient.getColor(interpolated_ratio, r, g, b);
      // [r,g,b] are in the range [0, 1]
- ```image```
  - ```image_concat.hpp```:
    - Horizontal concatenation of images.
    - Vertical concatenation of images.
  - ```image_container.hpp```:
    - Generic image class, Image data are stored by inheritance of an Eigen matrix.
    - Class ```Image```.
    - Full constructor.
    - Copy constructor.
    - Move constructor. 
    - Assignment operator.
    - Change geometry of image.
    - Retrieve the width of the image.
    - Retrieve the height of the image.
    - Return the depth in byte of the pixel.
    - constant random pixel access.
    - Get low level access to the internal pixel data.
    - Tell if a point is inside the image.
    - Pixelwise addition of two images.
    - Pixelwise subtraction of two images.
  - ```image_converter.hpp```:
    - Convert from one color type to another one.
    - Convert RGBColor to unsigned char color.
    - Convert RGBAColor to unsigned char color.
    - Convert RGBAColor to RGBColor.
    - Convert image from one internal pixel type to another one.
    - Convert RGB color stored as an int to RGB color stored as a float.
    - Convert float RGB color to Int RGB color.
    - Convert RGB image stored as float components to RGB image stored as int components.
  - ```image_convolution_base.hpp```:
    - Filter an extended row [halfKernelSize][row][halfKernelSize].
  - ```image_convolution.hpp```:
    - Standard 2D image convolution functions :
      - vertical
      - horizontal
      - 2D (using standard 2d kernel of with separable kernels)
    - General image convolution by a kernel, assume kernel has odd size in both dimensions and (border pixel are copied).
    - Horizontal (1d) convolution.
    - Vertical (1d) convolution.
    - Separable 2D convolution.
    - Specialization for Image<float> in order to use SeparableConvolution2d.
  - ```image_diffusion.hpp```:
    - Compute Perona and Malik G2 diffusion coefficient.
    - Apply Fast Explicit Diffusion to an Image (on central part).
    - Apply Fast Explicit Diffusion of an Image.
    - Compute Fast Explicit Diffusion cycle.
    - Compute if a number is prime of not.
    - Get the next prime number greater or equal to input.
    - Compute FED cycle timings using total time.
  - ```image_drawing.hpp```:
    - Put the pixel in the image to the given color only if the point (xc,yc) is inside the image. /!\ Be careful at the order (Y,X).
    - Bresenham approach to draw ellipse. 
      - @ref http://raphaello.univ-fcomte.fr/ig/algorithme/ExemplesGLUt/BresenhamEllipse.htm 
      - Add the rotation of the ellipse.
      - As the algo. use symmetry we must use 4 rotations.
    - Bresenham approach do not allow to draw concentric circle without holes.
      - So it's better the use the Andres method.
      - @ref http://fr.wikipedia.org/wiki/Algorithme_de_tracé_de_cercle_d'Andres.
    - Bresenham algorithm used to draw a line.
    - Draw filled circle. Exterior point computed with bresenham approach.
    - Draw a serie of circles along the line, the algorithm is slow but accurate.
  - ```image_filtering.hpp```:
    - standard image filtering functions: 
      - X,Y derivatives using : Central difference, Sobel filter, Scharr filter, Gaussian blur.
        //-- Bibliography --
        //------------------
        //- [1] "A Scheme for Coherence-Enhancing Diffusion Filtering with Optimized Rotation Invariance."
        //- Authors: Joachim Weickert and Hanno Scharr.
        //- Date: September 2002.
        //- Journal : Journal of Visual Communication and Image Representation.
    - Compute X-derivative using central difference.
    - Compute Y-derivative using central difference.
    - Compute X-derivative using 3x3 Sobel kernel.
    - Compute Y-derivative using 3x3 Sobel kernel.
    - Compute X-derivative using 3x3 Scharr kernel.
    - Compute Y-derivative using 3x3 Scharr filter.
    - Compute X-derivative using scaled Scharr filter.
    - Compute Y-derivative using scaled Scharr filter
    - Compute (isotropic) gaussian filtering of an image using filter width of k * sigma.
    - Compute 1D gaussian kernel of specified width.
    - Compute gaussian filtering of an image using user defined filter widths.
  - ```image_integral.hpp```:
    - Create a summed area table:
      -  http://en.wikipedia.org/wiki/Summed_Area_Table
      - "Summed-area tables for texture mapping". SIGGRAPH84. Crow, Franklin.
    - Compute the sum of the pixels in a rectangular region:
      -  http://en.wikipedia.org/wiki/Summed_Area_Table
      - "Summed-area tables for texture mapping". SIGGRAPH84. Crow, Franklin.
  - ```image_io.hpp```:
    - Format List of input format handled by IO operations.
    - Get format of an image.
    - Load an image<T> from the provided input filename.
    - Save an image<T> from the provided input filename.
    - Unsigned char specialization (The memory pointer must be null as input).
    - Write Image, Read Image.
    - Read PNG file from file.
    - Read PNG file from a stream.
    - Write PNG file to a file.
    - Write PNG file to a stream.
    - Read JPEG image from file.
    - Read JPEG image from stream.
    - Write JPEG file.
    - Read PNM/PGM file.
    - Read PNM/PGM from a stream.
    - Write PNM/PGM from to a file.
    - Write PNM/PGM to a stream.
    - Read TIFF image from a file.
    - write TIFF image to a file.
    - structure used to know the size of an image.
    - Read image header from a file.
    - Read PNG image header from a file.
    - Read JPEG image header from a file.
    - Read PNM/PGM image header from a file.
    - Read TIFF image header from a file.
    - Generic Image read from file.
    - Generic Image read from file (overload for RGBColor).
    - Generic Image read from file (overload for RGBAColor).
    - Write image to disk, support only unsigned char based type (gray, rgb, rgba).
  - ```image_resampling.hpp```
    - Half sample an image (ie reduce its size by a factor 2) using bilinear interpolation.
    - Image decimation (get only one pixel over two - no interpolation).
    - Image Upsample (by a factor of 2 by using linear interpolation).
    - Ressample an image using given sampling positions
  - ```image_warping.hpp```
    - Apply inplace homography transform for the given point (x,y).
    - Warp an image im given a homography H with a backward approach.
  - ```pixel_types.hpp```
    - Red Greeen Blue template pixel type.  
      - Full constructor.
      - Copy constructor.
      - Single value construction.
    - Get readonly Red channel value
    - Get rw Red channel value.
    - Get readonly Green channel value.
    - Get rw Green channel value.
    - Get approximate Gray value using rec601 Luma conversion.
    - scalar division.
    - scalar multiplication.
    - stream operator.
    - RGBA templated pixel type.
    - RGB constructor with default alpha value
    - Get readonly Red channel value.
  - ```sample.hpp```
    - Sampling functors
      ** These functors computes weight associated to each pixels

        For a (relative) sampling position x (\in [0,1]) between two (consecutives) points :

          A  .... x ......... B

        w[0] is the weight associated to A
        w[1] is the weight associated to B

        Note: The following functors generalize the sampling to more than two neighbors
        ** They all contains the neighbor_width variable that specify the number of neighbors used for sampling
    - Nearest sampling (ie: find the nearest pixel to a specified position).
      - Computes weight associated to neighboring pixels.
    - Linear sampling (ie: linear interpolation between two pixels)
      - Computes weight associated to neighboring pixels.
    - Cubic interpolation between 4 pixels.
      - Interpolation weight is for A,B,C and D pixels given a x position as illustrated as follow :
          A      B    x C      D
          @ref : Cubic Convolution Interpolation for Digital Image Processing , R. Keys, eq(4)
      - Computes weight associated to neighboring pixels.
    - Sampler spline16 -> Interpolation on 4 points used for 2d ressampling (16 = 4x4 sampling)
        Cubic interpolation with 0-derivative at edges (ie at A and D points)
        See Helmut Dersch for more details
      
        Some refs :
        -   http://forum.doom9.org/archive/index.php/t-147117.html
        -   http://avisynth.nl/index.php/Resampling
        -   http://www.ipol.im/pub/art/2011/g_lmii/
    - Sampler spline 36. Same as spline 16 but on 6 neighbors (used for 6x6 frame).
    - Sampler spline 64.

- ```linearProgramming```
  - ```linfinityCV```
- ```matching```
- ```matching_image_collection```
- ```multiview```
- ```numeric```
- ```robust_estimation```
- ```sfm```
- ```spherical```
- ```stl```
- ```system```
- ```tracks```

## 6 main steps of Structure from Motion in ```SfM_GlobalPipeline.py```

### 1. Intrinsics analysis

- Bin file: ```openMVG_main_SfMInit_ImageListing```

### 2. Compute features

- Bin file: ```openMVG_main_ComputeFeatures```

### 3. Compute matches

- Bin file: ```openMVG_main_ComputeMatches```

### 4. Do global reconstruction

- Bin file: ```openMVG_main_GlobalSfM```

### 5. Colorize structure

- Bin file: ```openMVG_main_ComputeSfM_DataColor```

### 6. Structure from known poses (robust triangulation):

- Bin file: ```openMVG_main_ComputeStructureFromKnownPoses```

Optional. Compute final valid structure from the know camera poses.

### 7. Compute sfm data color

- Bin file: ```openMVG_main_ComputeSfM_DataColor```

Optional. Compute again step 5.

## /src/software/SfM/

- ```clustering```

- ```export```

- ```import```
  - Step 1: ```main_SfMInit_ImageListingFromKnownPoses.cpp```
    - Copyright: Yan Qingsong, Pierre Moulon
    - Objective:
      // Create the description of an input image dataset for OpenMVG toolsuite
      // - Export a SfM_Data file with View & Intrinsic data
    - Commandline arguments: imageDirectory, groundTruthDirectory, groundTruthDataset, outputDirectory
    - Important variables: ```sfm_data_gt```
    - Has ```cout``` to print arguments'values
    - // Configure an empty scene with Views and their corresponding cameras and assign it into ```sfm_data_gt```
    - // Load the gt (groundtruth?) data
    - // Store SfM_Data views & intrinsic data into a file named ```sfm_data.json```
    - Has ```cout``` to print usable #File(s), usable #Pose(s), usable #Intrinsic(s) listed in sfm_data

- Step 2: ```main_ComputeFeatures.cpp```
  - Copyright: Pierre Moulon
  - Objective:
    /// - Compute view image description (feature & descriptor extraction)
    /// - Export computed data
  - Commandline arguments: 
    - Required: input_file (a SfM_Data file), outdir 
    - Optional: describerMethod (method used to describe an image), upright (use Upright feature 0 or 1), 
                force (force to recompute data), describerPreset (used to control the Image_describer configuration ("NORMAL", "HIGH" or "ULTRA")), 
                numThreads (number of parallel computations)
  - Important variables: ```image_describer```, ```sfm_data```, ```mask```, ```regions```
  - Has ```stringToEnum``` to convert feature level "NORMAL", "HIGH", "ULTRA" to a specific number.
  - Has ```cout``` to print arguments'values
  - // a. Load input scene: Load VIEWS/INTRICSICS from ```sfm_data.json``` (output of Step 1)
  - // b. Init the image_describer
    // - retrieve the used one in case of pre-computed features
    // - else create the desired one
    - // Dynamically load the image_describer from the file (will restore old used settings)
    - // Create the desired Image_describer method. // Don't use a factory, perform direct allocation
    - // Export the used Image_describer and region type for: // - dynamic future regions computation and/or loading
  - // Feature extraction routines
    // For each View of the SfM_Data container:
    // - if regions file exists continue,
    // - if no file, compute features
      - // Use a boolean to track if we must stop feature extraction
      - // If features or descriptors file are missing, compute them
      - // Look if there is occlusion feature mask
      - // Try to read the local mask
      - // Use the local mask only if it fits the current image size
      - // Try to read the global mask
      - // Use the global mask only if it fits the current image size
      - // Compute features (feat) and descriptors (desc) and export them to files ```frame0.feat```, ```frame0.desc```, ```frame1.feat```, ```frame1.desc```, ...
      - Has ```cout``` to print execution time "Task done in (s): "


- Step 3: ```main_ComputeMatches.cpp```
  - Copyright: Pierre Moulon
  - Objective:
    /// Compute corresponding features between a series of views:
    /// - Load view images description (regions: features & descriptors)
    /// - Compute putative local feature matches (descriptors matching)
    /// - Compute geometric coherent feature matches (robust model estimation from putative matches)
    /// - Export computed data
  - Commandline arguments:
    - Required: input_file (a SfM_Data file), out_dir (output path where computed are stored)
    - Optional: 
      - ratio (distance ratio to discard non meaningful matches), 
      - geometric_model(pairwise correspondences filtering thanks to robust model estimation),
        - << "   f: (default) fundamental matrix,\n"
        - << "   e: essential matrix,\n"
        - << "   h: homography matrix.\n"
        - << "   a: essential matrix with an angular parametrization,\n"
        - << "   o: orthographic essential matrix.\n"
        - << "   u: upright essential matrix.\n"
      - video_mode_matching (sequence matching with an overlap of X images),
      - pair_list (file), 
      - nearest_matching_method, 
      - force (force to recompute data),
      - guided_matching (use the found model to improve the pairwise correspondences), max_iteration, 
      - cache_size,
        - << "  Use a regions cache (only cache_size regions will be stored in memory)\n"
        - << "  If not used, all regions will be load in memory."
  - Important variables:
    - ```eGeometricModelToCompute``` (fundamental matrix, essential matrix, or homography matrix, ...)
    - ```sGeometricMatchesFilename``` (matches.f.bin, matches.e.bin, matches.h.bin, matches.o.bin)
    - ```collectionMatcher``` (matcher method)
  - Has ```cout``` to print arguments'values
  - // - Load SfM_Data Views & intrinsics data
    - // a. Compute putative descriptor matches
    - // b. Geometric filtering of putative matches
    - // + Export some statistics
  - // Read SfM Scene (image view & intrinsics data)
  - Load SfM Scene regions
    - Init the regions_type from the image describer file (used for image regions extraction)
    - // a. Compute putative descriptor matches
    - //    - Descriptor matching (according user method choice)
    - //    - Keep correspondences only if NearestNeighbor ratio is ok
      - // Load the corresponding view regions
      - // Show the progress on the command line
      - // Build some alias from SfM_Data Views data: // - List views as a vector of filenames & image sizes
      - // If the matches already exists, reload them (```matches.putative.txt```, ```matches.putative.bin```)
      - else // Compute the putative matches
      - // Allocate the right Matcher according the Matching requested method
      - // Perform matching. 
        - // From matching mode compute the pair list that have to be matched.
        - // Photometric matching of putative pairs
        - //-- Export putative matches into ```matches.putative.bin```
      - //-- export putative matches Adjacency matrix into ```PutativeAdjacencyMatrix.svg```
      - //-- export view pair graph once putative graph matches have been computed into ```putative_matches``` (GraphvizData)
    - // b. Geometric filtering of putative matches
    -  //    - AContrario Estimation of the desired geometric model
    -  //    - Use an upper bound for the a contrario estimated threshold
      - Switch cases for many different types of matrix: homography, fundamental, essential, ...
  - //-- Export geometric filtered matches
    - // -- export Geometric View Graph statistics
    - //-- export Adjacency matrix into ```GeometricAdjacencyMatrix.svg```.
    - //-- export view pair graph once geometric filter have been done into ```geometric_matches``` (GraphvizData)

- Step 4: ```main_GlobalSfM.cpp```
  - Copyright: Pierre Moulon
  - Objective: Global Structure from Motion
    - "Open Source implementation of the paper: Global Fusion of Relative Motions for Robust, Accurate and Scalable Structure from Motion."
    - "Pierre Moulon, Pascal Monasse and Renaud Marlet."
    - "ICCV 2013."
  - Commandline arguments:
    - input_file (path to a SfM_Data scene)
    - matchdir (path to the matches that corresponds to the provided SfM_Data scene)
    - match_file (path to the match file to use)
    - outdir (path where the output data will be stored)
    - rotationAveraging (L1 minimization or L2 minimization)
    - translationAveraging (L1 minimization, L2 minimization of sum of squared Chordal distance, SoftL1 minimization)
    - refineIntrinsics (Intrinsic parameters refinement option)
    - prior_usage (Enable usage of motion priors (i.e GPS positions))
  - Important variables: ```sfm_data```, ```sImage_describer```, ```regions_type```,```feats_provider```,```matches_provider```,```sfmEngine```
  - Bundle Adjusment Intrinsic parameter refinement option
  - // Load input SfM_Data scene
  - // Init the regions_type from the image describer file (used for image regions extraction)
  - // Features reading
  - // Matches reading. Try to read the provided match filename or the default one (matches.e.txt/bin).
  - // Global SfM reconstruction process
    - ```Reconstruction_Report.html```
    - // Configure the features_provider & the matches_provider (```sfmEngine.SetFeaturesProvider```, ```sfmEngine.SetMatchesProvider```)
    - // Configure reconstruction parameters (```sfmEngine.Set_Intrinsics_Refinement_Type```, ```sfmEngine.Set_Use_Motion_Prior```)
    - // Configure motion averaging method (```sfmEngine.SetRotationAveragingMethod```, ```sfmEngine.SetTranslationAveragingMethod```)
    - ```sfmEngine.Process```
      - Total Ac-Global-Sfm took (s)
      - Generating SfM_Report.html
      - //-- Export to disk computed scene (data & visualizable results) (```sfm_data.bin```, ```cloud_and_poses.ply```. These 2 files save the same data)

- Step 5: ```main_ComputeSfM_DataColor.cpp```
  - Copyright: Pierre Moulon
  - Objective: // Convert from a SfM_Data format to another
  - Commandline arguments:
    - input_file (path to the input SfM_Data scene)
    - output_file (path to the output PLY file)
  - Important variables: ```vec_3dPoints```, ```vec_tracksColor```, ```vec_camPosition```
  - /// Export camera poses positions as a Vec3 vector
  - Compute the scene structure color
  - // Export the SfM_Data scene in the expected format (a .ply file)

- Step 6 (optional): ```main_ComputeStructureFromKnownPoses.cpp```
  - Copyright: Pierre Moulon
  - Objective: /// Compute the structure of a scene according existing camera poses
  - Commandline arguments:
    - input_file (path to a SfM_Data scene)
    - match_dir (path to the features and descriptors that corresponds to the provided SfM_Data scene)
    - output_file (file where the output data will be stored (i.e. sfm_data_structure.bin))
    - [Triangulation mode]
    - [No Provided Matches -> Triangulation of guided epipolar geometry matches (default mode)]
    - match_file (path to a matches file (loaded pair indexes will be used))
    - pair_file (path to a pairs file (only those pairs will be considered to compute the structure)
    - [Provided Matches -> Robust triangulation of the match file (activated by -d)]
    - direct_triangulation (Robustly triangulate the tracks computed from the file given by [-f|--match_file])
    - triangulation_method (triangulation method: Direct Linear Transform (DLT), L1_Angular, ...)
    - bundle_adjustment ((switch) perform a bundle adjustment on the scene (OFF by default))
    - residual_threshold (maximal pixels reprojection error that will be considered for triangulations (4.0 by default))
    - cache_size (Use a regions cache (only cache_size regions will be stored in memory). If not used, all regions will be load in memory.)
  - Important variables: ```z_near```, ```z_far```, ```frustum_filter```, ```dMax_reprojection_error```, ```triangulation_method```, ```sfm_data```, ```sImage_describer```, ```regions_type```, ```regions_provider```, ```pairs```, ```minPointPerPose```, ```minTrackLength```, ```option```,
  - /// Build a list of pair from the camera frusta intersections
  - // Load input SfM_Data scene
  - // Init the regions_type from the image describer file (used for image regions extraction)
  - // Prepare the Regions provider
  - // Show the progress on the command line
  - Has ```cout``` to show information loaded from a sfm_data scene: #views, #poses, #intricsics, #tracks
  - Robust triangulation of the match file
  - // Compute the tracks from the pairwise estimation
  - // Compute tracks from matches
    - // List of features matches for each couple of images
    - //-- Build tracks with STL compliant type
    - // Display some statistics about the computed tracks. 
      - //-- Display stats :
      - //    - number of images
      - //    - number of tracks
  - Robust triangulation of the tracks, tracks computed from a match file
    - // Fill sfm_data with the computed tracks (no 3D yet)
    - // Compute 3D position of the landmark of the structure by robust triangulation of the observations
  - Robust triangulation of the tracks, Triangulation of guided epipolar geometry matches
    - //- Pair selection method:
    - //  - geometry guided -> camera frustum intersection,
    - //  - putative matches guided (photometric matches)
    - //     (keep pairs that have valid Intrinsic & Pose ids).
    - // Compute Structure from known camera poses
  - Remove outliers
  - // Check that poses & intrinsic cover some measures (after outlier removal)
  - Point cloud cleaning
  - // Enable sparse Bundle adjustment (BA) only if a sparse lib is available and if there more than 100 poses
    - ```options.preconditioner_type_```
    - ```options.linear_solver_type_```
  - Bundle adjustment
    - cameras::Intrinsic_Parameter_Type::ADJUST_ALL,
    - Extrinsic_Parameter_Type::ADJUST_ALL,
    - Structure_Parameter_Type::ADJUST_ALL)
  - Has ```cout```  "Found a sfm_data scene with: #views, #poses, #intricsics, #tracks"
  - Export to a ply file

- Step 7 (optional): ```main_ComputeSfM_DataColor.cpp```. Same as Step 5.