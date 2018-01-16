## OPCODE machine encoding

Each opcode and their encoding as signals in the PROM (Programmable Read Only Memory)


### HLT

Operand | Signals
--- | ---
Control | 

### NOP

Operand | Signals
--- | ---
Control | copper-plate: 1

### STORE

Operand | Signals
--- | ---
Control | copper-plate: 2
Operand_1 | L: 1, 1: *value*<br>B: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### LOAD

Operand | Signals
--- | ---
Control | copper-plate: 4
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### B

Operand | Signals
--- | ---
Control | copper-plate: 7
Operand_1 | K: 1, 0: *value*<br>A: *value*

### BZ

Operand | Signals
--- | ---
Control | copper-plate: 7, C: 1
Operand_1 | K: 1, 0: *value*<br>A: *value*

### BN

Operand | Signals
--- | ---
Control | copper-plate: 7, C: 2
Operand_1 | K: 1, 0: *value*<br>A: *value*

### CMEM

Operand | Signals
--- | ---
Control | copper-plate: 12, grey: 1, black: 1

### CREG

Operand | Signals
--- | ---
Control | copper-plate: 12, grey: 1

### CRAM

Operand | Signals
--- | ---
Control | copper-plate: 12, black: 1

### ALU

Operand | Signals
--- | ---
Control | copper-plate: 9
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*
Operand_4 | O: *value*
Operand_5 | 2: *value*
Operand_6 | 3: *value*
Operand_7 | F: *value*
Operand_8 | red: *value*

### MOV

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### ADD

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### SUB

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, 2: 1, 3: -1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### INC

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, 2: 1, 3: 1, B: 1
Operand_1 | U: *value*, K: 1, 0: *value*

### DEC

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, 2: 1, 3: 1, B: -1
Operand_1 | U: *value*, K: 1, 0: *value*

### CMP

Operand | Signals
--- | ---
Control | copper-plate: 9, 2: 1, 3: -1
Operand_1 | K: 1, 0: *value*<br>A: *value*
Operand_2 | L: 1, 1: *value*<br>B: *value*

### TST

Operand | Signals
--- | ---
Control | copper-plate: 9, 2: 1
Operand_1 | K: 1, 0: *value*<br>A: *value*

### MUL

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 1, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### DIV

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 2, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### POW

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 3, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### MOD

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 4, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### ASR

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 5, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### LSL

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 6, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### LSR

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 7, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### ROL

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 8, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### ROR

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 9, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### NOT

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 10, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*

### AND

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 11, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### OR

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 12, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

### XOR

Operand | Signals
--- | ---
Control | copper-plate: 9, red: 1, F: 13, 2: 1, 3: 1
Operand_1 | U: *value*
Operand_2 | K: 1, 0: *value*<br>A: *value*
Operand_3 | L: 1, 1: *value*<br>B: *value*

