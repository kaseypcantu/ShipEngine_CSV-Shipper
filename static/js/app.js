console.log('App.js Loaded')

document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    let notification = $delete.parentNode;

    $delete.addEventListener('click', () => {
      notification.parentNode.removeChild(notification);
    });
  });
});