from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path.cwd();D=R/'docs/internal/reports/maintenance-2026-11-18';B=R/'build/maintenance-2026-11-18';P=D/'primary-review'
snapshot=json.loads((R/'data/feed/raw/maintenance-2026-11-18/source-intake/all-source-snapshot.json').read_text());stamp=snapshot['generated_at']
shared_zh='11/18北京时间09:17–09:22实际尝试全部12路启用来源，严格窗口423次出现、388个稳定ID；窗口新增122条（103篇论文、19篇公告），另核实入库7个历史issue论文候选，总计新增129条（110篇论文、19篇公告），不是129篇已纳入论文。三路arXiv检索均成功返回窗口0条；五路RSS分别5、6、47、7、0条；13个GitHub仓库release检查成功、窗口0条。S2 citations保存277次窗口出现、246个ID，但46次请求含15次429且达到180秒截止；authors只有作者身份查询成功、论文遍历被6次429阻断，未访问覆盖仍unknown。'
shared_en='All 12 enabled sources were actually attempted on Nov 18 between 09:17 and 09:22 Asia/Shanghai. The strict source window contained 423 occurrences across 388 stable IDs and added 122 new records (103 papers and 19 posts). Seven historical issue paper candidates were separately verified and ingested, bringing total new records to 129 (110 papers and 19 posts), not 129 inclusions. Three arXiv queries returned zero window entries; the five RSS feeds returned 5, 6, 47, 7 and 0. Release checks succeeded for 13 GitHub repositories with no window releases. S2 citations retained 277 window occurrences across 246 IDs, but 46 requests included 15 rate limits and reached a 180-second cutoff. Author identity lookup succeeded but paper traversal was blocked by six rate limits; unvisited coverage remains unknown.'
reason17_zh='本期是延迟补发的采集与审核简报，实际审核日11/18，不冒称11/17准时完成。11/18复抓11/17完整HF推荐榜41篇，身份、推荐日期和稳定ID均已入库；三轮范围审查41篇均不符合本专题，故本期新增论文0篇。Sage的S1.5/S2.1称谓与SPILLWAY的版本数字冲突逐项保留；范围排除不等于已消除来源冲突。11/16晚到榜单已补齐40篇，并另按11/16推荐日出版。'+shared_zh
reason18_zh='截至该快照，HF11/18返回not_ready，available_through明确为11/17；这不等于空榜或所有来源没有更新。已同时复抓11/17全榜41篇与11/16全榜40篇，晚到成员和推荐日全部对账。'+shared_zh+'新增129个ID完成逐项范围意见：12个新纳入建议、112个排除、5个待补；其中ESI的主实验固定prompt/skill，SPG-Select缺实际采用技能的反馈修改链，ForgeSystem/RecurIR缺可核验Harness工件部署链，S2综述受429阻断。新的正例分别按11/16真实来源窗口或历史补录呈现，今日简报没有伪造新增论文。旧模型评测recall为0.892857、阈值0.90且评测不完整，告警保留；未重跑付费模型，工程测试不代替质量评测。'
reason17_en='This delayed collection and review bulletin was reviewed on Nov 18, not completed on Nov 17. A complete 41-paper HF board for Nov 17 was fetched on Nov 18 and reconciled by identity and recommendation date. Three-round scope review excludes all 41 from this topic, so this edition includes no new paper. The Sage S1.5/S2.1 naming conflict and the SPILLWAY version-number conflict remain recorded; scope exclusion does not resolve those source conflicts. The Nov 16 late board now contains 40 papers and is handled under its actual recommendation date. '+shared_en
reason18_en='At this snapshot, HF Nov 18 returned not_ready and explicitly reported available_through Nov 17. This is neither an empty board nor evidence that every source has no update. Complete Nov 17 (41 papers) and Nov 16 (40 papers) boards were also fetched, with all late members and recommendation dates reconciled. '+shared_en+'The 129 newly ingested identities have item-specific scope findings: 12 inclusion recommendations, 112 exclusions and five evidence deferrals. ESI keeps prompts and skills fixed in its principal experiment; SPG-Select lacks a bound feedback-to-deployed-skill change record; ForgeSystem and RecurIR lack a verifiable deployed Harness artifact chain; the S2 survey remains rate-limited. Positive papers are placed in the true Nov 16 source window or separately labelled historical additions, not presented as new papers in today\'s bulletin. The incomplete historical model evaluation remains at recall 0.892857 against threshold 0.90. Its warning is retained; no paid model evaluation was rerun and engineering tests are not quality evaluation.'
out=[]
for day,zh,en,status in [('2026-11-17',reason17_zh,reason17_en,'no_qualified_content'),('2026-11-18',reason18_zh,reason18_en,'hf_not_ready')]:
 out.append({'date':day,'reviewed_on':'2026-11-18','checked_at':stamp,'status':status,'reason_zh':zh,'reason_en':en,'observed_latest_successful_board':'2026-11-17','collection_report':'docs/internal/reports/maintenance-2026-11-18/source-intake/README.md','source_snapshot':'data/feed/raw/maintenance-2026-11-18/source-intake/all-source-snapshot.json','publication_boundary':'Draft until real date-specific review merge, publication PR, Pages deployment and live verification.','paid_generation_requests':0})
(P/'status-bulletins.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(P/'README.md').write_text('''# 11/18 三轮审查与补刊决策

原始来源、官方身份和日期在第一轮逐稳定 ID 对账；父审第二轮阅读全部逐项意见及正例/边界的原文方法与实验限制；独立子 agent 第三轮复核完整 HF 榜、其他新增项与关键历史记录。final-adjudication.json 保存逐项证据及未满足条件；原意见及后续 ESI、SPG-Select、WeVis 纠正全部保留。

129 个新增 ID 生效意见：12 个纳入建议、112 个排除、5 个待补。3 个旧 HF 成员分别为 MIRIX 首次出版、Mobile AI Factory 排除复用、Evidence-Governed Adoption 仅推荐日元数据回执；最后一项不重复出版，也不改写原批准的 source_hash。

11/16 补刊含 7 篇：2 个 HF 推荐项（其中 MIRIX 是此前发现的首次出版）和 5 篇真实其他来源窗口论文；reviewed_on 为11/18。11/17 与11/18 发布有实际采集和审核信息的简报，不冒充新增论文。6 项本次核实的较早论文及此前已批准未刊内容单列历史补录。原11/16已合并15行及证据unknown保持。当前文件只记录审查与出版草稿，真实日期PR、CI、合并、部署和线上回执另外保存。

旧全局模型质量告警保留，未降低阈值、未重跑付费模型、未把工程测试称为质量评测。没有实验复现或全表数字复算声明。
''')
print([(x['date'],x['status']) for x in out])
