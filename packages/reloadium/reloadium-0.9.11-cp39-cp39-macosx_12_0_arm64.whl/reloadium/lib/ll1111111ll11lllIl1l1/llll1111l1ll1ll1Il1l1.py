from contextlib import contextmanager
from pathlib import Path
import types
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Tuple, Type

from reloadium.lib.environ import env
from reloadium.corium.llll1ll11l1ll111Il1l1 import l111ll11ll1lll1lIl1l1
from reloadium.lib.ll1111111ll11lllIl1l1.ll11lll11ll11l1lIl1l1 import ll111ll1l111l1l1Il1l1
from reloadium.corium.ll1lll1l1ll11111Il1l1 import l1l11l1l111lll11Il1l1, l11l1l11l1111ll1Il1l1, ll111111l11l1l11Il1l1, ll1l1l1lllll11l1Il1l1
from reloadium.corium.l1l1l11ll1ll11llIl1l1 import ll1l1l11ll11l1llIl1l1
from reloadium.corium.ll1ll1l1l1lllll1Il1l1 import l1l1l1l11lllllllIl1l1

if (TYPE_CHECKING):
    from dataclasses import dataclass
else:
    from reloadium.vendored.dataclasses import dataclass


__RELOADIUM__ = True


@dataclass(**ll1l1l1lllll11l1Il1l1)
class ll11l1l11l1ll1llIl1l1(ll111111l11l1l11Il1l1):
    l1ll1111l11ll1l1Il1l1 = 'FlaskApp'

    @classmethod
    def l1l1ll1l111lll11Il1l1(l1ll1lll1111111lIl1l1, l111l111l111llllIl1l1: ll1l1l11ll11l1llIl1l1.l111l1ll111l1lllIl1l1, l111lll1ll1l1111Il1l1: Any, l11ll1111llll1l1Il1l1: l1l11l1l111lll11Il1l1) -> bool:
        import flask

        if (isinstance(l111lll1ll1l1111Il1l1, flask.Flask)):
            return True

        return False

    def ll1l11ll1l1lll1lIl1l1(lll111l1l11111l1Il1l1) -> bool:
        return True

    @classmethod
    def ll1111l1llllll11Il1l1(l1ll1lll1111111lIl1l1) -> int:
        return (super().ll1111l1llllll11Il1l1() + 10)


@dataclass(**ll1l1l1lllll11l1Il1l1)
class llllll1llll11l1lIl1l1(ll111111l11l1l11Il1l1):
    l1ll1111l11ll1l1Il1l1 = 'Request'

    @classmethod
    def l1l1ll1l111lll11Il1l1(l1ll1lll1111111lIl1l1, l111l111l111llllIl1l1: ll1l1l11ll11l1llIl1l1.l111l1ll111l1lllIl1l1, l111lll1ll1l1111Il1l1: Any, l11ll1111llll1l1Il1l1: l1l11l1l111lll11Il1l1) -> bool:
        if (repr(l111lll1ll1l1111Il1l1) == '<LocalProxy unbound>'):
            return True

        return False

    def ll1l11ll1l1lll1lIl1l1(lll111l1l11111l1Il1l1) -> bool:
        return True

    @classmethod
    def ll1111l1llllll11Il1l1(l1ll1lll1111111lIl1l1) -> int:

        return int(10000000000.0)


@dataclass
class llll11l1l1ll111lIl1l1(ll111ll1l111l1l1Il1l1):
    ll11lllll1llll1lIl1l1 = 'Flask'

    @contextmanager
    def ll111ll1111111l1Il1l1(lll111l1l11111l1Il1l1) -> Generator[None, None, None]:




        from flask import Flask as FlaskLib 

        def l1l11ll1111l1l1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            def l1l111111lllll1lIl1l1(ll1lll1lll11l111Il1l1: Any) -> Any:
                return ll1lll1lll11l111Il1l1

            return l1l111111lllll1lIl1l1

        lll1llll11ll1l11Il1l1 = FlaskLib.route
        FlaskLib.route = l1l11ll1111l1l1lIl1l1  # type: ignore

        try:
            yield 
        finally:
            FlaskLib.route = lll1llll11ll1l11Il1l1  # type: ignore

    def l11ll1l1l111llllIl1l1(lll111l1l11111l1Il1l1) -> List[Type[l11l1l11l1111ll1Il1l1]]:
        return [ll11l1l11l1ll1llIl1l1, llllll1llll11l1lIl1l1]

    def l1lllll111111l1lIl1l1(lll111l1l11111l1Il1l1, l1ll1l1lll1111l1Il1l1: types.ModuleType) -> None:
        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l1ll1l1lll1111l1Il1l1, 'flask.app')):
            lll111l1l11111l1Il1l1.ll1llll11lll1lllIl1l1()
            lll111l1l11111l1Il1l1.ll1ll1ll1l1l1l1lIl1l1()
            lll111l1l11111l1Il1l1.l11l1ll11l1l1111Il1l1()

        if (lll111l1l11111l1Il1l1.lllll11l1ll11lllIl1l1(l1ll1l1lll1111l1Il1l1, 'flask.cli')):
            lll111l1l11111l1Il1l1.lll1l1l1lllll1l1Il1l1()

    def ll1llll11lll1lllIl1l1(lll111l1l11111l1Il1l1) -> None:
        try:
            import werkzeug.serving
            import flask.cli
        except ImportError:
            return 

        l11l1l1llll1llllIl1l1 = werkzeug.serving.run_simple

        def llll11l11l11ll1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            with l111ll11ll1lll1lIl1l1():
                lll111ll1l11l1l1Il1l1 = l111lll1111l1ll1Il1l1.get('port')
                if ( not lll111ll1l11l1l1Il1l1):
                    lll111ll1l11l1l1Il1l1 = l1lll111l1l1l1llIl1l1[1]

                lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1 = lll111l1l11111l1Il1l1.lll111lll11l1l11Il1l1(lll111ll1l11l1l1Il1l1)
                if (env.page_reload_on_start):
                    lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.llll11l11l1l1l1lIl1l1(1.0)
            l11l1l1llll1llllIl1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1)

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(werkzeug.serving, 'run_simple', llll11l11l11ll1lIl1l1)
        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(flask.cli, 'run_simple', llll11l11l11ll1lIl1l1)

    def l11l1ll11l1l1111Il1l1(lll111l1l11111l1Il1l1) -> None:
        try:
            import flask
        except ImportError:
            return 

        l11l1l1llll1llllIl1l1 = flask.app.Flask.__init__

        def llll11l11l11ll1lIl1l1(ll111l1lll1l1111Il1l1: Any, *l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            l11l1l1llll1llllIl1l1(ll111l1lll1l1111Il1l1, *l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1)
            with l111ll11ll1lll1lIl1l1():
                ll111l1lll1l1111Il1l1.config['TEMPLATES_AUTO_RELOAD'] = True

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(flask.app.Flask, '__init__', llll11l11l11ll1lIl1l1)

    def ll1ll1ll1l1l1l1lIl1l1(lll111l1l11111l1Il1l1) -> None:
        try:
            import waitress  # type: ignore
        except ImportError:
            return 

        l11l1l1llll1llllIl1l1 = waitress.serve


        def llll11l11l11ll1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            with l111ll11ll1lll1lIl1l1():
                lll111ll1l11l1l1Il1l1 = l111lll1111l1ll1Il1l1.get('port')
                if ( not lll111ll1l11l1l1Il1l1):
                    lll111ll1l11l1l1Il1l1 = int(l1lll111l1l1l1llIl1l1[1])

                lll111ll1l11l1l1Il1l1 = int(lll111ll1l11l1l1Il1l1)

                lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1 = lll111l1l11111l1Il1l1.lll111lll11l1l11Il1l1(lll111ll1l11l1l1Il1l1)
                if (env.page_reload_on_start):
                    lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.llll11l11l1l1l1lIl1l1(1.0)

            l11l1l1llll1llllIl1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1)

        l1l1l1l11lllllllIl1l1.l1111l1l11l11111Il1l1(waitress, 'serve', llll11l11l11ll1lIl1l1)

    def lll1l1l1lllll1l1Il1l1(lll111l1l11111l1Il1l1) -> None:
        try:
            from flask import cli
        except ImportError:
            return 

        ll1l1l111l1l111lIl1l1 = Path(cli.__file__).read_text(encoding='utf-8')
        ll1l1l111l1l111lIl1l1 = ll1l1l111l1l111lIl1l1.replace('.tb_next', '.tb_next.tb_next')

        exec(ll1l1l111l1l111lIl1l1, cli.__dict__)

    def lll1lll1llllllllIl1l1(lll111l1l11111l1Il1l1) -> None:
        super().lll1lll1llllllllIl1l1()
        import flask.app

        l11l1l1llll1llllIl1l1 = flask.app.Flask.dispatch_request

        def llll11l11l11ll1lIl1l1(*l1lll111l1l1l1llIl1l1: Any, **l111lll1111l1ll1Il1l1: Any) -> Any:
            l111ll1llll11l1lIl1l1 = l11l1l1llll1llllIl1l1(*l1lll111l1l1l1llIl1l1, **l111lll1111l1ll1Il1l1)

            if ( not lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1):
                return l111ll1llll11l1lIl1l1

            if (isinstance(l111ll1llll11l1lIl1l1, str)):
                ll111l11ll111lllIl1l1 = lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.ll111l111ll1111lIl1l1(l111ll1llll11l1lIl1l1)
                return ll111l11ll111lllIl1l1
            elif ((isinstance(l111ll1llll11l1lIl1l1, flask.app.Response) and 'text/html' in l111ll1llll11l1lIl1l1.content_type)):
                l111ll1llll11l1lIl1l1.data = lll111l1l11111l1Il1l1.llll11ll11ll1ll1Il1l1.ll111l111ll1111lIl1l1(l111ll1llll11l1lIl1l1.data.decode('utf-8')).encode('utf-8')
                return l111ll1llll11l1lIl1l1
            else:
                return l111ll1llll11l1lIl1l1

        flask.app.Flask.dispatch_request = llll11l11l11ll1lIl1l1  # type: ignore
