def test_send(sample_signal):
    items = []
    item = "test"

    @sample_signal.connect
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

    @sample_signal.connect(sender=sender_obj)
    def receiver(data, **_):
        items.append(data)
        return True

    res = sample_signal.send(data=item)
    assert items == []
    assert res == []

    res = sample_signal.send(sender=sender_obj, data=item)
    assert items == [item]
    assert res == [True]
