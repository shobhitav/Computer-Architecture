"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg=[0]*8
        self.PC=0
        # self.MAR = 0
        # self.MDR = 0
        self.IR=0

    def ram_read(self, address):
        return self.ram[address]
        
    def ram_write(self,value,address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program=[]
        if len(sys.argv) < 2:
            print("did you forget the file to open?")
            print('Usage: filename file_to_open')
            sys.exit()

        try:    
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split=line.split('#')
                    possible_num=comment_split[0]

                    if possible_num=='':
                        continue
                    if possible_num[0]=='1'or possible_num[0]=='0':
                        num=possible_num[:8]
                        # print(f'{num}:{int(num,2)}')

                        program.append(int(num,2))
        except:
            print(f'{sys.argv[0]}:{sys.argv[1]} not found')


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MULT": 
            self.reg[reg_a] = self.reg[reg_a]*self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    

    def run(self):
        """Run the CPU."""
        LDI=0b10000010
        PRN=0b01000111
        MUL=0b10100010 
        HLT=0b00000001

        running = True

        while running:
            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            # LDI R0,8
            # PRN R0
            # HLT
            if self.IR == LDI :
               self.reg[operand_a] = operand_b
               self.PC += 3
            elif self.IR == PRN :
                print(self.reg[operand_a]) 
                self.PC += 2
            elif self.IR == MUL:
                self.reg[operand_a] = self.reg[operand_a]*self.reg[operand_b]
                self.PC +=3
            elif self.IR == HLT:
                running = False
