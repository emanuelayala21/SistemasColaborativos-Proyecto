document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");
    const messageDiv = document.getElementById("registerMessage");

    if (!form) {
        console.error("Formulario no encontrado en el DOM");
        return;
    }

    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Evita que la página se recargue

        // Capturar valores del formulario
        const nombre = document.getElementById("nombre").value.trim();
        const email = document.getElementById("email").value.trim();
        const contraseña = document.getElementById("password").value;

        // Validar que los campos no estén vacíos
        if (!nombre || !email || !contraseña) {
            showMessage("Todos los campos son obligatorios.", "error");
            return;
        }

        if (contraseña.length < 8) {
            showMessage("La contraseña debe tener al menos 8 caracteres.", "error");
            return;
        }

        try {
            // Enviar datos al servidor
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

            // Mostrar mensaje de éxito o error
            if (response.ok) {
                showMessage("¡Registro exitoso! Redirigiendo a iniciar sesión...", "success");
                form.reset(); // Limpiar formulario después del registro exitoso
                
                // Redirigir después de 2 segundos
                setTimeout(() => {
                    window.location.href = "login.html";
                }, 2000);
            } else {
                showMessage(data.message || "Hubo un error en el registro.", "error");
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
