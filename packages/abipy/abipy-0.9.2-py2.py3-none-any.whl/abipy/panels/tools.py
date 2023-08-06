""""Utilities for AbiPy panels."""

import panel as pn
import panel.widgets as pnw

def btn_open_link(url, new_tab=True, **btn_kwargs):
    """
    Return button to open link in a new tab.
    """
    name = btn_kwargs.get("name", "Open Link")
    btn = pnw.Button(name=name, **btn_kwargs)
    btn.js_on_click(code=f"window.open('{url}')" if new_tab else f"window.location.href='{url}'")

    return btn
