import difflib

def highlight_diff(old_text, new_text):
    old_lines = old_text.splitlines()
    new_lines = new_text.splitlines()

    diff = difflib.ndiff(old_lines, new_lines)

    result = []
    for line in diff:
        if line.startswith("+"):
            result.append(f"➕ {line[2:]}")
        elif line.startswith("-"):
            result.append(f"➖ {line[2:]}")
        else:
            result.append(f"  {line[2:]}")

    return "\n".join(result)