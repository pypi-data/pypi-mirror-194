/* _ckmeans_1d_dp.cpp
 *
 * Wrap the "kmeans_1d_dp()" function to make it accessible from python.
 *
 * Alden Bradford
 * Purdue University
 * bradfoa@purdue.edu
 */

#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "../src/Ckmeans.1d.dp.h"

namespace py = pybind11;

enum DISSIMILARITY parse(const std::string & dissimilarity){
    if (dissimilarity == "L2"){
        return L2;
    } else if (dissimilarity == "L1"){
        return L1;
    } else if (dissimilarity == "L2Y"){
        return L2Y;
    } else {
        throw std::runtime_error("not a valid dissimilarity!");
    }
}


void Ckmeans_1d_dp(py::array_t<double, py::array::c_style | py::array::forcecast> x,
                   py::array_t<double, py::array::c_style | py::array::forcecast> y,
                   const size_t minK,
                   const size_t maxK,
                   py::array_t<int> cluster,
                   py::array_t<double> centers,
                   py::array_t<double> withinss,
                   py::array_t<double> size,
                   py::array_t<double> BICs,
                   const std::string & estimate_k,
                   const std::string & method,
                   const std::string & dissimilarity)
{
    py::buffer_info bufx = x.request(), bufy = y.request();
    
    double *xp = static_cast<double *>(bufx.ptr);
    double *yp = static_cast<double *>(bufy.ptr);
    int *cluster_p = static_cast<int *>(cluster.request().ptr);
    double *center_p = static_cast<double *>(centers.request().ptr);
    double *wp = static_cast<double *>(withinss.request().ptr);
    double *sp = static_cast<double *>(size.request().ptr);
    double *bp = static_cast<double *>(BICs.request().ptr);

    // Call C++ version one-dimensional clustering algorithm*/
    if(bufy.size != bufx.size) { yp = 0; }
    
    size_t length =  x.shape(x.ndim()-1);
    enum DISSIMILARITY condition = parse(dissimilarity);
    
    for(size_t width = x.size()/length; width > 0; --width){
        kmeans_1d_dp(xp, length, yp, minK, maxK,
                   cluster_p, center_p, wp, sp, bp,
                   estimate_k, method, condition);
        xp += length;
        yp = yp ? yp + length : 0;
        cluster_p += length;
        center_p += maxK;
        wp += maxK;
        sp += maxK;
        bp += maxK-minK+1;
    }
}


PYBIND11_MODULE(_ckmeans_1d_dp, m){
    m.doc() = "Python binding for Ckmeans.1d.dp";
    
    m.def("ckmeans", &Ckmeans_1d_dp, "the Ckmeans.1d.dp function");
}