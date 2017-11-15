#!/usr/bin/env python3

import json
import csv
import sys

abbrev = {
    'New South Wales': 'NSW',
    'Victoria': 'VIC',
    'South Australia': 'SA',
    'Northern Territory': 'NT',
    'Queensland': 'QLD',
    'Tasmania': 'TAS',
    'Western Australia': 'WA',
    'Australian Capital Territory': 'ACT'
}


def main():
    fname = 'output/response/By Electorate.json'
    with open(fname) as fd:
        data = json.load(fd)

    electorates = []
    total_clear = 0
    total_not_clear = 0
    for state in data:
        for electorate, obj in data[state].items():
            clear = obj["Response clear"]["count"]
            not_clear = obj["Response not clear"]["count"]
            total_clear += clear
            total_not_clear += not_clear
            electorates.append([abbrev[state], electorate, round(100 * not_clear / (clear + not_clear), 2)])
    electorates.sort(key=lambda x: x[-1])
    w = csv.writer(sys.stdout)
    w.writerow(['State', 'Electorate', 'Informality %'])
    w.writerows(electorates)
    print(total_clear, total_not_clear, round(100 * (total_not_clear / (total_clear + total_not_clear)), 2))


if __name__ == '__main__':
    main()
