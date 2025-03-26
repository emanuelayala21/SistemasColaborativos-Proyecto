// Función para mostrar el formulario de edición con los datos del viaje
async function editarViaje(viajeId) {
    // Hacer una solicitud para obtener los datos del viaje
    try {
        const response = await fetch(`http://localhost:8000/api/viaje/${viajeId}/`, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token') // Usando el token del localStorage
            }
        });
        const viaje = await response.json();
        // Si la respuesta es exitosa, llenar el formulario con los datos del viaje
        if (response.ok) {
            console.log('Datos del viaje obtenidos:', viaje);
            // Llenar los campos del formulario con los datos del viaje
            document.getElementById('id').value = viaje.id;
            document.getElementById('nombre').value = viaje.titulo;
            document.getElementById('fecha-inicio-mod').value = viaje.fecha_inicio;
            document.getElementById('fecha-fin-mod').value = viaje.fecha_fin;
            document.getElementById('descripcion-mod').value = viaje.descripcion;
            // Mostrar el formulario de modificación
            document.getElementById('form-modificar-viaje').style.display = 'block'; 
        } else {
            console.error('Error al obtener los datos del viaje:', viaje);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

// Función para actualizar el viaje
async function actualizarViaje(event) {
    event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

    const viajeId = document.getElementById('viaje-id').value;
    const viajeData = {
        titulo: document.getElementById('nombre-mod').value,
        fecha_inicio: document.getElementById('fecha-inicio-mod').value,
        fecha_fin: document.getElementById('fecha-fin-mod').value,
        descripcion: document.getElementById('descripcion-mod').value
    };

    try {
        const response = await fetch(`http://localhost:8000/api/viaje/${viajeId}/actualizar/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token') // Usando el token del localStorage
            },
            body: JSON.stringify(viajeData)
        });

        if (response.ok) {
            alert('Viaje actualizado correctamente');
            // Ocultar el formulario de modificación después de la actualización
            document.getElementById('form-modificar-viaje').style.display = 'none';
            obtenerViajes(); // Recargar los viajes después de la actualización
        } else {
            console.error('Error al actualizar el viaje');
        }
    } catch (error) {
        console.error('Error de conexión al actualizar el viaje:', error);
    }
}

// Añadir el evento al formulario de modificación
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('form-modificar-viaje').addEventListener('submit', actualizarViaje);
});
