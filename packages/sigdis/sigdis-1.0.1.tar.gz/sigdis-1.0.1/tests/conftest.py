import pytest

from sigdis import Signal

_sample_signal = Signal()


@pytest.fixture
def sample_signal():
    try:
        yield _sample_signal
    finally:
        _sample_signal.clear()
