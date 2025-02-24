cmake_minimum_required(VERSION 3.30)
project(backtestingCpp VERSION 0.1.0)
set(CMAKE_CXX_STANDARD 17)

include(CTest)
enable_testing()

set(HDF5_ROOT "C:/Program Files/HDF_Group/HDF5/1.14.6")
find_package(HDF5 REQUIRED COMPONENTS C)
if (HDF5_FOUND)
    message(STATUS "HDF5 found: ${HDF5_INCLUDE_DIRS}")
else()
    message(FATAL_ERROR "HDF5 not found!")
endif()

include_directories(${HDF5_INCLUDE_DIRS})
link_directories(${HDF5_LIBRARY_DIRS})


set(SOURCE_FILES main.cpp
        Database.cpp
        Database.h)
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_link_libraries(${PROJECT_NAME} ${HDF5_LIBRARIES} ${HDF5_C_LIBRARIES})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)