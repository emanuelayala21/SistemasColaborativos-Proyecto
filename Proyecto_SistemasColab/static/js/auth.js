// auth.js
function checkAuth() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        // Si no hay token, redirige al login
        window.location.href = "http://127.0.0.1:8000/api/usuario/login_page/";
    }
}

// Llama a esta función en todas las páginas protegidas
checkAuth();
