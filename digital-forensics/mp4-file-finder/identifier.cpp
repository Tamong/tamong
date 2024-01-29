/*
    Philip Wallis | PTW190000
    CS 4398.001 - Digital Forensics
    Professor Neeraj Gupta - Spring 2023
    
*/

// imports
#include <iostream>
#include <iomanip>
#include <fcntl.h>
#include <unistd.h>

using namespace std;

// global variables
char* devicePath;

// function definitions
void getMP4BlockNum();

// main function

int main(int argc, char* argv[]) {

    cout << "PHILIP WALLIS | PTW190000" << endl;

    // check for correct number of arguments
    if (argc != 2) {
        cout << "Usage: ./finder <device path>" << endl;
        return 1;
    }
    // assign arguments to global variables
    devicePath = argv[1];

    cout << "mp4 files identified in the device " << devicePath << ":" << endl;
    cout << "File # | Block #" << endl;
    // print mp4 block numbers
    getMP4BlockNum();

    return 0;
}

// get mp4 block numbers
void getMP4BlockNum() {

    // Open the device or partition in read-only mode
    int fd = open(devicePath, O_RDONLY);
    int file_num = 1;

    // Check if the device was opened successfully
    if (fd == -1) {
        cerr << "Failed to open device\n";
        exit(1);
    }

    // Calculate the total number of blocks
    uint64_t end = lseek(fd, 0, SEEK_END);
    uint32_t num_blocks = end / 4096; // 4096 is the block size

    // Reset the file offset to the beginning of the partition
    lseek(fd, 0, SEEK_SET);

    // Iterate over each block
    for (uint32_t block_num = 0; block_num < num_blocks; block_num++) {
        bool found = false;

        // get the block offset
        uint64_t offset = block_num * 4096;

        // check if the offset is correct
        if (offset > end) {
            cerr << "Offset is out of bounds\n";
            exit(1);
        }

        // seek to the block offset in the device
        lseek(fd, offset, SEEK_SET);

        // read the next 8 bytes for ftyp
        unsigned char readblock[8];
        read(fd, readblock, 8);
        unsigned int ftyp = (readblock[4] << 24) | (readblock[5] << 16) | (readblock[6] << 8) | readblock[7];

        if (ftyp == 0x66747970) { // Compare ftyp with 0x66747970 directly
            found = true;
        }

        if(found){
            cout << setw(6) << right << file_num << " | " << setw(8) << left << block_num << endl;
            file_num++;
        }


    }

    // Close the device
    close(fd);
}
