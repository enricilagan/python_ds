cars = {
    'Ford': ['Falcon', 'Focus', 'Festiva', 'Fairlane'],
    'Holden': ['Commodore', 'Captiva', 'Barina', 'Trailblazer'],
    'Nissan': ['Maxima', 'Pulsar', '350Z', 'Navara'],
    'Honda': ['Civic', 'Accord', 'Odyssey', 'Jazz'],
    'Jeep': ['Grand Cherokee', 'Cherokee', 'Trailhawk', 'Trackhawk']
}


def get_all_jeeps(car=cars):
    """return a comma  + space (', ') separated string of jeep models (original order)"""
    return ', '.join(str(x) for x in car['Jeep'])


def get_first_model_each_manufacturer(car=cars):
    """return a list of matching models (original ordering)"""
    lst = []
    for keys in car.keys():
        lst.append(car[keys][0])
    return lst


def get_all_matching_models(car=cars, grep='trail'):
    """return a list of all models containing the case insensitive
       'grep' string which defaults to 'trail' for this exercise,
       sort the resulting sequence alphabetically"""
    lst = []
    for keys in car.keys():
        for x in range(len(car[keys])):
            if grep.lower() in car[keys][x].lower():
                lst.append(car[keys][x])
    return sorted(lst)


def sort_car_models(car=cars):
    """sort the car models (values) and return the resulting cars dict"""
    for keys, values in car.items():
        car[keys] = sorted(car[keys])
    return car