class RISC_V:
    def __init__(self):
        self.registers = [0] * 32  # 32 registers initialized to 0
        self.memory = bytearray(128)  # 128 bytes of memory initialized to 0
        self.pc = 0  # Program counter, keeps track of the current instruction
        self.labels = {}  # Dictionary to store label addresses
        self.instructions = []  # List to store the program instructions
        self.instruction_count = 0  # Counter to track the number of executed instructions
        self.cycle_count = 0  # Counter to track the number of cycles

    # ADD instruction: rd = rs1 + rs2
    def ADD(self, rd, rs1, rs2):
        self.registers[rd] = self.registers[rs1] + self.registers[rs2]
        self.pc += 1
        self.instruction_count += 1
        self.cycle_count += 1

    # SUB instruction: rd = rs1 - rs2
    def SUB(self, rd, rs1, rs2):
        self.registers[rd] = self.registers[rs1] - self.registers[rs2]
        self.pc += 1
        self.instruction_count += 1
        self.cycle_count += 1

    # LI instruction: Load immediate value into register
    def LI(self, rd, imm):
        self.registers[rd] = imm
        self.pc += 1
        self.instruction_count += 1
        self.cycle_count += 1

    # BEQ instruction: Branch if registers are equal
    def BEQ(self, rs1, rs2, label):
        if self.registers[rs1] == self.registers[rs2]:
            self.pc = self.labels[label]  # Jump to label if equal
        else:
            self.pc += 1
        self.instruction_count += 1
        self.cycle_count += 1

    # J instruction: Unconditional jump to label
    def J(self, label):
        if label in self.labels:
            self.pc = self.labels[label]  # Jump directly to label
        else:
            print(f"Label {label} not found")
        self.instruction_count += 1
        self.cycle_count += 1


    # JAL instruction: Jump and Link (store return address and jump)
    def JAL(self, label):
        if label in self.labels:
            self.registers[31] = self.pc + 1  # Store return address
            self.pc = self.labels[label]  # Jump directly to label
        else:
            print(f"Label {label} not found")
        self.instruction_count += 1
        self.cycle_count += 1

    # Decode and execute an instruction
    def decode_execute(self, instruction):
        parts = instruction.replace(",", "").split()  # Remove commas and split into parts
        if not parts:
            return
        
        opcode = parts[0].upper()  # Convert to uppercase to match function names
        args = parts[1:]

        try:
            if opcode in ["BEQ", "JAL", "J"]:
                # Handle branching and jump instructions separately
                if opcode == "BEQ":
                    self.BEQ(int(args[0]), int(args[1]), args[2])
                elif opcode == "JAL":
                    self.JAL(args[0])
                elif opcode == "J":
                    self.J(args[0])
            else:
                # Dynamically call the corresponding function (e.g., ADD, LI, etc.)
                getattr(self, opcode)(*map(int, args))
        except (IndexError, ValueError):
            print(f"Error decoding instruction: {instruction}")
            self.pc += 1

    # Load program from a text file
    def load_program(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()

        self.instructions = []
        self.labels = {}

        parsing = False
        instruction_index = 0

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):  
                continue  # Skip empty lines and comments

            if "program" in line and "=" in line:  
                parsing = True
                continue
            if line == "]":  
                break  # End of program

            if parsing:
                line = line.replace('"', '').replace(',', '').strip()

                if line.endswith(":"):
                    # Store label and its corresponding instruction index
                    label = line[:-1]
                    self.labels[label] = instruction_index
                else:
                    # Add instruction to the instruction list
                    self.instructions.append(line)
                    instruction_index += 1  

    # Run the program
    def run(self):
        self.pc = 0
        executed_instructions = set()  # Detect infinite loops

        while self.pc < len(self.instructions):
            if self.pc in executed_instructions:
                print(f"Infinite loop detected at PC: {self.pc}, stopping execution.")
                break  # Stop if the same instruction repeats continuously

            executed_instructions.add(self.pc)

            print(f"PC: {self.pc}, Executing: {self.instructions[self.pc]}")
            self.decode_execute(self.instructions[self.pc])

    # Print the final state of registers and memory
    def print_registers(self):
        print("\nFinal Register State:")
        for i in range(32):
            print(f"x{i}: {self.registers[i]}")
        print("\nFinal Memory State:", self.memory.hex())  # Print memory in hex 

    # Print instruction and cycle counts
    def print_counts(self):
        print(f"\nTotal Instructions Executed: {self.instruction_count}")
        print(f"Total Cycles: {self.cycle_count}")


if __name__ == "__main__":
    # Ensure the file 'program.txt' is in the same directory as your Python script
    filename = "program.txt"  # Read from 'program.txt' in the current directory
    interpreter = RISC_V()
    interpreter.load_program(filename)
    interpreter.run()
    interpreter.print_registers()
    interpreter.print_counts()  # Print the instruction and cycle counts
