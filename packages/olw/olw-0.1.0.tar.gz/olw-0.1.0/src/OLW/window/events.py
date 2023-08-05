from enum import StrEnum


class MouseEvents(StrEnum):
    LeftClick = '<Button-1>'
    CenterClick = '<Button-2>'
    RightClick = '<Button-3>'
    LeftDrag = '<B1-Motion>'
    CenterDrag = '<B2-Motion>'
    RightDrag = '<B3-Motion>'
    LeftRelease = '<ButtonRelease-1>'
    CenterRelease = '<ButtonRelease-2>'
    RightRelease = '<ButtonRelease-3>'
