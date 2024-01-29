# What the code does

1. Identify existing mp4 file starting block(s) for mp4 files
2. Iterate through all direct and indirect blocks to recover the bytes
3. Save the output(s) as Output\<x\>.mp4

# To run the Recovery Program

## SET UP THE FLASH DRIVE

### 1. Zero out, make ext3, get ownership

    $ sudo dd if=/dev/zero of=<device_path> bs=4M
    $ sudo mkfs.ext3 <device_path>
    $ sudo mkdir ~/<my_location>
    $ sudo mount <device_path> ~/<my_location>
    $ sudo chown -R <username>:<username> ~/<my_location>
    $ sudo chmod -R 777 ~/<my_location>

### 2. Move files into the flash drive

### 3. Use inode tool to verify block numbers, keep note of the datablocks in notes.txt

### 4. Remove files from the flash drive

    $ rm -f sample-5s.mp4
    $ rm -f sample-10s.mp4
    $ rm -f sample-15s.mp4
    $ rm -f sample-20s.mp4

### 5. Unmount the flash drive

    $ sudo umount <device_path>

## Executing the program

### 1. Open Terminal and navigate to source directory

### 2. Compile and Execute

    $ g++ recovery.cpp -o recovery
    $ sudo ./recovery <device_path>

## Output

### The outputX.mp4 will be saved to the directory of the source code.

## Condition in which the file can be successfully recovered.

    1. Open a terminal
    2. Navigate to the directory where the program is located
    3. Type: g++ recovery.cpp -o recovery
    4. Type: ./recovery <device path>
    5. The program will output the recovered video files into the directory of the code
