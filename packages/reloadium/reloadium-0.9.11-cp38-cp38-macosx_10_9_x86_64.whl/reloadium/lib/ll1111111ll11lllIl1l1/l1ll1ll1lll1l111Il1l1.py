from abc import ABC
from contextlib import contextmanager
from pathlib import Path
import sys
import types
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Generator, List, Optional, Tuple, Type

from reloadium.corium.l11l1lllll1111l1Il1l1 import ll11l1l1l1l11111Il1l1, l11l1lllll1111l1Il1l1
from reloadium.corium.ll1lll1l1ll11111Il1l1 import l11l1111llll1lllIl1l1, l11l1l11l1111ll1Il1l1
from reloadium.corium.ll11ll11111ll111Il1l1 import lll1111111ll1l11Il1l1, lll111l1lll11111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field

    from reloadium.lib.ll1111111ll11lllIl1l1.ll11lll1lll111llIl1l1 import l1ll1ll111l11l11Il1l1
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class llllllll1111l11lIl1l1:
    ll11lll1lll111llIl1l1: "l1ll1ll111l11l11Il1l1"

    ll11lllll1llll1lIl1l1: ClassVar[str] = NotImplemented
    ll1l1llllll1111lIl1l1: bool = field(init=False, default=False)

    ll1l1111111111llIl1l1: ll11l1l1l1l11111Il1l1 = field(init=False)

    def __post_init__(lll111l1l11111l1Il1l1) -> None:
        lll111l1l11111l1Il1l1.ll1l1111111111llIl1l1 = l11l1lllll1111l1Il1l1.lll1l1lll11llll1Il1l1(lll111l1l11111l1Il1l1.ll11lllll1llll1lIl1l1)
        lll111l1l11111l1Il1l1.ll1l1111111111llIl1l1.l1ll11l11l11l1l1Il1l1('Creating extension')
        lll111l1l11111l1Il1l1.ll11lll1lll111llIl1l1.ll1l1111l11lllllIl1l1.ll1l1l11l1l1lll1Il1l1.l111lll111l1ll1lIl1l1(lll111l1l11111l1Il1l1.ll11ll1l11l111l1Il1l1())

    def ll11ll1l11l111l1Il1l1(lll111l1l11111l1Il1l1) -> List[Type[l11l1l11l1111ll1Il1l1]]:
        ll111l11ll111lllIl1l1 = []
        ll1lll1l1ll11111Il1l1 = lll111l1l11111l1Il1l1.l11ll1l1l111llllIl1l1()
        for ll1l111lllllll11Il1l1 in ll1lll1l1ll11111Il1l1:
            ll1l111lllllll11Il1l1.l11111l1lll1111lIl1l1 = lll111l1l11111l1Il1l1.ll11lllll1llll1lIl1l1

        ll111l11ll111lllIl1l1.extend(ll1lll1l1ll11111Il1l1)
        return ll111l11ll111lllIl1l1

    def l11l1lll1l1lll11Il1l1(lll111l1l11111l1Il1l1) -> None:
        lll111l1l11111l1Il1l1.ll1l1llllll1111lIl1l1 = True

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        pass

    @contextmanager
    def ll111ll1111111l1Il1l1(lll111l1l11111l1Il1l1) -> Generator[None, None, None]:
        yield 

    def llll1l11l1lll1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        pass

    def ll1ll1l1ll111ll1Il1l1(lll111l1l11111l1Il1l1, l1l1l1lll11111l1Il1l1: Exception) -> None:
        pass

    def ll11l1l1lll1ll11Il1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional[lll1111111ll1l11Il1l1]:
        return None

    async def l1l1ll11llll1lllIl1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional[lll111l1lll11111Il1l1]:
        return None

    def l1l11l1llll1ll11Il1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional[lll1111111ll1l11Il1l1]:
        return None

    async def l1111ll11l1l1111Il1l1(lll111l1l11111l1Il1l1, ll11lllll1llll1lIl1l1: str) -> Optional[lll111l1lll11111Il1l1]:
        return None

    def ll1lll111llll111Il1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path) -> None:
        pass

    def ll11ll1l111l111lIl1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path) -> None:
        pass

    def llll111ll11lll11Il1l1(lll111l1l11111l1Il1l1, llll1lll1llll111Il1l1: Path, l11lll111ll1l1l1Il1l1: List[l11l1111llll1lllIl1l1]) -> None:
        pass

    def __eq__(lll111l1l11111l1Il1l1, ll1l111lll11ll1lIl1l1: Any) -> bool:
        return id(ll1l111lll11ll1lIl1l1) == id(lll111l1l11111l1Il1l1)

    def l11ll1l1l111llllIl1l1(lll111l1l11111l1Il1l1) -> List[Type[l11l1l11l1111ll1Il1l1]]:
        return []

    def lllll11l1ll11lllIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType, ll11lllll1llll1lIl1l1: str) -> bool:
        ll111l11ll111lllIl1l1 = (hasattr(l11l1lll11111111Il1l1, '__name__') and l11l1lll11111111Il1l1.__name__ == ll11lllll1llll1lIl1l1)
        return ll111l11ll111lllIl1l1


@dataclass(repr=False)
class l11l1111lllllll1Il1l1(lll1111111ll1l11Il1l1):
    l1ll1ll1lll1l111Il1l1: llllllll1111l11lIl1l1

    def __repr__(lll111l1l11111l1Il1l1) -> str:
        return 'ExtensionMemento'


@dataclass(repr=False)
class llll111l111ll1llIl1l1(lll111l1lll11111Il1l1):
    l1ll1ll1lll1l111Il1l1: llllllll1111l11lIl1l1

    def __repr__(lll111l1l11111l1Il1l1) -> str:
        return 'AsyncExtensionMemento'
