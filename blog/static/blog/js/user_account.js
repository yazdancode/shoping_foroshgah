// Example: Client-side form validation
document.querySelector('form').addEventListener('submit', function(event) {
  const firstName = document.getElementById('first_name').value;
  const lastName = document.getElementById('last_name').value;

  // Check if required fields are filled
  if (!firstName || !lastName) {
    alert("لطفاً نام و نام خانوادگی را وارد کنید.");
    event.preventDefault();  // Prevent form submission
  }
});
