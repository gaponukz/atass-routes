import typing

HashId: typing.TypeAlias = str

DayDate: typing.TypeAlias = str | typing.Literal['*']

PricesSchema = dict[HashId, dict[HashId, int]]

LangCode = typing.Literal['ua', 'en', 'pl']

MultiLanguages = dict[LangCode, str]
