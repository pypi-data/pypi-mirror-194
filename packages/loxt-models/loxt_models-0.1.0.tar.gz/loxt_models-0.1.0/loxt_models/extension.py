from __future__ import annotations

from loxt_models.sidebar import SidebarModel


class ExtensionBase:

    VERSION: str
    IDENTIFIER: str
    PLATFORM: str = 'all'
    OOO_MINIMAL_VERSION: str = None
    OOO_MINIMAL_VERSION_NAME: str = None
    UPDATE_INFORMATION_SRC: str = None
    LICENSE_ACCEPT_BY: str = 'user'
    LICENSE_SUPPRESS_ON_UPDATE = None
    LICENSE_TXT_HREF: str = None
    PUBLISHER_NAME: str
    PUBLISHER_NAME_HREF: str = None
    RELEASE_NOTES_HREF: str = None
    DISPLAY_NAME: str
    ICON_HREF_DEFAULT: str = None
    ICON_HREF_HIGH_CONTRAST: str = None
    DESCRIPTION_HREF: str = None

    def __init__(self):
        self.components: list[SidebarModel] = list()

    def add_component(self, component: SidebarModel):
        self.components.append(component)

    @property
    def sidebar(self):
        sidebar_list = [c for c in self.components if isinstance(c, SidebarModel)]

        if sidebar_list:
            return sidebar_list[0]
        else:
            return None
