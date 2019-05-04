import pprint

# user_skill1 = ['java', 'c', 'html', 'bootstrap', 'css', 'javascript']
# user_exp = 2
# user_skill2 = ['ML','css','java']
# user_skill3 = ['java','javascript','html']

# pp = pprint.PrettyPrinter(depth=6)
#
# companies = [
#     {"company_name": "slk", "keywords": ['ML', 'javascript', 'css', 'java'], 'salary': 100000, 'exp': 2},
#     {"company_name": "infosys", "keywords": ['c', 'java', 'javascript', 'c++', 'html'], 'salary': 400000, 'exp': 0},
#     {"company_name": "syntel", "keywords": ['java', 'c', 'html'], 'salary': 200000, 'exp': 3},
#     {"company_name": "ibm", "keywords": ['bootsrap'], 'salary': 300000, 'exp': 1},
#     {"company_name": "abc", "keywords": ['angular', 'javascript', 'css', 'web'], 'salary': 100000, 'exp': 2},
#     {"company_name": "oracle", "keywords": ['spring', 'java', 'servlet', ], 'salary': 100000, 'exp': 2},
#     {"company_name": "amazon", "keywords": ['IOT', 'Big data'], 'salary': 100000, 'exp': 2},
#     {"company_name": "flipkart", "keywords": ['php', 'javascript', 'mongodb', 'html', 'ML'], 'salary': 100000, 'exp': 2}
# ]

import re


def weightage(user_data, companies):
    unranked_companies = []

    # cleanse user data
    cleansed_user_data = cleanseData(user_data)

    for company in companies:
        count = 0
        matched_skills = []
        for skill in set(cleansed_user_data):
            for keyword in company['keywords']:
                if skill.strip().lower() == keyword.strip().lower():
                    matched_skills.append(skill)
                    count = count + 1
        company["matched_skills"]= matched_skills
        company["count"] = count
        unranked_companies.append(company)
    return rank(cleansed_user_data, unranked_companies)


def rank(user_skills, unranked_companies):
    sorted_company_by_count = multiSort(unranked_companies)
    # pp.pprint(sorted_company_by_count)
    company_map_count = []

    for company in sorted_company_by_count:

        if len(company_map_count) == 0:
            company_map_count.append({"weightage": company["count"], "companies": [company]})
        else:
            if checkIfKeyExists("weightage", company["count"], company_map_count):
                for ele in company_map_count:
                    if ele["weightage"] == company["count"]:
                        ele["companies"].append(company)
            else:
                company_map_count.append({"weightage": company["count"], "companies": [company]})

    # pp.pprint(company_map_count)
    return sortCompanyCat(company_map_count)


def checkIfKeyExists(key, ele_key, arr):
    for ele in arr:
        if ele[key] == ele_key:
            return True
    return False


def sortCompanyCat(company_map_count):
    # pp.pprint(company_map_count)
    # print()

    ranked_companies = []

    for cat in company_map_count:
        sequence = knn(cat)
        # pp.pprint(sequence)
        ranked_companies.append(sequence)

    # FINAL result of ranked companies
    # pp.pprint(company_map_count)
    return company_map_count


def knn(cat):
    for c in cat['companies']:
        if cat['weightage'] == 0 or cat['weightage'] == 1:
            weight = 0
            c['weight'] = weight
        else:
            weight = len(c['keywords']) / cat['weightage']
            c['weight'] = weight
    # pp.pprint(cat['companies'])
    # print()
    return weightageSort(cat['companies'])


# Python program for implementation of Multi Sort

def multiSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is lesser
            # than the next element
            if arr[j]['count'] < arr[j + 1]['count']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def weightageSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j]['weight'] > arr[j + 1]['weight']:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def cleanseData(arr):
    cleansed_data = []
    for data in arr:
        # using regular expression to remove punctuations and considering only alphanumeric characters
        filtered_data = re.sub('[^\w^\.]', '', data.strip().lower())
        cleansed_data.append(filtered_data)
    return cleansed_data

#weightage(user_skill1, companies)

