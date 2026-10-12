#!/usr/bin/env python3
"""Deterministic audit of selected MLPerf Tiny reported-public-artifact tables.
Run: python audit_extension.py  [from this folder; no third party packages].
This script tests CSV arithmetic. It does NOT assert independent hardware measurements.
"""
from pathlib import Path
import csv, statistics
root=Path(__file__).resolve().parent

def load(name):
    with (root/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
R=load('duplicate_median_diagnostic.csv')
print('v1.2-v1.3 duplicate median sensitivity:')
for x in R:
    naive=float(x['naively_pooled_median_uJ']);dedup=float(x['deduplicated_median_uJ']);p=100*(naive/dedup-1)
    assert abs(p-float(x['naive_vs_deduplicated_pct']))<.002
    print(x['task'],round(p,3),'%')
P=load('matched_release_v13_v14.csv');assert len(P)==8
E=[];L=[]
for x in P:
    e=100*(float(x['v14_energy_uJ'])/float(x['v13_energy_uJ'])-1)
    l=100*(float(x['v14_latency_ms'])/float(x['v13_latency_ms'])-1)
    assert abs(e-float(x['energy_shift_pct']))<1e-5
    assert abs(l-float(x['latency_shift_pct']))<1e-5
    E.append(abs(e));L.append(abs(l))
print('Matched release pairs',len(P),'median |energy shift|',statistics.median(E),'median |latency shift|',statistics.median(L))
S=load('deadline_selection_stress.csv');assert len(S)==164
flips=[x for x in S if x['selected_v13']!=x['selected_v14']]
print('Related threshold cases',len(S),'selection changes',len(flips))
assert len(flips)==2
M=load('software_margin_stress.csv');print('Software margins [(method, joint coverage, n)]')
for x in M:print(x['method'],x['joint_covered'],x['n'])
print('PASS: arithmetic and row-count checks. This is not a fresh source-byte verification.')
