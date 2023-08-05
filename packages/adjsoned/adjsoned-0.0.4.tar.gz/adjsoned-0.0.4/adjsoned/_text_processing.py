def pythonify_name(string: str) -> str:
    res = ""
    dashes_in_a_row = 0

    for c in string:
        if c.lower() != c or c == " ":
            res += "_" if (res and not res[-1] == "_" and not dashes_in_a_row) else ""
            c = c.lower()
            dashes_in_a_row += 1
        else:
            dashes_in_a_row = 0

        if c != " ":
            res += c

    return res


def _main():
    print(pythonify_name("camelToDash"))
    print(pythonify_name("_df3kGcamel_ToDaSH"))
    print(pythonify_name("FileJSON"))


if __name__ == '__main__':
    _main()