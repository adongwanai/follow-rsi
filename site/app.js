'use strict';
const D = window.HARNESS_DATA;
const P = D.papers, BY = Object.fromEntries(P.map(p => [p.id, p])), S = D.meta.sections;
const CHECKS = ['held_out','matched_budget_baseline','cross_model_transfer','cost_reported','disjoint_evolution_set','reliability_metric','code_released','evolved_harness_released'];
const KEYS = CHECKS.slice(0,4), FIELDS = [...CHECKS,'who_edits','feedback','timing','topology'];
const LABELS = {
 held_out:['留出集','Held-out'],matched_budget_baseline:['同预算对照','Matched budget'],cross_model_transfer:['跨模型迁移','Cross-model'],cost_reported:['报告成本','Cost reported'],
 disjoint_evolution_set:['不相交演化集','Disjoint evolution set'],reliability_metric:['可靠性指标','Reliability metric'],code_released:['开源代码','Code released'],evolved_harness_released:['公开演化出的 Harness','Evolved harness released'],
 who_edits:['谁来改','Who edits'],feedback:['反馈来源','Feedback'],timing:['改进时机','Timing'],topology:['演化结构','Topology']
};
const VALUES = {chain:['链','Chain'],tree:['树','Tree'],graph:['图','Graph'],yes:['有','Yes'],partial:['部分','Partial'],no:['没有','No'],unknown:['未审','Unknown'],na:['不适用','N/A'],self:['自改','Self'],external:['他改','External'],trained:['训练出的改进者','Trained'],self_human_reviewed:['自改 · 人工审查','Self, human reviewed'],ground_truth:['真值验证','Ground truth'],proxy:['代理信号','Proxy'],self_generated_tests:['自生成测试','Self-generated tests'],demonstrations:['人类示范','Demonstrations'],self_judgment:['模型自评','Self-judgment'],offline:['离线','Offline'],online:['在线持续','Online'],test_time:['测试时','Test time'],during_run:['运行中','During run']};
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let lang=document.documentElement.dataset.lang, view='home', openId=null, lastFocus=null, drawerIds=[];
const state={q:'',sections:[],must:false,verify:false,reviewed:false,filters:{},sort:'must'};
const METHOD_SECTIONS=['evolve_main','generalize','evidence_selection','improver','component','coevolution'];
const SECTION_NAMES={evolve_main:['搜索与演化','Search & evolution'],generalize:['泛化与成本','Generalization & cost'],evidence_selection:['任务与证据','Tasks & evidence'],improver:['改进器进化','Evolving the improver'],component:['组件级进化','Components'],coevolution:['模型协同','Co-evolution'],foundations:['奠基','Foundations'],evaluation:['评测','Evaluation'],survey_theory:['综述与理论','Surveys & theory'],candidates:['候选','Candidates']};
const t=(zh,en)=>lang==='zh'?zh:en;
const localized=values=>values[lang==='zh'?0:1];
const mark=(p,k)=>`<span class="ev ${p.evidence[k]}" role="img" aria-label="${esc(localized(LABELS[k])+': '+localized(VALUES[p.evidence[k]]))}" title="${esc(localized(LABELS[k])+': '+localized(VALUES[p.evidence[k]]))}"></span>`;
const verify=p=>p.needs_reading?`<span class="tag verify">${t('待细读','Needs verification')}</span>`:'';
const isRecent=p=>D.stats.recent_ids.includes(p.id);
function chrome(){
 $('eyebrow').textContent=t('当前专题 · Harness 自进化','Current topic · Harness evolution');
 $('h1').innerHTML=t('每天 5 分钟，<br><em>跟上 RSI 前沿</em>','Five minutes a day to keep up with<br><em>recursive self-improvement.</em>');
 $('lede').textContent=t('RSI 论文每天都在冒，但不是每个「变强了」都经得起检验。Follow RSI 从 RSI 里进展最快的 Harness 自进化做起：每天替你读新论文，逐篇核验它的提升是真改进，还是过拟合和多花的算力。','New RSI papers appear every day, but not every claim of improvement stands up to scrutiny. Follow RSI starts with harness evolution, one of RSI’s fastest-moving areas: reading new papers for you and checking whether the gains reflect real improvement, overfitting, or extra compute.');
 const stats=D.stats;
 $('hda-copy').innerHTML=t('搜索集上的演化收益，平均 <b>54%</b> 来自过拟合，<b>14%</b> 来自多花的测试时算力','On average, <b>54%</b> of search-set gains come from overfitting; <b>14%</b> from extra test-time compute');
 $('audit-copy').innerHTML=t('声称改进了「改进流程」的论文里，只有 <b>4 篇</b>在同起点、同预算下做了前后代对比','Of papers claiming to improve the improvement process, only <b>4</b> compare generations with the same starting point and budget');
 $('today-link').textContent=t('看今日动态','Read today’s updates');
 $('guide-link').textContent=t('从导读开始 →','Start with the guide →');
 $('q').placeholder=t('搜索论文、机构、机制或数字','Search papers, organizations, mechanisms or numbers');$('q').setAttribute('aria-label',$('q').placeholder);
 $('filter-open').textContent=t('筛选','Filters');$('clear').textContent=t('清除筛选','Clear filters');
 $('sort-label').textContent=t('排序','Sort');$('sort').setAttribute('aria-label',t('排序','Sort'));
 [...$('sort').options].forEach(o=>o.textContent=({newest:t('最新在前','Newest first'),oldest:t('最早在前','Oldest first'),must:t('必读优先','Must-read first'),evidence:t('证据最全','Most recorded evidence')})[o.value]);
 $('sort').value=state.sort;
 $('toggles').innerHTML=[['must',t('必读','Must-read')],['reviewed',t('已有证据记录','Recorded evidence')],['verify',t('待细读','Needs verification')]].map(([k,l])=>`<button type="button" class="chip" data-toggle="${k}" aria-pressed="${state[k]}">${l}</button>`).join('');
 $('sections').innerHTML=[['all',t('全部','All')],...METHOD_SECTIONS.map(id=>[id,localized(SECTION_NAMES[id])])].map(([id,name])=>`<button type="button" class="chip" data-section="${id}" aria-pressed="${id==='all'?state.sections.length===0:state.sections.includes(id)}">${esc(name)}<span class="n">${id==='all'?stats.total:stats.sections[id]}</span></button>`).join('')+`<label class="other-sections"><span class="sr-only">${t('评测、综述、奠基或候选','Evaluation, surveys, foundations or candidates')}</span><select id="other-sections"><option value="">${t('评测 · 综述 · 奠基','Evaluation · surveys · foundations')}</option>${Object.keys(S).filter(id=>!METHOD_SECTIONS.includes(id)).map(id=>`<option value="${id}" ${state.sections.includes(id)?'selected':''}>${localized(SECTION_NAMES[id])} · ${stats.sections[id]}</option>`).join('')}</select></label>`;
 $('advanced-title').textContent=t('证据与分类筛选','Evidence and classification filters');
 $('filter-rules').textContent=t('同一维度内按或筛选，不同维度之间按且筛选。方向与快捷筛选显示全库篇数；证据选项按其余条件计算。','OR within a dimension; AND across dimensions. Directions and quick filters show library totals; evidence counts respect the other filters.');
 $('legend').innerHTML=['yes','partial','no','unknown'].map(v=>`<span><i class="ev ${v}" aria-hidden="true"></i>${localized(VALUES[v])}</span>`).join('')+`<span class="mono">${t('列顺序：留出集 · 同预算对照 · 跨模型迁移 · 报告成本','Order: held-out · budget · transfer · cost')}</span>`;
 $('footer').innerHTML=`<span>${t('数据截至','Data as of')} <span class="mono">${D.meta.as_of}</span> · ${t('已审表示有记录，不表示通过','Reviewed means recorded, not passed')}</span><span><a href="${esc(D.config.author_url)}">${esc(D.config.author_name)}</a> · <a href="${esc(D.config.repository_url)}">GitHub</a> · ${t('代码 MIT · 内容 CC BY 4.0','Code MIT · Content CC BY 4.0')}</span>`;
}
const ENUMS={who_edits:['self','external','trained','self_human_reviewed','unknown'],feedback:['ground_truth','proxy','self_generated_tests','demonstrations','self_judgment','unknown'],timing:['offline','online','test_time','during_run','unknown'],topology:['chain','tree','graph','unknown']};
const DEFINITIONS={
 held_out:['评测集在整个搜索过程中不可见；仅有用于选择候选的验证集不等同于留出评测。','The evaluation set stays hidden throughout search; a validation set used to select candidates is not the held-out evaluation.'],
 matched_budget_baseline:['与总推理预算相匹配的并行采样、顺序修正等测试时扩展比较；明确演化成本如何计入。','Compare against test-time scaling such as parallel sampling or sequential revision under matched inference budgets; state how evolution cost is counted.'],
 cross_model_transfer:['不重新演化，将同一 Harness 迁移到其他模型家族并评测。','Evaluate the same harness on other model families without re-evolution.'],
 cost_reported:['报告 token 或美元成本，并包含演化过程本身。','Report token or dollar costs, including the evolution process itself.'],
 disjoint_evolution_set:['演化任务与下游评测基准不相交。','Evolution tasks are disjoint from downstream evaluation benchmarks.'],
 reliability_metric:['重复运行并报告方差、Pass^k 等可靠性指标。','Repeat runs and report variance or reliability measures such as Pass^k.'],
 code_released:['公开支持复现方法的代码；不等于公开最终演化产物。','Release code supporting reproduction of the method; this is distinct from releasing the evolved artifact.'],
 evolved_harness_released:['公开最终演化出的 Harness，而不只是优化器代码。','Release the final evolved harness, beyond the optimizer code.'],
 who_edits:['self：任务 Agent 自改；external：独立改进者；trained：训练出的改进者；self_human_reviewed：自改并经人工审查。','self: task agent; external: a separate improver; trained: a trained improver; self_human_reviewed: self-edits with human review.'],
 feedback:['ground_truth：真值；proxy：代理信号；self_generated_tests：自生成测试；demonstrations：示范；self_judgment：自评。','ground_truth: reference answers; proxy: surrogate signal; self_generated_tests: generated tests; demonstrations: examples; self_judgment: self-assessment.'],
 timing:['offline：部署前离线；online：持续在线；test_time：测试时适配；during_run：单次运行中修改。','offline: before deployment; online: continual online updates; test_time: adaptation at test time; during_run: changes within a run.'],
 topology:['chain：顺序版本链；tree：分支谱系；graph：含合并或多父关系的图。缺少正文依据时保持 unknown。','chain: sequential versions; tree: branching lineages; graph: merges or multiple-parent relations. Keep unknown without a source.']
};
function passes(p,omit=null){
 if(omit!=='section'&&state.sections.length&&!state.sections.includes(p.section))return false;
 if(omit!=='must'&&state.must&&!p.must_read || omit!=='verify'&&state.verify&&!p.needs_reading)return false;
 if(omit!=='reviewed'&&state.reviewed&&!CHECKS.some(k=>p.evidence[k]!=='unknown'))return false;
 for(const [key,values] of Object.entries(state.filters))if(key!==omit&&values.length&&!values.includes(p.evidence[key]))return false;
 return !state.q||[p.title,p.id,p.arxiv,...(p.orgs||[]),...(p.tags||[]),p.summary_zh,p.result_zh,p.summary_en,p.result_en].join(' ').toLowerCase().includes(state.q);
}
function renderFacets(){
 const helpOpen=new Set([...document.querySelectorAll('[data-help][aria-expanded="true"]')].map(b=>b.dataset.help));
 $('facets').innerHTML=FIELDS.map(k=>{
  const available=P.filter(p=>passes(p,k)),values=ENUMS[k]||['yes','partial','no','unknown','na'];
  return `<div class="facet"><div class="facet-heading"><span>${localized(LABELS[k])}</span><button class="help" type="button" data-help="${k}" aria-label="${t('解释','Define ')}${localized(LABELS[k])}" aria-expanded="${helpOpen.has(k)}" aria-controls="help-${k}">?</button></div><p class="facet-help" id="help-${k}" ${helpOpen.has(k)?'':'hidden'}>${localized(DEFINITIONS[k])} ${t('unknown 表示未审，不等于 no；partial 表示部分支持，na 表示不适用。','Unknown is unreviewed, not no; partial is incomplete support, and na is not applicable.')}</p><div class="facet-values">${values.map(v=>`<button type="button" class="chip" data-field="${k}" data-value="${v}" aria-pressed="${(state.filters[k]||[]).includes(v)}">${localized(VALUES[v])}<span class="n">${available.filter(p=>p.evidence[k]===v).length}</span></button>`).join('')}</div></div>`;
 }).join('');
 document.querySelectorAll('[data-toggle]').forEach(b=>{const label=({must:t('必读','Must-read'),reviewed:t('已有证据记录','Recorded evidence'),verify:t('待细读','Needs verification')})[b.dataset.toggle];const count=P.filter(p=>b.dataset.toggle==='must'?p.must_read:b.dataset.toggle==='verify'?p.needs_reading:CHECKS.some(k=>p.evidence[k]!=='unknown')).length;b.innerHTML=label+`<span class="n">${count}</span>`;});
}
function chip(id,step=false,why=null){
 const p=BY[id];
 const role=why?.[lang];
 return `<button type="button" class="pchip" data-open="${id}"${role?` title="${esc(role)}" aria-label="${esc(p.short_title+' · '+role)}"`:''}>${step?`<span class="step">${step}.</span>`:''}${esc(p.short_title)}${verify(p)}${step?`<time datetime="${p.date}">${p.date}</time>`:''}</button>`;
}
function renderHome(main){
 const edition=D.latest_edition;
 const today=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Shanghai'});
 const editionDate=edition&&(edition.end||edition.date);
 const title=edition?(edition.kind==='retrospective'?edition['title_'+lang]:editionDate===today?t('今天新增','New today'):t('最近一期','Latest edition')):t('今日动态','Today');
 const latest=edition?`<ol class="home-papers">${edition.items.slice(0,5).map(item=>`<li><a class="home-paper-title" href="${esc(item.repo_id?'#p-'+item.repo_id:edition.url)}">${esc(item.short_title)}</a>${item.direction.harness_sub?`<span class="home-subdirection">${esc(S[item.direction.harness_sub][lang])}</span>`:''}<p>${esc(item['summary_'+lang])}</p></li>`).join('')}</ol>`:`<p class="empty">${t('还没有发布的今日动态。先从导读和证据库开始。','No daily edition has been published yet. Start with the guide and evidence library.')}</p>`;
 const months=Object.entries(D.stats.months), max=Math.max(...months.map(([,n])=>n),1);
 const description=months.map(([month,n])=>`${month}: ${n}`).join('; ');
 const entrances=[
  ['papers',t('证据库','Evidence library'),t(`${D.stats.scopes.core} 篇方法 · 必读 ${D.stats.must_read}`,`${D.stats.scopes.core} methods · ${D.stats.must_read} must-reads`),t('用留出集、同预算、跨模型和成本，逐篇检视改进证据。','Examine held-out evaluation, matched budgets, transfer and cost, paper by paper.')],
  ['routes',t('阅读路线','Reading routes'),t(`${D.routes.length} 条路线`,`${D.routes.length} routes`),t('从基础到实验设计，带着一个问题连续读下去。','Read from foundations to experiment design, guided by a concrete question.')],
  ['gaps',t('研究空白','Open problems'),t(`${D.gaps.length} 个问题`,`${D.gaps.length} questions`),t('沿着已有结果，找到下一步值得做的实验。','Follow the existing results to experiments worth doing next.')]
 ];
 main.innerHTML=`<section class="home-latest"><div class="home-section-heading"><h2>${esc(title)}${edition?` <time datetime="${editionDate}">${edition.kind==='retrospective'?edition.start+' — '+edition.end:editionDate}</time>`:''}</h2>${edition?`<a href="${esc(edition.url)}">${t(`全部 ${edition.items.length} 篇 →`,`All ${edition.items.length} papers →`)}</a>`:''}</div>${latest}</section><section class="home-entrances" aria-label="${t('开始探索','Explore')}">${entrances.map(([id,name,count,copy])=>`<a href="#${id}" class="home-entrance"><span class="entrance-name">${name} <span aria-hidden="true">↗</span></span><strong>${count}</strong><p>${copy}</p></a>`).join('')}</section><section class="home-trend"><div class="home-section-heading"><h2>${t('发表趋势','Publication trend')}</h2><span class="mono note">2026.03–10</span></div><div class="trend" role="img" aria-label="${esc(description)}">${months.map(([month,n])=>`<span class="trend-item" aria-hidden="true"><span>${n}</span><span class="trend-bar" style="height:${n/max*90}px"></span><span>${month.slice(5)}</span></span>`).join('')}</div><p class="note">${t('按证据库正式收录论文的原始发表月份统计。','By original publication month of papers included in the evidence library.')}</p></section><p class="home-upcoming">${t('即将推出 Follow RSI Skill：在 Claude Code / OpenClaw 按子方向订阅。','Coming soon: Follow RSI Skill, with subdirection subscriptions in Claude Code / OpenClaw.')}${D.config.discussions_enabled?` <a href="${esc(D.config.repository_url)}/discussions">${t('下一个专题由读者投票 →','Vote for the next topic →')}</a>`:''}</p>`;
}
function matching(){
 const recorded=p=>CHECKS.filter(k=>p.evidence[k]!=='unknown').length;
 const order=Object.keys(S),support=p=>['background','general_rsi'].includes(p.scope);
 return P.filter(p=>passes(p)).sort((a,b)=>order.indexOf(a.section)-order.indexOf(b.section)||(a.section!=='foundations'&&a.section!=='candidates'?Number(support(a))-Number(support(b)):0)||(state.sort==='must'?Number(!!b.must_read)-Number(!!a.must_read):state.sort==='evidence'?recorded(b)-recorded(a):0)||(state.sort==='oldest'?a.date.localeCompare(b.date):b.date.localeCompare(a.date))||a.id.localeCompare(b.id));
}
function row(p){
 return `<button class="row" type="button" data-open="${p.id}"><span class="date">${p.date}</span><span class="body"><span class="t">${esc(p.short_title)}${p.must_read?`<span class="tag must">${t('必读','MUST READ')}</span>`:''}${verify(p)}${isRecent(p)?'<span class="tag new">NEW</span>':''}</span>${p.title!==p.short_title?`<span class="full">${esc(p.title)}</span>`:''}${p.orgs?`<span class="o">${esc(p.orgs.join(' · '))}</span>`:''}<span class="s">${esc(p['summary_'+lang])}</span></span><span class="marks">${KEYS.every(k=>p.evidence[k]==='unknown')?`<span class="evidence-pending">${t('证据待核','Evidence pending')}</span>`:KEYS.map(k=>mark(p,k)).join('')}</span></button>`;
}
function render(){
 $('home-hero').hidden=view!=='home';
 $('bar').hidden=view!=='papers';
 $('page-heading').hidden=view==='home';
 window.FollowRSIHeader.setActive(view);
 const headings={
  papers:[t('证据库','Evidence library'),t('每一篇论文，都要拿出凭证。按方向浏览，再核对留出集、预算、迁移与成本。','Every paper must show the evidence. Browse by direction, then inspect held-out evaluation, budget, transfer and cost.')],
  routes:[t('阅读路线','Reading routes'),t('新手先走「打基础」和「实验设计」两条，再按方向选一条。','New readers: start with Foundations and Experimental design, then choose a route for your interests.')],
  gaps:[t('研究空白','Open problems'),t('每一条都以收录论文为证据。适合给自己的论文找切入点。','Each question is grounded in the collection. Find a starting point for your research.')],
  map:[t('方向图','Research map'),t('按每一轮被改进并带入下一轮的对象划分。Harness 是当前专题。','Organized by the object improved and carried into the next round. Harness is the current topic.')]
 };
 if(view!=='home')$('page-heading').innerHTML=`<h1 class="page-h">${headings[view][0]}</h1><p class="page-sub">${headings[view][1]}</p>`;
 const main=$('content');
 if(view==='home'){renderHome(main);return;}
 if(view==='map'){renderMap(main);return;}
 if(view==='routes'){
  main.innerHTML=`<div class="routes">${D.routes.map(r=>`<article class="route" data-reading-order="${r.papers.join(' ')}"><h2>${esc(r['name_'+lang])}</h2><p class="route-load">${t(`${r.papers.length} 篇 · 约 ${r.papers.length*.75} 小时`,`${r.papers.length} papers · about ${r.papers.length*.75} hours`)}</p><p><strong>${t('读完能回答：','After reading: ')}</strong>${esc(r['question_'+lang])}</p><div class="chain">${r.papers.map((id,i)=>chip(id,i+1,r.why?.[id])).join('<span class="arr" aria-hidden="true">→</span>')}</div></article>`).join('')}</div>`;return;
 }
 if(view==='gaps'){
  const inline=s=>esc(s).replace(/\[([^\]]+)\]\(\.\.\/papers\/([a-z0-9-]+)\.md\)/g,'<a href="#p-$2">$1</a>');
  main.innerHTML=`<div class="gaps">${D.gaps.map(g=>`<article class="gap"><h2>${esc(g['title_'+lang])}</h2><div><p>${inline(g['text_'+lang])}</p><div class="chain">${g.refs.map(id=>chip(id)).join('')}</div>${g['experiment_'+lang]?`<p class="gap-experiment"><strong>${t('可以从这个实验开始：','Start with this experiment: ')}</strong>${esc(g['experiment_'+lang])}</p>`:''}${D.config.discussions_enabled?`<p class="discussion-link"><a href="${esc(D.config.repository_url)}/discussions">${t('去 GitHub Discussions 讨论 →','Discuss on GitHub →')}</a></p>`:''}</div></article>`).join('')}</div>`;return;
 }
 const list=matching();renderFacets();
 const included=list.filter(p=>p.status!=='candidate').length,candidates=list.length-included;
 $('result-count').textContent=t(`显示 ${included} / ${D.stats.included} 篇 · 候选 ${candidates} / ${D.stats.candidates}`,`Showing ${included} / ${D.stats.included} papers · candidates ${candidates} / ${D.stats.candidates}`);
 const groups=Object.keys(S).map(section=>[section,list.filter(p=>p.section===section)]).filter(([,papers])=>papers.length);
 main.innerHTML=(list.length?groups.map(([s,papers])=>{
  const expanded=Boolean(state.q)||state.sections.includes(s);
  const supporting=papers.filter(p=>['background','general_rsi'].includes(p.scope));
  const primary=papers.filter(p=>!['background','general_rsi'].includes(p.scope));
  const rows=items=>`<div class="rows">${items.map(row).join('')}</div>`;
  const sub=`<div class="gsub"><span>${esc(S[s][lang==='zh'?'en':'zh'])}</span><span>${papers.length} ${t('篇','papers')}</span></div>`;
  if(['foundations','candidates'].includes(s))return `<details class="group ${s}" data-section-id="${s}" ${expanded?'open':''}><summary class="group-head">${esc(S[s][lang])}<span class="note">${papers.length} ${t('篇','papers')}</span></summary>${sub}${rows(papers)}</details>`;
  const support=supporting.length?`<details class="supporting-papers" ${expanded?'open':''}><summary>${t('背景与通用 RSI','Background & general RSI')} <span class="mono">${supporting.length}</span></summary>${rows(supporting)}</details>`:'';
  return `<section class="group" data-section-id="${s}"><h2>${esc(S[s][lang])}</h2>${sub}${primary.length?rows(primary):''}${support}</section>`;
 }).join(''):`<p class="empty">${t('没有符合条件的论文。试试清除筛选，或换个关键词。','No papers match. Clear the filters or try another search.')}</p>`)+`<section class="verification-progress"><h2>${t('核验进度','Verification progress')}</h2><p>${t(`必读 ${D.stats.must_read} 篇：已核 ${D.stats.must_read_fully_reviewed} / ${D.stats.must_read}`,`Must-read papers: ${D.stats.must_read_fully_reviewed} / ${D.stats.must_read} fully reviewed`)}</p><p class="note">${t('全文核验完成才计入；已有证据字段记录不代表整篇核验完成。','Counted only after full-paper verification. Recorded evidence fields do not imply a completed full-paper review.')}</p></section>`;
}

function renderMap(main){
 const examples=items=>`<div class="map-examples">${items.map(([label,id])=>id?`<button type="button" data-open="${id}">${esc(label)}</button>`:`<span>${esc(label)}</span>`).join('<span class="map-separator" aria-hidden="true">·</span>')}</div>`;
 const tile=(title,description,works=[],extra='')=>`<article class="map-tile ${extra}"><h4>${title}</h4>${description?`<p>${description}</p>`:''}${works.length?examples(works):''}</article>`;
 const planned=[
  ['model_weights',t('模型 / 权重 RSI','Model-weight RSI'),t('模型用自己产生的数据训练自己','Models train on their own data'),[['RSIPO'],['Terminal-RSI'],['RISE']]],
  ['data_task',t('数据与任务 RSI','Data & task RSI'),t('数据配比 · 任务与课程 · 环境','Data mixtures · curricula · environments'),[['NeoHorse-1'],['ClawLoop']]],
  ['ai4ai',t('训练算法 / AI 研发','AI-for-AI RSI'),t('训练算法 · 模型研发 · 研究流程','Training algorithms · R&D · research'),[['Frontis-MA1'],['SwarmRSI']]],
  ['experience_world_model',t('经验与世界模型','Experience & world models'),t('记忆 · 规则手册 · 世界模型 · 探索','Memory · rulebooks · world models · exploration'),[['Memento 3'],['RSIAgent']]],
  ['meta',t('元 RSI','Meta-level RSI'),t('改进「负责改进的机制」本身','Improving the improver itself'),[['Hyperagents','hyperagents'],['Meta^n','meta-n'],['HSI','hsi']]],
  ['embodied',t('具身与物理 RSI','Embodied RSI'),t('机器人在仿真或真机中递归改进','Robots improving in sim or reality'),[['EMHO','emho'],['Physical RSI']]]
 ];
 const subdirections=[
  ['evolve_main',t('整体 Harness 搜索与演化','Harness search & evolution')],
  ['generalize',t('泛化、正则、准入与成本','Generalization, admission & cost')],
  ['evidence_selection',t('任务与证据选择','Task & evidence selection')],
  ['improver',t('改进器自身进化','Evolving the improver')],
  ['component',t('组件级进化','Component-level evolution')],
  ['coevolution',t('模型与 Harness 协同','Model–harness co-evolution')]
 ];
 const section=(id,title,description,columns,content)=>`<section class="map-section" data-map-row="${id}"><div class="map-section-heading"><h3>${title}</h3><p>${description}</p></div><div class="map-grid map-cols-${columns}">${content}</div></section>`;
 const harness=`<article class="map-tile map-focus"><div class="map-focus-heading"><h4><button type="button" class="map-title-button" data-map-section="">${t('Harness / 脚手架 RSI','Harness / scaffold RSI')}</button></h4><button type="button" class="map-count" data-map-section="">${t('当前专题','Current topic')} · <b data-map-total>${D.stats.scopes.core+D.stats.scopes.harness_eval}</b> ${t('篇','papers')} →</button></div><p>${t('提示 · 工具 · 记忆 · 技能 · 控制流 · 改进器本身','Prompts · tools · memory · skills · control flow · the improver')}</p>${examples([['AHE','ahe'],['Self-Harness','self-harness'],['DarwinX','darwinx'],['RRSI','rrsi'],['AIDE²','aide2']])}<div class="map-subdirections">${subdirections.map(([id,label])=>`<button type="button" data-map-section="${id}"><span>${label}</span><b class="mono">${D.stats.sections[id]}</b></button>`).join('')}</div><p class="map-count-note">${t(`${D.stats.scopes.core} 篇方法 · ${D.stats.scopes.harness_eval} 篇 Harness 评测与理论 · ${D.stats.scopes.background+D.stats.scopes.general_rsi} 篇背景与通用 RSI；共 ${D.stats.included} 篇。子方向数字按目录分类计数，包含分类待复核的背景条目。`,`${D.stats.scopes.core} methods · ${D.stats.scopes.harness_eval} harness evaluations and theory · ${D.stats.scopes.background+D.stats.scopes.general_rsi} background and general RSI; ${D.stats.included} papers in total. Subdirection counts follow catalog sections, including background entries whose classification is under review.`)}</p></article>`;
 const directions=harness+planned.map(([id,title,description,works])=>`<article class="map-tile map-planned" ${D.config.discussions_enabled?`data-map-plan="${id}"`:""}><h4>${D.config.discussions_enabled?`<button type="button" class="map-title-button">${title}</button>`:title}</h4><p>${description}</p>${examples(works)}<span class="map-status">${D.config.discussions_enabled?t('规划中 · 参与投票 →','Planned · vote for the next topic →'):t('专题规划中','Topic planned')}</span></article>`).join('');
 const cooperation=[
  tile(t('单层改进','Single-layer'),t('只改一类对象','One kind of object'),[[t('大多数工作','Most work')]]),
  tile(t('模型与 Harness 协同','Model–harness co-evolution'),t('Harness 与权重交替或联合更新','Harness and weights updated together'),[['HarnessX','harnessx'],['Self-HPO','self-hpo'],['CoEvo-RSI','coevo-rsi']]),
  tile(t('多层统一框架','Unified multi-layer'),t('模型、数据、Harness 统一调度','Model, data and harness scheduled jointly'),[['MetaRSI / RSI²','metarsi']])
 ].join('');
 const applications=[
  [t('编码与终端','Coding & terminal'),[['DGM','dgm'],['Ouroboros','ouroboros']]],
  [t('AI 研究与 MLE','AI research & MLE'),[['AIDE²','aide2'],['RHI','rhi']]],
  [t('科学发现','Scientific discovery'),[['SwarmRSI'],['ScienceBuddy']]],
  [t('企业流程','Enterprise workflows'),[['StarHarness','starharness'],['OO-Harness','oo-harness']]],
  [t('电脑操作','Computer use'),[['Agent S4','agent-s4'],['PILOT','pilot']]]
 ].map(([title,works])=>tile(title,'',works)).join('');
 const support=[
  [t('评测与基准','Benchmarks'),[['Evo-Bench','evo-bench'],['RSIGym','rsigym']]],
  [t('归因与可信度','Attribution & trust'),[['HDA','hda'],['Auditing','auditing-product']]],
  [t('理论与综述','Theory & surveys'),[['Self-Evolving Agent Harness','self-evolving-agent-harness']]],
  [t('安全与治理','Safety & governance'),[['Trusting Trust','trusting-trust-revisited']]]
 ].map(([title,works])=>tile(title,'',works)).join('');
 const cross=[
  [t('谁来改','Who edits'),t('自改 · 他改 · 训练出的改进者','self · external · trained')],
  [t('反馈来源','Feedback'),t('真值 · 代理信号 · 自评','ground truth · proxy · self')],
  [t('递归深度','Recursion depth'),'L1–L5'],
  [t('改进时机','Timing'),t('离线 · 在线 · 测试时','offline · online · test time')],
  [t('证据强度','Evidence'),t('留出集 · 同预算 · 跨模型','held-out · budget · transfer')]
 ].map(([title,description])=>tile(title,description,[],'map-cross')).join('');
 main.innerHTML=`${section('objects',t('改进对象','What improves'),t('主轴：每一轮被改进、并带入下一轮的对象','Main axis: the object improved and carried into the next round'),4,directions)}${D.config.discussions_enabled?`<aside class="map-vote" id="map-vote" hidden tabindex="-1" role="status"><p>${t('下一个专题由读者投票决定','Readers vote to choose the next topic')}</p><a href="${esc(D.config.repository_url.replace(/\/$/,''))}/discussions" target="_blank" rel="noopener">${t('去 GitHub Discussions 投票与讨论 →','Vote and discuss on GitHub Discussions →')}</a></aside>`:''}${section('cooperation',t('协同方式','How they combine'),t('一次改一类对象，还是多类一起改','One kind of object, or several at once'),3,cooperation)}${section('applications',t('应用场景','Where'),t('在哪里自我改进','Where self-improvement happens'),5,applications)}${section('support',t('支撑方向','Support'),t('怎么衡量、怎么解释、怎么管住','How it is measured, explained and governed'),4,support)}${section('cross',t('横切维度','Cross-cutting'),t('给自己的论文定位','Dimensions for positioning your own paper'),5,cross)}<p class="note map-foot"><span>${t('带下划线的可点开证据卡。','Underlined works open evidence cards.')}</span><a href="${esc(D.config.repository_url.replace(/\/$/,''))}/blob/main/assets/rsi-map-${lang==='zh'?'zh-':''}light.svg">${t('打开原始 SVG 方向图','Open the original SVG research map')}</a></p>`;
}

function paperLinks(p){
 const links=[];
 if(p.arxiv){links.push(['arXiv '+p.arxiv,'https://arxiv.org/abs/'+p.arxiv]);if(!p.arxiv.startsWith('cs/'))links.push(['HF Papers','https://huggingface.co/papers/'+p.arxiv]);}
 if(p.url)links.push([t('项目页','Website'),p.url]);if(p.code)links.push([t('代码','Code'),p.code]);if(p.note_url)links.push([t('精读笔记 →','Reading notes →'),p.note_url]);
 return links.map(([label,url])=>`<a href="${esc(url)}" target="_blank" rel="noopener">${esc(label)}</a>`).join('');
}
function sequence(){return drawerIds.map(id=>BY[id]);}
function updateHash(hash,replace=false){
 if(location.hash==='#'+hash)return;
 try{history[replace?'replaceState':'pushState'](null,'','#'+hash);}catch(error){if(error.name!=='SecurityError')throw error;}
}
function showView(next,updateUrl=true){
 if(openId)closeDrawer(false);
 view=next;render();
 if(updateUrl)updateHash(viewHash());
 window.scrollTo({top:0,behavior:'instant'});
}
function viewHash(){return view==='papers'&&state.sections.length?'papers?section='+state.sections.join(','):view;}
function showPaper(id,updateUrl=true,readingOrder=null){openDrawer(id,readingOrder);if(updateUrl)updateHash('p-'+id);}
function shareUrl(id){
 const base=D.config.base_url||(/^https?:$/.test(location.protocol)?new URL('.',location.href).href:null);
 if(!base)return null;
 try{const url=new URL('p/'+id+'.html',base.replace(/\/$/,'')+'/');return /^https?:$/.test(url.protocol)?url.href:null;}
 catch(error){if(!(error instanceof TypeError))throw error;return null;}
}
function openDrawer(id,readingOrder=null){
 if(!BY[id]){closeDrawer(false);$('content').innerHTML=`<p class="empty">${t('没有找到这篇论文。','Paper not found.')}</p>`;return;}
 if(!openId)lastFocus=document.activeElement;
 if(readingOrder)drawerIds=readingOrder;
 else if(!openId||!drawerIds.includes(id)){const list=matching();drawerIds=(list.some(p=>p.id===id)?list:P.filter(p=>p.section===BY[id].section).sort((a,b)=>b.date.localeCompare(a.date))).map(p=>p.id);}
 openId=id;const p=BY[id],known=FIELDS.filter(k=>p.evidence[k]!=='unknown'),unknown=FIELDS.filter(k=>p.evidence[k]==='unknown');
 const list=sequence(),index=list.findIndex(x=>x.id===id),routes=D.routes.filter(r=>r.papers.includes(id)),related=P.filter(x=>x.section===p.section&&x.id!==id).sort((a,b)=>b.date.localeCompare(a.date)).slice(0,4);
 $('drawer').innerHTML=`<div class="dhead"><span class="mono note">${esc(S[p.section][lang])}</span><button class="iconbtn" type="button" id="dclose">${t('关闭','Close')} Esc</button></div><article class="receipt">${p.must_read?'<span class="stamp">MUST READ</span>':''}<div class="sec">${p.date}${p.orgs?' · '+esc(p.orgs.join(' · ')):''}</div><h2 id="dtitle">${esc(p.title)}</h2><div class="links">${paperLinks(p)}</div>${verify(p)}${p.status==='candidate'?`<span class="tag verify">${t('候选','Candidate')}</span>`:''}<div class="block"><h4>${t('一句话','Summary')}</h4><p>${esc(p['summary_'+lang])}</p></div>${p['result_'+lang]?`<div class="block"><h4>${t('关键结果','Key result')}</h4><p>${esc(p['result_'+lang])}</p></div>`:''}${lang==='en'?'<p class="note">Machine translation of the curated Chinese text.</p>':''}${known.length?`<dl class="kv">${known.map(k=>`<dt>${localized(LABELS[k])}</dt><dd>${localized(VALUES[p.evidence[k]])}${CHECKS.includes(k)?mark(p,k):''}</dd>`).join('')}</dl>`:''}${unknown.length?`<details class="unreviewed"><summary>${t(`另有 ${unknown.length} 项未审`,`${unknown.length} other fields not yet reviewed`)}</summary><ul>${unknown.map(k=>`<li>${localized(LABELS[k])}</li>`).join('')}</ul></details>`:''}${p.needs_review?`<p class="review-suggestion note"><strong>${t('分类待复核','Classification under review')}</strong>${p['review_suggestion_'+lang]?' · '+esc(p['review_suggestion_'+lang]):''}</p>`:''}${p.bibtex?`<div class="copyrow"><button class="iconbtn" type="button" id="copy-bibtex">${t('复制 BibTeX','Copy BibTeX')}</button><span class="note" id="bibtex-msg" role="status"></span></div><pre id="bibtex-text" class="bibtex" hidden>${esc(p.bibtex)}</pre>`:''}</article><div class="receipt-nav"><button type="button" class="iconbtn" id="prev" ${index===0?'disabled':''}>← ${t('上一篇','Previous')}</button><button type="button" class="iconbtn" id="next" ${index===list.length-1?'disabled':''}>${t('下一篇','Next')} →</button></div><section class="related"><h3>${t('出现在哪些阅读路线','Reading routes featuring this paper')}</h3>${routes.length?routes.map(r=>`<p class="note">${esc(r['name_'+lang])}${r.why?.[id]?.[lang]?' · '+esc(r.why[id][lang]):''}</p><div class="chain" data-reading-order="${r.papers.join(' ')}">${r.papers.map((rid,i)=>chip(rid,i+1,r.why?.[rid])).join('')}</div>`).join(''):`<p class="note">${t('尚未编入阅读路线。','Not assigned to a reading route.')}</p>`}<h3>${t('同方向的相关论文','More in this direction')}</h3><div class="chain">${related.map(x=>chip(x.id)).join('')}</div></section><div class="sharewrap"><h4>${t('分享卡片','Share card')}</h4><img class="sharepreview" src="cards/${id}.png" alt="${esc(p.title)} · ${t('分享卡片','share card')}${p.needs_reading?' · 待细读 / Needs verification':''}" width="1080" height="1350" loading="lazy"><div class="copyrow"><button class="btn" type="button" id="copy">${t('复制链接','Copy link')}</button><a class="btn" href="cards/${id}.png" download="${id}.png">${t('下载分享卡片','Download card')}</a></div><p class="note" id="copymsg" role="status"></p></div>`;
 $('drawer').hidden=false;$('scrim').hidden=false;$('app').inert=true;document.body.style.overflow='hidden';$('drawer').scrollTop=0;$('dclose').focus();
 $('dclose').onclick=()=>closeDrawer();$('prev').onclick=()=>adjacent(-1);$('next').onclick=()=>adjacent(1);
 if(p.bibtex)$('copy-bibtex').onclick=async()=>{
  if(!navigator.clipboard){$('bibtex-text').hidden=false;$('bibtex-msg').textContent=t('可从下方选中复制。','Select and copy below.');return;}
  try{await navigator.clipboard.writeText(p.bibtex);$('bibtex-msg').textContent=t('已复制。','Copied.');}
  catch(error){if(!['NotAllowedError','SecurityError'].includes(error.name))throw error;$('bibtex-text').hidden=false;$('bibtex-msg').textContent=t('可从下方选中复制。','Select and copy below.');}
 };
 $('copy').onclick=async()=>{const url=shareUrl(id);if(!url){$('copymsg').textContent=t('请从已发布的网站复制分享链接。','Open the published site to copy a shareable link.');return;}$('copymsg').textContent=t('请复制：','Copy this URL: ')+url;if(location.origin==='null'||!navigator.clipboard)return;try{await navigator.clipboard.writeText(url);$('copymsg').textContent=t('已复制链接。','Link copied.');}catch(error){if(!['NotAllowedError','SecurityError'].includes(error.name))throw error;}};
}
function adjacent(direction){const list=sequence(),i=list.findIndex(p=>p.id===openId)+direction;if(i>=0&&i<list.length)showPaper(list[i].id);}
function closeDrawer(updateUrl=true){openId=null;drawerIds=[];$('drawer').hidden=true;$('scrim').hidden=true;$('app').inert=false;document.body.style.overflow='';if(updateUrl)updateHash(viewHash(),true);if(lastFocus?.isConnected&&!lastFocus.closest('[hidden]'))lastFocus.focus();else $('main').focus();}
function route(){
 const [hash,query='']=location.hash.slice(1).split('?');
 if(hash.startsWith('p-')){showPaper(hash.slice(2),false);return;}
 if(hash==='papers'){
  const section=new URLSearchParams(query).get('section');
  state.sections=section?section.split(',').filter(id=>Object.hasOwn(S,id)):[];
  chrome();
 }
 showView(['home','papers','routes','gaps','map'].includes(hash)?hash:'home',false);
}
$('q').addEventListener('input',()=>{state.q=$('q').value.trim().toLowerCase();render();});
$('sort').onchange=()=>{state.sort=$('sort').value;render();};
$('filter-open').onclick=()=>{const expanded=$('filter-panel').classList.toggle('expanded');$('filter-open').setAttribute('aria-expanded',String(expanded));};
$('clear').onclick=()=>{Object.assign(state,{q:'',sections:[],must:false,verify:false,reviewed:false,filters:{}});$('q').value='';chrome();render();updateHash(viewHash(),true);};
window.addEventListener('follow-rsi:language',event=>{lang=event.detail.language;chrome();render();if(openId)openDrawer(openId);});
window.addEventListener('follow-rsi:navigate',event=>showView(event.detail.view));
$('sections').addEventListener('change',event=>{if(event.target.id!=='other-sections')return;state.sections=state.sections.filter(id=>METHOD_SECTIONS.includes(id));if(event.target.value)state.sections.push(event.target.value);chrome();render();updateHash(viewHash(),true);$('other-sections').focus();});
$('scrim').onclick=()=>closeDrawer();
document.addEventListener('click',event=>{
 const open=event.target.closest('[data-open],a[href^="#p-"]');if(open){event.preventDefault();const readingOrder=open.closest('[data-reading-order]')?.dataset.readingOrder.split(' ');showPaper(open.dataset.open||open.getAttribute('href').slice(3),true,readingOrder);return;}
 const mapFilter=event.target.closest('[data-map-section]');if(mapFilter){Object.assign(state,{q:'',sections:mapFilter.dataset.mapSection?mapFilter.dataset.mapSection.split(','):[],must:false,verify:false,reviewed:false,filters:{}});$('q').value='';chrome();showView('papers');$('main').focus();return;}
 const planned=event.target.closest('[data-map-plan]');if(planned){$('map-vote').hidden=false;$('map-vote').focus();return;}
 const toggle=event.target.closest('[data-toggle]');if(toggle){state[toggle.dataset.toggle]=!state[toggle.dataset.toggle];toggle.setAttribute('aria-pressed',String(state[toggle.dataset.toggle]));render();return;}
 const help=event.target.closest('[data-help]');if(help){const expanded=help.getAttribute('aria-expanded')!=='true';help.setAttribute('aria-expanded',String(expanded));$('help-'+help.dataset.help).hidden=!expanded;return;}
 const facet=event.target.closest('[data-field]');if(facet){const {field,value}=facet.dataset,selected=state.filters[field]||[];state.filters[field]=selected.includes(value)?selected.filter(v=>v!==value):[...selected,value];render();document.querySelector(`[data-field="${field}"][data-value="${value}"]`).focus();return;}
 const section=event.target.closest('[data-section]');if(section){const id=section.dataset.section;state.sections=id==='all'?[]:state.sections.includes(id)?state.sections.filter(s=>s!==id):[...state.sections,id];chrome();render();updateHash(viewHash(),true);document.querySelector(`[data-section="${id}"]`).focus();}
});
document.addEventListener('keydown',event=>{
 const editing=event.target.matches('input,textarea,select,[contenteditable="true"]');
 if(event.key==='/'&&!editing&&!openId){event.preventDefault();if(view!=='papers')showView('papers');$('q').focus();}
 if(!openId)return;
 if(event.key==='Escape'){event.preventDefault();closeDrawer();}
 if(!editing&&(event.key==='ArrowLeft'||event.key==='ArrowRight')){event.preventDefault();adjacent(event.key==='ArrowLeft'?-1:1);}
 if(event.key==='Tab'){
  const focusable=[...$('drawer').querySelectorAll('a[href],button:not(:disabled),summary')],first=focusable[0],last=focusable.at(-1);
  if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
 }
});
window.addEventListener('hashchange',route);
window.addEventListener('popstate',route);
chrome();render();route();
