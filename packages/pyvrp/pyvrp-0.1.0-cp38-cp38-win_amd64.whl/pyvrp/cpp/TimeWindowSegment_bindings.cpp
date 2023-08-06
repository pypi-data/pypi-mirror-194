#include "TimeWindowSegment.h"

#include <pybind11/pybind11.h>

namespace py = pybind11;
using TWS = TimeWindowSegment;

PYBIND11_MODULE(_TimeWindowSegment, m)
{
    py::class_<TWS>(m, "TimeWindowSegment")
        .def(py::init<Matrix<int> const *, int, int, int, int, int, int>(),
             py::arg("dist"),
             py::arg("idx_first"),
             py::arg("idx_last"),
             py::arg("duration"),
             py::arg("time_warp"),
             py::arg("tw_early"),
             py::arg("tw_late"),
             py::keep_alive<1, 2>())  // keep matrix alive
        .def("total_time_warp", &TWS::totalTimeWarp)
        .def_static("merge", &TWS::merge<>)
        .def_static("merge", &TWS::merge<TWS>)
        .def_static("merge", &TWS::merge<TWS, TWS>);
}
