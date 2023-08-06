// (C) Koninklijke Philips Electronics N.V. 2016
//
// All rights are reserved. Reproduction or transmission in whole or in part, in
// any form or by any means, electronic, mechanical or otherwise, is prohibited
// without the prior written permission of the copyright owner.

#include "PhilipsPixelEngine/softwarerenderbackend.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(softwarerenderbackend, m)
{
  m.doc() = R"pbdoc(
    SoftwareRenderBackend Python plugin
      -----------------------
      .. currentmodule:: SoftwareRenderBackend
      .. autosummary::
      :toctree: _generate
    )pbdoc";

  py::class_<SoftwareRenderBackend, RenderBackend> softwarerenderbackend_class(
    m, "SoftwareRenderBackend");
  py::enum_<RenderBackend::ImageFormatType>(softwarerenderbackend_class, "Api")
    .value("RGB", RenderBackend::RGB)
    .value("RGBA", RenderBackend::RGBA)
    .value("LUMINANCE", RenderBackend::LUMINANCE)
    .value("UNDEFINED_FORMAT", RenderBackend::UNDEFINED_FORMAT)
    .export_values();
  softwarerenderbackend_class.def(
    py::init<RenderBackend::ImageFormatType>(), py::arg("image_format_type") = RenderBackend::RGBA);

#ifdef VERSION_INFO
  m.attr("__version__") = py::str(VERSION_INFO);
#else
  m.attr("__version__") = py::str("dev");
#endif
}
