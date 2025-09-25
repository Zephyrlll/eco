import json
def load_status(path):
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        if "status" in data:
            return data.get("status", {}), data.get("hazards", [])
        else:
            return data, []
    except (FileNotFoundError, json.JSONDecodeError):
        return {}, []
    
def unit_fmt(num):
    if num > 1_000_000_000_000:
        return f"{(num / 1_000_000_000_000):.1f}T"
    elif num > 1_000_000_000:
        return f"{(num / 1_000_000_000):.1f}B"
    elif num >1_000_000:
        return f"{(num / 1_000_000):.1f}M"
    elif num < 0:
        return f"{0}"
    elif num <= 3:
        return f"{num:.0f}"
    else:
        return f"{num:.0f}"