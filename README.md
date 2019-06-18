## Input File Format

The first line of the file will be a list of database element names and their initial values, space
separated, on a single line.
Each transaction will begin on a new line, with the transaction name and number of actions
in the first line, followed by actions of formREAD(), WRITE(), OUTPUT(), or an operation in
successive lines. Successive transactions are separated by a newline character. For example:

```
A 4 B 4 D 5
```
```
T1 4
READ(A, t)
t := t+
WRITE(A, t)
OUTPUT(A)
```

```
T2 5
READ(A, t)
t := t+
t := t-
WRITE(A, t)
OUTPUT(A)
```
The transactions are assumed to be executed in a Round-Robin(RR)fashion. For this an-
other additional command line argument is provided ’x’. Givenntransactions, carry out
firstxinstructions/actions of the first transaction, then the firstxinstructions/actions of the
second transaction and so on ...

The set of operations you’ll have to handle are{+,−,∗,/}and the second operand is always
an integer.

## Task: UNDOLogs

UNDOlogs for the set of transactions. In addition, after every log record also print the
values of the variables in both the main memory and the disk corresponding to the state
after the current log record. The variables should be in Lexicographic order.

Suppose the input file had contents as previously specified in the input file format section
and the value ofxis 1, the contents of the output file would look like this

```
<START T1>
```
### A 4 B 4 D 5

### <START T2>

### A 4

### A 4 B 4 D 5

### <T1, A, 4>

### A 8

### A 4 B 4 D 5

### <COMMIT T1>

### A 8

### A 8 B 4 D 5

### <T2, A, 8>

### A 4

### A 8 B 4 D 5

### <COMMIT T2>

### A 4

### A 4 B 4 D 5

where the first line after a log record is the contents of the main memory and the second line
is the contents of the disk. The values after theSTARTlog correspond to values of variables
right before the first action

Note: Please note that if the variable has already been read from the disk into the main
memory, anotherREAD()command will not result in another read operation. The contents
of the main memory will be used. Additionally, if the variable is not in the main memory
INPUT()will implicitly be called byREAD()



