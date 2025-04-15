/**
 * Main JavaScript file for YGITC Page Builder
 */

// Initialize HTMX events
document.addEventListener('DOMContentLoaded', function() {
  // Set up CSRF token for HTMX requests
  document.body.addEventListener('htmx:configRequest', function(event) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    if (csrfToken) {
      event.detail.headers['X-CSRFToken'] = csrfToken;
    }
  });

  // Notification handling
  document.body.addEventListener('htmx:afterSwap', function(event) {
    // Auto-dismiss notifications after 5 seconds
    const notifications = document.querySelectorAll('[data-auto-dismiss]');
    notifications.forEach(notification => {
      setTimeout(() => {
        notification.classList.add('opacity-0');
        setTimeout(() => {
          notification.remove();
        }, 500);
      }, 5000);
    });
  });
});

// Slug generation helper
function generateSlug(text) {
  return text.toString().toLowerCase()
    .replace(/\s+/g, '-')           // Replace spaces with -
    .replace(/[^\w\-]+/g, '')       // Remove all non-word chars
    .replace(/\-\-+/g, '-')         // Replace multiple - with single -
    .replace(/^-+/, '')             // Trim - from start of text
    .replace(/-+$/, '');            // Trim - from end of text
}
