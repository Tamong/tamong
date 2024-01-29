/*
    Philip Wallis | PTW190000
    CS 4398.001 - Digital Forensics
    Professor Neeraj Gupta - Spring 2023

    To RUN THE PROGRAM!!
    1. Open a terminal
    2. Navigate to the directory where the program is located
    3. Type: g++ recovery.cpp -o recovery
    4. Type: ./recovery <device path>
    5. The program will output the recovered video files into the directory of the code

    To set up the flash drive for testing:


    philip@forensics:~/Desktop/Final$ sudo dd if=/dev/zero of=/dev/sda1 bs=4M
    philip@forensics:~/Desktop/Final$ sudo mkfs.ext3 /dev/sda1
    philip@forensics:~/Desktop/Final$ sudo mount /dev/sda1 ~/Documents
    philip@forensics:~/Desktop/Final$ sudo chown -R philip:philip ~/Documents
    philip@forensics:~/Desktop/Final$ sudo chmod -R 777 ~/Documents

    move files

    philip@forensics:~/Documents$ rm -f sample-5s.mp4
    philip@forensics:~/Documents$ rm -f sample-10s.mp4
    philip@forensics:~/Documents$ rm -f sample-15s.mp4
    philip@forensics:~/Documents$ rm -f sample-20s.mp4

    philip@forensics:~/Desktop/Final$ sudo umount /dev/sda1


    Use inode tool to verify the block numbers of the files

    https://samplelib.com/sample-mp4.html
*/

// imports
#include <iostream>
#include <fstream>
#include <vector>
#include <list>
#include <string>
#include <iomanip>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "ext3structs.h"

using namespace std;

// global constants
#define BLOCK_SIZE 4096

// global variables
char* devicePath;
list<uint32_t> mp4BlockNums;
list<uint32_t> mp4Inodes;

// function definitions
void getMP4BlockNum();
uint8_t *copyBlock(uint32_t block_num);
void createOutput(uint32_t block_num, int count);
uint32_t getBlock(uint32_t block_number);
uint32_t getDoubleBlock(uint32_t block_number);
uint32_t getTripleBlock(uint32_t block_number);
uint32_t writeSingleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output);
uint32_t writeDoubleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output);
uint32_t writeTripleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output);

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
    
    getMP4BlockNum();

    //createOutput(18447, 0);  
    
    int count = 0;
    // create output file
    while(!mp4BlockNums.empty()){
        if(mp4BlockNums.front() >= 1000000){
            mp4BlockNums.pop_back();
            break;
        }

        cout << "*****************************" << endl;
        uint32_t block_num = mp4BlockNums.front();
        mp4BlockNums.pop_front();
        cout << "Creating output for Block Number: " << block_num << endl << endl;
        createOutput(block_num, count);
        count++;
    }
    
    cout << endl;
    

    //copyData();

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
    for (uint32_t block_num = 0; block_num < 1000000; block_num++) {
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
            mp4BlockNums.push_back(block_num);
            file_num++;
        }
    }

    // Close the device
    close(fd);
}

// copy block data
uint8_t* copyBlock(uint32_t block_num) {
    int fd = open(devicePath, O_RDONLY);

    // Check if the device was opened successfully
    if (fd == -1) {
        cerr << "Failed to open device in copyBlock\n";
        exit(1);
    }

    off_t offset = block_num * BLOCK_SIZE;
    if (lseek(fd, offset, SEEK_SET) == -1) {
        perror("Failed to seek file");
        close(fd);
        return NULL;
    }

    uint8_t* buf = (uint8_t*)malloc(BLOCK_SIZE);
    if (buf == NULL) {
        perror("Failed to allocate memory");
        close(fd);
        return NULL;
    }

    ssize_t num_read = 0;
    ssize_t total_read = 0;
    while (total_read < BLOCK_SIZE) {
        num_read = read(fd, buf + total_read, BLOCK_SIZE - total_read);
        if (num_read == -1) {
            perror("Failed to read file");
            delete[] buf;
            close(fd);
            return NULL;
        }
        total_read += num_read;
    }

    close(fd);

    return buf;
}

void createOutput(uint32_t block_num, int count){
    ofstream output;
    string fileName = "output" + to_string(count) + ".mp4";

    output.open(fileName, ios::out | ios::binary);
    if(output.is_open()){
        
        cout << "**Processing direct blocks..." << endl;
        for(int i = 0; i < 12; i++){
            uint8_t *buffer = copyBlock(block_num+i);
            output.write((char*)buffer, BLOCK_SIZE);
        }

        /***********************************************************/
        uint32_t lastSingleIndirectBlock = writeSingleIndirectBlocks(block_num+12, block_num+12, output);
        if(lastSingleIndirectBlock > 1){
            uint32_t lastDoubleIndirectBlock = writeDoubleIndirectBlocks(lastSingleIndirectBlock+1, lastSingleIndirectBlock+1, output);
            if(lastDoubleIndirectBlock > 1) {
                uint32_t lastTripleIndirectBlock = writeTripleIndirectBlocks(lastDoubleIndirectBlock+1, lastDoubleIndirectBlock+1, output);
                cout << "Last double indirect block from triple indirect block: " << lastTripleIndirectBlock << endl;
                //uint32_t lastTripleIndirectBlock = writeDoubleIndirectBlocks(lastDoubleIndirectBlock+1, output);
                //if(lastTripleIndirectBlock > 1){
                //    cout << "Last double indirect block from triple indirect block: " << lastTripleIndirectBlock << endl;
                //}
            }
        }
        /***********************************************************/

    }
    output.close();
    cout << "Output file created: " << fileName << endl;
    cout << endl;
}
       

uint32_t getBlock(uint32_t block_number){
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
    // block_num < num_blocks
    for (uint32_t block_num = 10000; block_num < num_blocks; block_num++) {
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

        // read the next 4 bytes
        uint32_t readblock[8];
        read(fd, readblock, 8);
        
        //cout << "Block " << block_num << " contains: " << readblock[0] << endl;
        if(readblock[0] == block_number ){
            cout << "Found data block " << dec << block_number << " from pointer block " << block_num << endl;
            return block_num;
        }

    }

    // Close the device
    close(fd);

    return (uint32_t)NULL;
}

uint32_t getDoubleBlock(uint32_t block_number){
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
    // block_num < num_blocks
    for (uint32_t block_num = 10000; block_num < num_blocks; block_num++) {
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

        // read the next 4 bytes
        uint32_t readblock[8];
        read(fd, readblock, 8);
        
        if(readblock[0] == block_number ){
            cout << "Found data block " << dec << block_number << " from pointer block " << block_num << endl;
            uint32_t doublePointer = getBlock(block_num);
            cout << "found pointer block " << block_num << " from double pointer block " << doublePointer << endl;
            return doublePointer;
        }

    }

    // Close the device
    close(fd);

    return (uint32_t)NULL;
}

uint32_t getTripleBlock(uint32_t block_number){
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
    // block_num < num_blocks
    for (uint32_t block_num = 10000; block_num < num_blocks; block_num++) {
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

        // read the next 4 bytes
        uint32_t readblock[8];
        read(fd, readblock, 8);
        
        if(readblock[0] == block_number ){
            cout << "Found pointer block " << dec << block_number << " from double pointer block " << block_num << endl;
            uint32_t doublePointer = getBlock(block_num);
            cout << "found double pointer block " << block_num << " from triple pointer block " << doublePointer << endl;
            return doublePointer;
        }

    }

    // Close the device
    close(fd);

    return (uint32_t)NULL;
}




uint32_t writeSingleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output) {
    cout << "**Process Single Indirect Blocks..." << endl;

    if(block_num == 0){
        return 0;
    }

    uint32_t singleIndirectBlock = getBlock(readFrom);
        
    // print each buffer in singleIndirectBuffer
    cout << "\nSingle Indirect Block Location: " << singleIndirectBlock << endl;
    uint8_t *singleBuffer = copyBlock(singleIndirectBlock);

    uint32_t lastSingleIndirectBlock = 0;

    for(int i = 0; i < 1024; i++){

        uint32_t block = (uint32_t) singleBuffer[i*4] | (uint32_t) singleBuffer[i*4+1] << 8 | 
                         (uint32_t) singleBuffer[i*4+2] << 16 | (uint32_t) singleBuffer[i*4+3] << 24;
        
        // If block is not 0, copy the block and write it to output
        if(block != 0){
            lastSingleIndirectBlock = block;
            uint8_t *buffer = copyBlock(block);
            output.write((char*)buffer, BLOCK_SIZE);
        } 
        else {
            lastSingleIndirectBlock = block;
            break;
        }
    }

    // Return the last block number if the loop reaches 1024
    cout << "Last data block from single indirect block: " << lastSingleIndirectBlock << endl;

    return lastSingleIndirectBlock;
}


uint32_t writeDoubleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output) {
    if (block_num == 0) {
        return 0;
    }
    uint32_t toCall = 0;
    cout << endl << "**Processing double indirect" << endl;
    uint32_t doubleIndirectBlock = getDoubleBlock(block_num);
    if (doubleIndirectBlock == 0) {
        cout << "Double Indirect Block not found, end of file..." << endl;
        return 0;
    }
    toCall = block_num;
    // Print each buffer in singleIndirectBuffer
    cout << "\nDouble Indirect Block Location: " << doubleIndirectBlock << endl;

    uint8_t* doubleBuffer = copyBlock(doubleIndirectBlock);
    uint32_t lastDoubleIndirectBlock = 0;

    for (int i = 0; i < 1024; i++) {
        uint32_t singleIndirectBlock = (uint32_t)doubleBuffer[i * 4] | (uint32_t)doubleBuffer[i * 4 + 1] << 8 |
                                        (uint32_t)doubleBuffer[i * 4 + 2] << 16 | (uint32_t)doubleBuffer[i * 4 + 3] << 24;

        if (singleIndirectBlock != 0) {
            cout << "Going to Single Indirect Block: " << singleIndirectBlock << endl;
            cout << "toCall is: " << toCall << endl;
            uint32_t lastSingleIndirectBlock = writeSingleIndirectBlocks(singleIndirectBlock, toCall, output);
            toCall = lastSingleIndirectBlock + 1;
            if (lastSingleIndirectBlock == 0) {
                break;
            } else {
                lastDoubleIndirectBlock = singleIndirectBlock;
                
            }
        } else {
            break;
        }
    }

    delete[] doubleBuffer;  // Free memory before returning
    return lastDoubleIndirectBlock;
}

uint32_t writeTripleIndirectBlocks(uint32_t block_num, uint32_t readFrom, ofstream& output) {
    if (block_num == 0) {
        return 0;
    }
    uint32_t toCall = 0;
    cout << endl << "**Processing triple indirect" << endl;
    uint32_t tripleIndirectBlock = getTripleBlock(block_num);
    if (tripleIndirectBlock == 0) {
        cout << "Triple Indirect Block not found, end of file..." << endl;
        return 0;
    }
    toCall = block_num;
    // Print each buffer in singleIndirectBuffer
    cout << "\nTriple Indirect Block Location: " << tripleIndirectBlock << endl;

    uint8_t* tripleBuffer = copyBlock(tripleIndirectBlock);
    uint32_t lastTripleIndirectBlock = 0;

    for (int i = 0; i < 1024; i++) {
        uint32_t doubleIndirectBlock = (uint32_t)tripleBuffer[i * 4] | (uint32_t)tripleBuffer[i * 4 + 1] << 8 |
                                        (uint32_t)tripleBuffer[i * 4 + 2] << 16 | (uint32_t)tripleBuffer[i * 4 + 3] << 24;

        if (doubleIndirectBlock != 0) {
            cout << "Going to Double Indirect Block: " << doubleIndirectBlock << endl;
            cout << "toCall is: " << toCall << endl;
            uint32_t lastDoubleIndirectBlock = writeDoubleIndirectBlocks(doubleIndirectBlock, toCall, output);
            toCall = lastDoubleIndirectBlock + 1;
            if (lastDoubleIndirectBlock == 0) {
                break;
            } else {
                lastTripleIndirectBlock = doubleIndirectBlock;
                
            }
        } else {
            break;
        }
    }

    delete[] tripleBuffer;  // Free memory before returning
    return lastTripleIndirectBlock;
}