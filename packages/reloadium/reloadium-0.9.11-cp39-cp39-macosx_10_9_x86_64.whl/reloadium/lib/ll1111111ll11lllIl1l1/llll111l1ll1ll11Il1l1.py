import types
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, List, Optional, Tuple, Type, Union, cast

from reloadium.lib.ll1111111ll11lllIl1l1.l1ll1ll1lll1l111Il1l1 import llllllll1111l11lIl1l1
from reloadium.lib import l1ll11ll1ll1l111Il1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass, field
else:
    from reloadium.vendored.dataclasses import dataclass, field


__RELOADIUM__ = True


@dataclass
class l11ll1l1l111111lIl1l1(llllllll1111l11lIl1l1):
    ll11lllll1llll1lIl1l1 = 'Multiprocessing'

    def __post_init__(lll111l1l11111l1Il1l1) -> None:
        super().__post_init__()

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l11l1lll11111111Il1l1, 'multiprocessing.popen_spawn_posix')):
            lll111l1l11111l1Il1l1.l1l11l11l1l11lllIl1l1(l11l1lll11111111Il1l1)

        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l11l1lll11111111Il1l1, 'multiprocessing.popen_spawn_win32')):
            lll111l1l11111l1Il1l1.l111lllll1l1l1l1Il1l1(l11l1lll11111111Il1l1)

    def l1l11l11l1l11lllIl1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_posix
        multiprocessing.popen_spawn_posix.Popen._launch = l1ll11ll1ll1l111Il1l1.llll111l1ll1ll11Il1l1.lllllllll1111ll1Il1l1  # type: ignore

    def l111lllll1l1l1l1Il1l1(lll111l1l11111l1Il1l1, l11l1lll11111111Il1l1: types.ModuleType) -> None:
        import multiprocessing.popen_spawn_win32
        multiprocessing.popen_spawn_win32.Popen.__init__ = l1ll11ll1ll1l111Il1l1.llll111l1ll1ll11Il1l1.__init__  # type: ignore
