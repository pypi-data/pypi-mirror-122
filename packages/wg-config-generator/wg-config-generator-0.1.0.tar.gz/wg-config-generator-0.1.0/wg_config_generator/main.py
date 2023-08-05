import click
from pathlib import Path
import subprocess
import yaml
from .config import parse_config, parse_config_privkeys, write_config_privkeys
from .tools import get_pubkey, gen_privkey
from .generator import gen_config_client, gen_config_server


@click.command()
@click.option("--config", default="config.yaml", help="configuration file")
@click.option("--privkeys", default="config.privkeys.yaml", help="private key file")
def main(config: str, privkeys: str):
    fn_config = Path(config)
    config_ = parse_config(fn_config)
    # print(config_)

    fn_config_privkeys = Path(privkeys)
    config_privkeys = parse_config_privkeys(fn_config_privkeys)

    def get_privkey(name):
        if name not in config_privkeys.privkeys:
            config_privkeys.privkeys[name] = gen_privkey()
        return config_privkeys.privkeys[name]

    server = config_.server
    hosts = config_.hosts

    server_privkey = get_privkey("server")
    server_pubkey = get_pubkey(server_privkey)

    fn = Path(f"build/{server.name}.server.{server.ip}.conf")
    fn.parent.mkdir(exist_ok=True, parents=True)
    fn.write_text(
        gen_config_server(
            fn=fn,
            name=server.name,
            wg_ip=server.ip,
            ext_port=server.port,
            privkey=server_privkey,
            clients=[(h.name, h.ip, get_pubkey(get_privkey(h.name))) for h in hosts],
            subset=server.subset,
        )
    )

    for h in hosts:
        port = h.port or server.port
        privkey = get_privkey(h.name)
        pubkey_ = get_pubkey(privkey)

        fn = Path(f"build/{server.name}.{h.name}.{h.ip}.conf")
        fn.parent.mkdir(exist_ok=True, parents=True)
        fn.write_text(
            gen_config_client(
                fn=fn,
                server_name=server.name,
                client_ip=h.ip,
                client_port=port,
                client_privkey=privkey,
                server_pubkey=server_pubkey,
                server_wg_ip=server.ip,
                server_ext_ip=server.ip_external,
                server_ext_port=server.port,
                subset=server.subset,
            )
        )

    write_config_privkeys(fn_config_privkeys, config_privkeys)


if __name__ == "__main__":
    main()
