from dataclasses import dataclass, field

"""
- add all properties
"""

@dataclass
class BaseWindow:
    top: str = field(init=False)
    left: str = field(init=False)
    width: str = field(init=False)
    height: str = field(init=False)
    title: str = field(init=False)

    def _setup_rect_properties(self):
        r = self._get_window_rect()
        self._rect = (r.left,
                      r.top,
                      r.right - r.left,
                      r.bottom - r.top)

    def _get_window_rect(self):
        raise NotImplementedError

    def __str__(self):
        r = self._get_window_rect()
        self.left = str(r[0])
        self.top = str(r[1])
        self.width = str(r[2] - r[0])
        self.height = str(r[3] - r[1])
        self.title = f"title {r}"

        return f"<{self.__class__.__qualname__}, " \
               f"left={self.left}, " \
               f"width={self.width}, " \
               f"height={self.height}, " \
               f"title={self.title}>"

    @property
    def left(self):
        return self._rect.left
