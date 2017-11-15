#!/usr/bin/env python3

import openpyxl
from collections import defaultdict
import json


def fix_val(v):
    return v


def brute_read(sheet, offset):
    return [t for t in [[fix_val(s.value) for s in t if s.value] for t in sheet.iter_rows(row_offset=offset)] if len(t) > 0]


def scrape_participation_aspect(sheet, aspect):
    rows = brute_read(sheet, 5)
    header = rows[0]
    rows = rows[1:]

    obj = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    def add_data(element, current_state, current_electorate, data):
        obj[element][current_state][current_electorate].update(data)

    current_state = None
    for row in rows:
        if len(row) == 1:
            if row[0].endswith(' Divisions'):
                current_state = row[0].rsplit(' ', 1)[0]
                continue
            else:
                break
        if row[1] == 'Total participants':
            current_electorate = row[0]
            add_data(row[1], current_state, current_electorate, zip(header, row[2:]))
        else:
            add_data(row[0], current_state, current_electorate, zip(header, row[1:]))

    def dump_elem(elem):
        with open('output/participation/%s - %s.json' % (aspect, elem), 'w') as fd:
            json.dump(obj[elem], fd, indent=4, separators=(',', ': '))

    dump_elem('Total participants')
    dump_elem('Eligible participants')
    dump_elem('Participation rate (%)')


def scrape_participation(fname):
    wb = openpyxl.load_workbook(fname)
    scrape_participation_aspect(wb.get_sheet_by_name("Table 4"), "All")
    scrape_participation_aspect(wb.get_sheet_by_name("Table 5"), "Male")
    scrape_participation_aspect(wb.get_sheet_by_name("Table 6"), "Female")


def scrape_response(fname):
    pass


def main():
    scrape_participation('data/xlsx/participation.xlsx')
    scrape_response('data/xlsx/participation.xlsx')
    pass


if __name__ == '__main__':
    main()
