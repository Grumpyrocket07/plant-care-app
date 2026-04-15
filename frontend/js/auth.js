// Check if already logged in
if (auth.isLoggedIn()) {
    window.location.href = 'dashboard.html';
}

// Toggle between login and register forms
document.getElementById('showRegister').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('loginForm').classList.add('d-none');
    document.getElementById('registerForm').classList.remove('d-none');
});

document.getElementById('showLogin').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('registerForm').classList.add('d-none');
    document.getElementById('loginForm').classList.remove('d-none');
});

// Handle Login
document.getElementById('loginFormElement').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');
    
    // Hide previous errors
    errorDiv.classList.add('d-none');
    
    try {
        const result = await api.login(email, password);
        
        // Save token
        auth.setToken(result.access_token);
        
        // Redirect to dashboard
        window.location.href = 'dashboard.html';
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.remove('d-none');
    }
});

// Handle Register
document.getElementById('registerFormElement').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const errorDiv = document.getElementById('registerError');
    const successDiv = document.getElementById('registerSuccess');
    
    // Hide previous messages
    errorDiv.classList.add('d-none');
    successDiv.classList.add('d-none');
    
    try {
        await api.register(name, email, password);
        
        // Show success message
        successDiv.textContent = 'Registration successful! You can now login.';
        successDiv.classList.remove('d-none');
        
        // Clear form
        document.getElementById('registerFormElement').reset();
        
        // Switch to login form after 2 seconds
        setTimeout(() => {
            document.getElementById('showLogin').click();
        }, 2000);
        
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.remove('d-none');
    }
});