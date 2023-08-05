from functools import wraps
import time
try:
    from collections.abc import MutableMapping  # Python 3.3+
except ImportError:
    from collections import MutableMapping  # Python 2.7+
import heapq
from threading import Lock


class _ExpiringMapping(MutableMapping):
    _INDEX = "_index_"

    def __init__(self, mapping=None, capacity=None, expires_in=None, lock=None,
        *args, **kwargs):
        """Items in this mapping can have individual shelf life,
        just like food items in your refrigerator have their different shelf life
        determined by each food, not by the refrigerator.

        Expired items will be automatically evicted.
        The clean-up will be done at each time when adding a new item,
        or when looping or counting the entire mapping.
        (This is better than being done indecisively by a background thread,
        which might not always happen before your accessing the mapping.)

        This implementation uses no dependency other than Python standard library.

        :param MutableMapping mapping:
            A dict-like key-value mapping, which needs to support __setitem__(),
            __getitem__(), __delitem__(), get(), pop().

            The default mapping is an in-memory dict.

            You could potentially supply a file-based dict-like object, too.
            This implementation deliberately avoid mapping.__iter__(),
            which could be slow on a file-based mapping.

        :param int capacity:
            How many items this mapping will hold.
            When you attempt to add new item into a full mapping,
            it will automatically delete the item that is expiring soonest.

            The default value is None, which means there is no capacity limit.

        :param int expires_in:
            How many seconds an item would expire and be purged from this mapping.
            Also known as time-to-live (TTL).
            You can also use :func:`~set()` to provide per-item expires_in value.

        :param Lock lock:
            A locking mechanism with context manager interface.
            If no lock is provided, a threading.Lock will be used.
            But you may want to supply a different lock,
            if your customized mapping is being shared differently.
        """
        super(_ExpiringMapping, self).__init__(*args, **kwargs)
        self._mapping = mapping if mapping is not None else {}
        self._capacity = capacity
        self._expires_in = expires_in
        self._lock = Lock() if lock is None else lock

    def _validate_key(self, key):
        if key == self._INDEX:
            raise ValueError("key {} is a reserved keyword in {}".format(
                key, self.__class__.__name__))

    def set(self, key, value, expires_in):
        # This method's name was chosen so that it matches its cousin __setitem__(),
        # and it also complements the counterpart get().
        # The downside is such a name shadows the built-in type set in this file,
        # but you can overcome that by defining a global alias for set.
        """It sets the key-value pair into this mapping, with its per-item expires_in.

        It will take O(logN) time, because it will run some maintenance.
        This worse-than-constant time is acceptable, because in a cache scenario,
        __setitem__() would only be called during a cache miss,
        which would already incur an expensive target function call anyway.

        By the way, most other methods of this mapping still have O(1) constant time.
        """
        with self._lock:
            self._set(key, value, expires_in)

    def _set(self, key, value, expires_in):
        # This internal implementation powers both set() and __setitem__(),
        # so that they don't depend on each other.
        self._validate_key(key)
        sequence, timestamps = self._mapping.get(self._INDEX, ([], {}))
        self._maintenance(sequence, timestamps)  # O(logN)
        now = int(time.time())
        expires_at = now + expires_in
        entry = [expires_at, now, key]
        is_new_item = key not in timestamps
        is_beyond_capacity = self._capacity and len(timestamps) >= self._capacity
        if is_new_item and is_beyond_capacity:
            self._drop_indexed_entry(timestamps, heapq.heappushpop(sequence, entry))
        else:  # Simply add new entry. The old one would become a harmless orphan.
            heapq.heappush(sequence, entry)
        timestamps[key] = [expires_at, now]  # It overwrites existing key, if any
        self._mapping[key] = value
        self._mapping[self._INDEX] = sequence, timestamps

    def _maintenance(self, sequence, timestamps):  # O(logN)
        """It will modify input sequence and timestamps in-place"""
        now = int(time.time())
        while sequence:  # Clean up expired items
            expires_at, created_at, key = sequence[0]
            if created_at <= now < expires_at:  # Then all remaining items are fresh
                break
            self._drop_indexed_entry(timestamps, sequence[0])  # It could error out
            heapq.heappop(sequence)  # Only pop it after a successful _drop_indexed_entry()
        while self._capacity is not None and len(timestamps) > self._capacity:
            self._drop_indexed_entry(timestamps, sequence[0])  # It could error out
            heapq.heappop(sequence)  # Only pop it after a successful _drop_indexed_entry()

    def _drop_indexed_entry(self, timestamps, entry):
        """For an entry came from index, drop it from timestamps and self._mapping"""
        expires_at, created_at, key = entry
        if [expires_at, created_at] == timestamps.get(key):  # So it is not an orphan
            self._mapping.pop(key, None)  # It could raise exception
            timestamps.pop(key, None)  # This would probably always succeed

    def __setitem__(self, key, value):
        """Implements the __setitem__().

        Same characteristic as :func:`~set()`,
        but use class-wide expires_in which was specified by :func:`~__init__()`.
        """
        if self._expires_in is None:
            raise ValueError("Need a numeric value for expires_in during __init__()")
        with self._lock:
            self._set(key, value, self._expires_in)

    def __getitem__(self, key):  # O(1)
        """If the item you requested already expires, KeyError will be raised."""
        self._validate_key(key)
        with self._lock:
            # Skip self._maintenance(), because it would need O(logN) time
            sequence, timestamps = self._mapping.get(self._INDEX, ([], {}))
            expires_at, created_at = timestamps[key]  # Would raise KeyError accordingly
            now = int(time.time())
            if not created_at <= now < expires_at:
                self._mapping.pop(key, None)
                timestamps.pop(key, None)
                self._mapping[self._INDEX] = sequence, timestamps
                raise KeyError("{} {}".format(
                    key,
                    "expired" if now >= expires_at else "created in the future?",
                    ))
            return self._mapping[key]  # O(1)

    def __delitem__(self, key):  # O(1)
        """If the item you requested already expires, KeyError will be raised."""
        self._validate_key(key)
        with self._lock:
            # Skip self._maintenance(), because it would need O(logN) time
            self._mapping.pop(key, None)  # O(1)
            sequence, timestamps = self._mapping.get(self._INDEX, ([], {}))
            del timestamps[key]  # O(1)
            self._mapping[self._INDEX] = sequence, timestamps

    def __len__(self):  # O(logN)
        """Drop all expired items and return the remaining length"""
        with self._lock:
            sequence, timestamps = self._mapping.get(self._INDEX, ([], {}))
            self._maintenance(sequence, timestamps)  # O(logN)
            self._mapping[self._INDEX] = sequence, timestamps
            return len(timestamps)  # Faster than iter(self._mapping) when it is on disk

    def __iter__(self):
        """Drop all expired items and return an iterator of the remaining items"""
        with self._lock:
            sequence, timestamps = self._mapping.get(self._INDEX, ([], {}))
            self._maintenance(sequence, timestamps)  # O(logN)
            self._mapping[self._INDEX] = sequence, timestamps
        return iter(timestamps)  # Faster than iter(self._mapping) when it is on disk


class _IndividualCache(object):
    # The code structure below can decorate both function and method.
    # It is inspired by https://stackoverflow.com/a/9417088
    # We may potentially switch to build upon
    # https://github.com/micheles/decorator/blob/master/docs/documentation.md#statement-of-the-problem
    def __init__(self, mapping=None, key_maker=None, expires_in=None):
        """Constructs a cache decorator that allows item-by-item control on
        how to cache the return value of the decorated function.

        :param MutableMapping mapping:
            The cached items will be stored inside.
            You'd want to use a ExpiringMapping
            if you plan to utilize the ``expires_in`` behavior.

            If nothing is provided, an in-memory dict will be used,
            but it will provide no expiry functionality.

            .. note::

                When using this class as a decorator,
                your mapping needs to be available at "compile" time,
                so it would typically be a global-, module- or class-level mapping::

                    module_mapping = {}

                    @IndividualCache(mapping=module_mapping, ...)
                    def foo():
                        ...

                If you want to use a mapping available only at run-time,
                you have to manually decorate your function at run-time, too::

                    def foo():
                        ...

                    def bar(runtime_mapping):
                        foo = IndividualCache(mapping=runtime_mapping...)(foo)

        :param callable key_maker:
            A callable which should have signature as
            ``lambda function, args, kwargs: "return a string as key"``.

            If key_maker happens to return ``None``, the cache will be bypassed,
            the underlying function will be invoked directly,
            and the invoke result will not be cached either.

        :param callable expires_in:
            The default value is ``None``,
            which means the content being cached has no per-item expiry,
            and will subject to the underlying mapping's global expiry time.

            It can be an integer indicating
            how many seconds the result will be cached.
            In particular, if the value is 0,
            it means the result expires after zero second (i.e. immediately),
            therefore the result will *not* be cached.
            (Mind the difference between ``expires_in=0`` and ``expires_in=None``.)

            Or it can be a callable with the signature as
            ``lambda function=function, args=args, kwargs=kwargs, result=result: 123``
            to calculate the expiry on the fly.
            Its return value will be interpreted in the same way as above.
        """
        self._mapping = mapping if mapping is not None else {}
        self._key_maker = key_maker or (lambda function, args, kwargs: (
            function,  # This default implementation uses function as part of key,
                # so that the cache is partitioned by function.
                # However, you could have many functions to use same namespace,
                # so different decorators could share same cache.
            args,
            tuple(kwargs.items()),  # raw kwargs is not hashable
            ))
        self._expires_in = expires_in

    def __call__(self, function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            key = self._key_maker(function, args, kwargs)
            if key is None:  # Then bypass the cache
                return function(*args, **kwargs)

            now = int(time.time())
            try:
                return self._mapping[key]
            except KeyError:
                # We choose to NOT call function(...) in this block, otherwise
                # potential exception from function(...) would become a confusing
                # "During handling of the above exception, another exception occurred"
                pass
            value = function(*args, **kwargs)

            expires_in = self._expires_in(
                function=function,
                args=args,
                kwargs=kwargs,
                result=value,
                ) if callable(self._expires_in) else self._expires_in
            if expires_in == 0:
                return value
            if expires_in is None:
                self._mapping[key] = value
            else:
                self._mapping.set(key, value, expires_in)
            return value

        return wrapper

