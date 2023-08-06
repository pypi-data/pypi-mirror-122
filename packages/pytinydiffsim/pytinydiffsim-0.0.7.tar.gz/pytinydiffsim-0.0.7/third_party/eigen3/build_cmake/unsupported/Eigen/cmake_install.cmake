# Install script for directory: /Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "local_install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE FILE FILES
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/AdolcForward"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/AlignedVector3"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/ArpackSupport"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/AutoDiff"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/BVH"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/EulerAngles"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/FFT"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/IterativeSolvers"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/KroneckerProduct"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/LevenbergMarquardt"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/MatrixFunctions"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/MoreVectorization"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/MPRealSupport"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/NonLinearOptimization"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/NumericalDiff"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/OpenGLSupport"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/Polynomials"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/Skyline"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/SparseExtra"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/SpecialFunctions"
    "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/Splines"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xDevelx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/eigen3/unsupported/Eigen" TYPE DIRECTORY FILES "/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/unsupported/Eigen/src" FILES_MATCHING REGEX "/[^/]*\\.h$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/Users/erwincoumans/develop/tds/tiny-differentiable-simulator/third_party/eigen3/build_cmake/unsupported/Eigen/CXX11/cmake_install.cmake")

endif()

