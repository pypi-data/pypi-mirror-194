import errno
import os
import signal
import sys
from typing import Union, Optional, Callable, Tuple, Any


class Daemon(object):

    def __init__(
            self,
            daemon: Union[bool] = True,
            chdir: Optional[str] = "/",
            umask: Optional[int] = 0o02,
            pid_file: Optional[str] = "/var/daemon.pid",
            stdin: Optional[str] = os.devnull,
            stdout: Optional[str] = os.devnull,
            stderr: Optional[str] = os.devnull,
            target: Optional[Callable] = Callable,
            params: Tuple[Any, ...] = tuple(),
            *args,
            **kwargs
    ):
        self.daemon = daemon
        self.chdir = chdir
        self.umask = umask
        self.pid_file = pid_file
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.alive = True
        self.target = target
        self.params = params

    def daemonize(self):
        def sigHandler(num, frame):
            self.alive = False
            sys.exit()

        try:
            if os.fork():
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("sub process fork 1 failed: (%s %s)" % (e.errno, e.strerror))
            sys.exit(1)

        os.umask(self.umask)
        os.chdir(self.chdir)
        os.setsid()
        try:
            pid = os.fork()
            if pid:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("sub process fork 2 failed: (%s %s)" % (e.errno, e.strerror))
            sys.exit(1)
        signal.signal(signal.SIGTERM, sigHandler)
        signal.signal(signal.SIGINT, sigHandler)
        open(self.pid_file, "w+").write("%s\n" % os.getpid())

    def start(self):

        try:
            with open(self.pid_file, 'r') as fd:
                pid = int(fd.readline().strip())
        except IOError:
            pid = None
        except SystemExit:
            sys.exit(1)
        if pid:
            sys.stderr.write("pidfile %s already exists. is it already running?" % self.pid_file)
            sys.exit(1)
        if self.daemon:
            self.daemonize()
        self.run()

    def stop(self):
        pid = self.get_pid()
        if not pid:
            sys.stderr.write("pidfile % s does not  exists" % self.pid_file)
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            return
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            if e.errno == errno.ESRCH:
                if os.path.exists((self.pid_file)):
                    os.remove(self.pid_file)
            else:
                print(str(e.strerror))
                sys.exit(1)
        print("%s process is stopped" % pid)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        self.target(*self.params)

    def get_pid(self):
        try:
            with open(self.pid_file, 'r') as fd:
                pid = int(fd.readline().strip())
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def del_pid(self):
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
