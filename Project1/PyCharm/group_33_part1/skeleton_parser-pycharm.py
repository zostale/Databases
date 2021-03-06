"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', \
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

category_list = []

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
As there are unterminated quotation marks, SQLite will throw an error during the import. To prevent this, you need to
perform both of the following:
1. Escape every instance of a double quote with another double quote.
2. Surround all strings with double quotes.
"""


def escapeQuotes(str):
    if str == None:
        return str
    return '"' + str.replace('"', '""') + '"';


"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


def addItems(item, itemF):
    itemDict = []
    itemDict.append(item["ItemID"])
    itemDict.append(escapeQuotes(item["Seller"]["UserID"]))
    itemDict.append(escapeQuotes(item["Name"]))
    itemDict.append(transformDollar(item["Currently"]))
    if "Buy_Price" in item:
        itemDict.append(transformDollar(item["Buy_Price"]))
    else:
        itemDict.append("NULL")
    itemDict.append(transformDollar(item["First_Bid"]))
    itemDict.append(item["Number_of_Bids"])
    itemDict.append(transformDttm(item["Started"]))
    itemDict.append(transformDttm(item["Ends"]))
    if "Description" in item and item["Description"] != None:
        itemDict.append(escapeQuotes(item["Description"]))
    else:
        itemDict.append("NULL")
    itemF.write(columnSeparator.join(map(lambda str: str or "", itemDict)))
    itemF.write("\n")



def addSellers(item, userF):
    user = []
    user.append(escapeQuotes(item["Seller"]["UserID"]))
    user.append(item["Seller"]["Rating"])
    user.append(escapeQuotes(item["Location"])) #can this be null ?
    user.append(escapeQuotes(item["Country"]))  #can this be null ?
    userF.write(columnSeparator.join(map(lambda str: str or "", user)))
    userF.write("\n")


def addBidsAndBidders(item, userF, bidsF):
    bids = item["Bids"]

    if bids != None:
        for bid in bids:
            bidData = bid["Bid"]
            bidder = bidData["Bidder"]
            user = []
            user.append(escapeQuotes(bidder["UserID"]))
            user.append(bidder["Rating"])
            user.append(escapeQuotes(bidder.get("Location", "NULL")))
            user.append(escapeQuotes(bidder.get("Country", "NULL")))
            userF.write(columnSeparator.join(map(lambda str: str or "", user)))
            userF.write("\n")


            bidMap = []
            bidMap.append(escapeQuotes(bidData["Bidder"]["UserID"]))
            bidMap.append(item["ItemID"])
            bidMap.append(transformDttm(bidData["Time"]))
            bidMap.append(transformDollar(bidData["Amount"]))
            bidsF.write(columnSeparator.join(map(lambda str: str or "", bidMap)))
            bidsF.write("\n")

def addCategories (item, categoryF, categoryListF):
    categories = item["Category"]
    itemId = item["ItemID"]
    for category in categories:
        categoryMap = []
        categoryMap.append(itemId)
        categoryMap.append(escapeQuotes(category))
        categoryF.write(columnSeparator.join(map(lambda str: str or "", categoryMap)))
        categoryF.write("\n")

        if category not in category_list:
            category_list.append(category)
            categoryListF.write(escapeQuotes(category))
            categoryListF.write("\n")

"""
Parsing JSON to extract schema
"""
def parseJson(json_file):
    fileNames = ["items.dat", "users.dat", "categories.dat", "bids.dat", "category_list.dat"]
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items']  # creates a Python dictionary of Items for the supplied json file
        itemF = open(fileNames[0], 'a')
        userF = open(fileNames[1], 'a')
        categoryF = open(fileNames[2], 'a')
        bidF = open(fileNames[3], 'a')
        categoryListF = open(fileNames[4], 'a')
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # Items(ItemID, Seller, Name, Currently, Buy_Price, First_Bid, Started, Ends, Description)
            addItems(item, itemF)
            # User(UserID, Rating, Location, Country)
            addSellers(item, userF)
            # Bids(UserID, Time, Amount)
            addBidsAndBidders(item, userF, bidF)
            # Category(ItemID, Category)
            # CategoryList (Category)
            addCategories(item, categoryF, categoryListF)

            pass


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""


def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f


if __name__ == '__main__':
    main(sys.argv)
