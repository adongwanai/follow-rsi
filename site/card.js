'use strict';
const data=window.HARNESS_DATA, card=document.getElementById('card');
const params=new URLSearchParams(location.search),isOG=params.get('og')==='1',lang=params.get('lang')==='en'?'en':'zh';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const t=(zh,en)=>lang==='zh'?zh:en;
const keys=['held_out','matched_budget_baseline','cross_model_transfer','cost_reported'];
const labels=lang==='zh'?['留出集','同预算对照','跨模型迁移','报告成本']:['Held-out','Matched budget','Cross-model','Cost'];
const symbols={yes:'✓',partial:'◐',no:'✕',unknown:'?',na:'–'};
function qr(url){
 if(!url)return `<div class="qr-placeholder">${t('回流二维码<br>发布后启用','Return QR code<br>pending URL')}<!-- TODO --></div>`;
 const code=new QRCode(-1,0);code.addData(encodeURI(url));code.make();const n=code.getModuleCount();let path='';
 for(let y=0;y<n;y++)for(let x=0;x<n;x++)if(code.isDark(y,x))path+=`M${x+4} ${y+4}h1v1h-1z`;
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n+8} ${n+8}" role="img" aria-label="${esc(url)}" shape-rendering="crispEdges"><rect width="100%" height="100%" fill="white"/><path d="${path}" fill="black"/></svg>`;
}
function bottom(p){
 const target=data.config.repository_url;
 const short=target?target.replace(/^https?:\/\//,'').replace(/\/$/,''):'github.com/'+data.config.repository;
 return `<div class="card-bottom"><div class="card-footer">${p?.arxiv?'arXiv '+esc(p.arxiv):p?esc(p.date):'follow-rsi'}<br>${isOG?'Code MIT · Content CC BY 4.0':'follow-rsi'}<div class="return-url">${esc(short)}</div></div><div class="qr">${qr(target)}<div class="qr-label">${t('扫码查看完整证据','Scan for the full evidence')}</div></div></div>`;
}
if(isOG){
 card.classList.add('og');card.innerHTML=`<p class="card-kicker">FOLLOW RSI · WITH RECEIPTS</p><div class="og-top"><div><h1>每一篇论文，<br>都要拿出凭证。</h1><p class="og-subtitle">Every paper. Show the evidence.</p></div><div class="og-stubs"><div class="og-stub"><span>HDA</span><b>54%</b><span>搜索集收益来自过拟合</span></div><div class="og-stub"><span>AUDITING</span><b>4/26</b><span>同起点、同预算比较</span></div></div></div>${bottom(null)}`;
}else{
 const p=data.papers.find(p=>p.id===params.get('id'));
 if(!p)throw new Error('Unknown paper id');
 card.innerHTML=`<p class="card-kicker">FOLLOW RSI · RECEIPT</p><h1>${esc(p.short_title)}</h1><div class="card-flags">${p.must_read?'<span class="card-flag">MUST READ</span>':''}${p.needs_reading?'<span class="card-flag verify">待细读 / Needs verification</span>':''}${p.status==='candidate'?'<span class="card-flag verify">候选 / Candidate</span>':''}</div><p class="card-summary">${esc(p['summary_'+lang])}</p><div class="card-evidence">${keys.map((k,i)=>`<div><b>${symbols[p.evidence[k]]}</b>${labels[i]}</div>`).join('')}</div>${p['result_'+lang]?`<p class="card-result">${esc(p['result_'+lang])}</p>`:''}${bottom(p)}`;
}
(async()=>{
 await document.fonts.ready;
 const title=card.querySelector('h1'),summary=card.querySelector('.card-summary'),result=card.querySelector('.card-result');
 while(card.scrollHeight>card.clientHeight){
  let changed=false;
  for(const [el,min] of [[title,40],[summary,25],[result,24]])if(el){const size=parseFloat(getComputedStyle(el).fontSize);if(size>min){el.style.fontSize=(size-1)+'px';changed=true;}}
  if(!changed)throw new Error('Share card content overflows');
 }
 document.documentElement.dataset.cardReady='true';
})();
