import sys
import os

opcodeStr = []  # <type 'list'>: ['Invalid Instruction', 'ADDI', 'SW', 'Invalid Instruction', 'LW', 'BLTZ', 'SLL',...]
validStr = []  # <type 'list'>: ['N', 'Y', 'Y', 'N', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y',...]
instrSpaced = []  # <type 'list'>: ['0 01000 00000 00001 00000 00000 001010', '1 01000 00000 00001 00000 00000 001010',...]
arg1 = []  # <type 'list'>: [0, 0, 0, 0, 0, 1, 1, 10, 10, 0, 3, 4, 152, 4, 10, 1, 0, 112, 0]
arg2 = []  # <type 'list'>: [0, 1, 1, 0, 1, 0, 10, 3, 4, 5, 0, 5, 0, 5, 6, 1, 1, 0, 0]
arg3 = []  # <type 'list'>: [0, 10, 264, 0, 264, 48, 2, 172, 216, 260, 8, 6, 0, 6, 172, -1, 264, 0, 0]
arg1Str = []  # <type 'list'>: ['', '\tR1', '\tR1', '', '\tR1', '\tR1', '\tR10', '\tR3', '\tR4', .....]
arg2Str = []  # <type 'list'>: ['', ', R0', ', 264', '', ', 264', ', #48', ', R1', ', 172', ', 216', ...]'
arg3Str = []  # <type 'list'>: ['', ', #10', '(R0)', '', '(R0)', '', ', #2', '(R10)', '(R10)', '(R0)',...]
mem = []  # <type 'list'>: [-1, -2, -3, 1, 2, 3, 0, 0, 5, -5, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
binMem = []  # <type 'list'>: ['11111111111111111111111111111111', '11111111111111111111111111111110', ...]
valid = []
opcode_list = []
opcode_dictionary = {2: "J", 3: "LW", 5: "BNE", 6: "BLEZ", 8: "ADDI", 11: "SW", 28: "MUL" }
fcodes_dictionary = {0: "SLL", 2: "SRL", 8: "JR", 10: "MOVZ", 13:"BREAK", 32: "ADD", 34: "SUB", 36: "AND", 37: "OR", 38: "XOR"}
registers = {
	 0:"R0",1:"R1",2:"R2",3:"R3",4:"R4",5:"R5",6:"R6",7:"R7",8:"R8",9:"R9",10:"R10",11:"R11",12:"R12",13:"R13",14:"R14",15:"R15",
	16:"R16",17:"R17",18:"R18",19:"R19",20:"R20",21:"R21",22:"R22",23:"R23",24:"R24",25:"R25",26:"R26",27:"R27",28:"R28",29:"R29",30:"R30",31:"R31"
}


class Dissemble:

    # def__init__(self):

    def parse_instruction(self,instruction):
        parsed = []
        output = ""
        parsed.append(bin(instruction & 0b111111)[2:].zfill(6))
        instruction = instruction >> 6
        parsed.append(bin(instruction & 0b11111)[2:].zfill(5))
        instruction = instruction >> 5
        parsed.append(bin(instruction & 0b11111)[2:].zfill(5))
        instruction = instruction >> 5
        parsed.append(bin(instruction & 0b11111)[2:].zfill(5))
        instruction = instruction >> 5
        parsed.append(bin(instruction & 0b11111)[2:].zfill(5))
        instruction = instruction >> 5
        parsed.append(bin(instruction & 0b11111)[2:].zfill(5))
        instruction = instruction >> 5
        parsed.append(bin(instruction)[2:])
        for i in reversed(parsed):
            output += i + " "
        return output
    def Disassemble_Data(self,instruction, program_counter):
        output = ""
        output += bin(instruction)[2:].zfill(32)
        output += " " + str(program_counter).ljust(3)
        output += "  " + str(instruction)
        return output

    def Disassemble(self,instruction,program_counter):
        output = ""
        #Add PC here?
        output += self.parse_instruction(instruction)
        output += " " + str(program_counter).ljust(3)
        output += "    "

        if(instruction >> 31 == 0):
            validStr.append("N")
            output += "Invalid Instruction"
            return output
        else:
            validStr.append("Y")

        opcode = (instruction & 0b01111100000000000000000000000000) >> (32 - 6)
        rs =     (instruction & 0b00000011111000000000000000000000) >> (32 - 11)
        rt =     (instruction & 0b00000000000111110000000000000000) >> (32 - 16)
        rd =     (instruction & 0b00000000000000001111100000000000) >> (32 - 21)
        sa =     (instruction & 0b00000000000000000000011111000000) >> (32 - 26)
        fcode =  (instruction & 0b00000000000000000000000000111111)
        #needs converted from two's complement
        immediate = (instruction & 0b00000000000000001111111111111111)

        if(opcode == 2):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            target = (instruction & 0b00000011111111111111111111111111) << 2
            output += "     " + "#" + str(target)
            return output
        elif (opcode == 3):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "    "
            output += registers[rt] + ", "
            output += str(immediate) + "(" + registers[rs] + ")"
            return output

        elif (opcode == 5):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "  "
            output += registers[rs] + ", "
            output += registers[rt] + ", "
            output += "#" + str(immediate << 2)
            return output

        elif (opcode == 6):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "  "
            output += registers[rs] + ", "
            output += "#" + str(immediate << 2)
            return output

        elif (opcode == 8):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "  "
            output += registers[rs] + ", "
            output += registers[rt] + ", "
            output += "#" + str(immediate)
            return output

        elif (opcode == 11):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "    "
            output += registers[rt] + ", "
            output += str(immediate) + "(" + registers[rs] + ")"
            return output

        elif (opcode == 28):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "   "
            output += registers[rd] + ", "
            output += registers[rs] + ", "
            output += registers[rt]
            return output

        elif(opcode == 0):
            fcode = (instruction & 0b00000000000000000000000000111111)

            #SLL r0,r0,r0 expressed as NOP
            if(fcode == 0):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rt] + ", "
                output += "#" + str(sa)
                return output
            if (fcode == 2):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rt] + ", "
                output += "#" + str(sa)
                return output
            if (fcode == 8):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rs]
                return output
            if (fcode == 10):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            if(fcode == 13):
                output += fcodes_dictionary[fcode]
                return output
            if (fcode == 32):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            if (fcode == 34):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            if (fcode == 36):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            if (fcode == 37):
                output += fcodes_dictionary[fcode]
                output += "   "
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            if (fcode == 38):
                output += fcodes_dictionary[fcode]
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                return output
            else:
                return ""
        else:
            return ""


    def run(self):
        '''
        global opcodeStr
        global validStr
        global arg1
        global arg2
        global arg3
        global arg1Str
        global arg2Str
        global arg3Str
        global mem
        global binMen
        global valid
        '''

        global opcode
        global fcodes


        for i in range(len(sys.argv)):

            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
                print(inputFileName)
            elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)): \
                    outputFileName = sys.argv[i + 1]

        program_counter = 96
        break_flag = False
        with open(inputFileName, "r") as Input_File:
            for line in Input_File:
                dissassembled_line = ""
                instruction = int(line,2)
                if(break_flag == False):
                    dissassembled_line += self.Disassemble(instruction,program_counter)
                    if (dissassembled_line[-5:] == "BREAK"):
                        break_flag = True
                else:
                    dissassembled_line += self.Disassemble_Data(instruction,program_counter)
                program_counter += 4
                print(dissassembled_line)



dissme = Dissemble()
dissme.run()