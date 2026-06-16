# GOL-Esolang

An esoteric programming language based on the simulation rules of Conway's Game of Life. It parses a grid layout, executes a specified number of simulation steps (epochs), and outputs the resulting matrix state.

## Syntax Rules

A valid .gol source file must contain three strict components:

1. S: Columns x Rows - Defines the dimensions of the grid. The matrix must be at least 3x3.
2. E: Epochs - An integer greater than or equal to 0 specifying the number of simulation generations.
3. F: - The field definition header followed by the grid token matrix wrapped inside single brackets [...]. Cells are separated by spaces or commas, where 1 represents a live cell and 0 represents a dead cell.

## Code Example

Create a file named glider.gol:

```text
S: 5x5
E: 4
F:
[
  0, 1, 0, 0, 0
  0, 0, 1, 0, 0
  1, 1, 1, 0, 0
  0, 0, 0, 0, 0
  0, 0, 0, 0, 0
]
```

## How to Run

Pass your source file as a command-line argument to the interpreter script:

python interpreter.py glider.gol

## Error Handling

The interpreter includes built-in diagnostics for code validation:
- GOL Syntax Error: Triggers if standard structural headers (S:, E:, F:) or brackets are missing or malformed.
- GOL Value Error: Triggers if negative epoch values are provided or grid sizing is below the 3x3 threshold.
- GOL Matrix Error: Triggers if the parsed cell count doesn't match the exact grid dimensions specified in the S: configuration.
- GOL Runtime Error: Triggers if illegal tokens other than 0 or 1 are present inside the matrix field.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
