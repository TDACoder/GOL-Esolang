import sys

def run_gol_interpreter(source_code):
    lines = [line.strip() for line in source_code.split('\n')]
    
    size_line = None
    epochs_line = None
    field_start_idx = None
    
    for i, line in enumerate(lines):
        if line.startswith("S:"):
            size_line = line
        elif line.startswith("E:"):
            epochs_line = line
        elif line.startswith("F:"):
            field_start_idx = i
            
    if not size_line:
        print("GOL Syntax Error: Missing grid size definition 'S:'.")
        return
    if not epochs_line:
        print("GOL Syntax Error: Missing epoch definition 'E:'.")
        return
    if field_start_idx is None:
        print("GOL Syntax Error: Missing field definition start 'F:'.")
        return

    try:
        size_parts = size_line.replace("S:", "").strip().split('x')
        if len(size_parts) != 2:
            raise ValueError
        cols = int(size_parts[0])
        rows = int(size_parts[1])
        if cols < 3 or rows < 3:
            print("GOL Value Error: Grid dimensions must be at least 3x3 for proper simulation.")
            return
    except Exception:
        print(f"GOL Syntax Error: Invalid format in '{size_line}'. Expected 'S: ColumnsxRows' (e.g., S: 5x5).")
        return

    try:
        epochs = int(epochs_line.replace("E:", "").strip())
        if epochs < 0:
            print("GOL Value Error: Epoch count cannot be negative.")
            return
    except ValueError:
        print(f"GOL Syntax Error: Invalid format in '{epochs_line}'. Expected an integer for epochs.")
        return

    field_lines = []
    for line in lines[field_start_idx:]:
        if line.startswith("F:"):
            line = line.replace("F:", "").strip()
        if line:
            field_lines.append(line)
            
    field_content = " ".join(field_lines)

    if "[" not in field_content:
        print("GOL Syntax Error: Missing opening bracket '[' in field definition.")
        return
    if "]" not in field_content:
        print("GOL Syntax Error: Missing closing bracket ']' in field definition.")
        return
        
    if field_content.count("[") > 1 or field_content.count("]") > 1:
        print("GOL Syntax Error: Nested or duplicate brackets are not allowed.")
        return

    try:
        inside_brackets = field_content.split("[")[1].split("]")[0]
    except IndexError:
        print("GOL Syntax Error: Malformed brackets layout.")
        return

    raw_tokens = [t.strip() for t in inside_brackets.replace(",", " ").split() if t.strip()]
    raw_cells = []
    
    for token in raw_tokens:
        if token in ("1", "0"):
            raw_cells.append(int(token))
        else:
            print(f"GOL Runtime Error: Invalid token '{token}'. Only '0' and '1' are allowed.")
            return

    expected_cells = cols * rows
    if len(raw_cells) < expected_cells:
        print(f"GOL Matrix Error: Insufficient matrix data for {cols}x{rows} grid. Expected {expected_cells} cells, but only found {len(raw_cells)}.")
        return
    elif len(raw_cells) > expected_cells:
        print(f"GOL Matrix Error: Too much matrix data for {cols}x{rows} grid. Expected {expected_cells} cells, but found {len(raw_cells)}.")
        return

    grid = []
    for r in range(rows):
        grid.append(raw_cells[r * cols : (r + 1) * cols])

    for _ in range(epochs):
        new_grid = [[0] * cols for _ in range(rows)]
        
        for r in range(rows):
            for c in range(cols):
                live_neighbors = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            live_neighbors += grid[nr][nc]
                
                if grid[r][c] == 1:
                    new_grid[r][c] = 1 if 2 <= live_neighbors <= 3 else 0
                else:
                    new_grid[r][c] = 1 if live_neighbors == 3 else 0
                        
        grid = new_grid

    print(f"S: {cols}x{rows}")
    print("E: 0")
    print("F:")
    print("[")
    for r in range(rows):
        row_str = ", ".join(map(str, grid[r]))
        print(f"  {row_str}")
    print("]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as file:
                run_gol_interpreter(file.read())
        except FileNotFoundError:
            print(f"GOL IO Error: File '{sys.argv[1]}' not found.")
    else:
        print("GOL Interpreter Usage: python interpreter.py <filename.gol>")
