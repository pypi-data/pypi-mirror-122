class Selector:
    _name: str = None
    _is_css_selector: bool = True
    _attr: dict = None
    _required_attr: str = None

    def __init__(self, name: str, is_css_selector=True, attr=None, required_attr=None):
        self._name = name
        self._is_css_selector = is_css_selector
        self._attr = attr
        self._required_attr = required_attr

    def __str__(self) -> str:
        return 'name is {}, attr is {}'.format(self.name, self._attr)

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def is_css_selector(self) -> bool:
        return self._is_css_selector

    @property
    def get_attr(self):
        return self._attr

    @property
    def get_required_attr(self):
        return self._required_attr
