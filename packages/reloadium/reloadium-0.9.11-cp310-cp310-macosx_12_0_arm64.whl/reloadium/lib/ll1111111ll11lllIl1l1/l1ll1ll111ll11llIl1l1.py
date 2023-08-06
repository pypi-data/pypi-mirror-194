from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, List

from reloadium.lib.ll1111111ll11lllIl1l1.l1ll1ll1lll1l111Il1l1 import llllllll1111l11lIl1l1
from reloadium.corium.ll1lll1l1ll11111Il1l1 import l11l1111llll1lllIl1l1
from reloadium.corium.ll1ll1l1l1lllll1Il1l1 import l1l1l1l11lllllllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class ll1l11l11lll1l1lIl1l1(llllllll1111l11lIl1l1):
    ll11lllll1llll1lIl1l1 = 'PyGame'

    lllll1111lllll1lIl1l1: bool = field(init=False, default=False)

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l1ll1l1lll1111l1Il1l1: types.ModuleType) -> None:
        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l1ll1l1lll1111l1Il1l1, 'pygame.base')):
            lll111l1l11111l1Il1l1.ll1lll1ll111l1llIl1l1()

    def ll1lll1ll111l1llIl1l1(lll111l1l11111l1Il1l1) -> None:
        import pygame.display

        l1ll11l1l1ll1l1lIl1l1 = pygame.display.update

        def l1ll1l11llll1l1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> None:
            if (lll111l1l11111l1Il1l1.lllll1111lllll1lIl1l1):
                l1l1l1l11lllllllIl1l1.lll11ll11l1111llIl1l1(0.1)
                return None
            else:
                return l1ll11l1l1ll1l1lIl1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1)

        pygame.display.update = l1ll1l11llll1l1lIl1l1

    def ll11ll1l111l111lIl1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path) -> None:
        lll111l1l11111l1Il1l1.lllll1111lllll1lIl1l1 = True

    def llll111ll11lll11Il1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path, l11lll111ll1l1l1Il1l1: List[l11l1111llll1lllIl1l1]) -> None:
        lll111l1l11111l1Il1l1.lllll1111lllll1lIl1l1 = False

    def ll1ll1l1ll111ll1Il1l1(lll111l1l11111l1Il1l1, l1l1l1lll11111l1Il1l1: Exception) -> None:
        lll111l1l11111l1Il1l1.lllll1111lllll1lIl1l1 = False
