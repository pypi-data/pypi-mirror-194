import os
from typing import Optional, Callable

import streamlit.components.v1 as components

_RELEASE = True
COMPONENT_NAME = "streamlit_cardv2"

if _RELEASE:  # use the build instead of development if release is true
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/build")

    _streamlit_cardv2 = components.declare_component(COMPONENT_NAME, path=build_dir)
else:
    _streamlit_cardv2 = components.declare_component(
        COMPONENT_NAME, url="http://localhost:3000"
    )


def card(
    title: str,
    text: str,
    image: Optional[str] = None,
    url: Optional[str] = None,
    on_click: Optional[Callable] = None,
    key: Optional[str] = None,
) -> bool:
    """Creates a UI card like component.

    Args:
        title (str): The title of the card.
        text (str): The text of the card.
        image (str, optional): An optional background image. Defaults to None.
        url (str, optional): An optional url to open when the card is clicked. Defaults to None.
        on_click (callable, optional): An optional function to call when the card is clicked. Defaults to None.
        key (str, optional): An optional key for the component. Defaults to None.
    """
    return _streamlit_cardv2(
        title=title, text=text, image=image, url=url, on_click=on_click, key=key, default=False
    )
