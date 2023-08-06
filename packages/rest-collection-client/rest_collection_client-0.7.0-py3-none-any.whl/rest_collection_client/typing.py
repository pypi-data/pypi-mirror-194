from typing import Any, Dict, List, Literal, Mapping, Sequence, Union

__all__ = [
    'JsonContentOrText',
    'SequenceOfMapping',
    'RawRestCollectionResponse',
    'RestCollectionJoinHowType',
]

JsonContentOrText = Union[Dict, List, str, int, float, None]
SequenceOfMapping = Sequence[Mapping[str, Any]]
RawRestCollectionResponse = Mapping[str, SequenceOfMapping]
RestCollectionJoinHowType = Literal['left', 'right', 'outer', 'inner']
