import subprocess
import sys
from datetime import datetime, timedelta
import shlex

class Tailer:
    def __init__(self, command, maxsize=float("inf"), maxtime=timedelta.max, func=sys.stdout.write):
        self.maxsize = maxsize
        self.maxtime = maxtime
        self.command = shlex.split(command)
        self.func = func
        self.chunk = bytearray()

    def run(self):
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE)
        self.lastsent = datetime.now()
        while True:
            output = process.stdout.read(1)
            if output == "" and process.poll() is not None:
                break
            if output:
                self.sendchunk(output)
                # sys.stdout.write(output.decode("utf-8"))
                # sys.stdout.flush()
            rc = process.poll()

    def sendchunk(self, output):
        self.chunk.extend(output)
        since = datetime.now() - self.lastsent
        if len(self.chunk) < self.maxsize and since < self.maxtime:
            pass
        else:
            self.func(self.chunk)
            # sys.stdout.write(self.chunk.decode("utf-8"))
            # sys.stdout.write(" ")
            # sys.stdout.flush()
            self.chunk = bytearray()
            self.lastsent = datetime.now()
    
def chunkprinter(chunk):    
    sys.stdout.write(chunk.decode("utf-8"))
    sys.stdout.write(" ")
    sys.stdout.flush()
     
command = "tail -f /tmp/0"
# command = ["tail", "-f", "/tmp/0"]
# t = Tailer(command, maxsize=4, maxtime=timedelta(seconds=2))
# t = Tailer(command, maxsize=8)
t = Tailer(command, maxtime=timedelta(seconds=2), func=chunkprinter)
t.run()
