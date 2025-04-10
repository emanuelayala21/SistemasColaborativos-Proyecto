document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logout-btn");
  
    if (logoutBtn) {
      logoutBtn.addEventListener("click", function () {
        // Verifica el valor del token antes de eliminarlo
        console.log("Token antes de eliminar:", localStorage.getItem("token")); // o sessionStorage.getItem("token")
        
        // Eliminar el token de sesión o localStorage
        localStorage.removeItem("access_token"); // o sessionStorage.removeItem("token");
        
        // Verifica el valor del token después de eliminarlo
        console.log("Token después de eliminar:", localStorage.getItem("token")); // o sessionStorage.getItem("token")
        
        // Redirigir a la página de inicio o login
        window.location.href = "http://127.0.0.1:8000/api/usuario/login_page/"; // Ajusta a la URL de tu página de login
      });
    }
  });
  