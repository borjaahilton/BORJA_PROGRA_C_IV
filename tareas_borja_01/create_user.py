import argparse
import getpass
import hashlib
from conexion import ConexionDB


CREATE_USUARIOS_TABLE = """
CREATE TABLE IF NOT EXISTS usuarios (
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


def hash_password(password: str) -> str:
    """Devuelve el hash SHA-256 de la contraseña en hex."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def tabla_existe(conexion, nombre_tabla: str) -> bool:
    cursor = conexion.cursor()
    try:
        cursor.execute("SHOW TABLES LIKE %s", (nombre_tabla,))
        filas = cursor.fetchall()
        return len(filas) > 0
    finally:
        cursor.close()


def crear_tabla_usuarios_si_no_existe(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute(CREATE_USUARIOS_TABLE)
        conexion.commit()
    finally:
        cursor.close()


def insertar_usuario(conexion, nombre_usuario: str, hashed_pass: str, email: str = None, rol: str = 'user'):
    cursor = conexion.cursor()
    try:
        query = "INSERT INTO usuarios (nombre_usuario, hashed_pass, email, rol) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre_usuario, hashed_pass, email, rol))
        conexion.commit()
        return True, None
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()


def main():
    parser = argparse.ArgumentParser(description="Crear un usuario en la base de datos")
    parser.add_argument('-u', '--username', help='Nombre de usuario', required=False)
    parser.add_argument('-e', '--email', help='Email del usuario', required=False)
    parser.add_argument('-r', '--role', help='Rol (user/admin)', default='user', required=False)
    parser.add_argument('--no-create-table', help='No crear la tabla si no existe', action='store_true')

    args = parser.parse_args()

    username = args.username
    if not username:
        username = input('Nombre de usuario: ').strip()

    if not username:
        print('Se requiere un nombre de usuario.')
        return

    # pedir contraseña de forma segura
    pwd = getpass.getpass('Contraseña: ')
    pwd2 = getpass.getpass('Confirmar contraseña: ')
    if pwd != pwd2:
        print('Las contraseñas no coinciden.')
        return

    if len(pwd) < 4:
        print('La contraseña debe tener al menos 4 caracteres.')
        return

    hashed = hash_password(pwd)

    db = ConexionDB()
    conexion = db.conectar()
    if not conexion:
        print('No se pudo conectar a la base de datos. Revisa las credenciales y que MySQL esté en ejecución.')
        return

    try:
        # detectar tabla 'usuarios' o 'usuario'
        if not tabla_existe(conexion, 'usuarios') and not tabla_existe(conexion, 'usuario'):
            if args.no_create_table:
                print("No existe la tabla 'usuarios' ni 'usuario'. Usa --no-create-table para impedir la creación automática.")
                return
            print("Tabla 'usuarios' no encontrada. Creando tabla 'usuarios'...")
            crear_tabla_usuarios_si_no_existe(conexion)

        # preferir 'usuarios' si existe, si no usar 'usuario'
        tabla_objetivo = 'usuarios' if tabla_existe(conexion, 'usuarios') else 'usuario'

        # si la tabla destino es 'usuario' (singular), adaptamos la inserción
        if tabla_objetivo == 'usuario':
            cursor = conexion.cursor()
            try:
                query = "INSERT INTO usuario (nombre_usuario, hashed_pass, email, rol) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, hashed, args.email, args.role))
                conexion.commit()
                print(f"Usuario '{username}' creado en la tabla 'usuario'.")
            except Exception as e:
                print('Error al crear usuario:', e)
            finally:
                cursor.close()
        else:
            ok, err = insertar_usuario(conexion, username, hashed, args.email, args.role)
            if ok:
                print(f"Usuario '{username}' creado en la tabla 'usuarios'.")
            else:
                print('Error al crear usuario:', err)

    finally:
        db.cerrar(conexion)


if __name__ == '__main__':
    main()
