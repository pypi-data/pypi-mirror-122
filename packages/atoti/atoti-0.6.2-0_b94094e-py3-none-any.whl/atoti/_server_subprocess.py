from __future__ import annotations

import os
import platform
import random
import re
import string
import time
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen  # nosec
from typing import TYPE_CHECKING, Collection, Optional, Tuple

from ._capturing_buffer import ProcessStdoutCapturingBuffer
from ._java_utils import JAR_PATH, get_java_path
from ._path_utils import get_atoti_home, to_absolute_path
from ._plugins import get_active_plugins

if TYPE_CHECKING:
    from .config import SessionConfig

DEFAULT_HADOOP_PATH = Path(__file__).parent / "bin" / "hadoop-3.2.1"

REGEX = "Py4J server started on port (?P<port>[0-9]+)"


def _create_session_directory() -> Path:
    """Create the directory that will contain the session files."""
    # Generate the directory name using a random string for uniqueness.
    random_string = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    session_directory = get_atoti_home() / f"{str(int(time.time()))}_{random_string}"

    # Create the session directory and its known sub-folders.
    session_directory.mkdir(parents=True)
    _compute_log_directory(session_directory).mkdir()

    return session_directory


def _compute_log_directory(session_directory: Path) -> Path:
    """Return the path to the logs directory."""
    return session_directory / "logs"


def get_plugin_jar_paths() -> Collection[str]:
    """Get the JAR paths of the available plugins."""
    return [
        str(plugin.get_jar_path())
        for plugin in get_active_plugins().values()
        if plugin.get_jar_path()
    ]


class ServerSubprocess:
    """A wrapper class to start and manage an atoti server from Python."""

    def __init__(self, *, config: SessionConfig):
        """Create and start the subprocess."""
        self._config = config
        self._log_to_stdout = (
            config.logging is not None and config.logging.file_path is None
        )
        self._capturing_buffer: Optional[ProcessStdoutCapturingBuffer] = None

        self._session_directory = _create_session_directory()
        self._subprocess_log_file = (
            _compute_log_directory(self._session_directory) / "subprocess.log"
            if not self._log_to_stdout
            else None
        )
        (self._process, self.py4j_java_port) = self._start()

    def wait(self) -> None:
        """Wait for the process to terminate.

        This will prevent the Python process to exit unless the Py4J gateway is closed since, in that case, the atoti server will stop itself.
        """
        self._process.wait()
        if self._capturing_buffer is not None:
            self._capturing_buffer.join()

    def _start(self) -> Tuple[Popen, int]:
        """Start the atoti server.

        Returns:
            A tuple containing the server process and the Py4J port.
        """
        process = self._create_subprocess()
        if self._log_to_stdout:
            self._capturing_buffer = ProcessStdoutCapturingBuffer(process)
            self._capturing_buffer.start()

        # Wait for it to start
        try:
            java_port = self._await_start()
            if self._capturing_buffer is not None:
                self._capturing_buffer.stop_writing_to_buffer()
        except Exception as error:
            process.kill()
            raise error

        # We're done
        return (process, java_port)

    def _create_subprocess(self) -> Popen:
        """Create and start the actual subprocess.

        Returns:
            The created process.
        """
        program_args = [
            str(get_java_path()),
            "-jar",
        ]

        program_args.append(f"-Dserver.session_directory={self._session_directory}")
        if not self._log_to_stdout:
            program_args.append("-Dserver.logging.disable_console_logging=true")

        if self._config.port is not None:
            program_args.append(f"-Dserver.port={self._config.port}")

        program_args.extend(self._config.java_options or [])

        if platform.system() == "Windows":
            program_args.append(
                f"-Dhadoop.home.dir={to_absolute_path(DEFAULT_HADOOP_PATH)}"
            )
            hadoop_path = to_absolute_path(DEFAULT_HADOOP_PATH / "bin")
            if hadoop_path not in os.environ["PATH"]:
                os.environ["PATH"] = f"{os.environ['PATH']};{hadoop_path}"

        # Put JARs from user config or from plugins into loader path
        jars = [*(self._config.extra_jars or []), *get_plugin_jar_paths()]
        if len(jars) > 0:
            program_args.append(
                f"-Dloader.path={','.join([to_absolute_path(jar) for jar in jars])}"
            )

        program_args.append(to_absolute_path(JAR_PATH))

        # Create and return the subprocess.
        # We allow the user to pass any argument to Java, even dangerous ones
        try:
            if self._log_to_stdout:
                process = Popen(  # pylint: disable=consider-using-with
                    program_args,
                    bufsize=1,
                    stderr=STDOUT,
                    stdout=PIPE,
                    universal_newlines=True,
                )  # nosec
            else:
                process = Popen(  # pylint: disable=consider-using-with
                    program_args,
                    stderr=STDOUT,
                    stdout=open(  # type: ignore  # pylint: disable=consider-using-with
                        self._subprocess_log_file, "wt"
                    ),
                )  # nosec
        except Exception as error:
            raise Exception(
                f"Could not start the session. You can check the logs at {self._subprocess_log_file}",
            ) from error

        return process

    def _await_start(self) -> int:
        """Wait for the server to start and return the Py4J Java port."""
        period = 0.25
        timeout = 60
        attempt_count = round(timeout / period)
        # Wait for the process to start and log the Py4J port.
        for _attempt in range(1, attempt_count):  # pylint: disable=unused-variable
            # Look for the started line.
            try:
                if self._capturing_buffer is None:
                    with open(self._subprocess_log_file) as log_file:  # type: ignore
                        for line in log_file:
                            match = re.search(REGEX, line.rstrip())
                            if match:
                                # Server should be ready.
                                return int(match.group("port"))
                else:
                    match = re.search(REGEX, self._capturing_buffer.buf.getvalue())
                    if match:
                        # Server should be ready.
                        return int(match.group("port"))

            except FileNotFoundError:
                # The logs file has not yet been created.
                pass

            # The server is not ready yet.
            # Wait for a bit.
            time.sleep(period)

        # The inner loop did not return.
        # This means that the server could not be started correctly.
        raise Exception(
            "Could not start server. " + f"Check the logs: {self._subprocess_log_file}"
        )

    @property
    def logs_path(self) -> Path:
        """Path to the server log file."""
        if self._log_to_stdout:
            raise ValueError("Logs have been configured to be written to stdout.")
        return (
            _compute_log_directory(self._session_directory) / "server.log"
            if self._config.logging is None or self._config.logging.file_path is None
            else Path(self._config.logging.file_path)
        )
