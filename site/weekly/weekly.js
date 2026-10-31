'use strict';
const editionSelect = document.getElementById('edition-select');
if (editionSelect) editionSelect.addEventListener('change', () => {
  if (editionSelect.value) location.href = editionSelect.value;
});
