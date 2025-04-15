document.getElementById("recuperar-form").addEventListener("submit", async function(e) {
    e.preventDefault();
    const correo = document.getElementById("correo").value;

    const res = await fetch("/api/usuario/enviar_correo_recuperacion/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ correo })
    });

    const data = await res.json();

    if (res.ok) {
        document.getElementById("mensaje").innerText = "Revisa tu correo electrónico.";
        setTimeout(() => {
            window.location.href = "http://127.0.0.1:8000/api/usuario/login_page/";
        }, 3000);
    } else {
        document.getElementById("mensaje").innerText = data.message || "Ocurrió un error.";
    }
});
