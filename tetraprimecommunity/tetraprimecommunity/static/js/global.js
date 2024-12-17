/**
 * Update a user preference via the API.
 * @param {string} key - The preference key to update (e.g., "onboarding").
 * @param {*} value - The value to set for the preference (e.g., true).
 * @param {function} onSuccess - Optional callback function to execute on success.
 * @param {function} onError - Optional callback function to execute on error.
 */
function updateUserPreference(key, value, onSuccess, onError) {
  fetch('/accounts/preferences/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken() // Ensure CSRF protection for POST requests
    },
    body: JSON.stringify({ [key]: value })
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Failed to update preference');
      }
    })
    .then(data => {
      console.log(`Preference "${key}" updated to`, value);
      if (onSuccess) {
        onSuccess(data); // Execute success callback if provided
      }
    })
    .catch(error => {
      console.error('Error updating preference:', error);
      if (onError) {
        onError(error); // Execute error callback if provided
      }
    });
}

/**
 * Retrieve the CSRF token from the page.
 * Assumes a CSRF token input exists with name="csrfmiddlewaretoken".
 */
function getCsrfToken() {
  const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
  return csrfInput ? csrfInput.value : '';
}


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('hide-onboarding').addEventListener('click', function () {
        updateUserPreference(
            'onboarding',
            false,
            function () {
                console.log('Onboarding preference updated successfully!');
                document.querySelector('#feature-onboarding').style.display = 'none'; // Hide the onboarding section
            },
            function (error) {
                console.log('Failed to update onboarding preference.');
            }
        );
    });
});
