# Unit tests for Antichecked Exceptions for Python
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

from antichecked import exceptions

class expect:
    def __init__(self, exc, *, cause, context):
        self.exc = exc
        self.cause = cause or type(None)
        self.context = context or type(None)

    def __enter__(self):
        pass

    def __exit__(self, exc_ty, exc_val, exc_tb):
        assert exc_ty is self.exc
        assert type(exc_val.__cause__) is self.cause
        assert type(exc_val.__context__) is self.context
        return True

def foo(i):
    with exceptions(ValueError) as r:
        try:
            x = int(i)
        except ValueError:
            # re-raise ValueError from int()
            raise r
        else:
            if x < 0:
                # attempt to raise r without a context
                # (should turn into RuntimeError, just like bare raise)
                raise r
            # this raises ValueError if x is not 1, and it becomes wrapped in
            # RuntimeError
            x, = [x]*x

def test_foo():
    # ValueError from int() passes through (re-raised), context/cause is None
    with expect(ValueError, cause=None, context=None):
        foo("false")
    # ValueError from unpacking gets wrapped, cause and context are ValueError
    with expect(RuntimeError, cause=ValueError, context=ValueError):
        foo("10")
    # raise r without context becomes RuntimeError
    with expect(RuntimeError, cause=None, context=None):
        foo("-10")
    # "1" gets accepted and doesn't raise anything
    foo("1")

def bar():
    with exceptions(ValueError) as r:
        raise r

def test_bar():
    with expect(RuntimeError, cause=None, context=None):
        bar()

def fake_gen():
    with exceptions(StopIteration) as r:
        next(iter([]))

def test_fake_gen():
    # actual generators don't use RuntimeError but we have no way of testing that
    with expect(RuntimeError, cause=StopIteration, context=StopIteration):
        fake_gen()

def baz(i):
    with exceptions(ValueError) as r:
        try:
            x = int(i)
        except ValueError:
            # raise new exception with context
            raise r(TypeError)
        else:
            if x < 0:
                # raise a new ValueError
                raise r(ValueError)
            try:
                x, = [x]*x
            except ValueError as e:
                # raise with cause
                raise r(TypeError) from e

def test_baz():
    # ValueError from int() becomes TypeError with context
    with expect(TypeError, cause=None, context=ValueError):
        baz("false")
    # raise TypeError with cause and context being ValueError
    with expect(TypeError, cause=ValueError, context=ValueError):
        baz("10")
    # raise ValueError through antichecked exceptions
    with expect(ValueError, cause=None, context=None):
        baz("-10")
    # "1" gets accepted and doesn't raise anything
    baz("1")


def test_all():
    test_foo()
    test_bar()
    test_fake_gen()
    test_baz()

if __name__ == "__main__":
    test_all()
