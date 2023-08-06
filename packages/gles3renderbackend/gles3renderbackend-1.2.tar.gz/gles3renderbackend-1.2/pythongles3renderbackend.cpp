// (C) Koninklijke Philips Electronics N.V. 2016
//
// All rights are reserved. Reproduction or transmission in whole or in part, in
// any form or by any means, electronic, mechanical or otherwise, is prohibited
// without the prior written permission of the copyright owner.

#include "PhilipsPixelEngine/gles3renderbackend.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(gles3renderbackend, m)
{
  m.doc() = R"pbdoc(
    Gles3RenderBackend Python plugin
      -----------------------
      .. currentmodule:: Gles3RenderBackend
      .. autosummary::
      :toctree: _generate
    )pbdoc";

  py::class_<Gles3RenderBackend, RenderBackend> gles3renderbackend_class(m, "Gles3RenderBackend");
  py::enum_<RenderBackend::ImageFormatType>(gles3renderbackend_class, "Api", py::module_local())
    .value("RGB", RenderBackend::RGB)
    .value("RGBA", RenderBackend::RGBA)
    .value("LUMINANCE", RenderBackend::LUMINANCE)
    .value("UNDEFINED_FORMAT", RenderBackend::UNDEFINED_FORMAT)
    .export_values();

  gles3renderbackend_class.def(py::init<RenderBackend::ImageFormatType, size_t>(),
    py::arg("image_format_type") = RenderBackend::RGBA,
    py::arg("tile_cache_sizeBytes") = RenderBackend::defaultTileCacheSizeBytes);

#ifdef VERSION_INFO
  m.attr("__version__") = py::str(VERSION_INFO);
#else
  m.attr("__version__") = py::str("dev");
#endif
}
