
def safeGetChildValue(parent, child, default=None):
    if parent == None:
        return default

    try:
        result = parent.find(f"{child}")
        if result is not None:
            return result.text

        return default
    except:
        return default
