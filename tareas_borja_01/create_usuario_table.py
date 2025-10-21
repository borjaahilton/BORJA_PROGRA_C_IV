from conexion import ConexionDB

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS usuario (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    hashed_pass VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    rol VARCHAR(50) DEFAULT 'user',
    activo TINYINT(1) DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def main():
    db = ConexionDB()
    conexion = db.conectar()
    if not conexion:
        print("No se pudo conectar a la base de datos. Revisa las credenciales y que MySQL esté en ejecución.")
        return

    try:
        cursor = conexion.cursor()
        print("Creando tabla 'usuario' (si no existe)...")
        cursor.execute(CREATE_TABLE_SQL)
        conexion.commit()
        print("Tabla 'usuario' creada o ya existente.")

        # Mostrar tablas para verificación
        cursor.execute("SHOW TABLES")
        tablas = [t[0] for t in cursor.fetchall()]
        print("Tablas en la base de datos:", tablas)

    except Exception as e:
        print("Error al crear la tabla usuario:", e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        db.cerrar(conexion)


if __name__ == '__main__':
    # Uso:
    #   python "create_usuario_table.py"
    # Esto creará la tabla `usuario` si no existe. Para reiniciar (borrar datos), ejecutar:
    #   - DROP TABLE usuario;  (ejecutar manualmente con precaución desde cliente MySQL)
    main()
