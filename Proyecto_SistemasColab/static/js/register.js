document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const messageDiv = document.getElementById("registerMessage");

    if (!form) {
        console.error("Formulario no encontrado en el DOM");
        return;
    }

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const nombre = document.getElementById("nombre").value.trim();
        const email = document.getElementById("email").value.trim();
        const contraseña = document.getElementById("password").value;

        if (!nombre || !email || !contraseña) {
            showMessage("Todos los campos son obligatorios.", "error");
            return;
        }

        if (contraseña.length < 8) {
            showMessage("La contraseña debe tener al menos 8 caracteres.", "error");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/api/usuario/crear_usuario/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    nombre_usuario: nombre,  
                    correo: email,
                    contrasena: contraseña
                })
            });

            const data = await response.json();

            if (response.ok) {
                showMessage("¡Registro exitoso! Redirigiendo...", "success");
                form.reset();
                setTimeout(() => {
                    window.location.href = "/api/usuario/custom_design/";
                }, 2000);
            } else {
                showMessage(data.message || "Error al registrar.", "error");
            }

        } catch (error) {
            console.error("Error en el registro:", error);
            showMessage("Error en el servidor. Inténtalo más tarde.", "error");
        }
    });

    function showMessage(message, type) {
        messageDiv.innerHTML = message;
        messageDiv.className = `register-message ${type}`;
        messageDiv.style.display = "block";

        setTimeout(() => {
            messageDiv.style.display = "none";
        }, 3000);
    }
});
