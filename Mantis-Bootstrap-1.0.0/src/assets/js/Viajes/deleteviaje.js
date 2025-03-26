// Función para eliminar un viaje con una alerta moderna
async function eliminarViaje(viajeId) {
    Swal.fire({
        title: "¿Estás seguro?",
        text: "Esta acción no se puede deshacer.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        cancelButtonColor: "#6c757d",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar"
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`http://localhost:8000/api/viaje/${viajeId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                    }
                });

                if (response.ok) {
                    Swal.fire({
                        title: "Eliminado",
                        text: "El viaje ha sido eliminado correctamente.",
                        icon: "success",
                        timer: 2000,
                        showConfirmButton: false
                    });
                    obtenerViajes(); // Actualizar la lista
                } else {
                    const errorData = await response.json();
                    Swal.fire({
                        title: "Error",
                        text: errorData.message || "No se pudo eliminar el viaje.",
                        icon: "error"
                    });
                }
            } catch (error) {
                console.error("Error al conectar con el servidor:", error);
                Swal.fire({
                    title: "Error de conexión",
                    text: "Inténtalo de nuevo más tarde.",
                    icon: "error"
                });
            }
        }
    });
}
