from anytree import Node, RenderTree, NodeMixin
from math import floor

    


class DataNode(NodeMixin):  
    def __init__(self, name, parent=None, children=None):
        super(DataNode, self).__init__()
        self.name = name
        self.parent = parent
        if children:
            self.children = children

files = {}
nodes = {}

# Root file class

class root_file():
    def __init__(self,name = "data.dat", size = 1000, track_size = 100):
        self.name = name
        self.size = size
        self.track_size = track_size
        self.available_tracks = list(range(1,floor(size / track_size) + 1))
        self.used_tracks = []


    def create_file(self):
        self.f = open(self.name, 'wb')
        self.f.seek(self.size-1)
        self.f.write(b"\0")
        self.f.close()

    def write_to_file(self, text):
        self.f = open(self.name, 'r+b')
        if self.available_tracks != []:
            self.f.seek((self.available_tracks[0] - 1 )*self.track_size)
            self.f.write(text.encode('utf-8'))
            temp = self.available_tracks.pop(0)
            self.used_tracks.append(temp)

    def write_to_file_at(self, text, write_at, track_num):
        self.f = open(self.name, 'r+b')
        self.f.seek(((track_num - 1)*self.track_size)+write_at)
        self.f.write(text.encode('utf-8'))

    def read_from_file(self,track_list,bytes_on_tracks):
            output = ""
            f = open("data.dat", "rb")
            for t in track_list:
                f.seek((t-1)*self.track_size)
                output += f.read(bytes_on_tracks[t]).decode('utf-8')
            f.close()
            return output.strip()

    def read_from_file_at(self,tracks,start_track,start_byte_position,size):
        remaining_bytes = size
        self.f = open("data.dat", "rb")
        content_to_read = ""
        bytes_to_read = 0
        for track in tracks:
            if track >= start_track:
                if remaining_bytes <= tracks[track]:
                    bytes_to_read = remaining_bytes
                else:
                    bytes_to_read = tracks[track]

                self.f.seek(((track - 1)*self.track_size)+start_byte_position)
                content_to_read += self.f.read(bytes_to_read).decode('utf-8')
                remaining_bytes -= bytes_to_read
        return content_to_read

root = root_file()
nodes["root"] = DataNode(root.name)

class FileObj():
    def __init__(self,name,mode,root_file = root):
        self.name = name
        self.mode = mode
        self.size = 0
        self.track = 0
        self.size_on_track = 0
        self.root_file = root_file
        self.file_tracks = []
        self.bytes_on_tracks = {}
        self.content = ""
        self.open = False

    def write_to_file(self,text):
        self.content += text
        self.root_file.write_to_file(text)
        track_num = self.root_file.used_tracks[-1]
        self.file_tracks.append(track_num)
        self.bytes_on_tracks[track_num] = len(text)
        self.size += len(text)
        nodes[track_num] = DataNode(track_num, parent=nodes[self.name])
        print("Data has been written to file!")

    def write_to_file_at(self,text,write_at=0):
        self.input_text = text
        self.content += self.input_text
        track_to_write = 0
        byte_counter = write_at
        if (write_at <= self.size):
            for key in self.bytes_on_tracks:
                if byte_counter < self.bytes_on_tracks[key]:
                    track_to_write = key
                    break
                else:
                    byte_counter -= self.bytes_on_tracks[key]
            self.root_file.write_to_file_at(self.input_text,byte_counter,track_to_write)
        else:
            self.write_to_file(text)


    def read_from_file(self):
        output = self.root_file.read_from_file(self.file_tracks,self.bytes_on_tracks)
        return output

    def track_finder(self,byte_position):
        track = 0
        byte_counter = byte_position
        for key in self.bytes_on_tracks:
            if byte_counter < self.bytes_on_tracks[key]:
                start_track = key
                break
            else:
                byte_counter -= self.bytes_on_tracks[key]
        return track,byte_counter

    def read_from_file_at(self,start,size):
        start_track, start_byte_counter = self.track_finder(start)
        read_content = self.root_file.read_from_file_at(self.bytes_on_tracks, start_track, start_byte_counter, size)
        return read_content



    def chDir(self,DirName):
        if DirName in nodes:
            children = nodes[self.name].children
            nodes[self.name].parent = None
            nodes[self.name] = DataNode(self.name, parent=nodes[DirName])
            nodes[self.name].children = children
        else:
            print("Given directory does not exist")

    def copy_within_file(self,start,size,target):
        content_to_copy = self.read_from_file_at(start,size)
        self.write_to_file_at(content_to_copy,write_at=start)
 

# Main required Functions
def open_file(fname, mode="r+w"):
    """ Modes: r = read, w = write, r+w = read and write (append) """
    files[fname] = FileObj(fname,mode)
    print("File has been opened!")
    return files[fname]

def create(fname, p = nodes["root"]):
    print("File has been created!")
    open_file(fname)
    nodes[fname] = DataNode(files[fname].name, parent=p)

def delete(fname):
    nodes[fname].parent = None
    print("File has been deleted!")

def close(fname):
    files[fname].open = False
    print("File has been Closed!")

def show_memory_map():
    print("Showing Memory Map: ")
    for pre, fill, node in RenderTree(nodes["root"]):
        print("%s%s" % (pre, node.name))

def makeDir(fname):
    nodes[fname] = DataNode(files[fname].name, parent= nodes["root"])
    print("Directory has been created!")




while True:
    print("What operation do you want to perform:\n1. Create File \n2. Delete File \n3. Open File \n4. Close File \n5. Write to file \n6. Write to file at \n7. Read from file \n 8. Read from file at \n9. Make Directory \n10. Change Directory \n11. Show memory map \n12. Exit")
    decision = int(input())
    if (decision == 1):
        file_name = input("Enter the name of the file: ")
        create(file_name)
        print("File created!")
    elif (decision == 2):
        file_name = input("Enter the name of the file: ")
        if file_name in files.keys():
            delete(file_name)
            print("File deleted")
        else:
            print("File does not exist")
    elif (decision == 3):
        file_name = input("Enter the name of the file: ")
        if file_name in files.keys():
            f = open(file_name)
            print("File opened")
        else:
            print("File does not exist")

    elif (decision == 4):
        file_name = input("Enter the name of the file: ")
        if file_name in files.keys():
            close(file_name)
            print("File closed")
        else:
            print("File does not exist")

    elif (decision == 5):
        file_name = input("Enter the name of the file: ")
        if file_name in files.keys():
            text = input("Enter the text to be written on file: ")
            files[file_name].write_to_file(text)
            print("Given content written to file successfully!")
        else:
            print("File does not exist")

    elif (decision == 6):
        file_name = input("Enter the name of the file: ")
        position = int(input("What position do you want to write at: "))
        if file_name in files.keys():
            text = input("Enter the text to be written on file: ")
            files[file_name].write_to_file_at(text,position)
            print("Given content written to file successfully!")
        else:
            print("File does not exist")

    elif (decision == 7):
        file_name = input("Enter the name of the file: ")
        if file_name in files.keys():
            print("Reading from file: ")
            print(files[file_name].read_from_file())
        else:
            print("File does not exist")

    elif (decision == 8):
        file_name = input("Enter the name of the file: ")
        position = int(input("Enter byte position to read the file: "))
        size = int(input("Enter the size of read: "))
        if file_name in files.keys():
            print("Reading from file: ")
            print(files[file_name].read_from_file_at(position,size))
        else:
            print("File does not exist")
    
    elif (decision == 9):
        directory = input("Enter name of the new directory: ")
        makeDir(directory)

    elif (decision == 10):
        file_name = input("Enter the name of the file whose directory is to be changed: ")
        target_directory = input("Enter name of target directory: ")
        files[file_name].chDir(target_directory)

    elif (decision == 11):
        show_memory_map()
    
    elif (decision == 12):
        break
    else:
        print("Invalid input")
