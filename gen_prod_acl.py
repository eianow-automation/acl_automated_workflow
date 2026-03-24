#!/usr/bin/python -tt
# Project: acl_automated_workflow
# Filename: gen_prod_acl.py
# claudiadeluna
# PyCharm

from __future__ import absolute_import, division, print_function

__author__ = "Claudia de Luna (claudia@indigowire.net)"
__version__ = ": 1.0 $"
__date__ = "3/24/26"
__copyright__ = "Copyright (c) 2023 Claudia"
__license__ = "Python"

import argparse
from jinja2 import Environment, FileSystemLoader
import yaml
import os

import utilities

def main(args):

    # Load templates from ./templates directory
    template_dir = './templates'
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load the specific template file
    template = env.get_template('production_acl.j2')

    # Get dns_ips either from InfraHub or YAML file
    if args.infrahub:
        dns_ips = utilities.get_prod_dhcp_ips()
    else:
        with open('prod_dhcp_ips.yml', 'r') as f:
            data = yaml.safe_load(f)
            dns_ips = data['dns_ips']

    # Render the template
    rendered_config = template.render(dns_ips=dns_ips)

    # Create output directory if it doesn't exist
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)

    # Save to output directory
    output_file = os.path.join(output_dir, 'production_acl.txt')
    with open(output_file, 'w') as f:
        f.write(rendered_config)

    print(f"Generated config saved to: {output_file}")
    print(rendered_config)  # Still print for console review


# Standard call to the main() function.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script Description",
                                     epilog="Usage: ' python gen_prod_acl.py' ")

    # parser.add_argument('all', help='Execute all exercises in week 4 assignment')
    parser.add_argument('-i', '--infrahub', help='Get Production IPs from InfraHub', action='store_true',default=False)
    arguments = parser.parse_args()
    main(arguments)
 