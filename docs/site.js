(() => {
  'use strict';
  document.documentElement.classList.add('js');

  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const nav = document.getElementById('primary-nav');
  function closeMenu(returnFocus = false) {
    if (!menu || !nav) return;
    menu.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
    if (returnFocus) menu.focus();
  }
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      menu.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('is-open', open);
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
    });
    document.addEventListener('click', event => { if (header && !header.contains(event.target)) closeMenu(); });
    window.matchMedia('(min-width: 701px)').addEventListener('change', event => { if (event.matches) closeMenu(); });
  }

  const filters = document.querySelectorAll('[data-filter]');
  const projects = document.querySelectorAll('#project-grid [data-categories]');
  const status = document.getElementById('filter-status');
  filters.forEach(button => button.addEventListener('click', () => {
    const category = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    projects.forEach(project => {
      const visible = category === 'all' || project.dataset.categories.split(' ').includes(category);
      project.hidden = !visible;
      if (visible) count += 1;
    });
    if (status) status.textContent = count + (count === 1 ? ' project' : ' projects');
  }));

  function revealHashTarget() {
    if (!window.location.hash) return;
    let id;
    try { id = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const disclosure = target.matches('details') ? target : target.closest('details');
    if (disclosure) {
      disclosure.open = true;
      requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    }
  }
  revealHashTarget();
  window.addEventListener('hashchange', revealHashTarget);
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    if (link.hash === window.location.hash) revealHashTarget();
  }));

  document.querySelectorAll('[data-copy-email]').forEach(button => {
    button.addEventListener('click', async () => {
      const message = button.parentElement.querySelector('.copy-status');
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(button.dataset.copyEmail);
        if (message) message.textContent = 'Email address copied.';
      } catch (_) {
        if (message) message.textContent = 'Select the address above to copy it.';
      }
    });
  });
})();
