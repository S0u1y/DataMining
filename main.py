import collections


MIN_SUPPORT = 0.004
MIN_CONFIDENCE = 0.5

dataset = "Datasets/" + "T10I4D100K.dat"
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


def add_confidence(item_set, confidences_list):
    if item_set in confidences_list:
        confidences_list[item_set] += 1
    else:
        confidences_list[item_set] = 1


def Apriori():
    confidences = {}

    transactions = parse_file(dataset)
    transactions = [set(t) for t in transactions]

    transactions_length = len(transactions)

    for i in range(transactions_length):
        transaction = transactions[i]
        print(transaction)
        for item in transaction:
            add_confidence(item, confidences)

    for key, value in confidences.items():
        confidences[key] = value / transactions_length

    confidences = collections.OrderedDict(sorted(confidences.items()))

    confidences = {
        key: value for key, value
        in confidences.items()
        if value >= MIN_SUPPORT
    }

    write_data(confidences)

    k = 0

    frequent = [confidences.copy()]

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

        new_confidences = {}
        for its_i, item_set in enumerate(item_sets):
            print(f"Evaluating Itemsets {its_i * 100 / len(item_sets)}")
            for t_i, transaction in enumerate(transactions):
                if set(item_set).issubset(transaction):
                    add_confidence(item_set, new_confidences)

        for key, value in new_confidences.items():
            new_confidences[key] = value / transactions_length

        new_confidences = {
            key: value for key, value
            in new_confidences.items()
            if value >= MIN_SUPPORT
        }

        frequent.append(new_confidences)

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

    frequent = [adjacency_matrix.keys()]
    k = 0
    while not len(frequent[k]) == 0:

        write_data(frequent[k])

        items = list(frequent[k])
        new_confidence = {}
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

                if item_set in new_confidence:
                    continue

                appearance_set = set()
                appearance_set = appearance_set.union(adjacency_matrix[item_set[-1]])
                for item_i in range(len(item_set) - 1):
                    appearance_set.intersection_update(adjacency_matrix[item_set[item_i]])

                if len(appearance_set) / transactions_length >= MIN_SUPPORT:
                    new_confidence[item_set] = len(appearance_set) / transactions_length

        frequent.append(new_confidence)

        k += 1


if __name__ == '__main__':

    with open("output.txt", "w"):
        pass

    transposed_matrix()


