import click
from pathlib import Path
import subprocess
import yaml


def gen_config_client(
    *,
    fn,
    client_ip,
    client_port,
    client_privkey,
    server_name,
    server_pubkey,
    server_wg_ip,
    server_ext_ip,
    server_ext_port,
    subset,
):
    return f"""

# save this file as
#> sudo cp {fn.name} /etc/wireguard/{server_name}.conf; sudo chmod 600 /etc/wireguard/{server_name}.conf
#
# test this connection with
#> sudo wg-quick up {server_name}; sudo wg; sudo wg-quick down {server_name}
#
# manage autostarts with
#> sudo systemctl enable wg-quick@{server_name}
#> sudo systemctl start wg-quick@{server_name}
#> sudo systemctl stop wg-quick@{server_name}
#> sudo systemctl disable wg-quick@{server_name}

[Interface]
Address = {client_ip}/{subset}
# SaveConfig = true
ListenPort = {client_port}
PrivateKey = {client_privkey}

# ec2-aisc-wg
[Peer]
PublicKey = {server_pubkey}
AllowedIPs = {server_wg_ip}/{subset}
Endpoint = {server_ext_ip}:{server_ext_port}
PersistentKeepalive = 25
"""


def gen_config_server(*, fn, name, wg_ip, ext_port, privkey, subset, clients):
    main = f"""

# save this file as
#> sudo cp {fn.name} /etc/wireguard/{name}.conf; sudo chmod 600 /etc/wireguard/{name}.conf
#
# test this connection with
#> sudo wg-quick up {name}; sudo wg; sudo wg-quick down {name}
#
# manage autostarts with
#> sudo systemctl enable wg-quick@{name}
#> sudo systemctl start wg-quick@{name}
#> sudo systemctl stop wg-quick@{name}
#> sudo systemctl disable wg-quick@{name}
#
# Assure that the server has ip forwarding enabled (see sysctl) and assure
# that the servers firewall allows accesses to udp port {ext_port}.



[Interface]
Address = {wg_ip}/{subset}
SaveConfig = false
ListenPort = {ext_port}
PrivateKey = {privkey}
"""
    clients_ = []
    for c_name, c_ip, c_pubkey in clients:
        clients_.append(
            f"""
[Peer]  # {c_name}
PublicKey = {c_pubkey}
AllowedIPs = {c_ip}/32
PersistentKeepalive = 25
"""
        )

    return main + "\n".join(clients_)
