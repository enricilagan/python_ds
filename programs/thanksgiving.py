import csv
import os
from collections import namedtuple, Counter
from typing import List
from itertools import chain

head = 'respondent_id,celebrate,main_dish,main_dish_other,main_dish_cooked,main_dish_cooked_other,stuffing,' \
       'stuffing_other,cranberry_sauce_type,cranberry_sauce_type_other,gravy,side_dishes_brussels_sprouts,' \
       'side_dishes_carrots,side_dishes_cauliflower,side_dishes_corn,side_dishes_cornbread,side_dishes_fruit_salad,' \
       'side_dishes_green_beans,side_dishes_macaroni_and_cheese,side_dishes_mashed_potatoes,' \
       'side_dishes_rolls_biscuits,side_dishes_squash,side_dishes_vegetable_salad,side_dishes_yams_casserole,' \
       'side_dishes_other,side_dishes_other2,pie_apple,pie_buttermilk,pie_cherry,pie_chocolate,' \
       'pie_coconut_cream,pie_key_lime,pie_peach,pie_pecan,pie_pumpkin,pie_sweet_potato,pie_none,pie_other,' \
       'pie_other2,desserts_apple_cobbler,desserts_blondies,desserts_brownies,desserts_carrot_cake,' \
       'desserts_cheesecake,desserts_cookies,desserts_fudge,desserts_ice_cream,desserts_peach_cobbler,' \
       'desserts_none,desserts_other,desserts_other2,pray,travel_distance,macys_parade,age_cutoff,' \
       'friends_meet_up,friendsgiving,black_friday,work_retail,work_black_friday,living_place,age,' \
       'gender,total_income,us_region'

data = []  # initialize a list of data
Record = namedtuple('Record', head.split(','))


def change_col():
    base_folder = os.path.dirname(__file__)
    file = 'thanksgiving-2015-poll-data.csv'
    filename = os.path.join(base_folder, 'data', file)
    with open(filename, 'r', encoding='utf-8') as fin:
        data_ = fin.read()
        data_ = data_.split('\n')[1:]

    file1 = 'thanksgiving-2015-polls.csv'
    filename1 = os.path.join(base_folder, 'data', file1)
    with open(filename1, 'w', encoding='utf-8') as out:
        out.write(head + '\n' + '\n'.join(data_))


def init():
    change_col()
    base_folder = os.path.dirname(__file__)
    file = 'thanksgiving-2015-polls.csv'
    filename = os.path.join(base_folder, 'data', file)

    with open(filename, 'r', encoding='utf-8') as fin:
        # Parsing
        reader = csv.DictReader(fin)

        data.clear()  # so running this will not overload the data
        for row in reader:
            record = Record(
                **row
            )
            data.append(record)


def parse_row(row):
    # Use this to load all data into a namedtuple, **row will load all rows.
    record = Record(**row)
    return record


def region() -> List[Record]:
    return list(set([r.us_region for r in data]))


def income(r) -> List[Record]:
    return list(set([i.total_income for i in data if i.us_region == r]))


def main_dish_selection(r, inc):
    m = list([i.main_dish for i in data if (i.celebrate == 'Yes') and (i.us_region == r) and (i.total_income == inc)])
    m = Counter(m).most_common(1)[0][0]
    cooked = Counter(list([i.main_dish_cooked for i in data if (i.celebrate == 'Yes') and (i.us_region == r)
                           and (i.total_income == inc) and (i.main_dish == m)])).most_common(1)[0][0]
    cranberry = Counter(list([i.cranberry_sauce_type for i in data if (i.celebrate == 'Yes') and (i.us_region == r)
                              and (i.total_income == inc) and (i.main_dish == m)])).most_common(1)[0][0]
    gravy = Counter(list([i.gravy for i in data if (i.celebrate == 'Yes') and (i.us_region == r)
                          and (i.total_income == inc) and (i.main_dish == m)])).most_common(1)[0][0]
    return m, cooked, cranberry, gravy


def side_dishes(r, inc):
    sd = list([i[11:26] for i in data if (i.celebrate == 'Yes') and (i.us_region == r) and (i.total_income == inc)])
    side = list(chain(*sd))
    while '' in side:
        side.remove('')
    return [x[0] for x in Counter(side).most_common(3)]


def which_pie(r, inc):
    pie = list([i[27:39] for i in data if (i.celebrate == 'Yes') and (i.us_region == r) and (i.total_income == inc)])
    p = list(chain(*pie))
    while '' in p:
        p.remove('')
    return Counter(p).most_common(1)[0][0]


def desserts(r, inc):
    desserts = list([i[40:51] for i in data if (i.celebrate == 'Yes') and (i.us_region == r) and (i.total_income == inc)])
    d = list(chain(*desserts))
    while '' in d:
        d.remove('')
    return Counter(d).most_common(1)[0][0]

"""
desserts_apple_cobbler,desserts_blondies,desserts_brownies,desserts_carrot_cake,' \
       'desserts_cheesecake,desserts_cookies,desserts_fudge,desserts_ice_cream,desserts_peach_cobbler,' \
       'desserts_none,desserts_other,desserts_other2'
"""

