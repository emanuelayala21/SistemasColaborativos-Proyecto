// auth.js
function checkAuth() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        // Si no hay token, redirige al login
        window.location.href = "/Mantis-Bootstrap-1.0.0/dist/Usuarios/login.html";
    }
}

// Llama a esta función en todas las páginas protegidas
checkAuth();
