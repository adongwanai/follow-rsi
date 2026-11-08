'use strict';
(() => {
  const contents = document.querySelector('.guide-toc');
  const buttons = [...contents.querySelectorAll('[data-guide-target]')];
  const lang = () => document.documentElement.dataset.lang;
  let queued = false;
  function highlight() {
    const headings = [...document.getElementById('guide-' + lang()).querySelectorAll('[data-guide-section]')];
    let current = headings[0].id;
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top <= window.innerHeight * .3) current = heading.id;
    }
    for (const button of buttons) {
      if (lang() + '-' + button.dataset.guideTarget === current) button.setAttribute('aria-current', 'location');
      else button.removeAttribute('aria-current');
    }
    document.title = (lang() === 'en' ? 'Harness self-evolution guide' : 'Harness 自进化导读') + ' · Follow RSI';
    queued = false;
  }
  contents.addEventListener('click', event => {
    const button = event.target.closest('[data-guide-target]');
    if (button) document.getElementById(lang() + '-' + button.dataset.guideTarget).scrollIntoView({block: 'start'});
  });
  window.addEventListener('scroll', () => {
    if (!queued) { queued = true; requestAnimationFrame(highlight); }
  }, {passive: true});
  window.addEventListener('follow-rsi:language', highlight);
  highlight();
})();
