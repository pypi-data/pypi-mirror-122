import selectors
import sys
from io import StringIO
from subprocess import Popen  # nosec
from threading import Thread
from typing import Any


class ProcessStdoutCapturingBuffer(Thread):
    """Capture the stdout of a process in a buffer before redirecting it to the parent process' stdout."""

    def __init__(
        self,
        # Omitting Popen's generic argument as it raises an error at runtime.
        process: Popen,  # type: ignore
    ):
        """Constructor.

        Args:
            process: The started process whose stdout we want to store.
                The process has to have been started with ``bufsize=1`` and ``universal_newlines=True``.
        """
        Thread.__init__(self)
        self.process = process
        self.buf = StringIO()
        self.selector = selectors.DefaultSelector()
        self.write_to_buffer = True
        self.selector.register(
            self.process.stdout, selectors.EVENT_READ, self.handle_output  # type: ignore
        )

    def handle_output(self, stream: Any):
        """Write the lines written to the stream in the buffer and then to the parent process' stdout"""
        line = stream.readline()
        if self.write_to_buffer:
            self.buf.write(line)
        sys.stdout.write(line)

    def stop_writing_to_buffer(self):
        self.write_to_buffer = False

    def run(self):
        # Loop until the process is terminated
        while self.process.poll() is None:
            events = self.selector.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
            if not self.write_to_buffer:
                self.buf.close()

        self.process.wait()
        self.selector.close()
