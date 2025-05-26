// This is to on page load listen for if the signup or login form is submitted and if so
// to execute the functions built below
document.addEventListener('DOMContentLoaded', function() {
    var signupForm = document.getElementById('signupForm');
    var loginForm = document.getElementById('loginForm');

    if (signupForm) {
        signupForm.addEventListener('submit', function(e){
            e.preventDefault();
            validateForm();
        })
    }
})

// Function to validate user input while registering

function validateForm() {
    var formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        confirm_password: document.getElementById('confirm_password').value
    };

    // AJAX call to validate
    fetch('/validate-signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'applications/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    then(data => {
        document.querySelectorAll('.error').forEach(el => el.textContent = '');
        
        if (data.errors) {
            Object.keys(data.errors).forEach(key => {
                document.getElementById(key + '-error').textContent = data.errors[key];
            });
        } else {
            console.log('Form is valid')
            createUser(formData);
        }
    })
    .catch(error => console.error('Validation Error:', error));
}

// Function to pass data to the user creation route

function createUser(formData){
    
}