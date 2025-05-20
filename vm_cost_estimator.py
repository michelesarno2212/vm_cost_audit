#!/usr/bin/env python3

import openstack
import datetime
from prettytable import PrettyTable

def main():
    conn = openstack.connect()

    table = PrettyTable()
    table.field_names = ["Nome VM", "RAM (MB)", "Uptime (ore)", "Costo stimato (€)"]

    for server in conn.compute.servers(details=True):
        flavor = conn.compute.get_flavor(server.flavor['id'])
        ram = flavor.ram

        uptime_hours = 0
        if server.launched_at:
            launched_at = server.launched_at
            if isinstance(launched_at, str):
                launched_at = datetime.datetime.fromisoformat(launched_at.replace("Z", "+00:00"))
            delta = datetime.datetime.now(datetime.timezone.utc) - launched_at
            uptime_hours = delta.total_seconds() / 3600

        cost = (ram / 1024) * uptime_hours * 0.05

        table.add_row([
            server.name,
            ram,
            round(uptime_hours, 2),
            round(cost, 2)
        ])

    print(table)

if __name__ == "__main__":
    main()
