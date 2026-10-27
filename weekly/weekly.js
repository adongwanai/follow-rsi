/* Publication is static; this switch only changes presentation. */
const weeklyLanguage = localStorage.getItem('harness.lang') === 'en' ? 'en' : 'zh';
document.documentElement.dataset.lang = weeklyLanguage;
document.documentElement.lang = weeklyLanguage === 'zh' ? 'zh-CN' : 'en';
document.getElementById('language').addEventListener('click', () => {
  const language = document.documentElement.dataset.lang === 'en' ? 'zh' : 'en';
  document.documentElement.dataset.lang = language;
  document.documentElement.lang = language === 'zh' ? 'zh-CN' : 'en';
  localStorage.setItem('harness.lang', language);
});
document.documentElement.dataset.theme = localStorage.getItem('harness.theme') || 'auto';
document.getElementById('theme').addEventListener('click', () => {
  const themes = ['auto', 'light', 'dark'];
  const theme = themes[(themes.indexOf(document.documentElement.dataset.theme) + 1) % 3];
  document.documentElement.dataset.theme = theme;
  localStorage.setItem('harness.theme', theme);
});
