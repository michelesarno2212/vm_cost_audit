#!/usr/bin/env python3

import openstack
import datetime
from prettytable import PrettyTable

def main():
    conn = openstack.connect()

    table = PrettyTable()
    table.field_names = ["Nome VM", "RAM (MB)", "Uptime (ore)", "Costo stimato (€)"]

    for server in conn.compute.servers(details=True):
        try:
            # Recupera il flavor anche se è un nome, non un ID numerico
            flavor_id = server.flavor['id']
            flavor = conn.compute.find_flavor(flavor_id, ignore_missing=False)
            ram = flavor.ram
        except Exception as e:
            print(f"[!] Errore nel recupero del flavor per la VM '{server.name}': {e}")
            continue

        # Calcolo uptime
        uptime_hours = 0
        try:
            if server.launched_at:
                launched_at = server.launched_at
                if isinstance(launched_at, str):
                    launched_at = datetime.datetime.fromisoformat(launched_at.replace("Z", "+00:00"))
                delta = datetime.datetime.now(datetime.timezone.utc) - launched_at
                uptime_hours = delta.total_seconds() / 3600
        except Exception as e:
            print(f"[!] Errore nel calcolo uptime per '{server.name}': {e}")
            continue

        # Calcolo costo: 0.05 €/GB/h
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
