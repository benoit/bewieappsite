// Native details keeps the flag menu usable without JavaScript.
for (const menu of document.querySelectorAll('.languages')) {
  document.addEventListener('click', event => {
    if (menu.open && !menu.contains(event.target)) menu.open = false;
  });
  menu.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      menu.querySelector('summary').focus();
      event.preventDefault();
    }
  });
}

