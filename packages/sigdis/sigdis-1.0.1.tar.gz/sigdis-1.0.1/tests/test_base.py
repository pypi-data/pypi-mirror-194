import pytest

from sigdis import make_receiver_id, make_sender_id


class CustomError(Exception):
    pass


def test_make_receiver_id_function():
    def func():
        pass

    assert make_receiver_id(func) == (id(func), "")


def test_make_receiver_id_method():
    class C:
        def func(self):
            pass

    c = C()
    assert make_receiver_id(c.func) == (id(c), c.func.__name__)


def test_make_sender_id():
    class C:
        pass

    assert make_sender_id(None) == id(None)
    assert make_sender_id(C) == id(C)


def test_connect_function(sample_signal):
    def receiver(**_):
        return True

    sample_signal.connect(receiver)
    assert receiver in list(f for _, f in sample_signal._live_receivers())


def test_connect_method(sample_signal):
    class C:
        def receiver(**_):
            return True

    c = C()
    sample_signal.connect(c.receiver)
    assert c.receiver in list(f for _, f in sample_signal._live_receivers())


def test_connect_with_sender(sample_signal):
    sender_obj = object()

    def receiver(**_):
        return True

    sample_signal.connect(receiver, sender=sender_obj)
    assert not list(sample_signal._live_receivers())
    assert list(sample_signal._live_receivers(sender_obj))


def test_disconnect(sample_signal):
    def receiver(**_):
        return True

    sample_signal.connect(receiver)
    assert receiver in list(f for _, f in sample_signal._live_receivers())

    res = sample_signal.disconnect(receiver)
    assert res is True
    assert receiver not in list(f for _, f in sample_signal._live_receivers())

    res = sample_signal.disconnect(receiver)
    assert res is False


def test_disconnect_with_sender(sample_signal):
    sender_obj = object()

    def receiver(**_):
        return True

    sample_signal.connect(receiver, sender=sender_obj)
    assert receiver in list(f for _, f in sample_signal._live_receivers(sender_obj))
    assert receiver not in list(f for _, f in sample_signal._live_receivers())

    res = sample_signal.disconnect(receiver)
    assert res is False
    assert receiver in list(f for _, f in sample_signal._live_receivers(sender_obj))

    res = sample_signal.disconnect(receiver, sender=sender_obj)
    assert res is True
    assert receiver not in list(f for _, f in sample_signal._live_receivers(sender_obj))


def test_send(sample_signal):
    items = []
    item = "test"

    def receiver(data, **_):
        items.append(data)
        return True

    sample_signal.connect(receiver)
    res = sample_signal.send(data=item)
    assert items == [item]
    assert res == [True]


def test_send_with_sender(sample_signal):
    sender_obj = object()
    items = []
    item = "test"

    def receiver(data, **_):
        items.append(data)
        return True

    sample_signal.connect(receiver, sender=sender_obj)

    res = sample_signal.send(data=item)
    assert items == []
    assert res == []

    res = sample_signal.send(sender=sender_obj, data=item)
    assert items == [item]
    assert res == [True]


def test_send_error(sample_signal):
    def receiver(**_):
        raise CustomError

    sample_signal.connect(receiver)
    with pytest.raises(CustomError):
        sample_signal.send()


def test_send_robust(sample_signal):
    items = []
    item = "test"

    def receiver(data, **_):
        items.append(data)
        return True

    sample_signal.connect(receiver)
    res = sample_signal.send_robust(data=item)
    assert items == [item]
    assert res == [True]


def test_send_robust_error(sample_signal, caplog):
    def receiver(**_):
        raise CustomError

    sample_signal.connect(receiver)
    sample_signal.send_robust()
    assert "CustomError" in caplog.text
