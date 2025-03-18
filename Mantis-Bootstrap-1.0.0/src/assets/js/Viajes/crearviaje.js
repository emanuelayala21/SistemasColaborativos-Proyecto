document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-viajes");

    if (!form) {
        console.error("Formulario de creación de viaje no encontrado en el DOM");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita la recarga de la página

        // Capturar valores del formulario
        const nombre = document.getElementById("nombre").value.trim();
        const fechaInicio = document.getElementById("fecha-inicio").value;
        const fechaFin = document.getElementById("fecha-fin").value;
        const descripcion = document.getElementById("descripcion").value.trim();
        const medio = document.getElementById("medio").value;

        // Validar que los campos no estén vacíos
        if (!nombre || !fechaInicio || !fechaFin || !descripcion) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        // Obtener el token desde el localStorage (suponiendo que el login ya guardó el token)
        const token = localStorage.getItem("access_token");

        if (!token) {
            alert("No se encontró el token de autenticación.");
            return;
        }

        try {
            // Enviar datos al servidor para crear el viaje
            const response = await fetch("http://localhost:8000/api/viaje/crear/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,  // Incluir el token en los headers
                },
                body: JSON.stringify({
                    titulo: nombre,
                    fecha_inicio: fechaInicio,
                    fecha_fin: fechaFin,
                    descripcion: descripcion,
                    medio_transporte: medio
                })
            });

            const data = await response.json();

            // Mostrar mensaje según la respuesta del servidor
            const viajesLista = document.getElementById("viajes-lista");
            if (response.ok) {
                // Si la creación fue exitosa, agregar el viaje a la lista
                const viajeItem = document.createElement("li");
                viajeItem.classList.add("list-group-item");
                viajeItem.textContent = `${data.titulo} (Desde: ${data.fecha_inicio} Hasta: ${data.fecha_fin})`;
                viajesLista.appendChild(viajeItem);

                // Limpiar el formulario
                form.reset();

                alert("Viaje creado exitosamente!");
            } else {
                alert(`Error: ${data.message || 'No se pudo crear el viaje'}`);
            }

        } catch (error) {
            console.error("Error en la creación del viaje:", error);
            alert("Error en el servidor.");
        }
    });
});
