#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
D=pd.read_csv(DATA/'v14_nonstreaming_core.csv').rename(columns={'metric_value':'energy_uJ'})
S=pd.read_csv(DATA/'v14_streaming_core.csv')
TASKS=['AD','IC','IC2','KWS','VWW']

def pareto(df,x='latency_ms',y='energy_uJ'):
    a=df.reset_index(drop=True); keep=[]
    for i,r in a.iterrows():
        dom=((a[x]<=r[x])&(a[y]<=r[y])&((a[x]<r[x])|(a[y]<r[y]))).any()
        if not dom: keep.append(i)
    return a.loc[keep].sort_values(x)

def robustness_radius(df,x='latency_ms',y='energy_uJ'):
    a=df.reset_index(drop=True); out=[]
    for _,r in pareto(a,x,y).iterrows():
        best=1.0; challenger=''
        for _,b in a.iterrows():
            if b.config==r.config and b[x]==r[x] and b[y]==r[y]: continue
            ratios=(b[y]/r[y],b[x]/r[x])
            eps=max([0.0]+[(q-1)/(q+1) for q in ratios if q>1])
            if eps<best: best,challenger=eps,b.config
        out.append({'task':r.task,'config':r.config,'status':r.status,'robustness_radius_pct':100*best,'nearest_challenger':challenger})
    return out

summary=(D.groupby('task').agg(n=('energy_uJ','size'),min_energy_uJ=('energy_uJ','min'),median_energy_uJ=('energy_uJ','median'),max_energy_uJ=('energy_uJ','max'),min_latency_ms=('latency_ms','min'),max_latency_ms=('latency_ms','max')).reset_index())
summary['energy_span_x']=summary.max_energy_uJ/summary.min_energy_uJ
summary['latency_span_x']=summary.max_latency_ms/summary.min_latency_ms
summary.to_csv(OUT/'task_dispersion.csv',index=False)

pf=[]; rr=[]
for task in TASKS:
    g=D[D.task==task]
    for scope,gg in [('overall',g),('available_only',g[g.status=='available'])]:
        for _,r in pareto(gg).iterrows():
            pf.append({'task':task,'scope':scope,'config':r.config,'status':r.status,'latency_ms':r.latency_ms,'energy_uJ':r.energy_uJ})
        rr += [dict(x,scope=scope) for x in robustness_radius(gg)]
pd.DataFrame(pf).to_csv(OUT/'pareto_frontiers.csv',index=False)
pd.DataFrame(rr).to_csv(OUT/'pareto_robustness_radius.csv',index=False)

loo=[]; loorg=[]
for task in TASKS:
    g=D[D.task==task]; full=g.energy_uJ.max()/g.energy_uJ.min(); vals=[]
    for cfg in sorted(D.config.unique()):
        q=g[g.config!=cfg]
        if len(q)>=2: vals.append((cfg,q.energy_uJ.max()/q.energy_uJ.min()))
    cfg,span=min(vals,key=lambda z:z[1])
    loo.append({'task':task,'full_span_x':full,'smallest_leave_one_config_span_x':span,'configuration_removed':cfg})
    for org in sorted(D.organization.unique()):
        q=g[g.organization!=org]
        if len(q)>=2: loorg.append({'task':task,'organization_removed':org,'remaining_n':len(q),'residual_span_x':q.energy_uJ.max()/q.energy_uJ.min()})
pd.DataFrame(loo).to_csv(OUT/'leave_one_configuration_out.csv',index=False)
pd.DataFrame(loorg).to_csv(OUT/'leave_one_organization_out.csv',index=False)

sp=S.rename(columns={'period_ms':'x','avg_power_mW':'y'}).reset_index(drop=True); keep=[]
for i,r in sp.iterrows():
    dom=((sp.x<=r.x)&(sp.y<=r.y)&((sp.x<r.x)|(sp.y<r.y))).any()
    if not dom: keep.append(i)
sp.loc[keep,['config','status','x','y','duty_cycle_pct']].rename(columns={'x':'period_ms','y':'avg_power_mW'}).to_csv(OUT/'streaming_power_frontier.csv',index=False)
print('Reproduced task dispersion, Pareto frontiers, exact robustness radii, composition sensitivity, and streaming-power frontier.')
