async function verificarNotificaciones() {
  const alerta = document.getElementById("notificacion-alerta");
  const icono = document.getElementById("icono-notificacion");
  // Obtener el token de localStorage
  const token = localStorage.getItem('access_token');

  // Verificar si el token está presente
  if (!token) {
    console.error("Token de autenticación no encontrado.");
    return;
  }

  try {
    console.log("Realizando la solicitud a la API..."); // Log para saber cuándo se hace la solicitud

    const response = await fetch("http://localhost:8000/api/notificacion/nuevas/", {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    });


    const data = await response.json();

    if (response.ok) {
      if (data.tiene_nuevas) {
        alerta.classList.remove("d-none");
        icono.classList.add("text-danger");
      } else {
        alerta.classList.add("d-none");
        icono.classList.remove("text-danger");
      }
    } else {
      console.error('Error al verificar notificaciones:', data);
    }
  } catch (error) {
    console.error("Error al verificar notificaciones:", error);
  }
}



// Función para cargar las notificaciones no leídas
async function cargarNotificaciones() {
  const contenedorNotificaciones = document.getElementById("contenedor-notificaciones");
  contenedorNotificaciones.innerHTML = ''; // Limpiar el contenedor

  // Obtener el token de autenticación
  const token = localStorage.getItem("access_token");

  if (!token) {
    alert("No se encontró el token de autenticación.");
    return;
  }

  try {
    const response = await fetch("/api/notificacion/noleidas/", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const notificaciones = await response.json();

    if (response.ok) {
      if (notificaciones.length === 0) {
        contenedorNotificaciones.innerHTML = "<p class='text-center text-muted'>No hay notificaciones nuevas.</p>";
      } else {
        for (const notif of notificaciones) {
          const div = document.createElement("div");
          div.className = "alert alert-info";

          const fecha = new Date(notif.fecha_creada);
          const fechaFormateada = fecha.toLocaleString();

          div.innerHTML = `<strong>${notif.tipo}</strong><br>${notif.mensaje}<br><small>${fechaFormateada}</small>`;
          contenedorNotificaciones.appendChild(div);

          await marcarNotificacionComoLeida(notif.id); // Espera a que se marque antes de seguir
        }

      }
      verificarNotificaciones();
    } else {
      console.error('Error al cargar las notificaciones:', notificaciones);
      contenedorNotificaciones.innerHTML = "<p class='text-center text-danger'>Error al cargar notificaciones.</p>";
    }
  } catch (error) {
    console.error("Error al cargar notificaciones:", error);
    contenedorNotificaciones.innerHTML = "<p class='text-center text-danger'>Error de conexión al cargar las notificaciones.</p>";
  }
}

// Función para marcar una notificación como leída
async function marcarNotificacionComoLeida(notifId) {
  const token = localStorage.getItem("access_token");

  if (!token) {
    console.error("Token de autenticación no encontrado.");
    return;
  }

  try {
    const response = await fetch(`/api/notificacion/${notifId}/leer/`, {
      method: "PUT",  // Cambiado a PUT
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`Notificación ${notifId} marcada como leída`);
    } else {
      console.error(`Error al marcar la notificación ${notifId} como leída`, data);
    }
  } catch (error) {
    console.error("Error al marcar como leída:", error);
  }
}

// Mostrar el modal con las notificaciones
document.getElementById("btn-notificaciones").addEventListener("click", () => {
  cargarNotificaciones();
  const modalNotificaciones = new bootstrap.Modal(document.getElementById("modalNotificaciones"));
  modalNotificaciones.show();
});

// Agrega un evento de cierre para asegurarte de que no queden capas o fondos oscuros
document.getElementById("modalNotificaciones").addEventListener("hidden.bs.modal", () => {
  const modalBackdrop = document.querySelector('.modal-backdrop');
  if (modalBackdrop) {
    modalBackdrop.remove();
  }
});


// Verificar nuevas notificaciones cada 30 segundos
setInterval(verificarNotificaciones, 30000);
verificarNotificaciones();

// Función para obtener el token CSRF desde las cookies
function getCSRFToken() {
  const cookie = document.cookie.split("; ").find(row => row.startsWith("csrftoken="));
  return cookie ? cookie.split("=")[1] : "";
}