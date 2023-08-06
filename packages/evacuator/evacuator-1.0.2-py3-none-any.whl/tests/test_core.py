import logging

import pytest

from evacuator import NeedEvacuation, evacuator


def test_core_decorator():
    @evacuator
    def main1():
        """doc"""
        raise NeedEvacuation("abc")

    with pytest.raises(SystemExit, match="125"):
        main1()

    assert main1.__doc__ == "doc"


def test_core_decorator_brackets():
    @evacuator()
    def main2():
        """doc"""
        raise NeedEvacuation("abc")

    with pytest.raises(SystemExit, match="125"):
        main2()

    assert main2.__doc__ == "doc"


def test_core_decorator_args():
    @evacuator()
    def main(arg, kwarg: int = None, *args, **kwargs):
        raise NeedEvacuation(f"arg={arg} kwarg={kwarg} args={args} kwargs={kwargs}")

    with pytest.raises(SystemExit, match="125"):
        main(1, 2, 3, key=4)


def test_core_decorator_exception():
    @evacuator(exception=RuntimeError)
    def main():
        raise RuntimeError("abc")

    with pytest.raises(SystemExit, match="125"):
        main()


def test_core_decorator_multiple_exceptions():
    @evacuator(exception=(RuntimeError, ValueError))
    def main():
        raise ValueError("abc")

    with pytest.raises(SystemExit, match="125"):
        main()


def test_core_decorator_exit_code():
    @evacuator(exit_code=32)
    def main():
        raise NeedEvacuation("abc")

    with pytest.raises(SystemExit):
        main()


def test_core_decorator_nothing_raised():
    @evacuator(exit_code=32)
    def main():
        logging.debug("abc")

    main()


def test_core_decorator_exception_not_match():
    @evacuator
    def main():
        raise RuntimeError("abc")

    with pytest.raises(RuntimeError, match="abc"):
        main()


def test_core_context():
    with pytest.raises(SystemExit, match="125"):
        with evacuator():
            raise NeedEvacuation("abc")


def test_core_context_exception():
    with pytest.raises(SystemExit, match="125"):
        with evacuator(exception=RuntimeError):
            raise RuntimeError("abc")


def test_core_context_multiple_exceptions():
    with pytest.raises(SystemExit, match="125"):
        with evacuator(exception=(RuntimeError, ValueError)):
            raise ValueError("abc")


def test_core_context_exit_code():
    with pytest.raises(SystemExit):
        with evacuator(exit_code=32):
            raise NeedEvacuation("abc")


def test_core_context_nothing_raised():
    with evacuator():
        logging.debug("abc")


def test_core_context_exception_not_match():
    with pytest.raises(RuntimeError, match="abc"):
        with evacuator():
            raise RuntimeError("abc")
