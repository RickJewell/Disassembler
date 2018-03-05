# Disassembler
Authors: Derrick Jewell djj74

This MIPS Dissasembler is written in Python and takes a subset
of the MIPS instructions. It will take a binary file containing 
machine code one line at a time and generate the assembly code. 
The first bit of the opcode is treated as a valid bit rather 
than part of the opcode.

It supports the following instructins:
J, JR, BNE, BLEZ
ADD, ADDI, SUB
SW, LW
SLL, SRL
MUL,
AND, OR,XOR
MOVZ
NOP

It can be run from the command line when given both an input binary txt
file and an output text file to write to. For examble in Linux:

$ python team#_project1.py -i test1_bin.txt -o team#_out
