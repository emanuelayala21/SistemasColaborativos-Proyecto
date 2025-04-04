document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("loginForm");

    if (!form) {
        console.error("Formulario de login no encontrado en el DOM");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/api/usuario/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    correo: email,
                    contrasena: password
                })
            });

            const messageBox = document.getElementById("loginMessage");
            const data = await response.json(); // ✅ solo una vez

            if (response.ok) {
                const token = data.access;

                if (token) {
                    localStorage.setItem("access_token", token);
                    messageBox.innerHTML = `<span class="success">✅ Autenticación exitosa. Bienvenido!</span>`;
                    form.reset();
                    // Redirige a la vista de Django
                    window.location.href = "/api/usuario/custom_design/";
                } else {
                    messageBox.innerHTML = `<span class="error">No se recibió un token válido.</span>`;
                }
            } else {
                messageBox.innerHTML = `<span class="error">${data.message || "Credenciales incorrectas."}</span>`;
            }

        } catch (error) {
            console.error("Error en la autenticación:", error);
            alert("Error en el servidor.");
        }
    });
});
