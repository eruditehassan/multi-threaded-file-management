# Multi Threaded File Management System
Operating System level Multi Threaded File Management System in Python

A brief documentation of the working of the project
## Dependencies and Libraries used
Following python libraries were used along with the purpose of use:
1. Math library was used briefly to handle a trivial calculation
2. Anytree library was obtained from pypi and a custom tree data structure was built after inheriting from the Anytree base NodeMixin class, and that tree data structure was used to keep track of the files and the memory storage locations and also for creating and visualizing a memory map.
3. Threading library used for creating threads

## SYSTEM DESCRIPTION
### File Management System Description
The implemented system is a file management system. It uses a single data.dat file as a main directory which further consists of small files, which are created by user. For example, if Data.dat file is of 1000 bytes i.e. 1KB. The file is further divided into 10 tracks with size of 100 bytes each.
We implemented a tree data structure to keep records of files in a directory. Data.dat file will be parent node of the tree. This is done by using anytree library of python. When a file named file1.txt is created, it will be stored in first track which ranges from 1st byte to 100th byte (index position 0 to 99). If another file is created, it will be stored in succeeding track i.e. 2nd track. When more content is to be added into file1.txt, it will be look for next available track, for example the 3rd track.
### Multithreaded File Management System Description
This system works with the help of threading library of python for creating threads and executing commands from input files in parallel manner. It is based on the previously built File management system. It parses commands and values from the input files and executes those commands with the help of values accordingly.

### Directory Structure
**Tree data structure** is used to show the directory and the corresponding memory locations of the files in the form of track numbers.

## USER MANUAL
The user is provided with an interface to use the system.
- System accepts text files with names of format “input_thread[x]" where x is the number of the thread.
- User must make sure that the number of input files equal to the chosen number of threads are present otherwise it might generate a runtime error
- User must make sure that the commands in the files are correct, and not invoking any errors.
- For input files, there must be in a folder named “Input” present in the same directory as the python script
- Output generated during the execution for each thread will be saved in separate files dedicated to each thread having file formats “output_thread[x]", where x is thread number
- To run the script from command line, following command can be used: `python lab_9.py -k`
where k is the number of threads to run
