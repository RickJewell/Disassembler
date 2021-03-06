import sys
import os

#Author: Derrick Jewell
#MIPS Disassembler
#Requires two arguments in its input an binary input file of instructions
#and location for an output file.

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
dataStorage = []
opcode_list = []
opcode_dictionary = {2: "J", 3: "LW", 5: "BNE", 6: "BLEZ", 8: "ADDI", 11: "SW", 28: "MUL" }
fcodes_dictionary = {-1: "NOP",0: "SLL", 2: "SRL", 8: "JR", 10: "MOVZ", 13:"BREAK", 32: "ADD", 34: "SUB", 36: "AND", 37: "OR", 38: "XOR"}
registers = {
	 0:"R0",1:"R1",2:"R2",3:"R3",4:"R4",5:"R5",6:"R6",7:"R7",8:"R8",9:"R9",10:"R10",11:"R11",12:"R12",13:"R13",14:"R14",15:"R15",
	16:"R16",17:"R17",18:"R18",19:"R19",20:"R20",21:"R21",22:"R22",23:"R23",24:"R24",25:"R25",26:"R26",27:"R27",28:"R28",29:"R29",30:"R30",31:"R31"
}
registerReversed = {
    "R0":0,"R1":1,"R2":2,"R3":3,"R4":4,"R5":5,"R6":6,"R7":7,"R8":8,"R9":9,"R10":10,"R11":11,"R12":12,"R13":13,"R14":14,"R15":15,
    "R16":16,"R17":17,"R18":18,"R19":19,"R20":20,"R21":21,"R22":22,"R23":23,"R24":24,"R25":25,"R26":26,"R27":27,"R28":28,"R29":29,"R30":30,"R31":31
}
instructionStr = []
registerStorage = [0] * 32
dataAddr = []


class Dissemble:

    # def__init__(self):

    #def simulator(self):


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
        count = 7
        for i in reversed(parsed):
            output += i
            if (count > 1):
                output += " "
            count =  count -1
        return output

    #Converter for two's Complement signed integer
    #Used on data and immediate values
    def Twos_Complement(self,value):
        converted = int(value,2)
        if(value[0] == "1"):
            converted -= 2**len(value)
            return converted
        return converted

    def Disassemble_Data(self,instruction, program_counter):
        output = ""
        #Add the binary represetation to file output
        output += bin(instruction)[2:].zfill(32)
        #Add Program Counter to the file output
        output += "\t" + str(program_counter)
        #Convert then add the value in decimal to the output file
        dataValue = str(self.Twos_Complement(bin(instruction)[2:].zfill(32)))
        output += "\t" + dataValue
        dataStorage.append(int(dataValue))
        return output

    def Disassemble(self,instruction,program_counter):
        output = ""
        #Add the instructions parsed for easier reading to the output file
        output += self.parse_instruction(instruction)
        # Add Program Counter to the file output
        output += "\t" + str(program_counter)
        output += "\t"

        #Check far left bit to see if we have a valid instruction
        if(instruction >> 31 == 0):
            validStr.append("N")
            output += "Invalid Instruction"
            opcode_list.append("Invalid Instruction")
            arg1.append("")
            arg2.append("")
            arg3.append("")
            return output
        else:
            validStr.append("Y")

        #opcode minus the valid bit
        opcode = (instruction & 0b01111100000000000000000000000000) >> (32 - 6)
        #four register sections of the instruction 5 bits each
        rs =     (instruction & 0b00000011111000000000000000000000) >> (32 - 11)
        rt =     (instruction & 0b00000000000111110000000000000000) >> (32 - 16)
        rd =     (instruction & 0b00000000000000001111100000000000) >> (32 - 21)
        sa =     (instruction & 0b00000000000000000000011111000000) >> (32 - 26)
        #bits 5-0 that represent the fcode
        fcode =  (instruction & 0b00000000000000000000000000111111)
        #Immediate value converted from two's complement, bits 15-0
        immediate = self.Twos_Complement(bin(instruction & 0b00000000000000001111111111111111)[2:].zfill(16))

        #"J"
        if(opcode == 2):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            target = (instruction & 0b00000011111111111111111111111111) << 2
            output += "\t" + "#" + str(target)
            arg1.append(str(target))
            arg2.append("")
            arg3.append("")
            return output

        #"LW"
        elif (opcode == 3):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rt] + ", "
            output += str(immediate) + "(" + registers[rs] + ")"
            arg1.append(registers[rt])
            arg2.append(str(immediate))
            arg3.append(registers[rs])
            return output

        #"BNE"
        elif (opcode == 5):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rs] + ", "
            output += registers[rt] + ", "
            output += "#" + str(immediate << 2)
            arg1.append(registers[rs])
            arg2.append(registers[rt])
            arg3.append(str(immediate << 2))
            return output

        #"BLEZ"
        elif (opcode == 6):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rs] + ", "
            output += "#" + str(immediate << 2)
            arg1.append(registers[rs])
            arg2.append(str(immediate << 2))
            arg3.append("")
            return output

        #"ADDI"
        elif (opcode == 8):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rt] + ", "
            arg1.append(registers[rt])
            output += registers[rs] + ", "
            arg2.append(registers[rs])
            output += "#" + str(immediate)
            arg3.append(str(immediate))
            return output

        #"SW"
        elif (opcode == 11):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rt] + ", "
            output += str(immediate) + "(" + registers[rs] + ")"
            arg1.append(registers[rt])
            arg2.append(str(immediate))
            arg3.append(registers[rs])
            return output

        #"MUL"
        elif (opcode == 28):
            opcode_list.append(opcode_dictionary[opcode])
            output += opcode_dictionary[opcode]
            output += "\t"
            output += registers[rd] + ", "
            arg1.append(registers[rd])
            output += registers[rs] + ", "
            arg2.append(registers[rs])
            output += registers[rt]
            arg3.append(registers[rt])
            return output

        #Special
        elif(opcode == 0):
            fcode = (instruction & 0b00000000000000000000000000111111)

            #"SLL" or r0,r0,r0 expressed as NOP
            if(fcode == 0):
                if(rd == 0 & rt == 0 & sa == 0):
                    output += fcodes_dictionary[-1]
                    opcode_list.append(fcodes_dictionary[-1])
                    arg1.append("")
                    arg2.append("")
                    arg3.append("")
                    return output
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rt] + ", "
                output += "#" + str(sa)
                arg1.append(registers[rd])
                arg2.append(registers[rt])
                arg3.append(str(sa))
                return output
            #"SRL"
            if (fcode == 2):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rt] + ", "
                output += "#" + str(sa)
                arg1.append(registers[rd])
                arg2.append(registers[rt])
                arg3.append(str(sa))
                return output

            #"JR"
            if (fcode == 8):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rs]
                arg1.append(registers[rs])
                arg2.append("")
                arg3.append("")
                return output

            #"MOVZ"
            if (fcode == 10):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output

            #"BREAK"
            if(fcode == 13):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                arg1.append("")
                arg2.append("")
                arg3.append("")
                return output

            #"ADD"
            if (fcode == 32):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output

            #"SUB"
            if (fcode == 34):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output

            #"AND"
            if (fcode == 36):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output

            #"OR"
            if (fcode == 37):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output

            #"XOR"
            if (fcode == 38):
                output += fcodes_dictionary[fcode]
                opcode_list.append(fcodes_dictionary[fcode])
                output += "\t"
                output += registers[rd] + ", "
                output += registers[rs] + ", "
                output += registers[rt]
                arg1.append(registers[rd])
                arg2.append(registers[rs])
                arg3.append(registers[rt])
                return output
            else:
                return ""
        else:
            return ""

    def J(self,validInstruc,program_counter):
        output = str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + "#" + str(arg1[validInstruc])
        if(program_counter == arg1[validInstruc]):
            return output, program_counter + 4,  1
        else:
            newPC = arg1[validInstruc]
            newInstrucNum = (int(newPC) - program_counter) / 4
            return output, int(newPC), int(newInstrucNum)
    def LW(self,validInstruc,program_counter):
        output = str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + str(arg2[validInstruc]) + "("+ arg3[validInstruc] +")"

        while (int(int((int(arg2[validInstruc]) - dataAddr[0] + registerStorage[
            registerReversed[arg3[validInstruc]]])) / 4) >= len(dataStorage)):
            dataStorage.extend((0,0,0,0,0,0,0,0))

        registerStorage[registerReversed[arg1[validInstruc]]] = dataStorage[int(int((int(arg2[validInstruc]) - dataAddr[0]
          + registerStorage[registerReversed[arg3[validInstruc]]])/4))]
        return output
    def BNE(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + "#" + str(arg3[validInstruc])
        if(registerStorage[registerReversed[arg1[validInstruc]]] ==  registerStorage[registerReversed[arg2[validInstruc]]]):
            return output, program_counter + 4,  1
        else:
            newPC = program_counter + 4 + (int(arg3[validInstruc]) )
            newInstrucNum = (newPC - program_counter) / 4
            return output, int(newPC), int(newInstrucNum)
    def BLEZ(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" +  arg1[validInstruc] + ", " + "#" + str(arg2[validInstruc])
        test = registerStorage[registerReversed[arg1[validInstruc]]]
        if(registerStorage[registerReversed[arg1[validInstruc]]] > 0):
            return output, program_counter + 4, 1
        else:
            test = arg2[validInstruc]
            newPC = program_counter + 4 + (int(arg2[validInstruc]) )
            newInstrucNum = (newPC - program_counter) / 4
            return output, int(newPC), int(newInstrucNum)
    def ADDI(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + "#" + str(arg3[validInstruc])
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] + int(arg3[validInstruc])
        return output
    def SW(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + str(arg2[validInstruc]) + "("+ arg3[validInstruc] +")"

        while (int(int((int(arg2[validInstruc]) - dataAddr[0] + registerStorage[
            registerReversed[arg3[validInstruc]]])) / 4) >= len(dataStorage)):
            dataStorage.extend((0,0,0,0,0,0,0,0))

        dataStorage[int(int((int(arg2[validInstruc]) - dataAddr[0] + registerStorage[registerReversed[arg3[validInstruc]]])) / 4)] = \
        registerStorage[registerReversed[arg1[validInstruc]]]
        return output
    def MUL(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] * \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output
    def NOP(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc]
        return output
    def SRL(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + "#" + str(arg3[validInstruc])
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] >> \
                                                                int(arg3[validInstruc])
        return output
    def SLL(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + "#" + str(arg3[validInstruc])
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] << \
                                                                int(arg3[validInstruc])
        return output
    def JR(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc]
        newPC = registerStorage[registerReversed[arg1[validInstruc]]]
        newInstrucNum = (newPC - program_counter) / 4
        return output,int(newPC),int(newInstrucNum)
    def MOVZ(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        if(registerStorage[registerReversed[arg3[validInstruc]]] == 0):
            registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]]
            return output
        else:
            return output
    def BREAK(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc]
        return output
    def ADD(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] + \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output
    def SUB(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] - \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output
    def AND(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] & \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output
    def OR(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] | \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output
    def XOR(self,validInstruc,program_counter):
        output =str(program_counter) + "\t" + opcode_list[validInstruc] + "\t" + arg1[validInstruc] + ", " + arg2[validInstruc] + ", " + arg3[validInstruc]
        registerStorage[registerReversed[arg1[validInstruc]]] = registerStorage[registerReversed[arg2[validInstruc]]] ^ \
                                                                registerStorage[registerReversed[arg3[validInstruc]]]
        return output



    def run(self):
        global opcode
        global fcodes
        global registers

        for i in range(len(sys.argv)):

            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
                print(inputFileName)
            elif (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)): \
                    outputFileName = sys.argv[i + 1]
        simOutputFileName = outputFileName[:-7] + "sim.txt"

        #Assume that the program counter begins at 96
        program_counter = 96
        break_flag = False
        output_file = open(outputFileName,"w")
        with open(inputFileName, "r") as Input_File:
            for line in Input_File:
                dissassembled_line = ""
                instruction = int(line,2)
                #While we havent reach the break line in instructions
                if(break_flag == False):
                    dissassembled_line += self.Disassemble(instruction,program_counter)
                    #After the break instruction begin processing the data
                    if (dissassembled_line[-5:] == "BREAK"):
                        dataAddr.append(program_counter + 4)
                        break_flag = True
                else:
                    dissassembled_line += self.Disassemble_Data(instruction,program_counter)
                program_counter += 4
                output_file.write(dissassembled_line)
                output_file.write("\n")
        output_file.close()

        #Start running Simulator
        output_file = open(simOutputFileName, "w")
        seperatorLine = "=====================\n"
        program_counter = 96
        validInstrucNum = 0
        cycle = 1
        instrucString = ""
        while True:
        #for arg in validStr:
            if(opcode_list[validInstrucNum] == "Invalid Instruction"):
                validInstrucNum += 1
                program_counter += 4
                continue
            if(opcode_list[validInstrucNum] == "ADDI"):    instrucString = self.ADDI(validInstrucNum,program_counter)
            elif(opcode_list[validInstrucNum] == "LW"):    instrucString = self.LW(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "SW"):   instrucString = self.SW(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "MUL"):  instrucString = self.MUL(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "NOP"):  instrucString = self.NOP(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "SRL"):  instrucString = self.SRL(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "SLL"):  instrucString = self.SLL(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "MOVZ"): instrucString = self.MOVZ(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "BREAK"):instrucString = self.BREAK(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "ADD"):  instrucString = self.ADD(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "SUB"):  instrucString = self.SUB(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "AND"):  instrucString = self.AND(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "OR"):   instrucString = self.OR(validInstrucNum,program_counter)
            elif (opcode_list[validInstrucNum] == "XOR"):  instrucString = self.XOR(validInstrucNum,program_counter)

            elif (opcode_list[validInstrucNum] == "J"):
                instrucString, newPC, newInstrucNum = self.J(validInstrucNum,program_counter)
                program_counter = newPC - 4
                validInstrucNum += newInstrucNum -1
            elif (opcode_list[validInstrucNum] == "BNE"):
                instrucString, newPC, newInstrucNum = self.BNE(validInstrucNum,program_counter)
                program_counter = newPC - 4
                validInstrucNum += newInstrucNum -1
            elif (opcode_list[validInstrucNum] == "BLEZ"):
                instrucString, newPC, newInstrucNum = self.BLEZ(validInstrucNum,program_counter)
                program_counter = newPC - 4
                validInstrucNum += newInstrucNum -1
            elif (opcode_list[validInstrucNum] == "JR"):
                instrucString, newPC, newInstrucNum = self.JR(validInstrucNum,program_counter)
                program_counter = newPC - 4
                validInstrucNum += newInstrucNum -1

            cycleLine = ""

            output_file.write(seperatorLine)
            cycleLine = "cycle:" + str(cycle) + "\t" +  instrucString
            output_file.write(cycleLine + "\n\n" + "registers:" + "\n")

            dataRange = registerStorage[0:8]
            dataLine = "r00:" + "\t" + str(dataRange).strip('[]').replace("," , "\t").replace(" ","") + "\n"
            output_file.write(dataLine)
            dataRange = registerStorage[8:16]
            dataLine = "r08:"+ "\t" + str(dataRange).strip('[]').replace("," , "\t").replace(" ","") + "\n"
            output_file.write(dataLine)
            dataRange = registerStorage[16:24]
            dataLine = "r16:"+ "\t" + str(dataRange).strip('[]').replace("," , "\t").replace(" ","") + "\n"
            output_file.write(dataLine)
            dataRange = registerStorage[24:32]
            dataLine = "r24:"+ "\t" + str(dataRange).strip('[]').replace("," , "\t").replace(" ","") + "\n"
            output_file.write(dataLine)

            output_file.write("\n")
            output_file.write("data:" + "\n")
            i = 0;
            d = dataAddr[0]


            while i < (len(dataStorage)):

                dataRange = dataStorage[i:i+8]
                dataString = []
                for j in dataRange:
                    dataString.append(int(j))
                dataLine = str(d) + ":" + "\t" + str(dataString).strip("[]").replace("," , "\t").replace(" ","") + "\n"
                output_file.write(dataLine)
                i+= 8
                d += 32


            if(opcode_list[validInstrucNum] == "BREAK"):
                break
            output_file.write("\n")
            validInstrucNum += 1
            cycle += 1

            program_counter +=4
        output_file.close()





dissme = Dissemble()
dissme.run()