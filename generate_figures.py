import csv,pathlib,matplotlib.pyplot as plt,numpy as np
p=pathlib.Path(__file__).resolve().parent
(p/'figures').mkdir(exist_ok=True)
rows=list(csv.DictReader(open(p/'generated/status_filter_winners.csv')))
fig,ax=plt.subplots(figsize=(7.2,3.3))
tasks=[r['task'] for r in rows];pos=np.arange(len(tasks)); a=[float(r['ungated_energy_uJ']) for r in rows]; b=[float(r['available_energy_uJ']) for r in rows]
ax.bar(pos-.19,a,.35,label='Lowest reported (includes preview)',color='#276A83')
ax.bar(pos+.19,b,.35,label='Lowest available',color='#B17B31')
ax.set_yscale('log');ax.set_ylabel('Energy per inference (uJ), log scale');ax.set_xticks(pos,tasks);ax.grid(axis='y',alpha=.23);ax.legend(frameon=False,ncol=2,fontsize=8,loc='upper left')
ax.set_title('Availability filtering changes five task-wise energy minima',fontsize=11,loc='left')
fig.tight_layout();fig.savefig(p/'figures/status_policy_ablation.png',dpi=210);plt.close(fig)
rows=list(csv.DictReader(open(p/'generated/deduplication_ablation.csv')))
fig,ax=plt.subplots(figsize=(7.2,3.1));tasks=[x['task'] for x in rows]; p2=np.arange(len(tasks)); vals=[float(x['naive_relative_difference_pct']) for x in rows];bars=ax.bar(p2,vals,color='#276A83')
ax.axhline(0,color='#666',lw=.7);ax.set_ylim(-36,5);ax.set_ylabel('Naive median vs deduplicated (%)');ax.set_xticks(p2,tasks);ax.grid(axis='y',alpha=.23)
for k,v in enumerate(vals):ax.text(k,v-2.2,f'{v:.1f}%',ha='center',fontsize=8)
ax.set_title('Repeated archival files distort cross-release descriptive medians',fontsize=11,loc='left');fig.tight_layout();fig.savefig(p/'figures/dedup_ablation.png',dpi=210);plt.close(fig)
