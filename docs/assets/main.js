// tnms — theme toggle & utilities
(function () {
  'use strict';

  const STORAGE_KEY = 'tnms-theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    updateToggleIcon(theme);
  }

  function updateToggleIcon(theme) {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    // Sun icon for dark mode (click to go light), Moon icon for light mode (click to go dark)
    btn.innerHTML = theme === 'dark'
      ? '<svg viewBox="0 0 24 24"><path d="M12 3a1 1 0 0 1 1 1v1a1 1 0 1 1-2 0V4a1 1 0 0 1 1-1Zm0 15a1 1 0 0 1 1 1v1a1 1 0 1 1-2 0v-1a1 1 0 0 1 1-1Zm9-6a1 1 0 0 1-1 1h-1a1 1 0 1 1 0-2h1a1 1 0 0 1 1 1ZM5 12a1 1 0 0 1-1 1H3a1 1 0 1 1 0-2h1a1 1 0 0 1 1 1Zm14.07-5.07a1 1 0 0 1 0 1.41l-.71.71a1 1 0 1 1-1.41-1.41l.7-.71a1 1 0 0 1 1.42 0ZM7.05 17.66a1 1 0 0 1 0 1.41l-.7.71a1 1 0 0 1-1.42-1.41l.71-.71a1 1 0 0 1 1.41 0Zm12.02.71a1 1 0 0 1-1.41 0l-.71-.71a1 1 0 0 1 1.41-1.41l.71.7a1 1 0 0 1 0 1.42ZM7.05 6.34a1 1 0 0 1-1.41 0l-.71-.7a1 1 0 0 1 1.41-1.42l.71.71a1 1 0 0 1 0 1.41ZM12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z"/></svg>'
      : '<svg viewBox="0 0 24 24"><path d="M12.1 22c5.52 0 10-4.48 10-10 0-4.75-3.31-8.72-7.75-9.74-.29-.07-.58.08-.68.36-.1.28-.01.59.22.78A7.46 7.46 0 0 1 16.86 9c0 4.14-3.36 7.5-7.5 7.5-1.76 0-3.38-.61-4.66-1.63-.2-.16-.48-.2-.72-.1-.24.1-.39.34-.36.6.5 5 4.63 8.63 9.48 8.63Z"/></svg>';
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }

  // Apply theme immediately (before DOM is fully ready) to prevent flash
  applyTheme(getPreferredTheme());

  document.addEventListener('DOMContentLoaded', function () {
    updateToggleIcon(getPreferredTheme());

    const btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.addEventListener('click', function () {
        const current = document.documentElement.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }
  });
})();
