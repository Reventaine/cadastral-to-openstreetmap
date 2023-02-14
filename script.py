from config import api
import functools


@functools.cache
def get_coordinates(cadastral):
    from rosreestr2coord import Area
    import webbrowser

    try:
        location = Area(cadastral, with_proxy=True).get_coord()
    except:
        # if connection to rosreestr was broken:
        location = Area(cadastral, with_proxy=True).get_coord()
        url = f'https://pkk.rosreestr.ru/api/features/1/{cadastral}'
        webbrowser.open(url)

    return list_to_dict(location)


def list_to_dict(lst):
    # ensures that output from the cadastral will be in form of {lon: lat, ...}
    result = {}
    i = 0
    while i < len(lst):
        if isinstance(lst[i], list):
            nested_dict = list_to_dict(lst[i])
            for key in nested_dict.keys():
                result[key] = nested_dict[key]
            i += 1
        else:
            result[lst[i]] = lst[i + 1]
            i += 2
    return result


def create_area(cadastral):
    from rosreestr2coord import Area
    import json

    try:
        with open('cache.json', 'r') as fp:
            cache = json.load(fp)
    except (FileNotFoundError, json.JSONDecodeError):
        cache = {}

    if cadastral not in cache:
        with api.Changeset({u"comment": u"Test area from Rosreestr"}):
            coordinates = get_coordinates(cadastral)

            # creates list of nodes for an area:
            ids = [api.NodeCreate({u"lon": k, u"lat": v, u"tag": {}})['id'] for k, v in coordinates.items()]

            # adds the first node at the end of list of nodes to get a closed area:
            ids.append(ids[0])

            # creates an area from list of nodes:
            ways = api.WayCreate({
                'nd': ids,
                'tag': {
                    'name': cadastral,
                    'is_in:country': 'Russia',
                    'utility': Area(cadastral).get_attrs()['util_by_doc'],
                    'address': Area(cadastral).get_attrs()['address'],
                    'landuse': 'construction',
                }})

            cache[cadastral] = ways

            with open('cache.json', 'w') as fp:
                json.dump(cache, fp)

    else:
        ways = cache[cadastral]

    return ways['id']


@functools.cache
def get_X_Y(cadastral):
    id = create_area(cadastral)
    way = api.WayFull(id)[0]['data']
    return way['lon'], way['lat']


def get_X(cadastral):
    return get_X_Y(cadastral)[0]


def get_Y(cadastral):
    return get_X_Y(cadastral)[1]

