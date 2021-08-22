from datetime import timedelta


class Color(object):
    """ Represents a color in the ASS format.
    """
    def __init__(self, r, g, b, a=0):
        """ Made up of red, green, blue and alpha components (in that order!).
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_int(self):
        return self.a + (self.b << 8) + (self.g << 16) + (self.r << 24)

    def to_ass(self):
        """ Convert this color to a Visual Basic (ASS) color code.
        """
        return "&H{a:02X}{b:02X}{g:02X}{r:02X}".format(**self.__dict__)

    @classmethod
    def from_ass(cls, v):
        """ Convert a Visual Basic (ASS) color code into an ``Color``.
        """
        if not v.startswith("&H"):
            raise ValueError("color must start with &H")

        rest = int(v[2:], 16)

        # AABBGGRR
        r = rest & 0xFF
        rest >>= 8

        g = rest & 0xFF
        rest >>= 8

        b = rest & 0xFF
        rest >>= 8

        a = rest & 0xFF

        return cls(r, g, b, a)

    def __repr__(self):
        return "{name}(r=0x{r:02x}, g=0x{g:02x}, b=0x{b:02x}, a=0x{a:02x})".format(
            name=self.__class__.__name__,
            r=self.r,
            g=self.g,
            b=self.b,
            a=self.a
        )


Color.WHITE = Color(255, 255, 255)
Color.RED = Color(255, 0, 0)
Color.BLACK = Color(0, 0, 0)


class _Field(object):
    _last_creation_order = -1

    def __init__(self, name, type, default=None):
        self.name = name
        self.type = type
        self.default = default

        _Field._last_creation_order += 1
        self._creation_order = self._last_creation_order

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.fields.get(self.name, self.default)

    def __set__(self, obj, v):
        obj.fields[self.name] = v

    @staticmethod
    def dump(v):
        if v is None:
            return ""

        if isinstance(v, bool):
            return str(-int(v))

        if isinstance(v, timedelta):
            return _Field.timedelta_to_ass(v)

        if isinstance(v, float):
            return "{0:g}".format(v)

        if hasattr(v, "to_ass"):
            return v.to_ass()

        return str(v)

    def parse(self, v):
        if self.type is None:
            return None

        if self.type is bool:
            return bool(-int(v))

        if self.type is timedelta:
            return _Field.timedelta_from_ass(v)

        if hasattr(self.type, "from_ass"):
            return self.type.from_ass(v)

        return self.type(v)

    @staticmethod
    def timedelta_to_ass(td):
        r = int(td.total_seconds())

        r, secs = divmod(r, 60)
        hours, mins = divmod(r, 60)

        return "{hours:.0f}:{mins:02.0f}:{secs:02.0f}.{csecs:02}".format(
            hours=hours,
            mins=mins,
            secs=secs,
            csecs=td.microseconds // 10000
        )

    @staticmethod
    def timedelta_from_ass(v):
        secs_str, _, csecs = v.partition(".")
        hours, mins, secs = map(int, secs_str.split(":"))

        r = hours * 60 * 60 + mins * 60 + secs + int(csecs) * 1e-2

        return timedelta(seconds=r)


class _WithFieldMeta(type):
    def __new__(cls, name, bases, dct):
        newcls = type.__new__(cls, name, bases, dct)

        field_defs = []
        field_mappings = {}
        field_attributes = {}
        for base in bases:
            if hasattr(base, "_field_defs"):
                field_defs.extend(base._field_defs)
            if hasattr(base, "_field_mappings"):
                field_mappings.update(base._field_mappings)
            if hasattr(base, "_field_attributes"):
                field_attributes.update(base._field_attributes)

        new_field_defs = []
        for name, f in dct.items():
            if isinstance(f, _Field):
                new_field_defs.append(f)
                field_mappings[f.name] = f
                field_attributes[f.name] = name

        field_defs.extend(sorted(new_field_defs, key=lambda f: f._creation_order))
        newcls._field_defs = tuple(field_defs)
        newcls._field_mappings = field_mappings
        newcls._field_attributes = field_attributes

        newcls.DEFAULT_FIELD_ORDER = tuple(f.name for f in field_defs)
        return newcls


class Tag(object):
    """ A tag in ASS, e.g. {\\b1}. Multiple can be used like {\\b1\\i1}. """

    def __init__(self, name, params):
        self.name = name
        self.param = params

    def to_ass(self):
        if not self.params:
            params = ""
        elif len(self.params) == 1:
            params = params[0]
        else:
            params = ("("
                      + ",".join(_Field.dump(param) for param in self.params)
                      + ")")

        return "\\{name}{params}".format(name=self.name, params=params)

    @staticmethod
    def strip_tags(parts, keep_drawing_commands=False):
        text_parts = []

        it = iter(parts)

        for part in it:
            if isinstance(part, Tag):
                # if we encounter a \p1 tag, skip everything until we get to
                # \p0
                if not keep_drawing_commands and part.name == "p" and part.params == [1]:
                    for part2 in it:
                        if isinstance(part2, Tag) and part2.name == "p" and part2.params == [0]:
                            break
            else:
                text_parts.append(part)

        return "".join(text_parts)

    @classmethod
    def from_ass(cls, s):
        raise NotImplementedError
