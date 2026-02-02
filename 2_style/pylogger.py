def findCaller(self):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe()
    f = f.f_back if f is not None else None # On some versions of IronPython, currentframe() returns None if IronPython isn't run with -X:Frames.

    return_value = "(unknown file)", 0, "(unknown function)"

    while hasattr(f, "f_code"):
        code = f.f_code
        filename = os.path.normcase(code.code_filename)

        # Checks filename
        if filename == _srcfile:
            f = f.f_back
            continue

        # Populate values
        return_value = (code.code_filename, f.f_lineno, code.code_name)
        break

    return return_value

