﻿#include "stdafx.h"
#include "Errors.h"
#include <stdarg.h>


// ************************************************************************************************************************************
Error::Error( const Error& r )
: m_what(r.m_what)
{
}


// ************************************************************************************************************************************
Error::Error( const char* format, ... )
{
    char buffer[800];

    va_list args;
    va_start(args, format);

    std::snprintf(buffer, 800, format, args);

    va_end(args);

    m_what = buffer;
}


// ************************************************************************************************************************************
const char* Error::what() const noexcept
{
    return m_what.c_str();
}
