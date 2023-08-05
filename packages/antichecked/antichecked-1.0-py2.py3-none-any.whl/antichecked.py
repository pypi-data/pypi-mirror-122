# Antichecked Exceptions for Python
# Copyright (c) 2021 Soni L.
#
# Permission is hereby granted, free of charge, to any person ("You") obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# This license shall be void if You bring a copyright lawsuit, related or
# unrelated to the Software, against any of the copyright holders.
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Antichecked exceptions for Python.

This package implements antichecked exceptions. They're analogous to the
reverse of checked exceptions, that's why they're called antichecked.

Just ``from antichecked import exceptions`` and you're ready to go!
"""

__version__ = '1.0'

class _hack:
    def __init__(self, ctx):
        self.ctx = ctx

    def __enter__(self):
        pass

    def __exit__(self, exc_ty, exc_val, exc_tb):
        exc_val.__context__ = self.ctx

class exceptions:
    """A context manager for antichecked exceptions.

    Antichecked exceptions are the reverse of checked exceptions: rather than
    requiring the caller to catch the exceptions, they actively check that
    your function/block actually intended to raise them.

    Examples:

        >>> from antichecked import exceptions

        Intercepting exceptions::

        >>> with exceptions(StopIteration) as r:
        ...     raise StopIteration
            RuntimeError

        Raising exceptions::

        >>> with exceptions(StopIteration) as r:
        ...     raise r(StopIteration)
            StopIteration

        Adding a cause::

        >>> with exceptions(StopIteration) as r:
        ...     raise r(StopIteration) from ValueError()
            StopIteration from ValueError

        Similarly, re-raising exceptions is done with ``raise r``.
    """

    def __init__(self, *args):
        """Creates an antichecked exception context for the given exceptions.

        Args:
            Accepts an arbitrary amount of exception types.
        """
        # each context manager gets an unique exception type
        class WrappedError(Exception):
            def __init__(self, exc=None):
                if isinstance(exc, BaseException) or exc is None:
                    self.value = exc
                else:
                    self.value = exc()
        self._exceptions = args
        self._error = WrappedError

    def __enter__(self):
        return self._error

    def __exit__(self, exc_ty, exc_val, exc_tb):
        if exc_ty is None:
            return
        if exc_ty is self._error:
            # handle `raise r(exc)` similar to `raise exc`
            if exc_val.value is not None:
                exc = exc_val.value
                exc.__cause__ = exc_val.__cause__
                exc.__suppress_context__ = exc_val.__suppress_context__
                with _hack(exc_val.__context__):
                    raise exc.with_traceback(exc_tb)
            # `raise r from foo` is unhandled, as `raise from foo` is not
            # valid python. TODO make this case a RuntimeError.
            pass
            # handle `raise r` similar to `raise`
            if exc_val.__context__ is None:
                with _hack(None):
                    exc = RuntimeError("No active exception to re-raise")
                    raise exc.with_traceback(exc_tb)
            with _hack(exc_val.__context__.__context__):
                raise exc_val.__context__
        if any(issubclass(exc_ty, e) for e in self._exceptions):
            # handle this similar to StopIteration in generators
            raise RuntimeError("Antichecked exception raised") from exc_val
