def print_flattened_logs_recursive(raw_logs):
    if not isinstance(raw_logs, dict) or not raw_logs:
        return

    flat_logs = {}

    def traverse_node(current_node, prefix):
        for key, value in current_node.items():
            current_key = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                if value:
                    traverse_node(value, current_key)
            else:
                flat_logs[current_key] = value

    traverse_node(raw_logs, "")

    for key in sorted(flat_logs.keys()):
        print(f"{key}: {flat_logs[key]}")