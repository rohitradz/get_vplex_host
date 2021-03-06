'''
Description:   Get hosts connected to a vplex
Prerequisties: box.txt should be present with names and ips of vplex arrays
Dev by: Rohit R
'''

import sys, requests, json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


hst_lst = []
test_vplex=''


def vpl_fetch(url):
    try:
        headers = {'content-type': 'application/json', 'Username': 'myuser', 'Password': 'mypass.'}
        resp1 = requests.get(url, verify=False, headers=headers).json()

        # This will fetch the storage view names from the json output
        clus1 = resp1["response"]["context"][0]["children"]

    except  requests.exceptions.RequestException as e:
        print("\n")
        print("Unable to connect to VPLEX ,try after sometime!")
        sys.exit(0)

    clus_v = []

    for i in clus1:
        clus_v.append(i["name"])

    # To remove json encoding
    clus_v1 = [str(r) for r in clus_v]

    clus_1 = []

    for i in clus_v1:
        if "V1_" in i:
            clus_1.append(i.split('V1_'))

        elif "V2_" in i:
            clus_1.append(i.split('V2_'))

        else:
            pass

    final_hst_lst = []
    for sublist in clus_1:
        for each in sublist:
            final_hst_lst.append(each)

    # Remove the duplicate server names and convert to upper case
    new_lst = []

    for i in final_hst_lst:
        if i not in new_lst:
            new_lst.append(i.upper())

    if '' == new_lst[0]:
        new_lst = new_lst[1:]
    return new_lst


# This will get the hosts for vplex box as an input

def vpl(ip):
    url = 'https://' + ip + '/vplex/clusters/cluster-1/exports/storage-views/'
    return vpl_fetch(url)


print(" 1) Display servers connected to a VPLEX \n")
print(" 2) Exit \n")

val = input()

if val == '1':
    d2 = {}
    try:
        with open('box.txt') as f:
            d2 = json.load(f)
            for k, v in d2.items():
                print(k.upper())
    except:
        print("box.txt is not present to proceed further.")
        sys.exit(0)

    box = input("\n Enter the box listed above:  \n").lower()

    for k, v in d2.items():
        if k == box:
            hst_lst = vpl(v)
            test_vplex = k

    if test_vplex != box:
        print("Wrong box, please try again")
        sys.exit(0)

else:
    sys.exit(0)

print ("\n")
for i in hst_lst:
    print(i)
