import click
from pathlib import Path
import subprocess
import yaml
import attr
from typing import Optional, List, Dict


@attr.s(auto_attribs=True)
class ConfigServer:
    name: str
    ip_external: str
    ip: str = "10.10.0.1"
    subset: int = 24
    port: int = 51830


@attr.s(auto_attribs=True)
class ConfigClient:
    name: str
    ip: str
    port: Optional[int] = None


@attr.s(auto_attribs=True)
class Config:
    server: ConfigServer = attr.ib(converter=lambda v: ConfigServer(**v))
    hosts: List[ConfigClient] = attr.ib(
        converter=lambda v: [ConfigClient(**it) for it in v]
    )


@attr.s(auto_attribs=True)
class ConfigPrivkeys:
    privkeys: Dict[str, str] = attr.ib(default=attr.Factory(dict))


def parse_config(fn_yaml: Path) -> Config:
    config = yaml.safe_load(fn_yaml.read_text())
    return Config(**config)


def parse_config_privkeys(fn_yaml: Path) -> ConfigPrivkeys:
    if fn_yaml.exists():
        data = yaml.safe_load(fn_yaml.read_text())
        config = ConfigPrivkeys(**data)
    else:
        config = ConfigPrivkeys()
    return config


def write_config_privkeys(fn_yaml: Path, config: ConfigPrivkeys):
    data = attr.asdict(config)
    fn_yaml.write_text(yaml.safe_dump(data, sort_keys=True))
