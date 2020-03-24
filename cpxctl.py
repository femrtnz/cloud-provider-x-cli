#!/usr/bin/env python3

from os import system, name
import click
import requests
from prettytable import PrettyTable
import time


__author__ = "Felipe Amaral"
default_server = "http://localhost:9999"


@click.group()
def list():
    pass

@list.command()
@click.argument('what')
@click.option('--server', default = default_server)
@click.option('--watch', default = False)
def get(what, server, watch):

    table = PrettyTable()

    while True:
        if what == 'average':
            average(table, server)
        else:
            services(what, table, server)
        print(table)

        if bool(watch) is not True:
            break
        time.sleep(2)
        clear()
        table = PrettyTable()


def get_servers(server):
    return requests.get(server + '/servers')


def get_details(server, ip):
    return requests.get(server + '/' + ip)


def average(table, server):
    table.field_names = ["Service", "CPU Average", "Memory Average", "Servers Healthy", "ACTION"]
    resp = get_servers(server)
    item_map = {}
    for ip in resp.json():
        item_resp = get_details(server,  ip)
        item = item_resp.json()

        if item['service'] in item_map:
            it = item_map[item['service']]
            it['cpu'] = it['cpu'] + float(item['cpu'].rstrip("%"))
            it['memory'] = it['memory'] + float(item['memory'].rstrip("%"))
            it['quantity'] = it['quantity'] + 1
            it['healthy'] = it['healthy'] + (float(item['cpu'].rstrip("%")) < 90 or float(item['memory'].rstrip("%")) < 90 and 1 or 0)
            item_map.update({item['service']: it})
        else:
            if float(item['cpu'].rstrip("%")) < 90 or float(item['memory'].rstrip("%")) < 90:
                healthy = 1
            else:
                healthy = 0
            item_map.update({item['service']: {
                    'ip': ip,
                    'cpu': float(item['cpu'].rstrip("%")),
                    'memory': float(item['memory'].rstrip("%")),
                    'quantity': 1,
                    'healthy': healthy}
                })

    for key, value in item_map.items():
        table.add_row([
            key,
            "{0:.2f}".format(value['cpu'] / value['quantity']) + "%",
            "{0:.2f}".format(value['memory'] / value['quantity']) + "%",
            value['healthy'],
            value['healthy'] < 2 and 'X' or ''
        ])


def services(what, table, server):
    table.field_names = ["IP", "Service", "Status", "CPU", "Memory"]
    resp = get_servers(server)
    for ip in resp.json():
        item_resp = get_details(server, ip)
        item = item_resp.json()
        if float(item['cpu'].rstrip("%")) > 90 or float(item['memory'].rstrip("%")) > 90:
            status = '\033[31m' + 'Unhealthy' + '\033[0m'
        else:
            status = 'Healthy'
        if what == 'all':
            table.add_row([ip, item['service'], status, item['cpu'], item['memory']])
        elif what == item['service']:
            table.add_row([ip, item['service'], status, item['cpu'], item['memory']])


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix') 
    else:
        _ = system('clear')

cli = click.CommandCollection(sources=[list])

if __name__ == '__main__':
    cli()
