"""Subprocess helper
"""

from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio import create_subprocess_exec, wait_for
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from subprocess import PIPE, CalledProcessError

from .logging import LOGGER

DEFAULT_PROG_TIMEOUT = 120  # 2 minutes


class CalledProcessState(Enum):
    """MKCTF called process states"""

    SUCCESS = 0x00000000
    NOT_APPLICABLE = 0x00000002
    MANUAL = 0x00000003
    NOT_IMPLEMENTED = 0x00000004
    FAILURE = 0xFFFFFFF1
    TIMEOUT = 0xFFFFFFF2
    EXCEPTION = 0xFFFFFFFF


_HEALTHY_STATES = {
    CalledProcessState.MANUAL,
    CalledProcessState.SUCCESS,
    CalledProcessState.NOT_APPLICABLE,
}
_CALLED_PROCESS_STATES = {
    CalledProcessState.SUCCESS,
    CalledProcessState.NOT_APPLICABLE,
    CalledProcessState.MANUAL,
    CalledProcessState.NOT_IMPLEMENTED,
}


@dataclass
class CalledProcessResult:
    """Called process result"""

    stdout: bytes | None = None
    stderr: bytes | None = None
    exception: str | None = None
    returncode: int = CalledProcessState.EXCEPTION.value

    @property
    def returnstate(self) -> CalledProcessState:
        """Called process return state"""
        if self.returncode in _CALLED_PROCESS_STATES:
            return CalledProcessState(self.returncode)
        return CalledProcessState.FAILURE

    @property
    def healthy(self) -> bool:
        """Determine if program return state is healthy"""
        return self.returnstate in _HEALTHY_STATES

    def to_dict(self):
        """Convert instance to dict"""
        return {
            'stdout': self.stdout,
            'stderr': self.stderr,
            'exception': self.exception,
            'returncode': self.returncode,
            'returnstate': self.returnstate.name,
        }


async def run_mkctf_prog(
    prog: str, cwd: Path, dev: bool, timeout: int | None = None
) -> CalledProcessResult:
    """Runs a script as an asynchronous subprocess"""

    if timeout is None:
        timeout = DEFAULT_PROG_TIMEOUT
    LOGGER.info("running '%s' within %s (timeout=%d)", prog, cwd, timeout)
    args = [str(cwd / prog)]
    if dev:
        args.append('--dev')
    proc = await create_subprocess_exec(
        *args, stdout=PIPE, stderr=PIPE, cwd=str(cwd)
    )
    try:
        stdout, stderr = await wait_for(proc.communicate(), timeout=timeout)
        return CalledProcessResult(
            stdout=stdout, stderr=stderr, returncode=proc.returncode
        )
    except AsyncioTimeoutError:
        proc.terminate()
        return CalledProcessResult(
            exception="timeout", returncode=CalledProcessState.TIMEOUT.value
        )
    except CalledProcessError as exc:
        return CalledProcessResult(
            stdout=exc.stdout,
            stderr=exc.stderr,
            exception="called process error",
            returncode=exc.returncode,
        )
    except Exception as exc:
        return CalledProcessResult(exception=str(exc))
