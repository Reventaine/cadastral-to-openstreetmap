from config import api


def get_coord(cadastral):
    from rosreestr2coord import Area
    import webbrowser
    try:
        area = Area(cadastral, with_proxy=True).get_coord()
        return list_to_dict(area)
    except:
        area = Area(cadastral, with_proxy=True).get_coord()
        url = f'https://pkk.rosreestr.ru/api/features/1/{cadastral}'
        webbrowser.open(url)


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
    import rosreestr2coord
    with api.Changeset({u"comment": u"Test area from Rosreestr"}):
        coords = get_coord(cadastral)

        # creates list of nodes for an area:
        ids = [api.NodeCreate({u"lon": k, u"lat": v, u"tag": {}})['id'] for k, v in coords.items()]

        # adds the first node at the end of list of nodes to get a closed area:
        ids.append(ids[0])

        # creates an area from list of nodes:
        ways = api.WayCreate({
            'nd': ids,
            'tag': {
                'landuse': 'construction',
                'назначение': rosreestr2coord.Area('38:06:144003:4723').get_attrs()['util_by_doc'],
                'name': 'Test_Cad',
                'is_in:country': 'Russia',
            }})

        return ways['id']


def get_X_Y(cadastral):
    id = create_area(cadastral)
    way = api.WayFull(id)[0]['data']
    return way['lon'], way['lat']


def get_X(cadastral):
    return get_X_Y(cadastral)[0]


def get_Y(cadastral):
    return get_X_Y(cadastral)[1]



