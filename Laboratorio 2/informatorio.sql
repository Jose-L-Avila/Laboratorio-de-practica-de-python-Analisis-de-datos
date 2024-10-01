CREATE DATABASE producto;
USE producto;
CREATE TABLE Producto(
nombre varchar(50) not null,
precio decimal(10,2)not null,
cantidad int not null,
idproducto varchar(10) primary key,
marca varchar(50) not null
);

CREATE TABLE ProductoElectronico(
idproducto varchar(10) primary key,
garantia int not null,
FOREIGN KEY (idproducto) REFERENCES Producto(idproducto) -- Relacion con Producto
);

CREATE TABLE ProductoAlimenticio(
idproducto varchar(10) primary key,
vencimiento int not null,
FOREIGN KEY (idproducto) REFERENCES Producto(idproducto) -- Relacion con Producto
);

SELECT * FROM producto;

