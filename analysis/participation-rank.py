#!/usr/bin/env python3

import json
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
    # attr: e.g. "18-19 years"
    fname, attr = sys.argv[1:]
    with open(fname) as fd:
        data = json.load(fd)

    electorates = []
    for state in data:
        for electorate, obj in data[state].items():
            if electorate.endswith(' (Total)'):
                continue
            electorates.append([abbrev[state] + ': ' + electorate, obj[attr]])
    electorates.sort(key=lambda x: x[1], reverse=True)
    for e, v in electorates:
        print(e, v)


if __name__ == '__main__':
    main()
