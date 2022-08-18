import csv
import json
import sys

# Global CLI arguments storage
args = {}


def get_args():
    """
    Get CLI arguments into a dict storage.
    """
    global args
    args = json.loads(sys.argv[1])


def shuffle(num_reducers=1):
    """
    Partition data into groups by map keys.
    """
    shuffled_items = []

    prev_key = None
    values = []

    try:
        for line in sys.stdin:
            key, title, year = line.split("\t")

            if key != prev_key and prev_key != None:
                shuffled_items.append((prev_key, values))
                values = []
                
            prev_key = key
            values.append((title.strip(), year.strip()))
    except:
        pass
    finally:
        if prev_key != None:
            shuffled_items.append((key, values))

    result = []
    num_items_per_reducer = len(shuffled_items) // num_reducers
    if len(shuffled_items) / num_reducers != num_items_per_reducer:
        num_items_per_reducer += 1
    for i in range(num_reducers):
        result.append(shuffled_items[num_items_per_reducer*i:num_items_per_reducer*(i+1)])

    return result


def reduce(key, values):
    """
    Reducer function for mapreduce flow.
    """
    if args['N'] is not None:
        values = values[:int(args['N'])]

    values.sort(key=lambda item: item[0])
    values.sort(key=lambda item: item[1], reverse=True)

    return key, values


def main():
    """
    Entry point: get CLI args and process reducing.
    """
    get_args()

    headers = ['genre', 'title', 'year']
    csv_writer = csv.DictWriter(sys.stdout, headers,
                                delimiter=args['dst_delimiter'].encode('utf-8'),
                                lineterminator='\n')

    for group in shuffle():
        for key, values in group:
            genre, title_year = reduce(key, values)

            for title, year in title_year:
                row = {'genre': genre, 'title': title, 'year': year}
                csv_writer.writerow(row)


if __name__ == '__main__':
    main()
