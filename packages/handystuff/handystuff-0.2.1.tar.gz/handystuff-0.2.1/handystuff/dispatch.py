import logging
import os
import subprocess
from collections.abc import Mapping
from enum import Enum
from typing import Dict, Any, List, Set

try:
    import click
except ImportError:
    raise ImportError("Install handystuff with dispatch options: \n\n pip install handystuff[dispatch]")
from dataclasses import dataclass, field, asdict, is_dataclass

import yaml
from handystuff.imports import construct, do_import
from handystuff.loaders import load_json, load_jsonnet
from handystuff.logs import setup_logging

setup_logging()
logger = logging.getLogger()


class Extension(Enum):
    Json = 'json'
    Python = 'py'
    Jsonnet = 'jsonnet'
    Yaml = 'yaml'

    @classmethod
    def from_str(cls, ext: str):
        for x in cls.__members__.values():
            if ext == x.value:
                return x
        raise ValueError(f"Unknown extension, {ext}")

    @classmethod
    def guess_extension(cls, path: str):
        return cls.from_str(os.path.splitext(path)[-1][1:])


DEFAULT_ORDER = ['env_vars', 'executable', "script", 'args', 'params']
PROTECTED = DEFAULT_ORDER + ['order']


@dataclass
class Parameters:
    script: str
    env_vars: Dict[str, Any] = field(default_factory=dict)
    args: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(init=False, default_factory=dict)
    executable: List[str] = field(default_factory=lambda: ['/usr/bin/env', 'python'])
    order: List[str] = field(default_factory=lambda: DEFAULT_ORDER)

    def __post_init__(self):
        new_params = [x for x in self.__dataclass_fields__.keys() if x not in PROTECTED]
        logger.debug(f"New params: {new_params}")
        for x in new_params:
            self.params[x] = getattr(self, x)

    @classmethod
    def from_kwargs(cls, **kwargs):
        logger.debug(kwargs)
        script = kwargs.pop('script')
        logger.debug(kwargs)
        p = Parameters(script=script)
        for k, v in kwargs.items():
            if k in PROTECTED:
                setattr(p, k, v)
            else:
                p.params[k] = v
        logger.debug(p)
        return p

    def __str__(self):
        return ' '.join(self.to_script())

    def to_script(self):
        return [z for k in self.order for z in unravel(getattr(self, k), k == 'env_vars')]

    def to_runable(self):
        return [z for k in self.order if k != 'env_vars' for z in unravel(getattr(self, k))]


def parse_config(config: str, overrides: Dict[str, Any], env_vars):
    extension = Extension.guess_extension(config)
    logger.debug(f"{extension.value} type detected!")
    if extension == Extension.Json:
        res = Parameters.from_kwargs(**{**load_json(config), **overrides})
    elif extension == Extension.Yaml:
        with open(config, 'r') as f:
            res = Parameters.from_kwargs(**{**yaml.safe_load(config), **overrides})
    elif extension == Extension.Jsonnet:
        res = Parameters.from_kwargs(**{**load_jsonnet(config), **overrides})
    elif extension == Extension.Python:
        config = os.path.relpath(config)
        config = config.replace('.py', '')
        if '..' in config:
            raise ValueError("No imports from higher-up packages possible (for now)!")
        if '.' in config:
            raise ValueError("Python config files can't have `.` in it!")
        config = config.replace('/', '.')
        imported_config = do_import('config', config)
        logger.info(imported_config)
        if isinstance(imported_config, Parameters):
            for k, v in overrides.items():
                imported_config.params[k] = v
                logger.debug(f"Overriding: {k} = {v}")
            res = imported_config
        elif isinstance(imported_config, Mapping):
            res = Parameters.from_kwargs(**{**dict(imported_config.items()), **overrides})
        elif is_dataclass(imported_config):
            res = Parameters.from_kwargs(**{**asdict(imported_config), **overrides})
        else:
            res = Parameters.from_kwargs(**{
                **{k: getattr(imported_config, k) for k in dir(imported_config) if not k.startswith('__')},
                **overrides
            })
    else:
        raise ValueError("This should never appear!")
    res.env_vars.update(env_vars)
    return res


def unravel(param, skip_minus=False):
    if isinstance(param, (list, set)):
        return list(param)
    if isinstance(param, dict):
        res = []
        for k, v in param.items():
            if skip_minus:
                res.append(f'{k}={v}')
            else:
                res.extend([f'--{k}', str(v)])
        return res
    else:
        return [param]


@click.command()
@click.argument('config', type=click.Path(exists=True, dir_okay=False))
@click.option('--overrides', type=str, default='')
@click.option('--run', is_flag=True, type=bool)
@click.option('--script', type=str, default=None)
@click.option('--log_under', type=str, default=None)
@click.option('--env_vars', type=str, default=dict())
def main(config, overrides, run, script, log_under, env_vars):
    overrides = dict(tuple(o.split('=')) for o in overrides.split(' ') if o)
    env_vars = dict(tuple(o.split('=')) for o in env_vars.split(' ') if o)
    logger.debug(f"Overrides: {overrides}")
    cfg = parse_config(config, overrides, env_vars)
    logger.debug(repr(cfg))
    click.secho(f"Command: {click.style(str(cfg), fg='blue')}")

    if script:
        with open(script, 'r') as f:
            script_content = f.read()
        cmd = [z for k in cfg.order for z in unravel(getattr(cfg, k), k == 'env_vars')]
    else:
        cmd = [z for k in cfg.order if k != 'env_vars' for z in unravel(getattr(cfg, k))]
    if log_under:
        with open(log_under, "w+") as f:
            click.echo(f"Logging under: {click.style(str(log_under), fg='blue')}")
            f.write(script_content.format(command=' '.join(cmd)))
    if run:
        if script:
            click.secho(f"Running script!", fg='green')
            script_executable = script_content.splitlines()[0].replace('#!', '').strip()

            p = subprocess.Popen([script_executable], stdin=subprocess.PIPE)
            p.communicate(bytes(script_content.format(command=' '.join(cmd)), 'utf-8'))
            p.wait()
        else:
            click.secho(f"Running command!", fg='green')
            p = subprocess.Popen(cmd, env={**os.environ, **cfg.env_vars})
            p.wait()


if __name__ == '__main__':
    main()
