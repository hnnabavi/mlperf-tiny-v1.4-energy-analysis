#!/usr/bin/env python3
"""Deterministic, standard-library-only provenance-aware audit of supplied MLPerf Tiny records.
This tool validates archival records; it is NOT an energy predictor or laboratory test.
Run: python validate_audit.py --input . --output generated
"""
import argparse,csv,json,math,statistics,pathlib,collections,hashlib

def read(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def write(p,rows,keys=None):
    rows=list(rows); keys=keys or list(rows[0]) if rows else (keys or [])
    with open(p,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys,extrasaction='ignore');w.writeheader();w.writerows(rows)

def metric_errors(row):
    typ=row['metric_class'];unit=row['unit']; v=float(row['metric_value'])
    errors=[]
    if typ not in ('energy_per_inference','streaming_average_system_power'):errors.append('UNKNOWN_METRIC')
    if typ=='energy_per_inference' and unit!='uJ/inference':errors.append('INVALID_ENERGY_UNIT')
    if typ=='streaming_average_system_power' and unit!='mW':errors.append('INVALID_POWER_UNIT')
    if not math.isfinite(v) or v <= 0:errors.append('NONPOSITIVE_OR_NONFINITE')
    if typ=='streaming_average_system_power' and row['task']!='SWW':errors.append('POWER_TASK_MISMATCH')
    if typ=='energy_per_inference' and row['task']=='SWW':errors.append('STREAMING_SEMANTIC_MISMATCH')
    return errors

def analyze(root,output):
    root=pathlib.Path(root);output=pathlib.Path(output);output.mkdir(parents=True,exist_ok=True)
    rows=read(root/'reported_88_cells.csv'); v14=read(root/'v14_nonstreaming_energy.csv'); sw=read(root/'v14_streaming_power.csv')
    ledger=read(root/'historical_source_ledger.csv'); matched=read(root/'matched_release_v13_v14.csv')
    decisions=read(root/'deadline_selection_stress.csv'); software=read(root/'software_configuration_holdout.csv')
    assert len(rows)==88 and len(v14)==37 and len(sw)==6 and len(ledger)==36
    findings=[];flags=collections.Counter()
    for i,r in enumerate(rows,1):
        e=metric_errors(r);e+=['EXACT_REUSE'] if r['duplicate_of'] else []
        e+=['UNAVAILABLE_OR_UNCHECKED'] if r['status']!='available' else []
        e+=['DIVISION_CONFLICT'] if r['division'].startswith('conflict') else []
        for issue in e:flags[issue]+=1
        findings.append({'row':i,'release':r['release'],'task':r['task'],'organization':r['organization'],
            'metric_class':r['metric_class'],'unit':r['unit'],'status':r['status'],
            'duplicate_of':r['duplicate_of'],'rules_triggered':'|'.join(e) or 'PASS',
            'source_url':r['source_url']})
    assert not any(metric_errors(r) for r in rows), 'Unexpected metric types or units'
    # Same bytes across archived releases: hash identity shows absence of NEW evidence, not independent re-measurement.
    by_sha=collections.defaultdict(list)
    for r in ledger:by_sha[r['energy_blob_sha']].append(r)
    sha_groups=[g for g in by_sha.values() if len(g)>1]
    assert len(sha_groups)==6 and all(len(g)==4 for g in sha_groups)
    lineage=[]
    for sha,g in sorted(by_sha.items()):
        lineage.append({'energy_blob_sha':sha,'published_release_count':len(g),'hardware':g[0]['hardware_identifier'],
            'task':g[0]['task'],'releases':';'.join(x['release'] for x in g),'exact_reuse':int(len(g)>1),
            'physical_independence_asserted':'NO'})
    # Algebraic demonstrations of comparability and ranking under a published "available" status filter.
    winners=[]
    for task in sorted({r['task'] for r in v14}):
        grp=[r for r in v14 if r['task']==task]
        allmin=min(grp,key=lambda x:float(x['metric_value']))
        eligible=[x for x in grp if x['status']=='available']
        avmin=min(eligible,key=lambda x:float(x['metric_value']))
        winners.append({'task':task,'all_records_n':len(grp),'available_records_n':len(eligible),
         'ungated_winner':allmin['config'],'ungated_winner_status':allmin['status'],
         'ungated_energy_uJ':allmin['metric_value'],'available_winner':avmin['config'],
         'available_energy_uJ':avmin['metric_value'],
         'winner_changes':int(allmin['config']!=avmin['config']),
         'available_to_ungated_min_energy_ratio':round(float(avmin['metric_value'])/float(allmin['metric_value']),5),
         'interpretation':'Comparison changes eligibility, NOT physical performance'})
    assert len(winners)==5
    # Source-based 1.2-1.3 descriptive medians, exactly deduplicating measured file identity for Syntiant.
    historic13=[r for r in rows if r['release'] in ('1.2','1.3') and r['metric_class']=='energy_per_inference']
    ded=[]
    for task in sorted({r['task'] for r in historic13}):
        g=[r for r in historic13 if r['task']==task]
        h=[r for r in g if not r['duplicate_of']]
        n=statistics.median(float(r['metric_value']) for r in g);d=statistics.median(float(r['metric_value']) for r in h)
        ded.append({'task':task,'reported_n':len(g),'retained_after_documented_reuse_n':len(h),
         'naive_median_uJ':round(n,6),'file_dedup_median_uJ':round(d,6),
         'naive_relative_difference_pct':round(100*(n/d-1),3)})
    shifts=[]
    for x in matched:
        e0,e1=float(x['v13_energy_uJ']),float(x['v14_energy_uJ'])
        t0,t1=float(x['v13_latency_ms']),float(x['v14_latency_ms'])
        computed=(e1/e0-1)*100
        assert abs(computed-float(x['energy_shift_pct']))<1e-8
        shifts.append({'hardware':x['device'],'task':x['task'],'energy_v13_uJ':e0,'energy_v14_uJ':e1,
         'energy_change_pct':round(computed,6),'latency_v13_ms':t0,'latency_v14_ms':t1,
         'latency_change_pct':round((t1/t0-1)*100,6),
         'same_blob':int(x['v13_energy_blob_sha']==x['v14_energy_blob_sha']),
         'energy_v13_src':x['energy_source_v13'],'energy_v14_src':x['energy_source_v14']})
    changed=sum(x['decision_matches'].lower()=='false' for x in decisions)
    guard_covered=sum(x['decision_matches'].lower()=='false' and x['guarded_v13_decision_1pct']=='ABSTAIN' for x in decisions)
    # Source-provided software pairs are *matched within source*, not per-chip DVFS tests.
    swstats=[]
    for x in software:
        ea,eb=float(x['energy_A_uJ']),float(x['energy_B_uJ']);la,lb=float(x['latency_A_ms']),float(x['latency_B_ms'])
        swstats.append({'submitter':x['submitter'],'task':x['task'],'board':x['board'],'config_A':x['configuration_A'],
         'config_B':x['configuration_B'],'energy_A_uJ':ea,'energy_B_uJ':eb,
         'energy_relative_shift_pct':round((eb/ea-1)*100,6),
         'latency_relative_shift_pct':round((lb/la-1)*100,6),
         'joint_inside_symmetric_10pct':int(abs(eb/ea-1)<=0.1 and abs(lb/la-1)<=0.1),
         'source_A':x['source_A'],'source_B':x['source_B']})
    summary={
      'total_source_rows':len(rows),'nonstream_energy_rows':sum(x['metric_class']=='energy_per_inference' for x in rows),
      'stream_average_power_rows':sum(x['metric_class']=='streaming_average_system_power' for x in rows),
      'v14_energy_rows':len(v14),'v14_streaming_power_rows':len(sw),
      'reused_records_v12_to_v13':sum(bool(x['duplicate_of']) for x in rows),
      'upper_bound_distinct_files_88':len(rows)-sum(bool(x['duplicate_of']) for x in rows),
      'historical_lineage_rows':len(ledger),'historical_distinct_energy_blobs':len(by_sha),
      'historical_reused_four_release_groups':len(sha_groups),
      'v14_ungated_vs_available_winner_changes':sum(x['winner_changes'] for x in winners),
      'v14_tasks_compared':len(winners),
      'v13_v14_matched_cases':len(shifts),
      'median_abs_energy_release_change_pct':statistics.median(abs(r['energy_change_pct']) for r in shifts),
      'median_abs_latency_release_change_pct':statistics.median(abs(r['latency_change_pct']) for r in shifts),
      'related_deadline_budget_scenarios':len(decisions),
      'release_selection_changes':changed,'changed_scenarios_caught_by_1pct_abstention':guard_covered,
      'software_configuration_pairs':len(software),
      'software_pairs_inside_joint_fixed10pct':sum(x['joint_inside_symmetric_10pct'] for x in swstats),
      'rule_trigger_counts':dict(flags),
      'scope':'archival secondary benchmarking; no new hardware measurements; correlated observations',
      'operational_claim':'No validated improvement in physical-deployment reliability'
    }
    for fn,data in [('type_and_eligibility_audit.csv',findings),('hash_lineage_audit.csv',lineage),
       ('status_filter_winners.csv',winners),('deduplication_ablation.csv',ded),('matched_release_recomputed.csv',shifts),
       ('software_configuration_stress.csv',swstats)]:write(output/fn,data)
    (output/'audit_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',default='.');p.add_argument('--output',default='generated');a=p.parse_args();analyze(a.input,a.output)
