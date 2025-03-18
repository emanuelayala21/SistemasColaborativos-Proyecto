document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");

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
            alert("Todos los campos son obligatorios.");
            return;
        }

        if (contraseña.length < 8) {
            alert("La contraseña debe tener al menos 8 caracteres.");
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
            alert(data.message);
            if (response.ok) {
                form.reset(); // Limpiar formulario después del registro exitoso
            }

        } catch (error) {
            console.error("Error en el registro:", error);
            alert("Error en el servidor.");
        }
    });
});
