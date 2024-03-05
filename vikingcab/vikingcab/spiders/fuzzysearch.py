#!/usr/bin/python

from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import json
import sys

import pdb

json_file = r'./items.json'
result_cnt = 10

def list2dict(db):
    db_dict = {}
    for item in db:
        if item['book_name'] in db_dict:
            #print("Book already existed: <<{}>>".format(item['book_name']))
            pass
        elif r'妹子' not in item['book_name']:
            db_dict[item['book_name']] = item['url']
    return db_dict

def main():
    if len(sys.argv) < 2:
        return
    global result_cnt
    keyword = sys.argv[1]
    if (len(sys.argv) > 2):
        result_cnt = int(sys.argv[2])
    with open(json_file, "r") as fp:
        db = json.load(fp)
    #breakpoint()
    db_dict = list2dict(db)
    bookname_list = list(db_dict.keys())
    match_ratios = process.extract(keyword, bookname_list, scorer = fuzz.token_sort_ratio, limit=result_cnt)
    for matchi in match_ratios:
        print("Score:{} Book Name:<<{}>> URL:{}".format(matchi[1], matchi[0], db_dict[matchi[0]]))

if __name__ == "__main__":
    main()
