import subprocess
import sys
from datetime import datetime, timedelta

class Tailer:
    def __init__(self, command, maxsize=float("inf"), maxtime=timedelta.max):
        self.maxsize = maxsize
        self.maxtime = maxtime
        self.command = command
        self.chunk = bytearray()
        if self.maxsize == float("inf") and self.maxtime == timedelta.max:
            raise Exception("maxsize or maxtime must be set")

    def run(self):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.lastsent = datetime.now()
        while True:
            output = process.stdout.read(1)
            if output == "" and process.poll() is not None:
                break
            if output:
                self.sendchunk(output, self.maxsize, self.maxtime)
                # sys.stdout.write(output.decode("utf-8"))
                # sys.stdout.flush()
            rc = process.poll()

    def sendchunk(self, output, size, maxtime):
        self.chunk.extend(output)
        since = datetime.now() - self.lastsent
        if len(self.chunk) < self.maxsize and since < self.maxtime:
            pass
        else:
            sys.stdout.write(self.chunk.decode("utf-8"))
            sys.stdout.write(" ")
            sys.stdout.flush()
            self.chunk = bytearray()
            self.lastsent = datetime.now()
    
    

command = ["tail", "-f", "/tmp/0"]
# t = Tailer(command, maxsize=4, maxtime=timedelta(seconds=2))
# t = Tailer(command, maxsize=8)
t = Tailer(command, maxtime=timedelta(seconds=2))
t.run()
