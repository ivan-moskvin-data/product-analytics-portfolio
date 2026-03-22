def print_flattened_logs_iterative(raw_logs):
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs = {}
    stack = [(raw_logs, "")]

    while stack:
        current_node, prefix = stack.pop()
        
        for key, value in current_node.items():
            current_key = f"{prefix}.{key}" if prefix else str(key)
            
            if isinstance(value, dict):
                if value:
                    stack.append((value, current_key))
            else:
                flat_logs[current_key] = value

    for key in sorted(flat_logs.keys()):
        print(f"{key}: {flat_logs[key]}")