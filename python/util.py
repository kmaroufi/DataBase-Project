def splitter(cmd):
    # print(cmd)
    tmp = cmd.split("-")
    params = []
    for i in range(len(tmp)):
        item = None
        if i == 0:
            item = tmp[0].split()[2]
        else:
            item = tmp[i].replace(" ", "")
        if item.__contains__(";"):
            # print("sql injectionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
            exit()
        params += [item]
    # print(params)
    return params

