DESCRIPTION = 'Independent cohort evidence synthesis'

"""Offline command-line interface with validated, non-overwriting outputs."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
import pandas as pd
from . import core


def main(argv=None):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    commands = parser.add_subparsers(dest='command', required=True)
    example = commands.add_parser('example', help='Run synthetic data, without network')
    example.add_argument('--output', type=Path, required=True)
    run = commands.add_parser('run', help='Analyze a CSV using the documented input schema')
    run.add_argument('--input', type=Path, required=True)
    run.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    output = args.output
    if output.exists():
        parser.error('Output already exists; choose a new directory')
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.athena-stage-', dir=output.parent) as tmp:
            args.output = Path(tmp)
            result = analyze(args)
            (args.output / 'result.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
            # Reserve exclusively only after all validation and serialization succeed.
            output.mkdir(exist_ok=False)
            for item in args.output.iterdir():
                shutil.move(str(item), output / item.name)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))
    return 0

def analyze(args):
    if args.command == 'example':
        frame = pd.DataFrame({'cohort': ['synthetic_a', 'synthetic_b', 'synthetic_c'],
            'endpoint': ['example_contrast'] * 3, 'unit': ['log_ratio'] * 3,
            'tissue': ['synthetic_csf'] * 3, 'effect': [.1, .2, .15], 'se': [.1, .1, .2]})
    else:
        frame = pd.read_csv(args.input, keep_default_na=False, dtype={'cohort': 'string', 'endpoint': 'string',
            'unit': 'string', 'tissue': 'string', 'independence_group': 'string'})
    return {'data_kind': 'synthetic' if args.command == 'example' else 'user_supplied',
            **core.pool_effects(frame)}
