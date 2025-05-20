#!/usr/bin/env python3

import openstack
import datetime
from prettytable import PrettyTable

def main():
    try:
        conn = openstack.connect()
    except Exception as e:
        print(f"[FATAL] Errore nella connessione a OpenStack: {e}")
        return

    table = PrettyTable()
    table.field_names = ["Nome VM", "RAM (MB)", "Uptime (ore)", "Costo stimato (€)"]

    try:
        servers = conn.compute.servers(details=True)
    except Exception as e:
        print(f"[FATAL] Impossibile recuperare le VM: {e}")
        return

    for server in servers:
        try:
            flavor_id = server.flavor.get('id')
            flavor = conn.compute.find_flavor(flavor_id, ignore_missing=False)
            ram = flavor.ram
        except Exception as e:
            print(f"[!] Errore nel recupero del flavor per la VM '{server.name}': {e}")
            continue

        uptime_hours = 0
        try:
            launched_at = server.launched_at
            if launched_at:
                if isinstance(launched_at, str):
                    launched_at = datetime.datetime.fromisoformat(launched_at.replace("Z", "+00:00"))
                if launched_at.tzinfo is None:
                    launched_at = launched_at.replace(tzinfo=datetime.timezone.utc)
                now = datetime.datetime.now(datetime.timezone.utc)
                delta = now - launched_at
                uptime_hours = delta.total_seconds() / 3600
        except Exception as e:
            print(f"[!] Errore nel calcolo uptime per '{server.name}': {e}")
            continue

        try:
            cost = (ram / 1024) * uptime_hours * 0.05  # 0.05 €/GB/h
            table.add_row([
                server.name,
                ram,
                round(uptime_hours, 2),
                round(cost, 2)
            ])
        except Exception as e:
            print(f"[!] Errore nel calcolo del costo per '{server.name}': {e}")
            continue

    print(table)

if __name__ == "__main__":
    main()
