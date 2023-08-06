// (C) Koninklijke Philips Electronics N.V. 2020
//
// All rights are reserved. Reproduction or transmission in whole or in part, in
// any form or by any means, electronic, mechanical or otherwise, is prohibited
// without the prior written permission of the copyright owner.


#include "PhilipsPixelEngine/pixelengine.hpp"
//#include "portablegui/rendercontext.hpp"
#include "PhilipsPixelEngine/renderbackend.hpp"

#include <pybind11/pybind11.h>

#include <functional>
#include <pybind11/cast.h>
#include <pybind11/numpy.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

namespace py = pybind11;

template<typename T>
using array_t = py::array_t<T, py::array::c_style | py::array::forcecast>;

class PyRenderBackend: public RenderBackend
{
public:
  using RenderBackend::RenderBackend;
  std::shared_ptr<RenderBackendInstance> createInstance(RenderContext const& context) override
  {
    PYBIND11_OVERLOAD_PURE(
      std::shared_ptr<RenderBackendInstance>, RenderBackend, createInstance, context);
  }
};

// FIXME: pybind11 seems to have s bug when deleting references of
// virtual-inheritance classes. A bug has been filed:
// (https://github.com/pybind/pybind11/issues/2073)
// For now a work-around is implemented by creating wrapper classes for
// PixelEngine::SourceView and PixelEngine::DisplayView that do not use virtual
// inheritance. We should revert this once the issue is fixed in pybind11

class PyView: public PixelEngine::View
{
public:
  PyView(PixelEngine::View& view): view_(view) {}
  PixelEngine::Level const& operator[](size_t level) const override
  {
    return view_.operator[](level);
  }
  void chainSourceView(View const& view, int xShift, int yShift, int levelShift) const override
  {
    view_.chainSourceView(view, xShift, yShift, levelShift);
  }
  PixelEngine::UserView& addChainedView() override { return view_.addChainedView(); }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
  }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions,
    PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(
      regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
  }
  ::PixelEngine::View::DerivedLevelPixelAlignment derivedLevelPixelAlignment() const override
  {
    return view_.derivedLevelPixelAlignment();
  }
  std::vector<std::array<uint32_t, 3>> const& dimensionRanges(size_t level) const override
  {
    return view_.dimensionRanges(level);
  }
  std::vector<std::string> const& dimensionNames() const override { return view_.dimensionNames(); }
  std::vector<std::string> const& dimensionUnits() const override { return view_.dimensionUnits(); }
  std::vector<std::string> const& dimensionTypes() const override { return view_.dimensionTypes(); }
  std::vector<std::vector<std::string>> const& dimensionDiscreteValues() const override
  {
    return view_.dimensionDiscreteValues();
  }
  std::vector<double> const& scale() const override { return view_.scale(); }
  std::vector<double> const& origin() const override { return view_.origin(); }
  PixelEngine::DataEnvelopes const& dataEnvelopes(size_t level) const override
  {
    return view_.dataEnvelopes(level);
  }
  uint16_t bitsAllocated() const override { return view_.bitsAllocated(); }
  uint16_t bitsStored() const override { return view_.bitsStored(); }
  uint16_t highBit() const override { return view_.highBit(); }
  uint16_t pixelRepresentation() const override { return view_.pixelRepresentation(); }
  uint16_t planarConfiguration() const override { return view_.planarConfiguration(); }
  uint16_t samplesPerPixel() const override { return view_.samplesPerPixel(); }
  size_t id() const override { return view_.id(); }
  size_t numDerivedLevels() const override { return view_.numDerivedLevels(); }
  std::vector<size_t> pixelSize() const override { return view_.pixelSize(); }

private:
  PixelEngine::View& view_;
};

class PyReconstructedView: public PixelEngine::ReconstructedView
{
public:
  PyReconstructedView(PixelEngine::ReconstructedView& view): view_(view) {}
  PixelEngine::Level const& operator[](size_t level) const override
  {
    return view_.operator[](level);
  }
  void chainSourceView(View const& view, int xShift, int yShift, int levelShift) const override
  {
    view_.chainSourceView(view, xShift, yShift, levelShift);
  }
  PixelEngine::UserView& addChainedView() override { return view_.addChainedView(); }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
  }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions,
    PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(
      regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
  }
  ::PixelEngine::View::DerivedLevelPixelAlignment derivedLevelPixelAlignment() const override
  {
    return view_.derivedLevelPixelAlignment();
  }
  std::vector<std::array<uint32_t, 3>> const& dimensionRanges(size_t level) const override
  {
    return view_.dimensionRanges(level);
  }
  std::vector<std::string> const& dimensionNames() const override { return view_.dimensionNames(); }
  std::vector<std::string> const& dimensionUnits() const override { return view_.dimensionUnits(); }
  std::vector<std::string> const& dimensionTypes() const override { return view_.dimensionTypes(); }
  std::vector<std::vector<std::string>> const& dimensionDiscreteValues() const override
  {
    return view_.dimensionDiscreteValues();
  }
  std::vector<double> const& scale() const override { return view_.scale(); }
  std::vector<double> const& origin() const override { return view_.origin(); }
  PixelEngine::DataEnvelopes const& dataEnvelopes(size_t level) const override
  {
    return view_.dataEnvelopes(level);
  }
  uint16_t bitsAllocated() const override { return view_.bitsAllocated(); }
  uint16_t bitsStored() const override { return view_.bitsStored(); }
  uint16_t highBit() const override { return view_.highBit(); }
  uint16_t pixelRepresentation() const override { return view_.pixelRepresentation(); }
  uint16_t planarConfiguration() const override { return view_.planarConfiguration(); }
  uint16_t samplesPerPixel() const override { return view_.samplesPerPixel(); }
  size_t id() const override { return view_.id(); }
  size_t numDerivedLevels() const override { return view_.numDerivedLevels(); }
  std::vector<size_t> pixelSize() const override { return view_.pixelSize(); }
  void loadDefaultParameters() override { view_.loadDefaultParameters(); }

private:
  PixelEngine::ReconstructedView& view_;
};

class PySourceView: public PixelEngine::SourceView
{
public:
  PySourceView(PixelEngine::SourceView& view): view_(view) {}
  PixelEngine::Level const& operator[](size_t level) const override
  {
    return view_.operator[](level);
  }
  void chainSourceView(View const& view, int xShift, int yShift, int levelShift) const override
  {
    view_.chainSourceView(view, xShift, yShift, levelShift);
  }
  PixelEngine::UserView& addChainedView() override { return view_.addChainedView(); }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
  }
  std::list<std::shared_ptr<PixelEngine::Region>> requestRegions(
    std::vector<std::vector<size_t>> const& regions,
    PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering = true,
    std::vector<size_t> const& backgroundColor = { 0, 0, 0 },
    PixelEngine::BufferType bufferType = PixelEngine::BufferType::RGB) override
  {
    return view_.requestRegions(
      regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
  }
  ::PixelEngine::View::DerivedLevelPixelAlignment derivedLevelPixelAlignment() const override
  {
    return view_.derivedLevelPixelAlignment();
  }
  std::vector<std::array<uint32_t, 3>> const& dimensionRanges(size_t level) const override
  {
    return view_.dimensionRanges(level);
  }
  std::vector<std::string> const& dimensionNames() const override { return view_.dimensionNames(); }
  std::vector<std::string> const& dimensionUnits() const override { return view_.dimensionUnits(); }
  std::vector<std::string> const& dimensionTypes() const override { return view_.dimensionTypes(); }
  std::vector<std::vector<std::string>> const& dimensionDiscreteValues() const override
  {
    return view_.dimensionDiscreteValues();
  }
  std::vector<double> const& scale() const override { return view_.scale(); }
  std::vector<double> const& origin() const override { return view_.origin(); }
  PixelEngine::DataEnvelopes const& dataEnvelopes(size_t level) const override
  {
    return view_.dataEnvelopes(level);
  }
  uint16_t bitsAllocated() const override { return view_.bitsAllocated(); }
  uint16_t bitsStored() const override { return view_.bitsStored(); }
  uint16_t highBit() const override { return view_.highBit(); }
  uint16_t pixelRepresentation() const override { return view_.pixelRepresentation(); }
  uint16_t planarConfiguration() const override { return view_.planarConfiguration(); }
  uint16_t samplesPerPixel() const override { return view_.samplesPerPixel(); }
  size_t id() const override { return view_.id(); }
  size_t numDerivedLevels() const override { return view_.numDerivedLevels(); }
  std::vector<size_t> pixelSize() const override { return view_.pixelSize(); }
  void loadDefaultParameters() override { view_.loadDefaultParameters(); }
  void truncation(
    bool enabled, bool rounding, std::map<size_t, std::vector<size_t>> const& truncLevels) override
  {
    view_.truncation(enabled, rounding, truncLevels);
  }

private:
  PixelEngine::SourceView& view_;
};

class PyDisplayView: public PySourceView
{
public:
  PyDisplayView(PixelEngine::DisplayView& view): PySourceView(view), view_(view) {}
  void sharpness(double gain) { view_.sharpness(gain); }
  double sharpness() const { return view_.sharpness(); }

  void contrastClipLimit(double clipLimit) { view_.contrastClipLimit(clipLimit); }
  double contrastClipLimit() const { return view_.contrastClipLimit(); }

  void colorCorrectionGamma(double gamma) { view_.colorCorrectionGamma(gamma); }
  double colorCorrectionGamma() const { return view_.colorCorrectionGamma(); }

  void colorCorrectionBlackPoint(double blackpoint) { view_.colorCorrectionBlackPoint(blackpoint); }
  double colorCorrectionBlackPoint() const { return view_.colorCorrectionBlackPoint(); }

  void colorCorrectionWhitePoint(double whitepoint) { view_.colorCorrectionWhitePoint(whitepoint); }
  double colorCorrectionWhitePoint() const { return view_.colorCorrectionWhitePoint(); }

  void colorGain(double gain) { view_.colorGain(gain); }
  double colorGain() const { return view_.colorGain(); }

private:
  PixelEngine::DisplayView& view_;
};

class PyUserView: public PyView
{
public:
  PyUserView(PixelEngine::UserView& view): PyView(view), view_(view) {}
  std::unique_ptr<PixelEngine::FilterHandle> addFilter(std::string const& filterName)
  {
    return view_.addFilter(filterName);
  }
  void filterParameterDouble(
    std::unique_ptr<PixelEngine::FilterHandle>& filter, std::string const& name, double value)
  {
    view_.filterParameterDouble(filter, name, value);
  }
  void filterParameterMatrix3x3(std::unique_ptr<PixelEngine::FilterHandle>& filter,
    std::string const& name, std::array<double, 9> const& value)
  {
    view_.filterParameterMatrix3x3(filter, name, value);
  }

private:
  PixelEngine::UserView& view_;
};

class PyFilterHandle
{
public:
  PyFilterHandle(std::unique_ptr<PixelEngine::FilterHandle>&& handle): handle_(std::move(handle)) {}
  std::unique_ptr<PixelEngine::FilterHandle>& ref() { return handle_; }
  std::vector<std::string> const& supportedParameters() { return handle_->supportedParameters(); }

private:
  std::unique_ptr<PixelEngine::FilterHandle> handle_;
};

PYBIND11_MODULE(pixelengine, m)
{
  m.doc() = R"pbdoc(
    PixelEngine Python plugin
      -----------------------
      .. currentmodule:: PixelEngine
      .. autosummary::
      :toctree: _generate
    )pbdoc";

  py::class_<RenderBackend, PyRenderBackend> renderbackend_class(m, "RenderBackend");
  renderbackend_class.def(py::init())
    .def("create_instance", &RenderBackend::createInstance, "Create RenderBackend instance.");

  py::class_<RenderContext> rendercontext_class(m, "RenderContext");
  rendercontext_class.def(py::init())
    .def("width", &RenderContext::width, "Returns window Width.")
    .def("height", &RenderContext::height, "Returns window Height.");

  py::class_<PixelEngine> pixelengine_class(m, "PixelEngine");
  pixelengine_class.def(py::init())
    .def(py::init<RenderBackend&, RenderContext&>(), py::keep_alive<1, 2>(), py::keep_alive<1, 3>())
    .def("__getitem__", &PixelEngine::operator[], py::return_value_policy::reference_internal)
    .def_property_readonly_static(
      "version", [](py::object) { return PixelEngine::version(); }, "Returns the software version.")
    .def("containers", &PixelEngine::containers, py::return_value_policy::copy,
      "List of available image containers that specify storage format in the files.")
    .def("container_version", &PixelEngine::containerVersion,
      "Get version of container implementation.", py::arg("container"))
    .def("compressors", &PixelEngine::compressors, py::return_value_policy::copy,
      "List of available compressors that can be selected for compressing new files.")
    .def("pixel_transforms", &PixelEngine::pixelTransforms, py::return_value_policy::copy,
      "List of available pixel-transforms that can be selected for creating new files.")
    .def("block_sizes", &PixelEngine::blockSizes, py::return_value_policy::copy,
      "List of possible of block sizes that can be used when creating new files.",
      py::arg("pixel_transform"))
    .def("colorspace_transforms", &PixelEngine::colorspaceTransforms, py::return_value_policy::copy,
      "List of available color transformations that can be used when creating new files.")
    .def("quality_presets", &PixelEngine::qualityPresets, py::return_value_policy::copy,
      "List of available quality presets that can be used when creating new files.")
    .def("supported_filters", &PixelEngine::supportedFilters, py::return_value_policy::copy,
      "List of supported filter that can be added to a userview")
    .def("compress",
      [](PixelEngine& self, std::string const& compressor, array_t<uint8_t> const& source,
        std::vector<size_t> const& vectorization, array_t<uint8_t>& dest, size_t numberOfBlocks,
        std::vector<size_t> const& partitionSize, size_t sourceRowStride) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        self.compress(compressor, sourceData, vectorization, destData, typeid(uint8_t),
          numberOfBlocks, partitionSize, sourceRowStride);
      })
    .def("compress",
      [](PixelEngine& self, std::string const& compressor, array_t<int16_t> const& source,
        std::vector<size_t> const& vectorization, array_t<uint8_t>& dest, size_t numberOfBlocks,
        std::vector<size_t> const& partitionSize, size_t sourceRowStride) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        self.compress(compressor, sourceData, vectorization, destData, typeid(int16_t),
          numberOfBlocks, partitionSize, sourceRowStride);
      })
    .def("compress",
      [](PixelEngine& self, std::string const& compressor, size_t quality,
        array_t<uint8_t> const& source, std::vector<size_t> const& vectorization,
        array_t<uint8_t>& dest, size_t numberOfBlocks, std::vector<size_t> const& partitionSize,
        size_t sourceRowStride) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        self.compress(compressor, quality, sourceData, vectorization, destData, typeid(uint8_t),
          numberOfBlocks, partitionSize, sourceRowStride);
      })
    .def("compress",
      [](PixelEngine& self, std::string const& compressor, size_t quality,
        array_t<int16_t> const& source, std::vector<size_t> const& vectorization,
        array_t<uint8_t>& dest, size_t numberOfBlocks, std::vector<size_t> const& partitionSize,
        size_t sourceRowStride) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        self.compress(compressor, quality, sourceData, vectorization, destData, typeid(int16_t),
          numberOfBlocks, partitionSize, sourceRowStride);
      })
    .def("decompress",
      [](PixelEngine& self, std::string const& compressor, array_t<uint8_t> source,
        array_t<uint8_t> dest, size_t compressedLength, size_t numberOfBlocks,
        std::vector<size_t> const& partitionSize) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        return self.decompress(compressor, sourceData, destData, compressedLength, typeid(uint8_t),
          numberOfBlocks, partitionSize);
      })
    .def("decompress",
      [](PixelEngine& self, std::string const& compressor, array_t<uint8_t> source,
        array_t<int16_t> dest, size_t compressedLength, size_t numberOfBlocks,
        std::vector<size_t> const& partitionSize) {
        auto s = source.unchecked();
        void const* sourceData = reinterpret_cast<void const*>(s.data(0));
        auto d = dest.mutable_unchecked();
        void* destData = reinterpret_cast<void*>(d.mutable_data(0));
        return self.decompress(compressor, sourceData, destData, compressedLength, typeid(int16_t),
          numberOfBlocks, partitionSize);
      })
    .def("wait_all", &PixelEngine::waitAll,
      "Method to get pixel data in an synchronous manner for the provided list of Regions.",
      py::arg("region list"))
    .def(
      "wait_any",
      [](PixelEngine& self) -> py::tuple {
        auto cppRes = self.waitAny();
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return std::move(pyResult);
      },
      "Method to get pixel data asynchronously from previously requested regions")
    .def(
      "wait_any",
      [](PixelEngine& self,
        std::list<std::shared_ptr<PixelEngine::Region>> const& list) -> py::tuple {
        auto cppRes = self.waitAny(list);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return std::move(pyResult);
      },
      "Method to get pixel data in an asynchronous manner for the provided list of Regions.",
      py::arg("region list"))
    .def("clear_render_target", &PixelEngine::clearRenderTarget,
      "Clear a render target with a constant color.", py::arg("color"), py::arg("target") = 0)
    .def("clear_render_cache", &PixelEngine::clearRenderCache, "Clear render cache.")
    .def("clear_render_buffers", &PixelEngine::clearRenderBuffers, "Clear render buffers.")
    .def_property("network_settings",
      (PixelEngine::NetworkSettings const& (PixelEngine::*)() const) & PixelEngine::networkSettings,
      (void (PixelEngine::*)(PixelEngine::NetworkSettings const&)) & PixelEngine::networkSettings,
      "Network settings");

  py::enum_<PixelEngine::BufferType>(pixelengine_class, "BufferType")
    .value("RGB", PixelEngine::BufferType::RGB)
    .value("RGBA", PixelEngine::BufferType::RGBA);

  py::enum_<PixelEngine::View::DerivedLevelPixelAlignment>(
    pixelengine_class, "DerivedLevelPixelAlignment")
    .value("CENTER", PixelEngine::View::DerivedLevelPixelAlignment::CENTER)
    .value("LEFT_EDGE", PixelEngine::View::DerivedLevelPixelAlignment::LEFT_EDGE);

  py::class_<PixelEngine::NetworkSettings>(pixelengine_class, "NetworkSettings")
    .def_property("global_initialization",
      (bool (PixelEngine::NetworkSettings::*)() const)
        & PixelEngine::NetworkSettings::globalInitialization,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(bool))
        & PixelEngine::NetworkSettings::globalInitialization,
      "Set if the pixel engine should do global initialization and cleanup")
    .def_property("timeout",
      (size_t(PixelEngine::NetworkSettings::*)() const) & PixelEngine::NetworkSettings::timeout,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(size_t))
        & PixelEngine::NetworkSettings::timeout,
      "Network timeout on requests to avoid the default behaviour of indefinite waiting. 0 means "
      "no timeout.")
    .def_property("verbose_logging",
      (bool (PixelEngine::NetworkSettings::*)() const)
        & PixelEngine::NetworkSettings::verboseLogging,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(bool))
        & PixelEngine::NetworkSettings::verboseLogging,
      "Set verbose logging for the network stack")
    .def_property("certificates",
      (std::string const& (PixelEngine::NetworkSettings::*)() const)
        & PixelEngine::NetworkSettings::certificates,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(std::string const&))
        & PixelEngine::NetworkSettings::certificates,
      "Path to Certificate Authority (CA) bundle")
    .def_property("rate_limit",
      (bool (PixelEngine::NetworkSettings::*)() const) & PixelEngine::NetworkSettings::rateLimiting,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(bool))
        & PixelEngine::NetworkSettings::rateLimiting,
      "Set rate limiting on/off, without rate limiting memory usage will grow and putpixels will "
      "not "
      "block ... default on")
    .def_property("retries_after_delays",
      (std::vector<size_t> const& (PixelEngine::NetworkSettings::*)() const)
        & PixelEngine::NetworkSettings::retriesAfterDelays,
      (PixelEngine::NetworkSettings & (PixelEngine::NetworkSettings::*)(std::vector<size_t> const&))
        & PixelEngine::NetworkSettings::retriesAfterDelays,
      " Define number of retries and delay between retries in seconds");

  py::class_<PixelEngine::CompressionParameters,
    std::shared_ptr<PixelEngine::CompressionParameters>>(
    pixelengine_class, "CompressionParameters");

  py::class_<PixelEngine::WSICompressionParametersBuilder>(
    pixelengine_class, "WSICompressionParametersBuilder")
    .def(py::init<std::vector<size_t> const&>())
    .def("with_num_derived_levels",
      &PixelEngine::WSICompressionParametersBuilder::withNumDerivedLevels,
      "number of derived levels created by the selected pixel transform")
    .def("with_block_size", &PixelEngine::WSICompressionParametersBuilder::withBlockSize,
      "block size (eg. '128x128').")
    .def("with_pixel_transform", &PixelEngine::WSICompressionParametersBuilder::withPixelTransform,
      "pixel transformation (eg. 'legall53').", py::arg("pixelTransform"),
      py::arg("kernel") = std::vector<int16_t>())
    .def("with_compressor", &PixelEngine::WSICompressionParametersBuilder::withCompressor,
      "compressor (eg. 'hulsken2').")
    .def("with_colorspace_transform",
      &PixelEngine::WSICompressionParametersBuilder::withColorspaceTransform,
      "colorspaceTransform (eg. 'RGB2YCoCg').")
    .def("with_bit_depth", &PixelEngine::WSICompressionParametersBuilder::withBitDepth, "bitDepth")
    .def("with_num_threads", &PixelEngine::WSICompressionParametersBuilder::withNumThreads,
      "numThreads")
    .def("with_default_color_intensity",
      &PixelEngine::WSICompressionParametersBuilder::withDefaultColorIntensity,
      "defaultColorIntensity")
    .def("with_quality_preset", &PixelEngine::WSICompressionParametersBuilder::withQualityPreset,
      "quality preset (eg. 'Q2').")
    .def("with_quality", &PixelEngine::WSICompressionParametersBuilder::withQuality,
      "quality in 1 to 100 range (eg. '80') per level starting from base.")
    .def("with_origin", &PixelEngine::WSICompressionParametersBuilder::withOrigin,
      "origin shared between images")
    .def("with_scale", &PixelEngine::WSICompressionParametersBuilder::withScale, "pixel spacing")
    .def("with_downsample_factor",
      &PixelEngine::WSICompressionParametersBuilder::withDownsampleFactor, "downsample factor")
    .def("build", &PixelEngine::WSICompressionParametersBuilder::build);

  py::class_<PixelEngine::SecondaryCaptureCompressionParametersBuilder>(
    pixelengine_class, "SecondaryCaptureCompressionParametersBuilder")
    .def(py::init<std::string const&, uint32_t, uint32_t>())
    .def("with_origin", &PixelEngine::SecondaryCaptureCompressionParametersBuilder::withOrigin,
      "origin shared between images")
    .def("with_scale", &PixelEngine::SecondaryCaptureCompressionParametersBuilder::withScale,
      "pixel spacing")
    .def("build", &PixelEngine::SecondaryCaptureCompressionParametersBuilder::build);

  py::class_<PixelEngine::DataEnvelopes>(pixelengine_class, "DataEnvelopes")
    .def("as_extreme_vertices_model", &PixelEngine::DataEnvelopes::asEVM,
      "Data envelopes as extreme vertices model point set.")
    .def("as_rectangles", &PixelEngine::DataEnvelopes::asRectangles,
      "Data envelopes as set of rectangles.");

  py::class_<PixelEngine::Region, std::shared_ptr<PixelEngine::Region>>(pixelengine_class, "Region")
    .def("__eq__",
      [](PixelEngine::Region& region1, PixelEngine::Region& region2) -> bool {
        return region1.id() == region2.id();
      })
    .def("__lt__",
      [](PixelEngine::Region& region1, PixelEngine::Region& region2) -> bool {
        return region1.id() < region2.id();
      })
    .def("__hash__",
      [](PixelEngine::Region& region1) -> size_t { return std::hash<size_t>{}(region1.id()); })
    .def_property_readonly("ready", &PixelEngine::Region::ready,
      "Check if all a-synchronous (data fetching and optionally rendering) processing finished.")
    .def_property_readonly("range", &PixelEngine::Region::range, "Dimension ranges of the region.")
    .def(
      "get",
      [](PixelEngine::Region& self, array_t<uint8_t>& buffer) {
        auto r = buffer.mutable_unchecked();
        void* data = reinterpret_cast<void*>(r.mutable_data(0));
        size_t arraySize = r.nbytes();
        return self.get(data, arraySize);
      },
      py::return_value_policy::move)
    .def(
      "get",
      [](PixelEngine::Region& self, array_t<int16_t>& buffer) {
        auto r = buffer.mutable_unchecked();
        void* data = reinterpret_cast<void*>(r.mutable_data(0));
        size_t arraySize = r.nbytes();
        return self.get(data, arraySize);
      },
      py::return_value_policy::move)
    .def("draw", &PixelEngine::Region::draw, "Draw region to target.", py::arg("target"));

  py::class_<PyFilterHandle> filterhandle_class(m, "FilterHandle");
  filterhandle_class.def("supported_parameters", &PyFilterHandle::supportedParameters,
    py::return_value_policy::copy, "List of supported parameter names for this filter");

  py::class_<PixelEngine::Level>(pixelengine_class, "Level")
    .def("chain_source_view", &PixelEngine::Level::chainSourceView, "TODO: description",
      py::arg("view"), py::arg("x_shift"), py::arg("y_shift"), py::arg("level_shift"))
    .def("filter_width", &PixelEngine::Level::filterWidth, "TODO: description", py::arg("coord"),
      py::arg("dimensions"));

  py::class_<PixelEngine::View>(pixelengine_class, "View")
    .def("__getitem__", &PixelEngine::View::operator[], py::return_value_policy::reference_internal)
    .def("chain_source_view", &PixelEngine::View::chainSourceView, "TODO: description",
      py::arg("view"), py::arg("x_shift"), py::arg("y_shift"), py::arg("level_shift"))
    .def(
      "request_regions",
      [](PixelEngine::View& self, std::vector<std::vector<size_t>> const& regions,
        bool enableAsyncRendering, std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes
          = self.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("regions"), py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def(
      "request_regions",
      [](PixelEngine::View& self, std::vector<std::vector<size_t>> const& regions,
        PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering,
        std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes = self.requestRegions(
          regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("regions"), py::arg("data_envelopes"),
      py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def_property_readonly("derived_level_pixel_alignment",
      &PixelEngine::View::derivedLevelPixelAlignment, "Alignment of pixels in derived levels")
    .def("dimension_ranges", &PixelEngine::View::dimensionRanges,
      "Ranges of All image dimensions at the specified level as [start:increment:end] triplets.",
      py::arg("level"))
    .def_property_readonly("dimension_names", &PixelEngine::View::dimensionNames,
      "Names of the dimensions of this view.")
    .def_property_readonly("dimension_units", &PixelEngine::View::dimensionUnits,
      "Unit (eg. MicroMeter) of any physical size returned by other methods of this view.")
    .def_property_readonly("dimension_types", &PixelEngine::View::dimensionTypes,
      "Lists of dimension types in the same order as dimension names (eg. Spatial, "
      "color_component).")
    .def_property_readonly(
      "scale", &PixelEngine::View::scale, "Physical pixel spacing of adjacent pixel centers.")
    .def_property_readonly("origin", &PixelEngine::View::origin,
      "Physical distance between origin that is shared between all sub-images in a file.")
    .def_property_readonly("dimension_discrete_values", &PixelEngine::View::dimensionDiscreteValues,
      "Names of discrete values in dimension (eg. 'R', 'G', 'B' for color dimension.")
    .def("data_envelopes", &PixelEngine::View::dataEnvelopes,
      py::return_value_policy::reference_internal,
      "Valid image data envelopes, shapes that encompass the area's that contain valid pixels.",
      py::arg("level"))
    .def_property_readonly("bits_allocated", &PixelEngine::View::bitsAllocated,
      "Number of bits allocated for each sample.")
    .def_property_readonly("bits_stored", &PixelEngine::View::bitsStored,
      "Number of bits actually used for each sample.")
    .def_property_readonly(
      "high_bit", &PixelEngine::View::highBit, "Most significant bit for samples.")
    .def_property_readonly("pixel_representation", &PixelEngine::View::pixelRepresentation,
      "Data representation of the pixel samples. Each sample shall have the same pixel "
      "representation.")
    .def_property_readonly("planar_configuration", &PixelEngine::View::planarConfiguration,
      "Indicates whether the pixel data are encoded color-planar (1) or color-interleaved (0).")
    .def_property_readonly("samples_per_pixel", &PixelEngine::View::samplesPerPixel,
      "Number of samples (color planes) per pixel.")
    .def_property_readonly("id", &PixelEngine::View::id, "Identifier of view.")
    .def_property_readonly(
      "num_derived_levels", &PixelEngine::View::numDerivedLevels, "Number of derived levels.")
    .def_property_readonly(
      "pixel_size", &PixelEngine::View::pixelSize, "Dimensions of base level.");

  py::class_<PyReconstructedView>(pixelengine_class, "ReconstructedView")
    .def("load_default_parameters", &PyReconstructedView::loadDefaultParameters)
    .def(
      "__getitem__", &PyReconstructedView::operator[], py::return_value_policy::reference_internal)
    .def("chain_source_view", &PyReconstructedView::chainSourceView, "TODO: description",
      py::arg("view"), py::arg("x_shift"), py::arg("y_shift"), py::arg("level_shift"))
    .def(
      "add_user_view", [](PyReconstructedView& self) { return PyUserView(self.addChainedView()); },
      "creates a new user view based on this view and chains it after")
    .def(
      "request_regions",
      [](PyReconstructedView& self, std::vector<std::vector<size_t>> const& regions,
        bool enableAsyncRendering, std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes
          = self.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("region"), py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def(
      "request_regions",
      [](PyReconstructedView& self, std::vector<std::vector<size_t>> const& regions,
        PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering,
        std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes = self.requestRegions(
          regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("region"), py::arg("data_envelopes"),
      py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def_property_readonly("dimension_names", &PyReconstructedView::derivedLevelPixelAlignment,
      "Alignment of pixels in derived levels")
    .def("dimension_ranges", &PyReconstructedView::dimensionRanges,
      "Ranges of all image dimensions at the specified level as [start:increment:end] triplets.",
      py::arg("level"))
    .def_property_readonly("dimension_names", &PyReconstructedView::dimensionNames,
      "Names of the dimensions of this view.")
    .def_property_readonly("dimension_units", &PyReconstructedView::dimensionUnits,
      "Unit (eg. MicroMeter) of any physical size returned by other methods of this view.")
    .def_property_readonly("dimension_types", &PyReconstructedView::dimensionTypes,
      "Lists of dimension types in the same order as dimension names (eg. Spatial, "
      "color_component).")
    .def_property_readonly(
      "scale", &PyReconstructedView::scale, "Physical pixel spacing of adjacent pixel centers.")
    .def_property_readonly("origin", &PyReconstructedView::origin,
      "Physical distance between origin that is shared between all sub-images in a file.")
    .def_property_readonly("dimension_discrete_values",
      &PyReconstructedView::dimensionDiscreteValues,
      "Names of discrete values in dimension (eg. 'R', 'G', 'B' for color dimension).")
    .def("data_envelopes", &PyReconstructedView::dataEnvelopes,
      py::return_value_policy::reference_internal,
      "Valid image data envelopes, shapes that encompass the area's that contain valid pixels.",
      py::arg("level"))
    .def_property_readonly("bits_allocated", &PyReconstructedView::bitsAllocated,
      "Number of bits allocated for each sample.")
    .def_property_readonly("bits_stored", &PyReconstructedView::bitsStored,
      "Number of bits actually used for each sample.")
    .def_property_readonly(
      "high_bit", &PyReconstructedView::highBit, "Most significant bit for samples.")
    .def_property_readonly("pixel_representation", &PyReconstructedView::pixelRepresentation,
      "Data representation of the pixel samples. Each sample shall have the same pixel "
      "representation.")
    .def_property_readonly("planar_configuration", &PyReconstructedView::planarConfiguration,
      "Indicates whether the pixel data are encoded color-planar (1) or color-interleaved (0).")
    .def_property_readonly("samples_per_pixel", &PyReconstructedView::samplesPerPixel,
      "Number of samples (color planes) per pixel.")
    .def_property_readonly("id", &PyReconstructedView::id, "Identifier of view.")
    .def_property_readonly(
      "num_derived_levels", &PyReconstructedView::numDerivedLevels, "Number of derived levels.")
    .def_property_readonly(
      "pixel_size", &PyReconstructedView::pixelSize, "Dimensions of base level.");

  py::class_<PySourceView>(pixelengine_class, "SourceView")
    .def("load_default_parameters", &PySourceView::loadDefaultParameters)
    .def("truncation", &PySourceView::truncation, "Chop of the digits to zero.", py::arg("enable"),
      py::arg("rounding"), py::arg("truncationlevel"))
    .def("__getitem__", &PySourceView::operator[], py::return_value_policy::reference_internal)
    .def("chain_source_view", &PySourceView::chainSourceView, "TODO: description", py::arg("view"),
      py::arg("x_shift"), py::arg("y_shift"), py::arg("level_shift"))
    .def(
      "add_user_view", [](PySourceView& self) { return PyUserView(self.addChainedView()); },
      "creates a new user view based on this view and chains it after")
    .def(
      "request_regions",
      [](PySourceView& self, std::vector<std::vector<size_t>> const& regions,
        bool enableAsyncRendering, std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes
          = self.requestRegions(regions, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("region"), py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def(
      "request_regions",
      [](PySourceView& self, std::vector<std::vector<size_t>> const& regions,
        PixelEngine::DataEnvelopes const& dataEnvelopes, bool enableAsyncRendering,
        std::vector<size_t> const& backgroundColor,
        PixelEngine::BufferType bufferType) -> py::list {
        auto cppRes = self.requestRegions(
          regions, dataEnvelopes, enableAsyncRendering, backgroundColor, bufferType);
        py::list pyResult;
        for ( std::shared_ptr<PixelEngine::Region> const& item : cppRes )
        {
          auto pyObj = py::cast(item);
          pyResult.append(pyObj);
          py::detail::keep_alive_impl(pyObj, py::cast(&self));
        }
        return pyResult;
      },
      "Request an image region.", py::arg("region"), py::arg("data_envelopes"),
      py::arg("enable_async_rendering") = true,
      py::arg("background_color") = std::vector<size_t>({ 0, 0, 0 }),
      py::arg("buffer_type") = PixelEngine::BufferType::RGB)
    .def("derived_level_pixel_alignment", &PySourceView::derivedLevelPixelAlignment,
      "Alignment of pixels in derived levels")
    .def("dimension_ranges", &PySourceView::dimensionRanges,
      "Ranges of all image dimensions at the specified level as [start:increment:end] triplets.",
      py::arg("level"))
    .def_property_readonly(
      "dimension_names", &PySourceView::dimensionNames, "Names of the dimensions of this view.")
    .def_property_readonly("dimension_units", &PySourceView::dimensionUnits,
      "Unit (eg. MicroMeter) of any physical size returned by other methods of this view.")
    .def_property_readonly("dimension_types", &PySourceView::dimensionTypes,
      "Lists of dimension types in the same order as dimension names (eg. Spatial, "
      "color_component).")
    .def_property_readonly(
      "scale", &PySourceView::scale, "Physical pixel spacing of adjacent pixel centers.")
    .def_property_readonly("origin", &PySourceView::origin,
      "Physical distance between origin that is shared between all sub-images in a file.")
    .def_property_readonly("dimension_discrete_values", &PySourceView::dimensionDiscreteValues,
      "Names of discrete values in dimension (eg. 'R', 'G', 'B' for color dimension).")
    .def("data_envelopes", &PySourceView::dataEnvelopes,
      py::return_value_policy::reference_internal,
      "Valid image data envelopes, shapes that encompass the area's that contain valid pixels.",
      py::arg("level"))
    .def_property_readonly(
      "bits_allocated", &PySourceView::bitsAllocated, "Number of bits allocated for each sample.")
    .def_property_readonly(
      "bits_stored", &PySourceView::bitsStored, "Number of bits actually used for each sample.")
    .def_property_readonly("high_bit", &PySourceView::highBit, "Most significant bit for samples.")
    .def_property_readonly("pixel_representation", &PySourceView::pixelRepresentation,
      "Data representation of the pixel samples. Each sample shall have the same pixel "
      "representation.")
    .def_property_readonly("planar_configuration", &PySourceView::planarConfiguration,
      "Indicates whether the pixel data are encoded color-planar (1) or color-interleaved (0).")
    .def_property_readonly("samples_per_pixel", &PySourceView::samplesPerPixel,
      "Number of samples (color planes) per pixel.")
    .def_property_readonly("id", &PySourceView::id, "Identifier of view.")
    .def_property_readonly(
      "num_derived_levels", &PySourceView::numDerivedLevels, "Number of derived levels.")
    .def_property_readonly("pixel_size", &PySourceView::pixelSize, "Dimensions of base level.");

  py::class_<PyDisplayView, PySourceView>(pixelengine_class, "DisplayView")
    .def_property("sharpness", (double (PyDisplayView::*)() const) & PyDisplayView::sharpness,
      (void (PyDisplayView::*)(double)) & PyDisplayView::sharpness, "sharpening gain")
    .def_property("contrast_clip_limit",
      (double (PyDisplayView::*)() const) & PyDisplayView::contrastClipLimit,
      (void (PyDisplayView::*)(double)) & PyDisplayView::contrastClipLimit, "CLAHE clipLimit")
    .def_property("color_correction_gamma",
      (double (PyDisplayView::*)() const) & PyDisplayView::colorCorrectionGamma,
      (void (PyDisplayView::*)(double)) & PyDisplayView::colorCorrectionGamma,
      "Set color correction gamma value")
    .def_property("color_correction_black_point",
      (double (PyDisplayView::*)() const) & PyDisplayView::colorCorrectionBlackPoint,
      (void (PyDisplayView::*)(double)) & PyDisplayView::colorCorrectionBlackPoint,
      "Set color correction black point")
    .def_property("color_correction_white_point",
      (double (PyDisplayView::*)() const) & PyDisplayView::colorCorrectionWhitePoint,
      (void (PyDisplayView::*)(double)) & PyDisplayView::colorCorrectionWhitePoint,
      "Set color correction white point")
    .def_property("color_gain", (double (PyDisplayView::*)() const) & PyDisplayView::colorGain,
      (void (PyDisplayView::*)(double)) & PyDisplayView::colorGain, "image brightness");

  py::class_<PyUserView, PixelEngine::View>(pixelengine_class, "UserView")
    .def(
      "add_filter",
      [](PyUserView& self, std::string const& filterName) {
        return PyFilterHandle(self.addFilter(filterName));
      },
      "Add filter based on the given name", py::arg("filterName"))
    .def(
      "filter_parameter_double",
      [](PyUserView& self, PyFilterHandle& filter, std::string const& name, double value) {
        self.filterParameterDouble(filter.ref(), name, value);
      },
      "set a filter parameter of type \"double\"", py::arg("filter"), py::arg("parameter name"),
      py::arg("parameter value"))
    .def(
      "filter_parameter_matrix3x3",
      [](PyUserView& self, PyFilterHandle& filter, std::string const& name,
        std::array<double, 9> const& value) {
        self.filterParameterMatrix3x3(filter.ref(), name, value);
      },
      "set a filter parameter of type \"Matrix3x3\"", py::arg("filter"), py::arg("parameter name"),
      py::arg("parameter value"));

  py::class_<PixelEngine::SubImage>(pixelengine_class, "SubImage")
    .def("include_input_region", &PixelEngine::SubImage::includeInputRegion,
      "Includes the region specified")
    .def("preallocate_pixels", &PixelEngine::SubImage::preallocatePixels,
      "Declare order and regions that will provided using putPixel calls later")
    .def("put_pixels",
      [](PixelEngine::SubImage& self, array_t<uint8_t> const& buffer,
        std::vector<size_t> const& vectorization, size_t colorDimension, size_t level) {
        auto r = buffer.unchecked();
        void const* data = reinterpret_cast<void const*>(r.data(0));
        self.putPixels(data, typeid(uint8_t), vectorization, colorDimension, level);
      })
    .def("put_pixels",
      [](PixelEngine::SubImage& self, array_t<int16_t> const& buffer,
        std::vector<size_t> const& vectorization, size_t colorDimension, size_t level) {
        auto r = buffer.unchecked();
        void const* data = reinterpret_cast<void const*>(r.data(0));
        self.putPixels(data, typeid(int16_t), vectorization, colorDimension, level);
      })

    // views on the image for pixel/meta data retrieval
    .def_property_readonly(
      "reconstructed_view",
      [](PixelEngine::SubImage& self) { return PyReconstructedView(self.reconstructedView()); },
      "Returns the instance of reconstructed view.")
    .def_property_readonly(
      "source_view", [](PixelEngine::SubImage& self) { return PySourceView(self.sourceView()); },
      "Returns the instance of source view.")
    .def_property_readonly("has_display_view", &PixelEngine::SubImage::hasDisplayView,
      "flag indicating availability of display view that contains image post-processing")
    .def_property_readonly(
      "display_view", [](PixelEngine::SubImage& self) { return PyDisplayView(self.displayView()); },
      "Returns the instance of display view.")
    // read blocks (raw)
    .def("block_size", &PixelEngine::SubImage::blockSize,
      "The WSI image is divided into multiple tile regions. These tiles are in turn com- pressed "
      "and stored in iSyntax format to allow region based access. blockSize re- fers to the "
      "dimension of the tile which was used for creating the iSyntax file.",
      py::arg("template_id") = 0)
    .def("block_pos", &PixelEngine::SubImage::blockPos, "Returns coordinate of a block.",
      py::arg("block_ind"))
    .def(
      "ordered_block_coordinates",
      [](PixelEngine::SubImage& self) { return self.orderedBlockCoordinates(); },
      "returns the coordinates of all blocks as expected by the pixel engine")
    .def(
      "block_dimension_names",
      [](PixelEngine::SubImage& self) { return self.blockDimensionNames(); },
      " names of dimensions in coordinates returned by ordered_block_coordinates")
    .def(
      "read_block",
      [](PixelEngine::SubImage& self, array_t<uint8_t>& buffer) {
        auto r = buffer.mutable_unchecked();
        void* data = reinterpret_cast<void*>(r.mutable_data(0));
        size_t arraySize = r.nbytes();
        return self.readBlock(data, arraySize);
      },
      "Reads next block data")
    .def(
      "read_block",
      [](
        PixelEngine::SubImage& self, array_t<uint8_t>& buffer, std::vector<size_t> const& indices) {
        auto r = buffer.mutable_unchecked();
        void* data = reinterpret_cast<void*>(r.mutable_data(0));
        size_t arraySize = r.nbytes();
        return self.readBlock(data, arraySize, indices);
      },
      "Reads block data for given coordinates.")
    .def("put_block",
      [](PixelEngine::SubImage& self, array_t<uint8_t> const& buffer, size_t block_size) {
        auto r = buffer.unchecked();
        auto data = reinterpret_cast<void const*>(r.data(0));
        self.putBlock(data, block_size);
      })

    // image properties
    .def_property_readonly("image_type", &PixelEngine::SubImage::imageType,
      "Get image type (eg. WSI, MACROIMAGE, LABELIMAGE).")
    .def_property_readonly("pixel_transform", &PixelEngine::SubImage::pixelTransform,
      "Represents the pixel transform which was used for creating the iSyntax file.")
    .def_property_readonly("pixel_transform_kernel", &PixelEngine::SubImage::pixelTransformKernel,
      "Represents the downsample kernel which was used for creating the iSyntax file.")
    .def_property_readonly("quality_preset", &PixelEngine::SubImage::qualityPreset,
      "Returns iSyntax quality preset(Q0 or Q1 or Q2).")
    .def_property_readonly("quality", &PixelEngine::SubImage::quality, "Returns iSyntax quality.")
    .def_property_readonly(
      "compressor", &PixelEngine::SubImage::compressor, "Return type of compressor.")
    .def_property_readonly("colorspace_transform", &PixelEngine::SubImage::colorspaceTransform,
      "Returns Color space transform id (None or RGB2YCoCg or RGB10Packed2RGB or "
      "RGB10Packed2YCoCg).")
    .def_property_readonly(
      "num_tiles", &PixelEngine::SubImage::numTiles, "Returns number of tiles in an Image.")
    .def_property("icc_profile",
      (std::string const& (PixelEngine::SubImage::*)() const) & PixelEngine::SubImage::iccProfile,
      (void (PixelEngine::SubImage::*)(std::string const&)) & PixelEngine::SubImage::iccProfile,
      "ICC Profile")
    .def_property_readonly("icc_matrix", &PixelEngine::SubImage::iccMatrix,
      "ICC matrix (3x3) containing affine transformation for color correction caclulated from the "
      "ICC profile")
    .def_property(
      "image_data",
      [](PixelEngine::SubImage const& self) {
        std::vector<uint8_t> const& val = self.imageData();
#if defined(PY_MAJOR_VERSION) && (PY_MAJOR_VERSION >= 3)
        PyObject* mView = PyMemoryView_FromMemory(
          reinterpret_cast<char*>(const_cast<uint8_t*>(val.data())), val.size(), PyBUF_READ);
        if ( !PyMemoryView_Check(mView) )
          throw std::runtime_error("PixelEngine error: could not get memoryview.");
        return py::reinterpret_borrow<py::object>(mView);
#else
  Py_buffer buffer;
  int res = PyBuffer_FillInfo(
    &buffer, 0, const_cast<uint8_t*>(val.data()), val.size(), true, PyBUF_CONTIG_RO);
  if ( res == -1 )
    throw std::runtime_error(
      "PixelEngine error: get property could not get a C contiguous buffer object.");
  return py::reinterpret_borrow<py::object>(PyMemoryView_FromBuffer(&buffer));
#endif
      },
      [](PixelEngine::SubImage& self, py::object memView) {
        PyObject* mView = memView.ptr();
        if ( !PyMemoryView_Check(mView) )
          throw std::runtime_error(
            "PixelEngine error: set property requires a memoryview object as input.");
        Py_buffer* buffer = PyMemoryView_GET_BUFFER(mView);
        if ( !PyBuffer_IsContiguous(buffer, 'C') )
          throw std::runtime_error("PixelEngine error: could not get memoryview buffer.");
        std::vector<uint8_t> val(
          static_cast<uint8_t*>(buffer->buf), static_cast<uint8_t*>(buffer->buf) + buffer->len);
        self.imageData(val);
      },
      "Returns image data for secondary capture images like Label and Macro image.")
    .def_property("lossy_image_compression",
      (std::string const& (PixelEngine::SubImage::*)() const)
        & PixelEngine::SubImage::lossyImageCompression,
      (void (PixelEngine::SubImage::*)(std::string const&))
        & PixelEngine::SubImage::lossyImageCompression,
      "Denotes if the image is compressed as lossy or lossless.")
    .def_property("lossy_image_compression_ratio",
      (double (PixelEngine::SubImage::*)() const)
        & PixelEngine::SubImage::lossyImageCompressionRatio,
      (void (PixelEngine::SubImage::*)(double)) & PixelEngine::SubImage::lossyImageCompressionRatio,
      "DICOM Lossy Image Compression ratio.")
    .def_property("lossy_image_compression_method",
      (std::string const& (PixelEngine::SubImage::*)() const)
        & PixelEngine::SubImage::lossyImageCompressionMethod,
      (void (PixelEngine::SubImage::*)(std::string const&))
        & PixelEngine::SubImage::lossyImageCompressionMethod,
      "DICOM Lossy Image Compression Method.")
    .def_property("color_linearity",
      (std::string const& (PixelEngine::SubImage::*)() const)
        & PixelEngine::SubImage::colorLinearity,
      (void (PixelEngine::SubImage::*)(std::string const&)) & PixelEngine::SubImage::colorLinearity,
      "DICOM Lossy Image Compression Method.")
    .def_property("scan_regions_determination",
      (std::string const& (PixelEngine::SubImage::*)() const)
        & PixelEngine::SubImage::scanRegionsDetermination,
      (void (PixelEngine::SubImage::*)(std::string const&))
        & PixelEngine::SubImage::scanRegionsDetermination,
      "Scan protocol used when scanning the image");

  py::class_<PixelEngine::ISyntaxFacade>(pixelengine_class, "ISyntaxFacade")
    // Open file (url or stream)
    .def(
      "open",
      [](PixelEngine::ISyntaxFacade& self, std::string const& url, std::string const& container,
        std::string const& mode, std::string const& cacheName) {
        std::ios_base::openmode openmode;
        if ( mode == "r" )
          openmode = std::ios::in | std::ios::binary;
        else if ( mode == "w" )
          openmode = std::ios::out | std::ios::binary;
        else
          throw std::runtime_error("mode needs to be either 'r' or 'w'");
        self.open(url, container, openmode, cacheName);
      },
      "Open isyntax image with URL, container name, mode (Read = 'r' and Write = 'w') and cache "
      "folder path or cache file path.",
      py::arg("url"), py::arg("container_name") = std::string(""),
      py::arg("mode") = std::string("r"), py::arg("cache_name") = std::string(""))
    .def("add_sub_image", &PixelEngine::ISyntaxFacade::addSubImage,
      "Add sub image (WSI or Secondary-Capture).", py::return_value_policy::reference_internal)
    // sub-images: eg: WSI, MACROIMAGE, LABELIMAGE
    .def_property_readonly("num_images", &PixelEngine::ISyntaxFacade::numImages,
      "Number of images (The iSyntax data model represents the slide as three images: Macro, Label "
      " and WSI).")
    .def("__getitem__",
      (PixelEngine::SubImage & (PixelEngine::ISyntaxFacade::*)(size_t))
        & PixelEngine::ISyntaxFacade::operator[],
      py::return_value_policy::reference_internal)
    .def("__getitem__",
      (PixelEngine::SubImage & (PixelEngine::ISyntaxFacade::*)(std::string const& type))
        & PixelEngine::ISyntaxFacade::operator[],
      py::return_value_policy::reference_internal)

    // call after subimages are initialized, before putting pixels
    .def("finalize_geometry_and_properties",
      &PixelEngine::ISyntaxFacade::finalizeGeometryAndProperties)

    // properties
    .def_property_readonly("isyntax_file_version", &PixelEngine::ISyntaxFacade::iSyntaxFileVersion,
      "Returns isyntax file version.")
    .def_property_readonly("id", &PixelEngine::ISyntaxFacade::id)
    .def_property("barcode",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::barcode,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::barcode,
      "Barcode number for the whole slide image.")
    .def_property("scanner_calibration_status",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::scannerCalibrationStatus,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::scannerCalibrationStatus,
      "Get Scanner calibration Status. 'OK' or 'NOT OK'.")
    .def_property("software_versions",
      (std::vector<std::string> const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::softwareVersions,
      (void (PixelEngine::ISyntaxFacade::*)(std::vector<std::string> const&))
        & PixelEngine::ISyntaxFacade::softwareVersions,
      "Manufacturer's designation of software version of the equipment that produced the "
      "composite instances.")
    .def_property("derivation_description",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::derivationDescription,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::derivationDescription,
      "A text description of how this image was derived. Description contains UFS version, Quality "
      "level, wavelet transform type, compression type.")
    .def_property("acquisition_datetime",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::acquisitionDateTime,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::acquisitionDateTime,
      "The Date Time common data type which indicates a concatenated date-time ASCII string in "
      "the format-YYYYMMDDHHMMSS.FFFFFF&ZZZZ.")
    .def_property("manufacturer",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::manufacturer,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::manufacturer,
      "Manufacturer of the equipment that produced the composite instances.")
    .def_property("model_name",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::modelName,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::modelName,
      "Manufacturer's model name of the equipment that produced the composite instances.")
    .def_property("device_serial_number",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::deviceSerialNumber,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::deviceSerialNumber,
      "Manufacturer's serial number of the equipment that produced the composite instances.")
    .def_property("scanner_rack_number",
      (uint16_t(PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::scannerRackNumber,
      (void (PixelEngine::ISyntaxFacade::*)(uint16_t))
        & PixelEngine::ISyntaxFacade::scannerRackNumber,
      "Number of the rack that the glass slide was placed into when the iSyntax file was created.")
    .def_property("scanner_slot_number",
      (uint16_t(PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::scannerSlotNumber,
      (void (PixelEngine::ISyntaxFacade::*)(uint16_t))
        & PixelEngine::ISyntaxFacade::scannerSlotNumber,
      "Number of the slot that the glass slide was placed in when the iSyntax file was created.")
    .def_property("scanner_operator_id",
      (std::string const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::scannerOperatorId,
      (void (PixelEngine::ISyntaxFacade::*)(std::string const&))
        & PixelEngine::ISyntaxFacade::scannerOperatorId,
      "Operator id of the scanner.")
    .def_property("scanner_rack_priority",
      (uint16_t(PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::scannerRackPriority,
      (void (PixelEngine::ISyntaxFacade::*)(uint16_t))
        & PixelEngine::ISyntaxFacade::scannerRackPriority,
      "Priority state of the rack the glass slide was placed in.")
    .def_property("date_of_last_calibration",
      (std::vector<std::string> const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::dateOfLastCalibration,
      (void (PixelEngine::ISyntaxFacade::*)(std::vector<std::string> const&))
        & PixelEngine::ISyntaxFacade::dateOfLastCalibration,
      "Date when the image acquisition device calibration was last changed in any way.")
    .def_property("time_of_last_calibration",
      (std::vector<std::string> const& (PixelEngine::ISyntaxFacade::*)() const)
        & PixelEngine::ISyntaxFacade::timeOfLastCalibration,
      (void (PixelEngine::ISyntaxFacade::*)(std::vector<std::string> const&))
        & PixelEngine::ISyntaxFacade::timeOfLastCalibration,
      "Time when the image acquisition device calibration was last changed in any way.")

    .def_property_readonly("is_philips", &PixelEngine::ISyntaxFacade::isPhilips,
      "Returns True if the scanner is manufactured by Philips.")
    .def_property_readonly("is_UFS", &PixelEngine::ISyntaxFacade::isUFS,
      "Returns True if the slide is scanned by Philips UFS scanner.")
    .def_property_readonly("is_UFSb", &PixelEngine::ISyntaxFacade::isUFSb)
    .def_property_readonly("is_UVS", &PixelEngine::ISyntaxFacade::isUVS)

    // Close the image and free resources
    .def("close", &PixelEngine::ISyntaxFacade::close, "Close an image and release resources.")
    .def("abort", &PixelEngine::ISyntaxFacade::abort, "Stop storing/reading image data.")
    .def_property_readonly("remainingPixelsToEncode",
      &PixelEngine::ISyntaxFacade::remainingPixelsToEncode,
      "Returns the number of pixels to be encoded until the slide is ready.");

  m.attr("__version__") = PixelEngine::version();
}
