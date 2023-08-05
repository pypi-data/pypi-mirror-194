import logging
import typing as t
import weakref

ReceiverID = t.Tuple[int, str]

NONE_ID = id(None)


def make_receiver_id(target: t.Callable) -> ReceiverID:
    if hasattr(target, "__self__") and hasattr(target, "__func__"):
        return id(target.__self__), target.__func__.__name__
    return id(target), ""


def make_sender_id(sender: t.Any) -> int:
    if sender is None:
        return NONE_ID
    return id(sender)


class LookupKey(t.NamedTuple):
    receiver_id: ReceiverID
    sender_id: int


Receiver = t.Union[weakref.ReferenceType, t.Callable]
References = t.Dict[LookupKey, Receiver]

logger = logging.getLogger(__name__)


class Signal:
    __slots__ = ("_references",)

    def __init__(self) -> None:
        self._references: References = {}

    def _live_receivers(self, sender: t.Any = None) -> t.Generator[t.Tuple[LookupKey, t.Callable], None, None]:
        sender_id = make_sender_id(sender)
        for key, func in tuple(self._references.items()):
            if isinstance(func, weakref.ReferenceType):
                func = func()
            if func:
                if key.sender_id == NONE_ID or key.sender_id == sender_id:
                    yield key, func
            else:
                del self._references[key]

    def connect(self, receiver: t.Callable = None, sender: t.Any = None, weak: bool = True) -> t.Optional[t.Callable]:
        if not receiver:
            return lambda f: self.connect(f, sender=sender, weak=weak)
        key = LookupKey(make_receiver_id(receiver), make_sender_id(sender))
        if key not in self._references:
            if weak:
                ref_type: t.Type[weakref.ReferenceType] = weakref.ref
                if hasattr(receiver, "__self__") and hasattr(receiver, "__func__"):
                    ref_type = weakref.WeakMethod
                self._references[key] = ref_type(receiver)
            else:
                self._references[key] = receiver
        return receiver

    def disconnect(self, receiver: t.Callable, sender: t.Any = None) -> bool:
        for key, live_receiver in self._live_receivers(sender):
            if receiver == live_receiver:
                del self._references[key]
                return True
        return False

    def clear(self) -> None:
        self._references.clear()

    def send(self, sender=None, **kwargs: t.Any) -> t.List[t.Any]:
        responses = []
        for _, receiver in self._live_receivers(sender):
            res = receiver(sender=sender, **kwargs)
            if res:
                responses.append(res)
        return responses

    def send_robust(self, sender=None, **kwargs: t.Any) -> t.List[t.Any]:
        responses = []
        for _, receiver in self._live_receivers(sender):
            try:
                res = receiver(sender=sender, **kwargs)
            except Exception as e:
                logger.error(
                    "Error calling %s in Signal.send_robust() (%s)",
                    receiver.__qualname__,
                    e,
                    exc_info=e,
                )
            else:
                if res:
                    responses.append(res)
        return responses
