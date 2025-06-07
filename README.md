# RISC-V-Simulator

This project is a basic RISC-V instruction simulator written in Python. It reads from a program.txt file, which contains RISC-V assembly instructions and input values. The interpreter processes these instructions sequentially, simulating a register file and memory, and produces the final state of the system along with performance statistics.


📌 Features
✅ Supports core RISC-V instructions:
ADD, SUB, LW, SW, BEQ, JAL

🧠 Functional register file with proper updates

💾 Simulated memory model for load/store

📄 Reads and executes RISC-V programs from text files

📊 Outputs instruction and cycle counts

🔁 Control flow support via branching and jumps

*Disclaimer*: Instructions BEQ and JAL do not work yet.
