document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    if (!form) {
        console.error("Formulario de login no encontrado en el DOM");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita la recarga de la página

        // Capturar valores del formulario
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        // Validar que los campos no estén vacíos
        if (!email || !password) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        try {
            // Enviar datos al servidor para autenticación
            const response = await fetch("http://localhost:8000/api/usuario/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    correo: email,
                    contrasena: password
                })
            });

            const data = await response.json();

            // Mostrar mensaje según la respuesta del servidor
            const messageBox = document.getElementById("loginMessage");
            if (response.ok) {
                const token = data.access; // Ajusta según la respuesta de tu servidor

                if (token) {
                    // Guardar el token en el localStorage
                    localStorage.setItem("access_token", token);

                    messageBox.innerHTML = `<span class="success">✅ Autenticación exitosa. Bienvenido!</span>`;
                    form.reset(); // Limpiar el formulario después de un inicio de sesión exitoso

                    // Redirigir a la página principal (o cualquier página que elijas)
                    window.location.href = "http://127.0.0.1:8000/api/viaje/dashboard/"; // Cambia a la URL que desees
                } else {
                    messageBox.innerHTML = `<span class="error">No se recibió un token válido.</span>`;
                }
            } else {
                messageBox.innerHTML = `<span class="error"> ${data.message}</span>`;
            }

        } catch (error) {
            console.error("Error en la autenticación:", error);
            alert("Error en el servidor.");
        }
    });
});
