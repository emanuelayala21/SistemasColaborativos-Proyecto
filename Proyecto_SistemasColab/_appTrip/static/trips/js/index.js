document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("access_token");

    if (!token) {
        console.warn("No hay token guardado en localStorage.");
        return;
    }

    // Función para decodificar el JWT
    function parseJwt (token) {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64).split('').map(c =>
                    '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
                ).join('')
            );
            return JSON.parse(jsonPayload);
        } catch (e) {
            console.error("Token inválido:", e);
            return null;
        }
    }

    const contenido = parseJwt(token);
    console.log("✅ Token cargado desde localStorage:");
    console.log(contenido);
});
