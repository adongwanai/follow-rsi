'use strict';
(() => {
  const header = document.getElementById('site-header');
  const read = key => { try { return localStorage.getItem(key); } catch (error) { if (error.name !== 'SecurityError') throw error; return null; } };
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch (error) { if (error.name !== 'SecurityError') throw error; } };
  const themes = ['auto', 'light', 'dark'];
  const languageButton = document.getElementById('lang');
  const themeButton = document.getElementById('theme');
  function language(language) {
    document.documentElement.dataset.lang = language;
    document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
    languageButton.textContent = language === 'zh' ? 'EN' : '中文';
    languageButton.setAttribute('aria-label', language === 'zh' ? 'Switch to English' : '切换到中文');
    theme(document.documentElement.dataset.theme || 'auto');
  }
  function theme(value) {
    document.documentElement.dataset.theme = value;
    const chinese = document.documentElement.dataset.lang !== 'en';
    themeButton.textContent = (chinese ? '主题：' : 'Theme: ') + ({auto: chinese ? '自动' : 'Auto', light: chinese ? '浅色' : 'Light', dark: chinese ? '深色' : 'Dark'})[value];
    themeButton.setAttribute('aria-label', themeButton.textContent);
  }
  function setActive(view) {
    for (const item of header.querySelectorAll('[data-header-view], [data-header-page]')) {
      const selected = (item.dataset.headerView || item.dataset.headerPage) === view;
      if (selected) item.setAttribute('aria-current', 'page');
      else item.removeAttribute('aria-current');
    }
    const selected = header.querySelector('[aria-current="page"]');
    if (selected) header.querySelector('.site-nav').scrollLeft = Math.max(0, selected.offsetLeft - header.querySelector('.site-nav').offsetLeft - 12);
  }
  const storedTheme = read('harness.theme');
  theme(themes.includes(storedTheme) ? storedTheme : 'auto');
  language(read('harness.lang') === 'en' ? 'en' : 'zh');
  languageButton.addEventListener('click', () => {
    const next = document.documentElement.dataset.lang === 'zh' ? 'en' : 'zh';
    const selected = header.querySelector('[aria-current="page"]');
    language(next); save('harness.lang', next);
    if (selected) setActive(selected.dataset.headerView || selected.dataset.headerPage);
    window.dispatchEvent(new CustomEvent('follow-rsi:language', {detail: {language: next}}));
  });
  themeButton.addEventListener('click', () => {
    const next = themes[(themes.indexOf(document.documentElement.dataset.theme) + 1) % themes.length];
    theme(next); save('harness.theme', next);
    window.dispatchEvent(new CustomEvent('follow-rsi:theme', {detail: {theme: next}}));
  });
  header.addEventListener('click', event => {
    const button = event.target.closest('[data-header-view]');
    if (!button) return;
    const view = button.dataset.headerView;
    if (['home', 'papers', 'routes', 'map', 'gaps'].includes(header.dataset.page)) {
      setActive(view);
      window.dispatchEvent(new CustomEvent('follow-rsi:navigate', {detail: {view}}));
    } else location.href = header.dataset.siteIndex + '#' + view;
  });
  window.FollowRSIHeader = {setActive};
  setActive(header.dataset.page);
})();
