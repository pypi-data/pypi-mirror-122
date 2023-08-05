from typing import Union

from compound_types.built_ins import \
    BoolIterable, DictIterable, FloatIterable, IntIterable, StrIterable
from compound_types.built_ins.sizeds import \
    BoolSized, DictSized, FloatSized, IntSized, StrSized

BoolSizedIterable = Union[BoolSized, BoolIterable]
DictSizedIterable = Union[DictSized, DictIterable]
FloatSizedIterable = Union[FloatSized, FloatIterable]
IntSizedIterable = Union[IntSized, IntIterable]
StrSizedIterable = Union[StrSized, StrIterable]