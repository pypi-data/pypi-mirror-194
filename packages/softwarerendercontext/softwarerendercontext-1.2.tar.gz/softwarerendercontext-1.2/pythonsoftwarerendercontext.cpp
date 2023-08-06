// (C) Koninklijke Philips Electronics N.V. 2016
//
// All rights are reserved. Reproduction or transmission in whole or in part, in
// any form or by any means, electronic, mechanical or otherwise, is prohibited
// without the prior written permission of the copyright owner.

#include "PhilipsPixelEngine/softwarerendercontext.hpp"
#include <pybind11/pybind11.h>

namespace py = pybind11;

class PySoftwareRenderContext: public SoftwareRenderContext
{
public:
  using SoftwareRenderContext::SoftwareRenderContext;
  void swapBuffers() override
  {
    PYBIND11_OVERLOAD_PURE(void, SoftwareRenderContext, swapBuffers, );
  }
  void makeContextCurrent() override
  {
    PYBIND11_OVERLOAD_PURE(void, SoftwareRenderContext, makeContextCurrent, );
  }
  size_t width() const override { PYBIND11_OVERLOAD(size_t, SoftwareRenderContext, width, ); }
  size_t height() const override { PYBIND11_OVERLOAD(size_t, SoftwareRenderContext, height, ); }
};

PYBIND11_MODULE(softwarerendercontext, m)
{
  m.doc() = R"pbdoc(
    SoftwareRenderContext Python plugin
      -----------------------
      .. currentmodule:: SoftwareRenderContext
      .. autosummary::
      :toctree: _generate
    )pbdoc";

  py::class_<SoftwareRenderContext, RenderContext, PySoftwareRenderContext>
    softwarerendercontext_class(m, "SoftwareRenderContext");
  softwarerendercontext_class.def(py::init())
    .def(py::init<size_t, size_t>(), py::arg("width"), py::arg("height"))
    .def("swap_buffers", &SoftwareRenderContext::swapBuffers)
    .def("make_context_current", &SoftwareRenderContext::makeContextCurrent)
    .def_property_readonly("width", &SoftwareRenderContext::width)
    .def_property_readonly("height", &SoftwareRenderContext::height);

#ifdef VERSION_INFO
  m.attr("__version__") = py::str(VERSION_INFO);
#else
  m.attr("__version__") = py::str("dev");
#endif
}
