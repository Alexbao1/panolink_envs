import bz2
import gzip
import lzma
from subprocess import Popen, PIPE
from typing import Optional
from shutil import which

def fopen(filename, mode='rt', *args, **kwargs):
    """
    Opens file for reading or writing as either gzip, bzip2, xz, or uncompressed depending on extensions.
    :param filename: name of file to read/write
    :param mode: any valid file mode for the type of file (wt, rt, wb, rb) are universal
    :param args: passthrough positional arguments
    :param kwargs: passthrough keywork arguments
    :return: opened file object
    """
    if filename.endswith('.gz'):
        return gzip.open(filename, mode, *args, **kwargs)
    elif filename.endswith('.bz2'):
        return bz2.open(filename, mode, *args, **kwargs)
    elif filename.endswith('.xz'):
        return lzma.open(filename, mode, *args, **kwargs)
    return open(filename, mode, *args, **kwargs)

class fopen2:
    read = '{} -d -c {}'
    write = '{} > {}'

    def __init__(self, filename, mode='rt', processes=0, *args, **kwargs):
        self.filename = filename
        self.mode = mode
        self.args = args
        self.kwargs = kwargs
        self.f = None
        self.p: Optional[Popen] = None
        if which('pigz') is not None:
            self.gz = 'pigz'
        else:
            self.gz = 'gzip'
        if which('lbzip2') is not None:
            self.bz = 'lbzip2'
            if processes > 0:
                self.bz += ' -n {}'.format(processes)
        else:
            self.bz = 'bzip2'

        if self.filename.endswith('.gz'):
            comp = self.gz
        elif self.filename.endswith('.bz2'):
            comp = self.bz
        else:
            self.f = open(self.filename, self.mode, *self.args, **self.kwargs)
            return
        if self.mode[0] == 'r':
            cmd = self.read
            stdout = PIPE
            stdin = None
        else:
            cmd = self.write
            stdout = None
            stdin = PIPE
        cmd = cmd.format(comp, self.filename)
        if len(self.mode) > 1 and self.mode[1] == 't':
            universal_newlines = True
        else:
            universal_newlines = False
        self.p = Popen(cmd, shell=True, universal_newlines=universal_newlines, stdout=stdout, stdin=stdin)
        if stdout is not None:
            self.f = self.p.stdout
        elif stdin is not None:
            self.f = self.p.stdin

    def __iter__(self):
        return self.f

    def __enter__(self):
        # if self.filename.endswith('.gz'):
        #     comp = self.gz
        # elif self.filename.endswith('.bz2'):
        #     comp = self.bz
        # else:
        #     self.f = open(self.filename, self.mode, *self.args, **self.kwargs)
        #     return self.f
        # if self.mode[0] == 'r':
        #     cmd = self.read
        #     stdout = PIPE
        #     stdin = None
        # else:
        #     cmd = self.write
        #     stdout = None
        #     stdin = PIPE
        # cmd = cmd.format(comp, self.filename)
        # if len(self.mode) > 1 and self.mode[1] == 't':
        #     universal_newlines = True
        # else:
        #     universal_newlines = False
        # self.p = Popen(cmd, shell=True, universal_newlines=universal_newlines, stdout=stdout, stdin=stdin)
        # if stdout is not None:
        #     self.f = self.p.stdout
        # elif stdin is not None:
        #     self.f = self.p.stdin
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.f.close()
        if self.p is not None:
            self.p.wait()
