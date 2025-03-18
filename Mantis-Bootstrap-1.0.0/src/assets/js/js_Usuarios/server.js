const express = require("express");
const sql = require("mssql");
const cors = require("cors");
const bcrypt = require("bcrypt");
require("dotenv").config();

require("dotenv").config({ path: __dirname + "/configuracion.env" });

console.log("🔹 Usuario:", process.env.DB_USER);
console.log("🔹 Contraseña:", process.env.DB_PASSWORD);
console.log("🔹 Servidor:", process.env.DB_SERVER);
console.log("🔹 Base de datos:", process.env.DB_DATABASE);
console.log("🔹 Puerto:", process.env.DB_PORT);

// Configuración de Express
const app = express();
app.use(express.json());
app.use(cors());

// Configuración de la conexión a SQL Server
const dbConfig = {
    user: process.env.DB_USER,    
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: false, // Cambia a true si usas Azure SQL
        trustServerCertificate: true,
    },
};

// Conectar a SQL Server
sql.connect(dbConfig)
    .then(() => console.log("Conexión exitosa a SQL Server"))
    .catch((err) => console.error("Error de conexión:", err));

// 🟢 Endpoint para registrar usuarios
app.post("/registro", async (req, res) => {
    const { nombre, apellido, email, contraseña } = req.body;

    if (!nombre || !apellido || !email || !contraseña) {
        return res.status(400).json({ message: "Todos los campos son obligatorios." });
    }

    try {
        // Hashear la contraseña antes de insertarla
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(contraseña, saltRounds);

        // Query para insertar usuario
        const query = `INSERT INTO Usuarios (nombre, apellido, email, contraseña) VALUES (@nombre, @apellido, @correo, @contraseña)`;
        const request = new sql.Request();
        request.input("nombre", sql.NVarChar, nombre);
        request.input("apellido", sql.NVarChar, apellido);
        request.input("correo", sql.NVarChar, email);
        request.input("contraseña", sql.NVarChar, hashedPassword);

        await request.query(query);
        res.status(201).json({ message: "✅ Usuario registrado exitosamente." });

    } catch (err) {
        console.error("Error al registrar usuario:", err);
        res.status(500).json({ message: "Error en el servidor." });
    }
});

// 🟢 Iniciar el servidor en el puerto 3000
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
