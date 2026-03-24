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
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_prod_dhcp_ips():
    """
    Fetch production DHCP IPs from InfraHub GraphQL API.
    
    Returns:
        tuple: (ip_list, error_message) where ip_list is a list of IP strings
               and error_message is None on success or a string describing the error.
    """
    INFRAHUB_URL = os.getenv("INFRAHUB_URL", "https://sandbox.infrahub.app/graphql")
    API_TOKEN = os.getenv("INFRAHUB_TOKEN")
    NAMESPACE_NAME = "Production_DHCP"
    
    if not API_TOKEN:
        error_msg = "INFRAHUB_TOKEN not found in environment variables. Please set it in .env file."
        print(error_msg)
        return [], error_msg

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

    try:
        response = requests.post(
            INFRAHUB_URL,
            json={'query': query, 'variables': variables},
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            
            # Check for GraphQL errors
            if 'errors' in data:
                error_msg = f"GraphQL Error: {data['errors']}"
                print(error_msg)
                return [], error_msg
            
            # Check if data structure is as expected
            if 'data' not in data or 'IpamIPAddress' not in data['data']:
                error_msg = f"Unexpected response structure from InfraHub"
                print(f"{error_msg}: {data}")
                return [], error_msg
                
            edges = data['data']['IpamIPAddress']['edges']

            ip_list = []
            print(f"Found {len(edges)} IP addresses:")
            for edge in edges:
                ip = edge['node']['address']['value']
                print(ip)
                ip_list.append(ip)
            return ip_list, None
        else:
            error_msg = f"HTTP Error {response.status_code}: {response.text}"
            print(error_msg)
            return [], error_msg
            
    except requests.exceptions.ConnectionError as e:
        error_msg = "Connection Error: Failed to connect to InfraHub. Check your network connection."
        print(f"{error_msg}\nDetails: {str(e)}")
        return [], error_msg
    except requests.exceptions.Timeout as e:
        error_msg = "Timeout Error: Request to InfraHub timed out after 30 seconds."
        print(error_msg)
        return [], error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"Request Error: {str(e)}"
        print(error_msg)
        return [], error_msg
    except (KeyError, TypeError) as e:
        error_msg = f"Data Parsing Error: Unexpected response format from InfraHub. {str(e)}"
        print(error_msg)
        return [], error_msg
    except Exception as e:
        error_msg = f"Unexpected Error: {str(e)}"
        print(error_msg)
        return [], error_msg


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
