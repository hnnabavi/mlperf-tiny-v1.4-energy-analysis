#!/usr/bin/env python3
"""Normalize user-supplied TinyML task-level records, without changing the frozen paper corpus.

This importer validates a *declared* physical quantity. It does not determine the
physical measurement boundary or authenticate a hardware experiment.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import sys

TASKS = {'AD','IC','IC2','KWS','VWW','SWW'}
ENERGY_TASKS = TASKS - {'SWW'}
METRICS = {'energy_per_inference': 'uJ/inference', 'streaming_average_system_power': 'mW'}
COLUMNS = ['release','task','configuration','metric_class','unit','value','status', 'source_url', 'source_hash']
ALLOWED_STATUS = {'available','preview','unchecked','unknown'}


def normalize(source, release, mapping=None):
    """Return typed records + validated diagnostics; raise ValueError for invalid rows."""
    mapping = mapping or {field: field for field in COLUMNS}
    source = Path(source)
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError('CSV file has no header')
        mandatory = ['task','configuration','metric_class','unit','value','status','source_url']
        missing = [f for f in mandatory if mapping.get(f, f) not in reader.fieldnames]
        if missing:
            raise ValueError('Missing required input columns: ' + ', '.join(missing))
        results = []
        seen_keys = set()
        for i, row in enumerate(reader, start=2):
            def get(field): return (row.get(mapping.get(field,field)) or '').strip()
            task = get('task').upper()
            kind, unit, status = get('metric_class'), get('unit'), get('status').lower()
            if task not in TASKS: raise ValueError(f'Line {i}: unknown task: {task!r}')
            if kind not in METRICS: raise ValueError(f'Line {i}: unknown metric_class: {kind!r}')
            if unit != METRICS[kind]: raise ValueError(f'Line {i}: incorrect unit for {kind}: {unit!r}')
            if task == 'SWW' and kind != 'streaming_average_system_power':
                raise ValueError(f'Line {i}: SWW requires streaming average-power records')
            if task != 'SWW' and kind != 'energy_per_inference':
                raise ValueError(f'Line {i}: non-streaming tasks require energy-per-inference records')
            if status not in ALLOWED_STATUS: raise ValueError(f'Line {i}: unrecognized status {status!r}')
            try: value = float(get('value'))
            except ValueError: raise ValueError(f'Line {i}: nonnumeric value') from None
            if not math.isfinite(value) or value <= 0: raise ValueError(f'Line {i}: value must be finite and positive')
            if not get('configuration') or not get('source_url'):
                raise ValueError(f'Line {i}: configuration and source_url are required')
            if get('release') and get('release') != release:
                raise ValueError(f'Line {i}: source release {get("release")!r} differs from requested {release!r}')
            key = (task, get('configuration'),kind)
            if key in seen_keys: raise ValueError(f'Line {i}: repeated configuration/task/metric key: {key}')
            seen_keys.add(key)
            results.append({'release':release,'task':task,'configuration':get('configuration'),
              'metric_class':kind,'unit':unit,'value':format(value,'.12g'),
              'status':status,'source_url':get('source_url'), 'source_hash':get('source_hash'),
              'source_hash_verified':'no', 'manual_measurement_boundary_review':'required'})
    return results


def main(args=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--release', required=True, help='Distinct release label, e.g. v1.5')
    parser.add_argument('--output', required=True)
    parser.add_argument('--map', help='Optional JSON map of canonical CSV column name to source name')
    arg = parser.parse_args(args)
    mapping = json.loads(Path(arg.map).read_text(encoding='utf-8')) if arg.map else None
    output = Path(arg.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    values = normalize(arg.input, arg.release, mapping)
    cols = COLUMNS + ['source_hash_verified','manual_measurement_boundary_review']
    with output.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=cols)
        writer.writeheader();writer.writerows(values)
    print(f'Validated {len(values)} records to {output}; physical boundary and source hashes are NOT independently verified')

if __name__=='__main__': main()
