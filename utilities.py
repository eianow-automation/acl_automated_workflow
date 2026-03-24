#!/usr/bin/python -tt
# Project: acl_automated_workflow
# Filename: utilities.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "3/24/26"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
import requests


def get_prod_dhcp_ips():


    INFRAHUB_URL = "https://sandbox.infrahub.app/graphql"
    API_TOKEN = "189fcd13-e4d0-9e78-d865-1065e4c7260b"
    NAMESPACE_NAME = "Production_DHCP"

    # GraphQL Query
    query = """
    query GetIPsByNamespace($name: String!) {
      IpamIPAddress(ip_namespace__name__value: $name) {
        edges {
          node {
            address {
              value
            }
          }
        }
      }
    }
    """

    variables = {
        "name": NAMESPACE_NAME
    }

    headers = {
        "X-INFRAHUB-KEY": API_TOKEN,
        "Content-Type": "application/json"
    }

    def fetch_ips():
        response = requests.post(
            INFRAHUB_URL,
            json={'query': query, 'variables': variables},
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            edges = data['data']['IpamIPAddress']['edges']

            ip_list = []
            print(f"Found {len(edges)} IP addresses:")
            for edge in edges:
                ip = edge['node']['address']['value']
                print(ip)
                ip_list.append(ip)
            return ip_list
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    if __name__ == "__main__":
        fetch_ips()


def main():
    get_prod_dhcp_ips()

# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python utilities.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    # parser.add_argument('-a', '--all', help='Execute all exercises in week 4 assignment', action='store_true',default=False)
    arguments = parser.parse_args()
    main()
