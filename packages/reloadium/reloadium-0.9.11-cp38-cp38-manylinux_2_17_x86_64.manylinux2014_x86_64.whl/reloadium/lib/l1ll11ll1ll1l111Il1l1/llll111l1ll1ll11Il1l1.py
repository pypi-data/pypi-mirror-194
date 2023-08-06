import sys

__RELOADIUM__ = True


def lllllllll1111ll1Il1l1(ll111l1lll1l1111Il1l1, ll1l1l111l1lll11Il1l1):
    from pathlib import Path
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    import io
    import os

    def ll1lll1ll11ll11lIl1l1(*l111l1ll1l111ll1Il1l1):

        for l1ll1111111l1l1lIl1l1 in l111l1ll1l111ll1Il1l1:
            os.close(l1ll1111111l1l1lIl1l1)

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
    else:
        from multiprocessing import semaphore_tracker as tracker 

    ll1l11lll11ll1l1Il1l1 = tracker.getfd()
    ll111l1lll1l1111Il1l1._fds.append(ll1l11lll11ll1l1Il1l1)
    l1ll1ll11l1l11llIl1l1 = spawn.get_preparation_data(ll1l1l111l1lll11Il1l1._name)
    ll111ll111l111llIl1l1 = io.BytesIO()
    set_spawning_popen(ll111l1lll1l1111Il1l1)

    try:
        reduction.dump(l1ll1ll11l1l11llIl1l1, ll111ll111l111llIl1l1)
        reduction.dump(ll1l1l111l1lll11Il1l1, ll111ll111l111llIl1l1)
    finally:
        set_spawning_popen(None)

    l1ll11l1ll11ll1lIl1l1l1l1l1ll1l11111lIl1l1ll1l1ll11ll1ll11Il1l1llll11llllll1lllIl1l1 = None
    try:
        (l1ll11l1ll11ll1lIl1l1, l1l1l1ll1l11111lIl1l1, ) = os.pipe()
        (ll1l1ll11ll1ll11Il1l1, llll11llllll1lllIl1l1, ) = os.pipe()
        lll111l11lll1l1lIl1l1 = spawn.get_command_line(tracker_fd=ll1l11lll11ll1l1Il1l1, pipe_handle=ll1l1ll11ll1ll11Il1l1)


        l111lll11l11111lIl1l1 = str(Path(l1ll1ll11l1l11llIl1l1['sys_argv'][0]).absolute())
        lll111l11lll1l1lIl1l1 = [lll111l11lll1l1lIl1l1[0], '-B', '-m', 'reloadium', 'spawn_process', str(ll1l11lll11ll1l1Il1l1), 
str(ll1l1ll11ll1ll11Il1l1), l111lll11l11111lIl1l1]
        ll111l1lll1l1111Il1l1._fds.extend([ll1l1ll11ll1ll11Il1l1, l1l1l1ll1l11111lIl1l1])
        ll111l1lll1l1111Il1l1.pid = util.spawnv_passfds(spawn.get_executable(), 
lll111l11lll1l1lIl1l1, ll111l1lll1l1111Il1l1._fds)
        ll111l1lll1l1111Il1l1.sentinel = l1ll11l1ll11ll1lIl1l1
        with open(llll11llllll1lllIl1l1, 'wb', closefd=False) as ll1lll1lll11l111Il1l1:
            ll1lll1lll11l111Il1l1.write(ll111ll111l111llIl1l1.getbuffer())
    finally:
        l1l1111l1l1lll11Il1l1 = []
        for l1ll1111111l1l1lIl1l1 in (l1ll11l1ll11ll1lIl1l1, llll11llllll1lllIl1l1, ):
            if (l1ll1111111l1l1lIl1l1 is not None):
                l1l1111l1l1lll11Il1l1.append(l1ll1111111l1l1lIl1l1)
        ll111l1lll1l1111Il1l1.finalizer = util.Finalize(ll111l1lll1l1111Il1l1, ll1lll1ll11ll11lIl1l1, l1l1111l1l1lll11Il1l1)

        for l1ll1111111l1l1lIl1l1 in (ll1l1ll11ll1ll11Il1l1, l1l1l1ll1l11111lIl1l1, ):
            if (l1ll1111111l1l1lIl1l1 is not None):
                os.close(l1ll1111111l1l1lIl1l1)


def __init__(ll111l1lll1l1111Il1l1, ll1l1l111l1lll11Il1l1):
    from multiprocessing import util, spawn
    from multiprocessing.context import reduction, set_spawning_popen
    from multiprocessing.popen_spawn_win32 import TERMINATE, WINEXE, WINSERVICE, WINENV, _path_eq
    from pathlib import Path
    import os
    import msvcrt
    import sys
    import _winapi

    if (sys.version_info > (3, 8, )):
        from multiprocessing import resource_tracker as tracker 
        from multiprocessing.popen_spawn_win32 import _close_handles
    else:
        from multiprocessing import semaphore_tracker as tracker 
        _close_handles = _winapi.CloseHandle

    l1ll1ll11l1l11llIl1l1 = spawn.get_preparation_data(ll1l1l111l1lll11Il1l1._name)







    (l11ll11l11lll1l1Il1l1, llll1ll11l1l1111Il1l1, ) = _winapi.CreatePipe(None, 0)
    llll1l1ll111ll11Il1l1 = msvcrt.open_osfhandle(llll1ll11l1l1111Il1l1, 0)
    lll1l1l1111ll1llIl1l1 = spawn.get_executable()
    l111lll11l11111lIl1l1 = str(Path(l1ll1ll11l1l11llIl1l1['sys_argv'][0]).absolute())
    lll111l11lll1l1lIl1l1 = ' '.join([lll1l1l1111ll1llIl1l1, '-B', '-m', 'reloadium', 'spawn_process', str(os.getpid()), 
str(l11ll11l11lll1l1Il1l1), l111lll11l11111lIl1l1])



    if ((WINENV and _path_eq(lll1l1l1111ll1llIl1l1, sys.executable))):
        lll1l1l1111ll1llIl1l1 = sys._base_executable
        l1lllll1l11ll1llIl1l1 = os.environ.copy()
        l1lllll1l11ll1llIl1l1['__PYVENV_LAUNCHER__'] = sys.executable
    else:
        l1lllll1l11ll1llIl1l1 = None

    with open(llll1l1ll111ll11Il1l1, 'wb', closefd=True) as l1lll1l11ll11lllIl1l1:

        try:
            (l11l11l1l1l1l111Il1l1, l1l1lll1l1l1llllIl1l1, ll11l11l11lll1l1Il1l1, l111ll11l11l11l1Il1l1, ) = _winapi.CreateProcess(lll1l1l1111ll1llIl1l1, lll111l11lll1l1lIl1l1, None, None, False, 0, l1lllll1l11ll1llIl1l1, None, None)


            _winapi.CloseHandle(l1l1lll1l1l1llllIl1l1)
        except :
            _winapi.CloseHandle(l11ll11l11lll1l1Il1l1)
            raise 


        ll111l1lll1l1111Il1l1.pid = ll11l11l11lll1l1Il1l1
        ll111l1lll1l1111Il1l1.returncode = None
        ll111l1lll1l1111Il1l1._handle = l11l11l1l1l1l111Il1l1
        ll111l1lll1l1111Il1l1.sentinel = int(l11l11l1l1l1l111Il1l1)
        if (sys.version_info > (3, 8, )):
            ll111l1lll1l1111Il1l1.finalizer = util.Finalize(ll111l1lll1l1111Il1l1, _close_handles, (ll111l1lll1l1111Il1l1.sentinel, int(l11ll11l11lll1l1Il1l1), 
))
        else:
            ll111l1lll1l1111Il1l1.finalizer = util.Finalize(ll111l1lll1l1111Il1l1, _close_handles, (ll111l1lll1l1111Il1l1.sentinel, ))



        set_spawning_popen(ll111l1lll1l1111Il1l1)
        try:
            reduction.dump(l1ll1ll11l1l11llIl1l1, l1lll1l11ll11lllIl1l1)
            reduction.dump(ll1l1l111l1lll11Il1l1, l1lll1l11ll11lllIl1l1)
        finally:
            set_spawning_popen(None)
