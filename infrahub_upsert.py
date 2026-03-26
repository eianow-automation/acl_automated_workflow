#!/usr/bin/python -tt
# Project: acl_automated_workflow
# Filename: infrahub_upsert.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "3/26/26"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import requests


def gql_request(query, variables=None):
    response = requests.post(URL, json={'query': query, 'variables': variables}, headers=HEADERS)
    return response.json().get('data', {})


def upsert_data():
    # 1. Check/Create Namespace
    find_ns = gql_request("query($n: String!){IpamNamespace(name__value: $n){edges{node{id}}}}",
                          {"n": NAMESPACE_NAME})
    ns_edges = find_ns.get('IpamNamespace', {}).get('edges', [])

    if ns_edges:
        ns_id = ns_edges[0]['node']['id']
        print(f"✔ Namespace found: {ns_id}")
    else:
        create_ns = gql_request("mutation($n: String!){IpamNamespaceCreate(data:{name:{value:$n}}){object{id}}}",
                                {"n": NAMESPACE_NAME})
        ns_id = create_ns['IpamNamespaceCreate']['object']['id']
        print(f"✚ Namespace created: {ns_id}")

    # 2. Check/Create IPs
    ips = ["10.10.10.11/24", "10.10.10.12/24", "10.10.10.13/24"]
    for ip in ips:
        find_ip = gql_request("""
            query($a: String!, $ns: ID!){
                IpamIPAddress(address__value: $a, ip_namespace__ids: [$ns]){
                    edges{node{id}}
                }
            }
        """, {"a": ip, "ns": ns_id})

        if find_ip.get('IpamIPAddress', {}).get('edges'):
            print(f"  ✔ {ip} exists.")
        else:
            gql_request("""
                mutation($a: String!, $ns: ID!){
                    IpamIPAddressCreate(data:{address:{value:$a}, ip_namespace:{id:$ns}}){ok}
                }
            """, {"a": ip, "ns": ns_id})
            print(f"  ✚ {ip} created.")


def main():


    URL = "https://sandbox.infrahub.app/graphql"
    HEADERS = {"X-INFRAHUB-KEY": "your_token_here", "Content-Type": "application/json"}



    if __name__ == "__main__":
        upsert_data()

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python infrahub_upsert.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
