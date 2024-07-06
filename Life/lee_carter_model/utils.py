def load_data(path):
    '''
    input: path to .txt file containing death probabilities.
    output: dictionary where keys are years and entries are lists containing one-year-death-probability for each age.
    '''
    data = {}

    with open(path, 'r') as file:
        for line in file:
            split = line.strip().split("\t")

            data[split[0]] = [float(element) for element in split[1:]]

    return data


def trim_qxt(qxt_dict, *argv):
    '''
    input: the qxt dictionary as returned by load_data(), the required ranges and the start age of the data. If no arguments specified, the dictionary
           will just be converted to a list.
    output: the trimmed qxt.
    '''

    qxt = []
    #If the arguments are given, trim.
    if len(argv) == 5:
        start_date = argv[0]
        end_date = argv[1]
        start_age = argv[2]
        end_age = argv[3]
        start_age_data = argv[4]

        for key in qxt_dict:
            if start_date <= int(key) <= end_date:
                try:
                    qxt.append(qxt_dict[key][start_age-start_age_data:end_age + 1])
                except:
                    print("specified start age is smaller than start age of input")
                    return 1
     #Use entire data. This simple functionality should be possible without providing any arguments, therefore the use of *args.
    elif len(argv) == 0:
        for key in qxt_dict:
            qxt.append(qxt_dict[key])

    else:
        print("invalid number of arguments.")
        return 1

    return qxt
