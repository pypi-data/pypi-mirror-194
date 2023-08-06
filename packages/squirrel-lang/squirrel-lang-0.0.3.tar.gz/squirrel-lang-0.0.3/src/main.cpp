#include <pybind11/pybind11.h>
#include <codecvt>
#include "nutcracker/stdafx.h"
#include "nutcracker/NutScript.h"
#include <squirrel.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)


namespace py = pybind11;

py::bytes decompile(std::string bytecode) {
    std::stringbuf buff;
    int size = bytecode.length();
    buff.sputn(bytecode.c_str(), size);
    if (!size) {
        throw pybind11::value_error("empty bytecode! please valid input.");
    }

    NutScript script;
    try {
        script.LoadFromStream(&buff, size);
    }
    catch (std::exception& ex)
    {
        throw py::value_error(ex.what());
    }

    std::wstringstream outstream;
    try {
        script.GetMain().GenerateBodySource(0, outstream);
        std::wstring_convert<std::codecvt_utf8<wchar_t>> conv;
        auto out = conv.to_bytes(outstream.str());
        return py::bytes(out);
    }
    catch (std::exception& ex) {
        throw py::value_error(ex.what());
    }
    throw py::value_error("invalid bytecode: \n" + bytecode);
}


SQInteger write_stringbuf(SQUserPointer output,SQUserPointer source,SQInteger size)
{
    return ((std::stringbuf*)output)->sputn((const char*)source, size);
}


py::bytes compile(std::string sourcecode) {
    HSQUIRRELVM v;
    v=sq_open(1024);
    sq_pushroottable(v);

    if(!SQ_SUCCEEDED(sq_compilebuffer(v, sourcecode.c_str(), sourcecode.length(), _SC("interactive console"), SQTrue))) {
        throw py::value_error("invalid sourcecode, failed to compile");
    }

    std::stringbuf buff;
    if(!SQ_SUCCEEDED(sq_writeclosure(v,write_stringbuf, (SQUserPointer)&buff))) {
        throw py::value_error("failed serialize closure");
    }
    sq_close(v);
    return py::bytes(buff.str());
}


PYBIND11_MODULE(nutcracker, m) {
    m.doc() = R"pbdoc(
        NutCracker - Squirrel-Lang bytecode cracker, used to decompile .cnut bytecode
        -----------------------

        .. currentmodule:: nutcracker

        .. autosummary::
           :toctree: _generate

           decompile
    )pbdoc";

    m.def("decompile", &decompile, R"pbdoc(
        decompile Squirrel-Lang bytecode(.cnut) to .nut

        Usage:
        with open("*.cnut", mode="rb") as fh:
            nut = nutcracker.decompile(fh.read())
    )pbdoc"), py::arg("bytecode");

    m.def("compile", &compile, R"pbdoc(
        compile Squirrel-Lang sourcecode(.nut) to .cnut

        Usage:
        with open("*.nut", mode="r") as fh:
            cnut = nutcracker.sourcecode(fh.read())
    )pbdoc"), py::arg("sourcecode");


#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif

m.attr("__author__") = "shabbywu<shabbywu@qq.com>";
}
