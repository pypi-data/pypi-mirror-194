// (C) Koninklijke Philips Electronics N.V. 2016
//
// All rights are reserved. Reproduction or transmission in whole or in part, in
// any form or by any means, electronic, mechanical or otherwise, is prohibited
// without the prior written permission of the copyright owner.

#include "PhilipsPixelEngine/eglrendercontext.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

class PyEglRenderContext: public EglRenderContext
{
public:
  using EglRenderContext::EglRenderContext;
  void swapBuffers() override { PYBIND11_OVERLOAD_PURE(void, EglRenderContext, swapBuffers, ); }
  void makeContextCurrent() override
  {
    PYBIND11_OVERLOAD_PURE(void, EglRenderContext, makeContextCurrent, );
  }
  size_t width() const override { PYBIND11_OVERLOAD(size_t, EglRenderContext, width, ); }
  size_t height() const override { PYBIND11_OVERLOAD(size_t, EglRenderContext, height, ); }
};

PYBIND11_MODULE(eglrendercontext, m)
{
  m.doc() = R"pbdoc(
    EglRenderContext Python plugin
      -----------------------
      .. currentmodule:: EglRenderContext
      .. autosummary::
      :toctree: _generate
    )pbdoc";

  py::class_<EglRenderContext, RenderContext, PyEglRenderContext> eglrendercontext_class(
    m, "EglRenderContext");
  py::enum_<EglRenderContext::Api>(eglrendercontext_class, "Api")
    .value("GL", EglRenderContext::GL)
    .value("ES", EglRenderContext::ES)
    .value("VG", EglRenderContext::VG)
    .export_values();
  eglrendercontext_class
    .def(py::init<size_t, size_t, EglRenderContext::Api, size_t, size_t>(), py::arg("width"),
      py::arg("height"), py::arg("api") = EglRenderContext::ES, py::arg("version") = 2,
      py::arg("device_index") = 0)
    .def(py::init<EglRenderContext::Api, size_t, size_t>(), py::arg("api") = EglRenderContext::ES,
      py::arg("version") = 2, py::arg("device_index") = 0)
    .def("swap_buffers", &EglRenderContext::swapBuffers)
    .def("make_context_current", &EglRenderContext::makeContextCurrent)
    .def("width", &EglRenderContext::width)
    .def("height", &EglRenderContext::height);

#ifdef VERSION_INFO
  m.attr("__version__") = py::str(VERSION_INFO);
#else
  m.attr("__version__") = py::str("dev");
#endif
}
