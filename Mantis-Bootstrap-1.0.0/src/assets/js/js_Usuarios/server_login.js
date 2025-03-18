require("dotenv").config();
const express = require("express");
const sql = require("mssql");
const cors = require("cors");
const bcrypt = require("bcrypt");

const app = express();
app.use(express.json());
app.use(cors());

// Configuración de conexión a SQL Server desde .env
const dbConfig = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    port: parseInt(process.env.DB_PORT, 10),
    options: {
        encrypt: false,
        trustServerCertificate: true
    }
};

// Conexión con la base de datos
sql.connect(dbConfig)
    .then(() => console.log("✅ Conexión exitosa a SQL Server"))
    .catch(err => console.error("❌ Error conectando a SQL Server:", err));

// Ruta para el login (Validación de usuario)
app.post("/login", async (req, res) => {
    const { email, password } = req.body;

    if (!email || !password) {
        return res.status(400).json({ message: "❌ Todos los campos son obligatorios." });
    }

    try {
        const pool = await sql.connect(dbConfig);
        const result = await pool
            .request()
            .input("email", sql.VarChar, email)
            .query("SELECT Contraseña FROM Usuarios WHERE Email = @email");

        if (result.recordset.length === 0) {
            return res.status(401).json({ message: "❌ Correo no registrado." });
        }

        const storedHash = result.recordset[0].Contraseña;

        // Comparar la contraseña ingresada con el hash almacenado
        const isPasswordValid = bcrypt.compareSync(password, storedHash);

        if (!isPasswordValid) {
            return res.status(401).json({ message: "❌ Contraseña incorrecta." });
        }

        res.json({ message: "✅ Autenticación exitosa." });

    } catch (error) {
        console.error("❌ Error en la consulta:", error);
        res.status(500).json({ message: "Error en el servidor." });
    }
});

// Iniciar el servidor en el puerto 3000
app.listen(3000, () => {
    console.log("🚀 Servidor corriendo en http://localhost:3000");
});
