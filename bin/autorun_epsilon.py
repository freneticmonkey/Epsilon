#!C:\Python27\python.exe
import os
import sys
import subprocess
import time
import operator

ignore_ext = [".swp", ".txt", ".pyc", ".cfg"]

def file_filter(name):
    passed = True

    if name.startswith("."):
        passed = False
    else:
        for ext in ignore_ext:
            if name.endswith(ext):
                passed = False
                break
    return passed

def file_times(path):
    
    for top_level in filter(file_filter, os.listdir(path)):

        #print os.walk(os.path.join(path,top_level))
        for root, dirs, files in os.walk(os.path.join(path,top_level)):#os.walk(top_level):
            for f in filter(file_filter, files):
                #print os.path.join(root, f)
                #result.append(os.stat(os.path.join(root, f)).st_mtime)
                yield (os.stat(os.path.join(root, f)).st_mtime, f)

def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print stdout


# We concatenate all of the arguments together, and treat that as the command to run
#command = ' '.join(sys.argv[1:])
command = "python run_epsilon.py"

# Gen the epsilon path
epsilon_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

# The path to watch
path = epsilon_path#'.'

# How often we check the filesystem for changes (in seconds)
wait = 3

# The process to autoreload
process = subprocess.Popen(command)

# The current maximum file modified time under the watched directory
last_mtime = max(file_times(path), key=operator.itemgetter(0))

while True:
    max_mtime = max(file_times(path), key=operator.itemgetter(0))
    print_stdout(process)
    if max_mtime[0] > last_mtime[0]:
        last_mtime = max_mtime

        print '\n>> File Change detected in: %s. Restarting process.\n' % max_mtime[1]
        
        process.kill()
        process = subprocess.Popen(command)

    else:
        # Check if the process has been closed. If so exit.
        process.poll()
        if process.returncode == 0:
            print "\n>> Process terminated.  Autorun exiting."
            break
    time.sleep(wait)