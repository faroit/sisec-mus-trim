import csv


def csv_to_dict(csv_path="data/previews.csv"):
    previews = {}
    with open(csv_path, 'r') as csvfile:
        preview_reader = csv.reader(csvfile, delimiter=',')
        for row in preview_reader:
            previews[int(row[0])] = (int(row[1]), int(row[2]))

    return previews
