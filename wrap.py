from inspect import getmembers


def proxy(attr, sniffcall, sniffret):
    if sniffcall and sniffret:

        def f(self, *args):
            sniffcall(self, attr, args)
            r = getattr(self.victim, attr)(*args)
            return sniffret(self, attr, args, r)

    elif sniffcall:

        def f(self, *args):
            sniffcall(self, attr, args)
            return getattr(self.victim, attr)(*args)

    elif sniffret:

        def f(self, *args):
            r = getattr(self.victim, attr)(*args)
            return sniffret(self, attr, args, r)

    else:

        def f(self, *args):
            return getattr(self.victim, attr)(*args)

    return f


def dowrap(
    victim, sniffcall=None, sniffret=None, calls={}, rets={}, init=None, **kwargs
):
    class Wrap(object):
        def __init__(self, victim):
            self.victim = victim
            self.init()

    exclude = set(dir(Wrap) + list(kwargs.keys()))
    exclude.add("__class__")
    for k, f in kwargs.items():
        setattr(Wrap, k, f)
    if init is not None:
        setattr(Wrap, "init", init)
    else:
        setattr(Wrap, "init", lambda self: None)
    for attr, _ in getmembers(victim, callable):
        if attr not in exclude:
            sc = sniffcall
            sr = sniffret
            if attr in calls:
                sc = calls[attr]
            if attr in rets:
                sr = rets[attr]
            setattr(Wrap, attr, proxy(attr, sc, sr))
    wrap = Wrap(victim)
    return wrap


def classwrap(wrappedcls, **kwargs):
    class Temp:
        def __new__(cls):
            d = wrappedcls()
            w = dowrap(d, **kwargs)
            return w

    return Temp
