def load_data(path):

    data = {}

    with open(path, 'r') as file:

        for line in file:

            split = line.strip().split("\t")

            data[split[0]] = split[1:]

    return data
