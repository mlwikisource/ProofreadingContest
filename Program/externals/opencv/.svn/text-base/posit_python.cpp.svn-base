//#include "opencv2/highgui/highgui.hpp"
//#include "opencv2/imgproc/imgproc.hpp"
//#include "opencv2/features2d/features2d.hpp"
//#include "opencv2/ml/ml.hpp"
#include "opencv2/calib3d/calib3d.hpp"
// CvMatr32f, CvVect32f, ...
#include "opencv2/legacy/compat.hpp"

//#include <fstream>
#include <iostream>
//#include <memory>
#include <iterator>

#if defined WIN32 || defined _WIN32
#include "sys/types.h"
#endif
#include <sys/stat.h>

//#define DEBUG_DESC_PROGRESS

#define FOCAL_LENGTH 760.0

using namespace cv;
using namespace std;


/** 
* Patch to enable compilation and usage as python module also
* Code from: /usr/share/opencv/samples/cpp/bagofwords_classification.cpp
*            (fedora 15 package opencv-devel-docs-2.2.0-6 / opencv-devel-2.2.0-6)
* Library: lots (opencv, boost, python, ...)
*
* https://code.ros.org/trac/opencv/browser/trunk/opencv/samples/cpp/bagofwords_classification.cpp?rev=3714
* http://pascallin.ecs.soton.ac.uk/challenges/VOC/
* http://wiki.python.org/moin/boost.python/module
* http://stackoverflow.com/questions/7195959/hello-world-with-boost-python-and-python-3-2
* http://mail.python.org/pipermail/cplusplus-sig/2008-August/013592.html
*/

#include <boost/python.hpp>
//#include <boost/python/module.hpp>
//#include <boost/python/def.hpp>
//#include <boost/python/object.hpp>
#include <boost/python/stl_iterator.hpp>
//TODO: use 'bp::numeric::array' according to http://www.shocksolution.com/python-basics-tutorials-and-examples/boostpython-numpy-example/
//#include <boost/python/extract.hpp>
//#include <boost/python/numeric.hpp>
#include <streambuf>

namespace bp = boost::python;

// http://bo-peng.blogspot.com/2004/10/how-to-re-direct-cout-to-python_05.html
// http://mail.python.org/pipermail/cplusplus-sig/2005-September/009252.html
// A streambuf class for output to a Python stream.
/* Example usage:

using namespace boost::python;
object sys(PyImport_ImportModule("sys"));
object sys_stdout = sys.attr("stdout");
object sys_stderr = sys.attr("stderr");

if (PyObject_HasAttrString( sys_stdout.ptr(), "write"))
	std::cout.rdbuf( new py_ostreambuf( sys_stdout));
if (PyObject_HasAttrString( sys_stderr.ptr(), "write"))
	std::cerr.rdbuf( new py_ostreambuf( sys_stderr));

*/
class py_ostreambuf : public std::streambuf
{
 private:
    boost::python::object file;
    bool have_flush;

 public:
    py_ostreambuf( boost::python::object file_object)
        : file( file_object)
    {
        have_flush = PyObject_HasAttrString( file.ptr(), "flush");
    }

 protected:
    virtual int_type overflow( int_type c) 
    {
        file.attr("write")( static_cast<char>(c));
        return c;
    }

    virtual std::streamsize xsputn(const char_type* s, std::streamsize n)
    {
        file.attr("write")( std::string( s, n));
        return n;
    }
    
    virtual int sync()
    {
        if (have_flush) {
            file.attr("flush")();
            // Perhaps we should only return 0 if this path is followed?
        }
        // And return -1 here?  Methinks that might make anything that uses
	// std::endl fail.
        return 0;
    }
};

void raise(std::streambuf* sb, const bool& trigger, const string& msg)
{
    if (trigger)
    {
        cout << "ERROR: " << msg << endl;
        std::cout.rdbuf(sb);
        throw 0;    // in python; RuntimeError: unidentifiable C++ exception
    }
    return;
}



/*int main(int argc, char** argv)*/
//vector<float> worker(const bp::list& object_points = bp::list(),
//const bp::tuple& worker(const bp::list& object_points = bp::list(),
bp::tuple worker(const bp::list&  object_points = bp::list(),
                 const bp::list&  image_points  = bp::list(),
                 const bp::tuple& criterias     = bp::make_tuple(100, 1.0e-4f))
{
//    boost::python::stl_input_iterator<string> begin(files_list), end;
//    vector<string> files_vec;
//    std::copy( begin, end, back_inserter(files_vec) );
//#ifdef DEBUG_DESC_PROGRESS
//    std::ostream_iterator<string> out_it (cout, ", ");
//    std::copy ( begin, end, out_it );
//    cout << endl;
//    std::cout.rdbuf(sb);
//#endif

    // enable output to python stdout stream
    std::streambuf *sb = std::cout.rdbuf();
    boost::python::object sys(boost::python::detail::new_reference(PyImport_ImportModule("sys")));
    boost::python::object sys_stdout = sys.attr("stdout");
    if (PyObject_HasAttrString(sys_stdout.ptr(), "write"))
        sb = std::cout.rdbuf( new py_ostreambuf(sys_stdout) );

    // POSIT tutorial: http://opencv.willowgarage.com/wiki/Posit, POSIT.rar (main.cpp)
    //                 http://xuvif.blogspot.ch/2011/05/head-pose-estimation-by-using-posit-in.html

    // 3D Model Points
    //  Create the model pointss
    //  The first one must be (0,0,0)
    raise(sb, (bp::len(object_points) < 1), "list 'object_points' is empty!");
    //float cubeSize = 10.0;
    //bp::object elem;
    bp::tuple tpl;
    float val1, val2, val3;
    std::vector<CvPoint3D32f> modelPoints;
    //modelPoints.push_back(cvPoint3D32f(0.0f, 0.0f, 0.0f)); //The first must be (0,0,0)
    //modelPoints.push_back(cvPoint3D32f(0.0f, 0.0f, cubeSize));
    //modelPoints.push_back(cvPoint3D32f(cubeSize, 0.0f, 0.0f));
    //modelPoints.push_back(cvPoint3D32f(0.0f, cubeSize, 0.0f));
#ifdef DEBUG_DESC_PROGRESS
    cout << "object_points:" << endl;
    std::cout.rdbuf(sb);
#endif
    for (int i = 0; i < bp::len(object_points); ++i)
    {
        //elem = object_points[i];
        tpl = bp::extract<bp::tuple>(object_points[i]);
        raise(sb, (bp::len(tpl) < 3), "tuple items in 'object_points' need 3 entries!");
        val1 = bp::extract<float>(tpl[0]);
        val2 = bp::extract<float>(tpl[1]);
        val3 = bp::extract<float>(tpl[2]);
//  The first one must be (0,0,0)
        modelPoints.push_back(cvPoint3D32f(val1, val2, val3));
#ifdef DEBUG_DESC_PROGRESS
        cout << val1 << " " << val2 << " " << val3 << endl;
        std::cout.rdbuf(sb);
#endif
    }

    //  Create the POSIT object with the model points
    //CVAPI(CvPOSITObject*)  cvCreatePOSITObject( CvPoint3D32f* points, int point_count );
    CvPOSITObject *positObject = cvCreatePOSITObject( &modelPoints[0], static_cast<int>(modelPoints.size()) );

    // Image Points
    //  Create the image points 
    raise(sb, (bp::len(image_points) < 1), "list 'image_points' is empty!");
    std::vector<CvPoint2D32f> imagePoints;
    //imagePoints.push_back( cvPoint2D32f( -48, -224 ) );
    //imagePoints.push_back( cvPoint2D32f( -287, -174 ) );
    //imagePoints.push_back( cvPoint2D32f( 132, -153 ) );
    //imagePoints.push_back( cvPoint2D32f( -52, 149 ) );
#ifdef DEBUG_DESC_PROGRESS
    cout << "image_points:" << endl;
    std::cout.rdbuf(sb);
#endif
    for (int i = 0; i < bp::len(image_points); ++i)
    {
        tpl = bp::extract<bp::tuple>(image_points[i]);
        raise(sb, (bp::len(tpl) < 2), "tuple items in 'image_points' need 2 entries!");
        val1 = bp::extract<float>(tpl[0]);
        val2 = bp::extract<float>(tpl[1]);
        imagePoints.push_back(cvPoint2D32f(val1, val2));
#ifdef DEBUG_DESC_PROGRESS
        cout << val1 << " " << val2 << endl;
        std::cout.rdbuf(sb);
#endif
    }

    // Pose Estimation
    // http://www710.univ-lyon1.fr/~eguillou/documentation/opencv2/globals_type.html
    raise(sb, (bp::len(criterias) < 2), "tuple 'criterias' needs 2 entries!");
    long val4;
#ifdef DEBUG_DESC_PROGRESS
    cout << "criterias:" << endl;
    std::cout.rdbuf(sb);
#endif
    val4 = bp::extract<long>(criterias[0]);
    val1 = bp::extract<float>(criterias[1]);
#ifdef DEBUG_DESC_PROGRESS
    cout << val4 << " " << val1 << endl;
    std::cout.rdbuf(sb);
#endif
    //CvMat abc;
    CvMatr32f rotation_matrix = new float[9];
    CvVect32f translation_vector = new float[3];
    //set posit termination criteria: 100 max iterations, convergence epsilon 1.0e-5
    //CvTermCriteria criteria = cvTermCriteria(CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, 100, 1.0e-4f);
    CvTermCriteria criteria = cvTermCriteria(CV_TERMCRIT_EPS | CV_TERMCRIT_ITER, val4, val1);
    //CVAPI(void)  cvPOSIT(  CvPOSITObject* posit_object, CvPoint2D32f* image_points,
    //                       double focal_length, CvTermCriteria criteria,
    //                       float* rotation_matrix, float* translation_vector);
    cvPOSIT( positObject, &imagePoints[0], FOCAL_LENGTH, criteria, rotation_matrix, translation_vector );
    cvReleasePOSITObject(&positObject);
    //createOpenGLMatrixFrom( rotation_matrix, translation_vector);
//Show the results
#ifdef DEBUG_DESC_PROGRESS
    cout << "-......- POSE ESTIMATED -......-\n";
    cout << "-.- SOURCE MODEL POINTS -.-\n";
    for ( size_t  p=0; p<modelPoints.size(); p++ )
        cout << modelPoints[p].x << ", " << modelPoints[p].y << ", " << modelPoints[p].z << "\n";

    cout << "-.- SOURCE IMAGE POINTS -.-\n";
    //for ( size_t p=0; p<modelPoints.size(); p++ )
    for ( size_t p=0; p<imagePoints.size(); p++ )
        cout << imagePoints[p].x << ", " << imagePoints[p].y << " \n";

    //cout << "\n-.- REAL POSE\n";
    //for ( size_t p=0; p<4; p++ )
    //    cout << poseReal[p] << " | " << poseReal[p+4] << " | " << poseReal[p+8] << " | " << poseReal[p+12] << "\n";

    cout << "-.- ESTIMATED POSE\n";
    //for ( size_t p=0; p<4; p++ )
    //    cout << posePOSIT[p] << " | " << posePOSIT[p+4] << " | " << posePOSIT[p+8] << " | " << posePOSIT[p+12] << "\n";

    cout << "-.- ESTIMATED ROTATION\n";
    for ( size_t p=0; p<3; p++ )
        cout << rotation_matrix[p*3] << " | " << rotation_matrix[p*3+1] << " | " << rotation_matrix[p*3+2] << "\n";

    cout << "-.- ESTIMATED TRANSLATION\n";
    cout << translation_vector[0] << " | " << translation_vector[1] << " | " << translation_vector[2] << "\n";
#endif

/*
    // Project the model points with the estimated pose
    // http://opencv.willowgarage.com/documentation/cpp/camera_calibration_and_3d_reconstruction.html
    // intrinsic: camera matrix
    // extrinsic: rotation-translation matrix [R|t]
    CvMat* intrinsics = cvCreateMat( 3, 3, CV_32F );
    int width = 100;
    int height = 100;
    cvSetZero( intrinsics );
    cvmSet( intrinsics , 0, 0, FOCAL_LENGTH );
    cvmSet( intrinsics , 1, 1, FOCAL_LENGTH );
    cvmSet( intrinsics , 0, 2, width * 0.5 );//principal point in the centre of the image
    cvmSet( intrinsics , 1, 2, height * 0.5 );
    cvmSet( intrinsics , 2, 2, 1.0 );

    //  The origin of the coordinates system is in the centre of the image
    std::vector<CvPoint2D32f> projectedPoints;
    CvMat poseMatrix = cvMat( 4, 4, CV_32F, pose );
    for ( size_t  p=0; p<modelPoints.size(); p++ )
    {
            float modelPoint[] =  { modelPoints[p].x, modelPoints[p].y, modelPoints[p].z, 1.0f };
            CvMat modelPointMatrix = cvMat( 4, 1, CV_32F, modelPoint );
            float point3D[4];
            CvMat point3DMatrix = cvMat( 4, 1, CV_32F, point3D );
            //Transform the points from model space coordinates to camera space
            //The pose must be transposed because is in OpenGL format
            cvGEMM( &poseMatrix, &modelPointMatrix, 1.0, NULL, 0.0, &point3DMatrix, CV_GEMM_A_T );
            //Project the transformed 3D points
            CvPoint2D32f point2D = cvPoint2D32f( 0.0, 0.0 );
            if ( point3D[2] != 0 )
            {
                    point2D.x = cvmGet( intrinsics, 0, 0 ) * point3D[0] / point3D[2];
                    point2D.y = cvmGet( intrinsics, 1, 1 ) * point3D[1] / point3D[2];
            }
            projectedPoints.push_back( point2D );
    }

#ifdef DEBUG_DESC_PROGRESS
    //  Draw the projected model points
    cout << "\n-.- ESTIMATED IMAGE POINTS -.-\n";
    for ( size_t p=0; p<projectedPoints.size(); p++ )
    {
        cout << projectedPoints[p].x << ", " << projectedPoints[p].y << " \n";
    }
#endif
*/


    // convert float arrays to python lists
    //float* begin = &translation_vector[0];
    //float* end   = &translation_vector[3];
    //vector<float> tvec;
    //std::copy( begin, end, back_inserter(tvec) );
    bp::list rmat;
    for(int i = 0; i < 9; i++)
        (rmat).append(rotation_matrix[i]);
    bp::list tvec;
    for(int i = 0; i < 3; i++)
        (tvec).append(translation_vector[i]);

    delete rotation_matrix;
    delete translation_vector;

    /*return 0;*/
    std::cout.rdbuf(sb);    // if anything was forgotten
    return bp::make_tuple(rmat, (tvec));
}

/*
int main(int argc, char** argv)
{
    // in order to be able to use boost::python::list, boost::python::len, ...
    // we have to use 'embedding' additionally to 'extending' be call 'Py_Initialize'
    // http://osdir.com/ml/python.c++/2003-03/msg00095.html
    // http://docs.python.org/c-api/init.html
    if      (( argc == 3 ) or ( argc == 6 ))
    {
        Py_Initialize();
        worker();
    }
    else
    {
    	help(argv);
        return -1;
    }

    return 0;
}
*/



// http://stackoverflow.com/questions/5314319/how-to-export-stdvector
template<class T>
struct VecToList
{
    static PyObject* convert(const std::vector<T>& vec)
    {
        boost::python::list* l = new boost::python::list();
        for(size_t i = 0; i < vec.size(); i++)
            (*l).append(vec[i]);

        return l->ptr();
    }
};

//#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

BOOST_PYTHON_MODULE(posit)
{
  /*def("name", function_ptr);
  def("name", function_ptr, call_policies);
  def("name", function_ptr, "documentation string");
  def("name", function_ptr, call_policies, "documentation string");*/
  using namespace boost::python;
  to_python_converter<std::vector<float, std::allocator<float> >, VecToList<float> >();
  //class_<std::vector<float> >("float_vector")
  //    .def(vector_indexing_suite<std::vector<float> >())
  //;
  def("main", worker, "posit main function");
}
