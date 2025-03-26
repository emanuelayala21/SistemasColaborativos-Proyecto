// Función para obtener los viajes creados por el usuario
async function obtenerViajes() {
    const viajesLista = document.getElementById('viajes-lista');
    viajesLista.innerHTML = ''; // Limpiar la lista antes de actualizar

    try {
        const response = await fetch('http://localhost:8000/api/viaje/mis_viajes/', {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            }
        });
        const viajes = await response.json();

        // Si la respuesta es exitosa, mostrar los viajes
        if (response.ok) {
            viajes.forEach(viaje => {
                if (!document.querySelector(`.viaje-item[data-id='${viaje.id}']`)) {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item', 'viaje-item', 'mb-3', 'position-relative', 'shadow-sm');
                    li.setAttribute('data-id', viaje.id);  // Añadir data-id

                    li.innerHTML = `
                        <div class="viaje-container">
                            <!-- Botones de editar y eliminar -->
                            <div class="botones-viaje">
                                <button class="btn btn-sm btn-warning btn-icon" onclick="editarViaje(${viaje.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn btn-sm btn-danger btn-icon" onclick="eliminarViaje(${viaje.id})">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </div>

                            <!-- Contenido del viaje -->
                            <div class="viaje-info">
                                <h5>${viaje.titulo}</h5>
                                <p><strong>Inicio:</strong> ${viaje.fecha_inicio} <strong>Fin:</strong> ${viaje.fecha_fin}</p>
                                <p>${viaje.descripcion}</p>
                            </div>

                            <!-- Fecha de creación del viaje -->
                            <span class="badge bg-primary text-white">${viaje.fecha_creacion}</span>
                        </div>
                    `;

                    viajesLista.appendChild(li);
                }
            });
        } else {
            console.error('Error al obtener los viajes:', viajes);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}


// Llamar la función para cargar los viajes cuando la página se carga
document.addEventListener('DOMContentLoaded', obtenerViajes);


// Función para actualizar el viaje
// Función para actualizar el viaje
async function actualizarViaje(event) {
    event.preventDefault();
    const viajeId = document.getElementById('viaje-id').value;
    const viajeData = {
        titulo: document.getElementById('nombre-mod').value,
        fecha_inicio: document.getElementById('fecha-inicio-mod').value,
        fecha_fin: document.getElementById('fecha-fin-mod').value,
        descripcion: document.getElementById('descripcion-mod').value
    };

    try {
        const response = await fetch(`http://localhost:8000/api/viaje/${viajeId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('access_token')
            },
            body: JSON.stringify(viajeData)
        });

        if (response.ok) {
            const viajeModificado = await response.json();

            // Aquí puedes modificar directamente el viaje en la lista sin recargar toda la lista
            const viajeElemento = document.querySelector(`.viaje-item[data-id='${viajeModificado.id}']`);

            if (viajeElemento) {
                viajeElemento.querySelector('.viaje-info h5').innerText = viajeModificado.titulo;
                viajeElemento.querySelector('.viaje-info p').innerHTML = `
                    <strong>Inicio:</strong> ${viajeModificado.fecha_inicio} <strong>Fin:</strong> ${viajeModificado.fecha_fin}
                    <p>${viajeModificado.descripcion}</p>
                `;
            }

            // Mostrar mensaje bonito con SweetAlert2
            Swal.fire({
                title: '¡Éxito!',
                text: 'El viaje ha sido actualizado correctamente.',
                icon: 'success',
                confirmButtonText: '¡Genial!',
                customClass: {
                    confirmButton: 'btn btn-success'
                },
                background: '#f8f9fa', // Fondo claro para el mensaje
                buttonsStyling: false // Desactivar los estilos predeterminados
            });

            // Ocultar el formulario de modificación después de la actualización
            document.getElementById('form-modificar-viaje').style.display = 'none';
        } else {
            console.error('Error al actualizar el viaje');
        }
    } catch (error) {
        console.error('Error de conexión al actualizar el viaje:', error);
    }
}
