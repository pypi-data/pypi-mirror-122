class Callback:
    """
    Base class and interface for callback mechanism

    This class can be used directly for monitoring file transfers by
    providing ``callback=Callback(hooks=...)`` (see the ``hooks`` argument,
    below), or subclassed for more specialised behaviour.

    Parameters
    ----------
    size: int (optional)
        Nominal quantity for the value that corresponds to a complete
        transfer, e.g., total number of tiles or total number of
        bytes
    value: int (0)
        Starting internal counter value
    hooks: dict or None
        A dict of named functions to be called on each update. The signature
        of these must be ``f(size, value, **kwargs)``
    """

    def __init__(self, size=None, value=0, hooks=None, **kwargs):
        self.size = size
        self.value = value
        self.hooks = hooks or {}
        self.kw = kwargs

    def set_size(self, size):
        """
        Set the internal maximum size attribute

        Usually called if not initially set at instantiation. Note that this
        triggers a ``call()``.

        Parameters
        ----------
        size: int
        """
        self.size = size
        self.call()

    def absolute_update(self, value):
        """
        Set the internal value state

        Triggers ``call()``

        Parameters
        ----------
        value: int
        """
        self.value = value
        self.call()

    def relative_update(self, inc=1):
        """
        Delta increment the internal cuonter

        Triggers ``call()``

        Parameters
        ----------
        inc: int
        """
        self.value += inc
        self.call()

    def call(self, hook_name=None, **kwargs):
        """
        Execute hook(s) with current state

        Each funcion is passed the internal size and current value

        Parameters
        ----------
        hook_name: str or None
            If given, execute on this hook
        kwargs: passed on to (all) hoook(s)
        """
        if not self.hooks:
            return
        kw = self.kw.copy()
        kw.update(kwargs)
        if hook_name:
            if hook_name not in self.hooks:
                return
            return self.hooks[hook_name](self.size, self.value, **kw)
        for hook in self.hooks.values() or []:
            hook(self.size, self.value, **kw)

    def wrap(self, iterable):
        """
        Wrap an iterable to call ``relative_update`` on each iterations

        Parameters
        ----------
        iterable: Iterable
            The iterable that is being wrapped
        """
        for item in iterable:
            self.relative_update()
            yield item

    def branch(self, path_1, path_2, kwargs):
        """
        Set callbacks for child transfers

        If this callback is operating at a higher level, e.g., put, which may
        trigger transfers that can also be monitored. The passed kwargs are
        to be *mutated* to add ``callback=``, if this class supports branching
        to children.

        Parameters
        ----------
        path_1: str
            Child's source path
        path_2: str
            Child's destination path
        kwargs: dict
            arguments passed to child method, e.g., put_file.

        Returns
        -------

        """
        return None

    def no_op(self, *_, **__):
        pass

    def __getattr__(self, item):
        """
        If undefined methods are called on this class, nothing happens
        """
        return self.no_op

    @classmethod
    def as_callback(cls, maybe_callback=None):
        """Transform callback=... into Callback instance

        For the special value of ``None``, return the global instance of
        ``NoOpCallback``. This is an alternative to including
        ``callback=_DEFAULT_CALLBACK`` directly in a method signature.
        """
        if maybe_callback is None:
            return _DEFAULT_CALLBACK
        return maybe_callback


class NoOpCallback(Callback):
    """
    This implementation of Callback does exactly nothing
    """

    def call(self, *args, **kwargs):
        return None


class DotPrinterCallback(Callback):
    """
    Simple example Callback implementation

    Almost identical to Callback with a hook that prints a char; here we
    demonstrate how the outer layer may print "#" and the inner layer "."
    """

    def __init__(self, chr_to_print="#", **kwargs):
        self.chr = chr_to_print
        super().__init__(**kwargs)

    def branch(self, path_1, path_2, kwargs):
        """Mutate kwargs to add new instance with different print char"""
        kwargs["callback"] = DotPrinterCallback(".")

    def call(self, **kwargs):
        """Just outputs a character"""
        print(self.chr, end="")


_DEFAULT_CALLBACK = NoOpCallback()
