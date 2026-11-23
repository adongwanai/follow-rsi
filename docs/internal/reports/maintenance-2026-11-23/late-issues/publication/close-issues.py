from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess,hashlib
from scripts.feed.storage import load_items
from scripts.feed.review import source_hash
R=Path.cwd();B=R/'build/maintenance-2026-11-23';L=B/'late-issues';D=R/'docs/internal/reports/maintenance-2026-11-23/late-issues';OUT=L/'final-issue-actions';OUT.mkdir(exist_ok=True);ENV={**os.environ,'GODEBUG':'http2client=0'};REPO='adongwanai/follow-rsi'
review=json.loads((L/'review-pr.json').read_text());pub=json.loads((L/'publication-pr.json').read_text());live=json.loads((B/'late-live-verification.json').read_text());assert live['online_verified'] and len(live['requests'])==40
items={x['id']:x for x in load_items(R)};primary={x['id']:x for x in json.loads((D/'primary-review.json').read_text())['items']};marker='<!-- follow-rsi-late-addendum-final-2026-11-23 -->';link=f'https://github.com/{REPO}/blob/main/docs/internal/reports/maintenance-2026-11-23/late-issues/'
def gh(*a):return subprocess.check_output(['gh',*a],text=True,env=ENV).strip()
def gj(*a):return json.loads(gh(*a))
actions=[]
for n,ident in [(160,'arxiv:2611.27285'),(162,'arxiv:2611.27110'),(163,'arxiv:2611.27006'),(60,None)]:
 issue=gj('api',f'repos/{REPO}/issues/{n}');pages=gj('api','--paginate','--slurp',f'repos/{REPO}/issues/{n}/comments?per_page=100');comments=[c for p in pages for c in p];(OUT/f'issue-{n}-before.json').write_text(json.dumps({'issue':issue,'comments':comments},ensure_ascii=False,indent=2)+'\n');assert issue['state']=='open'
 if ident:
  item=items[ident];r=primary[ident];assert source_hash(item)==r['source_hash']==item['review']['source_hash'];assert item['review']['github_pr']==review['number'];body=f"{marker}\n晚到条目 `{ident}` 已完成三轮来源与范围审核，真实日期审核 PR #{review['number']}，实际审核日 11/23；原发表日与版本日均为 11/20，未推断 HF 推荐日。审核来源哈希 `{r['source_hash']}`。\n\n{r['reason']}\n\n[主审和独立原文证据]({link}primary-review.json)，[数字及边界复核]({link}independent/final.json)。\n\n"
  if n in (160,162):body+=f"出版 PR #{pub['number']} 已合并，Pages部署成功，[11/20补刊](https://adongwanai.github.io/follow-rsi/daily/2026-11-20.html)及W47、Atom、归档和latest.json的公开字节已核验。本期11/20含10篇，W47含34篇日报条目；没有把晚到论文冒充11/23新论文。\n\n"
  if n==160:body+='范围纳入已完成，但本 issue 保持 open 以跟踪一个明确的数字缺口：原摘要“14 benchmarks / 6 single-degradation / 8 mixed-degradation scenarios”与正文枚举的数据集/场景映射尚未逐项核清。原摘要数字不改，公开摘要不复述该计数且标明待核。恢复条件是作者补充的具体混合场景清单、附录或可核验配置能映射这组数量；届时仅重审该数字，不重复全历史。不是实验复现。\n'
  elif n==162:body+='关闭已完成的候选提醒；保留远域负迁移、遗忘、底模及预算比较限制，不声称实验复现。\n'
  else:body+='按范围排除后关闭候选提醒。HTML 404 后已读官方 PDF，修改的是外部推断算法；如果新版本/实现证明研究代理自身 Harness 被反馈改写并保留，可按同一ID恢复。不是因存在模型训练而排除，也不声称已复现实验。\n'
 else:
  body=f"{marker}\n11/23初始公开快照后，GitHub监控另发现15条候选提醒，其中12条已与正式审核对账并逐项关闭；3个新稳定ID按官方原文补审：SIR-Agent、RemoteEvolver纳入11/20补刊，PhyRSI因外部科研算法产物边界排除。真实日期审核 #{review['number']}、出版 #{pub['number']} 均已合并并核验线上字节。\n\n合计新增规范记录237条 = 原批次234 + 晚到3；正式处理为27篇日报纳入、4篇历史补录、203条排除、3条具体待补。11/18、19、20补刊分别7、10、10篇，W47为34篇日报和33篇既有历史条目。初始快照与审查意见保持原样，晚到增量在[单独账本]({link}publication/backlog-overlay.json)关联。全历史覆盖9,295个稳定ID、2,459条规范记录，原2,096条版本任务和41条旧模型错误未丢弃或冒称解决。\n\n三条正式待补仍是EVA-RSI的实际外部Harness工件链、DailyBrick跨配置接受/激活/后续消费链、仅S2截断摘要综述的全文与专项范围证据。旧 #19、#20、#23、#30、#119、#128 继续保留各自外部证据条件；#160 另跟踪已纳入SIR-Agent的场景计数映射，未将未核数字写入公共摘要。\n\n[当日状态简报](https://adongwanai.github.io/follow-rsi/daily/2026-11-23.html)仍明确对应其真实采集快照；没有用旧论文填充当日。S2限流与全局质量评测未通过的原告警保留。新增付费模型请求0、生成token0。\n"
 p=OUT/f'issue-{n}-comment.md';p.write_text(body);existing=[c for c in comments if marker in c['body']];url=existing[-1]['html_url'] if existing else gh('issue','comment',str(n),'--repo',REPO,'--body-file',str(p))
 if n in (162,163):gh('issue','close',str(n),'--repo',REPO,'--reason','completed')
 after=gj('api',f'repos/{REPO}/issues/{n}');expected='closed' if n in (162,163) else 'open';assert after['state']==expected;(OUT/f'issue-{n}-after.json').write_text(json.dumps(after,ensure_ascii=False,indent=2)+'\n');a={'issue':n,'id':ident,'comment_url':url,'state_after':expected,'observed_at':datetime.now(timezone.utc).isoformat(),'comment_sha256':hashlib.sha256(p.read_bytes()).hexdigest()};actions.append(a);(OUT/'actions.json').write_text(json.dumps(actions,ensure_ascii=False,indent=2)+'\n');print(json.dumps(a),flush=True)
