DROP TABLE IF EXISTS Usuario;
CREATE TABLE Usuario (
    cedula VARCHAR(9) PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    fecha_creacion DATE
);

DROP TABLE IF EXISTS Viaje;
CREATE TABLE Viaje (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cedula_creador VARCHAR(9) NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    descripcion  VARCHAR(200),
    fecha_creacion DATE,
    FOREIGN KEY (cedula_creador) REFERENCES Usuario(cedula) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Participante_Viaje;
CREATE TABLE Participante_Viaje (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_viaje INT NOT NULL,
    cedula_usuario VARCHAR(9) NOT NULL,
    fecha_union DATE,
    es_admin BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_viaje) REFERENCES Viaje(id) ON DELETE CASCADE,
    FOREIGN KEY (cedula_usuario) REFERENCES Usuario(cedula) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Votacion;
CREATE TABLE Votacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_viaje INT NOT NULL,
    cedula_usuario VARCHAR(9) NOT NULL,
    titulo VARCHAR(100) NOT NULL, 
    descripcion VARCHAR(150) NOT NULL, 
    fecha_creacion DATE,
    FOREIGN KEY (id_viaje) REFERENCES Viaje(id) ON DELETE CASCADE,
    FOREIGN KEY (cedula_usuario) REFERENCES Usuario(cedula) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Opcion_Votacion;
CREATE TABLE Opcion_Votacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_votacion INT NOT NULL,
    opcion VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_votacion) REFERENCES Votacion(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Respuesta_Votacion;
CREATE TABLE Respuesta_Votacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_votacion INT NOT NULL,
    cedula_usuario VARCHAR(9) NOT NULL,
    id_opcion INT NOT NULL,
    fecha_respuesta DATE,
    FOREIGN KEY (id_votacion) REFERENCES Votacion(id) ON DELETE CASCADE,
    FOREIGN KEY (cedula_usuario) REFERENCES Usuario(cedula) ON DELETE CASCADE,
    FOREIGN KEY (id_opcion) REFERENCES Opcion_Votacion(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS Nota_Importante;
CREATE TABLE Nota_Importante (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_viaje INT NOT NULL,
    cedula_usuario VARCHAR(9) NOT NULL, 
    titulo VARCHAR(25) NOT NULL,
    contenido VARCHAR(255) NOT NULL,
    fecha_creacion DATE,
    FOREIGN KEY (id_viaje) REFERENCES Viaje(id) ON DELETE CASCADE,
    FOREIGN KEY (cedula_usuario) REFERENCES Usuario(cedula) ON DELETE CASCADE
);