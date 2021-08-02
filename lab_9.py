from threading import Thread, Lock
from lab6_code import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('k', metavar='k', type=int, help='Number of threads to run')
args = parser.parse_args()
k = args.k
thread_id = 0
mutex = Lock()
print(k)
input()
threads = []

class file_thread(Thread):
    def __init__(self):
        global thread_id
        Thread.__init__(self)
        thread_id +=1
        self.id = thread_id
        self.input_file = ""
        self.output_file = ""
    def run(self):
        print("File thread no ",self.id, " is running")
        self.input_file = "input_thread" + str(self.id) + ".txt"
        path = "Input/" + self.input_file
        f = open(path)
        self.output_file = "output_thread" + str(self.id) + ".txt"
        op_path = "Output/" + self.output_file
        output = open(op_path, 'w')
        commands = f.read().split('\n')
        for command in commands:
            command_data = command.split(' ', maxsplit=2)

            if command_data[0].lower() == 'create':
                create(command_data[1])
                op_text = "File "+ command_data[1] + " has been created\n"
                output.write(op_text)

            elif command_data[0].lower() == 'write_to_file':
                mutex.acquire()
                files[command_data[1]].write_to_file(command_data[2])
                mutex.release()
                op_text = "Data has been written to file: "+ command_data[1] + " \n"
                output.write(op_text)

            elif command_data[0].lower() == 'delete':
                delete(command_data[1])
                op_text = "File: "+ command_data[1] + " has been deleted!\n"
                output.write(op_text)

            elif command_data[0].lower() == 'read_from_file':
                op_text = "Reading data from file: "+ command_data[1] + " \n"
                output.write(op_text)
                print(files[command_data[1]].read_from_file())

            elif command_data[0].lower() == 'open':
                open_file(command_data[1])
                op_text = "File: "+ command_data[1] + " has been opened!\n"
                output.write(op_text)

            elif command_data[0].lower() == 'close':
                close(command_data[1])
                op_text = "File: "+ command_data[1] + " has been closed!\n"
                output.write(op_text)

            elif command_data[0].lower() == 'show_memory_map':
                op_text = "Showing memory map on console!\n"
                output.write(op_text)
                show_memory_map()
        output.close()
        f.close()

for _ in range(k):
    newthread = file_thread()
    newthread.daemon = True
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()

show_memory_map()
