from .color_cmdline import cstring, COLORS

def view(old: str, new: str, withcolor=True):
    if type(old) is not str:
        raise TypeError("old is not str")
    if type(new) is not str:
        raise TypeError("new is not str")

    old = old.replace("\r", "")
    new = new.replace("\r", "")

    toReturn = [[], []]
    if old == new :
        return toReturn

    old_lines = old.split("\n")
    new_lines = new.split("\n")

    old_lines_set = set(old_lines)
    #print(old_lines_set)
    new_lines_set = set(new_lines)
    #print(new_lines_set)

    old_added = old_lines_set - new_lines_set
    old_removed = new_lines_set - old_lines_set

    if withcolor is True:
        print_to_commandline([old_lines, old_added, old_removed, new_lines])
        return
    else:
        for line in old_lines:
            if line in old_added:
                toReturn[0].append(line.strip())
            elif line in old_removed:
                toReturn[0].append(line.strip())

        for line in new_lines:
            if line in old_added:
                toReturn[1].append(line.strip())
            elif line in old_removed:
                toReturn[1].append(line.strip())

    return toReturn

def print_to_commandline(args):
    [old_lines, old_added, old_removed, new_lines] = args
    for line in old_lines:
        if line in old_added:
            print("-", cstring(line.strip(), COLORS.RED).string)
        elif line in old_removed:
            print("+", cstring(line.strip(), COLORS.GREEN).string)

    for line in new_lines:
        if line in old_added:
            print("-", cstring(line.strip(), COLORS.RED).string)
        elif line in old_removed:
            print("+", cstring(line.strip(), COLORS.GREEN).string)
