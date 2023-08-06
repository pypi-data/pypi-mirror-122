class Needle:
    _text = None
    _tag = None

    def __init__(self, text: str, tag=None):
        self._tag = tag
        self._text = text

    def __str__(self) -> str:
        return 'text is {}, tag is {}'.format(self._text, self._tag)

