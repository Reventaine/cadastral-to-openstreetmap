import osmapi
import pprint
from rosreestr2coord import Area

pp = pprint.PrettyPrinter(indent=4)

# credentials for OpenStreetMap:
api = osmapi.OsmApi(api="https://www.openstreetmap.org", username=u"Reventaine", password=u"A2480353bc")

# test coordinates:
nodes = {41.9119731: 42.2708720, 41.9143203: 42.2723311, 41.9119411: 42.2734040, 41.9109411: 42.2704040}


def create_area():
    with api.Changeset({u"comment": u"Add"}) as changeset_id:
        print(f"Part of Changeset {changeset_id}")

        # creates list of nodes for an area:
        ids = [api.NodeCreate({u"lon": k, u"lat": v, u"tag": {}})['id'] for k, v in nodes.items()]

        # adds the first node at the end of list of nodes to get a closed area:
        ids.append(ids[0])

        # creates an area from list of nodes:
        ways = api.WayCreate({
            'nd': ids,
            'tag': {
                'landuse': 'forest',
                'name': 'TestForest',
                'is_in:country': 'Russia',
            }})

        print(ways)


# create_area()
# shows the list of nodes:
# pp.pprint(api.WayGet(4305976864))

# shows list of nodes with lat and lon:
# pp.pprint(api.NodeGet(4332663959))

# shows changeset:
# pp.pprint(api.ChangesetGet(253220))

# shows entire information for area:
# pp.pprint(api.WayFull(26471061))
