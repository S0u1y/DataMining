import collections


MIN_SUPPORT = 0.2
MIN_CONFIDENCE = 0.5

dataset = "Datasets/" + "itemsets_test.dat"
# Vozik - 0.004 = 630 first pass, 760 second, 552 third, 233, 59, 3
# Vozik - 0.009 = 404 first pass, 15 second, 2 third

def parse_file(filename: str):
    with open(filename, "r") as file:
        lines = [line.replace('\n', "").split(" ") for line in file.readlines()]

    for line in lines:
        if '' in line:
            line.remove('')

    return lines


def write_data(data):
    with open("output.txt", "a+") as output:
        output.write(data.__str__() + "\n")


def add_support(item_set, supports_list):
    if item_set in supports_list:
        supports_list[item_set] += 1
    else:
        supports_list[item_set] = 1


def Apriori():
    supports = {}

    transactions = parse_file(dataset)
    transactions = [set(t) for t in transactions]

    transactions_length = len(transactions)

    for i in range(transactions_length):
        transaction = transactions[i]
        print(transaction)
        for item in transaction:
            add_support(item, supports)

    for key, value in supports.items():
        supports[key] = value / transactions_length

    supports = collections.OrderedDict(sorted(supports.items()))

    supports = {
        key: value for key, value
        in supports.items()
        if value >= MIN_SUPPORT
    }

    write_data(supports)

    k = 0

    frequent = [supports.copy()]

    while not len(frequent[k]) == 0:
        items = list(frequent[k].keys())
        items_length = len(frequent[k])
        item_sets = set([])
        for i in range(items_length - 1):
            for j in range(1, items_length - i):
                if isinstance(items[i], tuple):
                    items_a = set([x for x in items[i]])
                    items_b = [x for x in items[i + j]]
                    sorted(items_a.union(items_b))
                    item_sets.add(tuple(items_a.union(items_b)))
                else:
                    item_sets.add((items[i], items[i + j]))

        new_supports = {}
        for its_i, item_set in enumerate(item_sets):
            print(f"Evaluating Itemsets {its_i * 100 / len(item_sets)}")
            for t_i, transaction in enumerate(transactions):
                if set(item_set).issubset(transaction):
                    add_support(item_set, new_supports)

        for key, value in new_supports.items():
            new_supports[key] = value / transactions_length

        new_supports = {
            key: value for key, value
            in new_supports.items()
            if value >= MIN_SUPPORT
        }

        frequent.append(new_supports)

        k += 1

    print()
    frequent[0] = dict(frequent[0])
    for freq in frequent:
        print(freq)


def transposed_matrix():
    transactions = parse_file(dataset)
    transactions_length = len(transactions)

    maximum = max([max(transaction) for transaction in transactions])
    adjacency_matrix = {f"{i}": [] for i in range(int(maximum) + 1)}

    # Add ID of transaction to each item
    for t_i, transaction in enumerate(transactions):
        for item in transaction:
            adjacency_matrix[item].append(t_i)

    # Filter out items
    adjacency_matrix = {key: set(value) for key, value in adjacency_matrix.items() if
                        (value and len(value) / transactions_length >= MIN_SUPPORT)}

    frequent = [{key: len(value)/transactions_length for key, value in adjacency_matrix.items()}]
    k = 0
    write_data(frequent[k])
    confidences = {}
    while not len(frequent[k]) == 0:
        items = list(frequent[k])
        new_supports = {}
        items_length = len(items)
        for i in range(items_length - 1):
            print(f"Evaluating item #{i + 1}/{items_length}")
            items_a = [x for x in items[i]]
            for j in range(1, items_length - i):
                if isinstance(items[i], tuple):
                    items_b = [x for x in items[i + j]]
                    item_set = tuple(sorted(tuple(set(items_a).union(items_b))))
                else:
                    item_set = (items[i], items[i + j])

                if item_set in new_supports:
                    continue

                appearance_set = set()
                appearance_set = appearance_set.union(adjacency_matrix[item_set[-1]])
                for item_i in range(len(item_set) - 1):
                    appearance_set.intersection_update(adjacency_matrix[item_set[item_i]])

                if len(appearance_set) / transactions_length >= MIN_SUPPORT:
                    new_supports[item_set] = len(appearance_set) / transactions_length

        frequent.append(new_supports)

        for key_b, value_a_u_b in frequent[k+1].items():
            for key_a, value_a in frequent[k].items():
                if set(key_a).issubset(key_b):
                    a = key_a
                    a_u_b = set(key_b).difference(a)

                    if value_a == 0 or (value_a_u_b / value_a) < MIN_CONFIDENCE:
                        continue

                    if not a.__str__() in confidences:
                        confidences[a.__str__()] = {}
                    confidences[a.__str__()][a_u_b.__str__()] = value_a_u_b / value_a

        k += 1
        write_data(frequent[k])

    write_data("")
    write_data(confidences)

if __name__ == '__main__':

    with open("output.txt", "w"):
        pass

    transposed_matrix()


