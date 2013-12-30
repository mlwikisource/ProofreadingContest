import sys, os, warnings

scriptdir = os.path.dirname(sys.argv[0])
if not os.path.isabs(scriptdir):
    scriptdir = os.path.abspath(os.path.join(os.curdir, scriptdir))
    
libdir = os.path.join(scriptdir, 'externals/opencv')
if not os.path.exists(libdir):
    os.makedirs(libdir)
# path has to exist BEFORE appending, otherwise the re-import fails
sys.path.append(libdir)

import numpy

# suppress .../pywikipedia/externals/opencv/__init__.py:43: RuntimeWarning: to-Python converter for std::vector<float, std::allocator<float> > already registered; second conversion method ignored.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # better would be to catch the warnings into a list... but how? ;)

    try:
        # try to import
        import BoWclassify as _BoWclassify
    except ImportError, e:
        print "(re-)compilation triggered because of: '%s'" % e

        cur = os.path.abspath(os.curdir)
        os.chdir( os.path.join(scriptdir, 'externals/opencv') )

        # remove/reset if existing already
        if os.path.exists(os.path.join(libdir, 'BoWclassify.so')):
            os.remove( os.path.join(libdir, 'BoWclassify.so') )

        # compile python module (may be use 'distutil' instead of 'make' here)
        if os.system("make BoWclassify.so"):
            raise ImportError("'BoWclassify.so' could not be compiled!")

        os.chdir( cur )

        # re-try to import
        import BoWclassify as _BoWclassify

    try:
        # try to import
        import posit as _posit
    except ImportError, e:
        print "(re-)compilation triggered because of: '%s'" % e

        cur = os.path.abspath(os.curdir)
        os.chdir( os.path.join(scriptdir, 'externals/opencv') )

        # remove/reset if existing already
        if os.path.exists(os.path.join(libdir, 'posit.so')):
            os.remove( os.path.join(libdir, 'posit.so') )

        # compile python module (may be use 'distutil' instead of 'make' here)
        if os.system("make posit.so"):
            raise ImportError("'posit.so' could not be compiled!")

        os.chdir( cur )

        # re-try to import
        import posit as _posit

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def posit(model, image, crit):
    # translation to origin (since first point has to be (0, 0, 0))
    model  = numpy.array(model)
    origin = model[0]
    model  = model - origin

    _model = [ tuple(item) for item in model.astype(float) ]
    _image = [ tuple(item) for item in numpy.array(image).astype(float) ]
    #_crit  = tuple(crit.astype(float))
    _crit  = (long(crit[0]), float(crit[1]))

    try:
        (_rmat, _tvec) = _posit.main(_model, _image, _crit)
    except Exception, e:
        raise e.__class__("Error in 'cvPOSIT' wrapper 'posit.so' (%s)" % e)

    rmat = numpy.reshape(numpy.array(_rmat), (3,3))
    tvec = numpy.array(_tvec)
    return (rmat, tvec, model)

def BoWclassify(*args):
    return _BoWclassify.main(*args)

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

def unit_test():
    print "TEST 'BoWclassify'"
    pass

    print "TEST 'posit'"
    cubeSize = 10.0
    model  = [(0.0, 0.0, 0.0),
              (0.0, 0.0, cubeSize),
              (cubeSize, 0.0, 0.0),
              (0.0, cubeSize, 0.0),]
    image  = [( -48, -224),
              (-287, -174),
              ( 132, -153),
              ( -52,  149),]
    crit  = (100, 1.0e-4)
    #model = np.array(model)
    #image = np.array(image)
    #crit  = np.array(crit)
    (rmat, tvec, mdl) = posit(model, image, crit)
    print rmat
    print tvec
