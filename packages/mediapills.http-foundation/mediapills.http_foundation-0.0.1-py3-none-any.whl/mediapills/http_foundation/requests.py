# Copyright (c) 2021-2021 Mediapills HttpFoundation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import abc
from enum import Enum

METHOD_GET = "GET"

METHOD_HEAD = "HEAD"

METHOD_POST = "POST"

METHOD_PURGE = "PURGE"

METHOD_PUT = "PUT"

METHOD_DELETE = "DELETE"

METHOD_CONNECT = "CONNECT"

METHOD_OPTIONS = "OPTIONS"

METHOD_PATCH = "PATCH"

METHOD_TRACE = "TRACE"

"""HTTP defined request methods set."""
METHODS = frozenset(  # dead: disable
    [
        METHOD_GET,
        METHOD_HEAD,
        METHOD_POST,
        METHOD_PURGE,
        METHOD_PUT,
        METHOD_DELETE,
        METHOD_CONNECT,
        METHOD_OPTIONS,
        METHOD_PATCH,
        METHOD_TRACE,
    ]
)


class HTTPRequestMethod(Enum):  # dead: disable
    """Enumerated HTTP method constants."""

    GET = METHOD_GET  # dead: disable
    HEAD = METHOD_HEAD  # dead: disable
    POST = METHOD_POST  # dead: disable
    PURGE = METHOD_PURGE  # dead: disable
    PUT = METHOD_PUT  # dead: disable
    DELETE = METHOD_DELETE  # dead: disable
    CONNECT = METHOD_CONNECT  # dead: disable
    OPTIONS = METHOD_OPTIONS  # dead: disable
    PATCH = METHOD_PATCH  # dead: disable
    TRACE = METHOD_TRACE  # dead: disable


class BaseRequest(metaclass=abc.ABCMeta):  # dead: disable
    """Request content made by a client, to a named host."""

    pass
