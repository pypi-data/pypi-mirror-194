def test_gc_function(sample_signal):
    items = []

    def receiver(data, **_):
        data.append(1)

    sample_signal.connect(receiver)
    sample_signal.send(data=items)
    assert len(items) == 1

    del receiver

    sample_signal.send(data=items)
    assert len(items) == 1


def test_gc_method(sample_signal):
    items = []

    class X:
        def receiver(self, data, **_):
            data.append(1)

    obj = X()
    sample_signal.connect(obj.receiver)
    sample_signal.send(data=items)
    assert len(items) == 1

    del obj

    sample_signal.send(data=items)
    assert len(items) == 1


def test_gc_function_non_weak(sample_signal):
    items = []

    def receiver(data, **_):
        data.append(1)

    sample_signal.connect(receiver, weak=False)
    sample_signal.send(data=items)
    assert len(items) == 1

    del receiver

    sample_signal.send(data=items)
    assert len(items) == 2


def test_gc_method_non_weak(sample_signal):
    items = []

    class X:
        def receiver(self, data, **_):
            data.append(1)

    obj = X()
    sample_signal.connect(obj.receiver, weak=False)
    sample_signal.send(data=items)
    assert len(items) == 1

    del obj

    sample_signal.send(data=items)
    assert len(items) == 2
