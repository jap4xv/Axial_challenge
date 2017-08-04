import json
import sys
from collections import OrderedDict


input_seller = sys.argv[1]


def get_data():
    with open('sample_data.json', 'r') as data_file:
        # json_data = data_file.read()
        data = json.load(data_file)

    return data


def get_buyers_and_sellers(data):
    sellers = {}
    buyers = {}

    for object in data:
        if object['type'] == 'seller':
            sellers[object['id']] = object
        elif object['type'] == 'buyer':
            buyers[object['id']] = object

    return buyers, sellers


def get_matched_buyers(seller_object, buyers):
    target_geographies = set(seller_object['details']['geography_ids'])
    target_industries = set(seller_object['details']['industry_ids'])
    matched_buyers = {}
    for potential_buyer_id, buyer_object in buyers.iteritems():

        buyer_geographies = set(buyer_object['details']['geography_ids'])
        buyer_industries = set(buyer_object['details']['industry_ids'])

        intersecting_geographies = target_geographies & buyer_geographies
        intersecting_industries = target_industries & buyer_industries

        if intersecting_geographies and intersecting_industries:
            matched_buyers[potential_buyer_id] = len(intersecting_geographies) + len(intersecting_industries)

    matched_buyers = OrderedDict(sorted(matched_buyers.items(), key=lambda t: t[1], reverse=True))

    return matched_buyers


data = get_data()
buyers, sellers = get_buyers_and_sellers(data)
seller_object = sellers[input_seller]
matched_buyers = get_matched_buyers(seller_object, buyers)

print "Matched Buyers:"
for buyer, score in matched_buyers.iteritems():
    print 'Buyer ID: ' + buyer + ', match score: ' + str(score)



