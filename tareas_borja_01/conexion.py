import os
import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        # Leer credenciales desde variables de entorno para facilitar pruebas
        self.host = os.getenv("MYSQL_HOST", "localhost")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASS", "")
        self.database = os.getenv("MYSQL_DB", "Horarios_Marello")

    def conectar(self):
        try:
            conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conexion.is_connected():
                print("✅ Conexión exitosa a la base de datos")
                return conexion
        except Error as e:
            err_no = getattr(e, 'errno', None)
            print(f"❌ Error al conectar con la base de datos: {e} (errno={err_no})")
            if err_no == 1045:
                print("   → Access denied: revisa usuario/contraseña y permisos (error 1045).")
            if err_no == 2003:
                print("   → Can't connect to MySQL server: verifica que el servicio MySQL esté en ejecución.")
            return None

    def cerrar(self, conexion):
        if conexion and conexion.is_connected():
            conexion.close()
            print("🔒 Conexión cerrada correctamente")

    # 🔹 Login de usuario
    def login_usuario(self, nombre_usuario, clave):
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}

        try:
            cursor = conexion.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND hashed_pass = %s"
            cursor.execute(query, (nombre_usuario, clave))
            usuario = cursor.fetchone()

            if usuario:
                return {"status": True, "mensaje": "Login exitoso", "data": usuario}
            else:
                return {"status": False, "mensaje": "Usuario o contraseña incorrectos"}
        except Error as e:
            return {"status": False, "mensaje": f"Error en la consulta: {e}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    # 🔹 CORREGIDO: listar_docentes()
    def listar_docentes(self):
        """Devuelve una lista de docentes con sus datos personales y especialidad."""
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}

        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
            SELECT 
                d.docente_id,
                p.nombres,
                p.apellidos,
                e.nombre AS especialidad,
                d.codigo_docente,
                d.activo,
                d.observaciones,
                d.creado_en,
                d.actualizado_en
            FROM docentes d
            INNER JOIN personas p ON d.persona_id = p.persona_id
            INNER JOIN especialidades e ON d.especialidad_id = e.especialidad_id
            ORDER BY p.apellidos, p.nombres;
            """
            cursor.execute(query)
            filas = cursor.fetchall()

            return {
                "status": True,
                "mensaje": f"Se encontraron {len(filas)} docentes",
                "data": filas
            }

        except Error as e:
            return {"status": False, "mensaje": f"Error en la consulta: {e}", "data": []}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def listar_tablas(self):
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}
        try:
            cursor = conexion.cursor()
            cursor.execute("SHOW TABLES")
            tablas = [t[0] for t in cursor.fetchall()]
            return {"status": True, "mensaje": "Tablas obtenidas", "data": tablas}
        except Error as e:
            return {"status": False, "mensaje": str(e), "data": []}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def columnas_de_tabla(self, tabla_nombre):
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}
        try:
            cursor = conexion.cursor()
            cursor.execute("SHOW COLUMNS FROM %s" % tabla_nombre)
            cols = [row[0] for row in cursor.fetchall()]
            return {"status": True, "mensaje": "Columnas obtenidas", "data": cols}
        except Error as e:
            return {"status": False, "mensaje": str(e), "data": []}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def listar_personas(self):
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM personas")
            filas = cursor.fetchall()
            return {"status": True, "mensaje": "Listado de personas obtenido", "data": filas}
        except Error as e:
            return {"status": False, "mensaje": f"Error en la consulta: {e}", "data": []}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def listar_especialidades(self):
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.execute("SELECT especialidad_id, nombre, descripcion FROM especialidades")
            filas = cursor.fetchall()
            return {"status": True, "mensaje": "Especialidades listadas correctamente", "data": filas}
        except Error as e:
            return {"status": False, "mensaje": f"Error en la consulta: {e}", "data": []}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)


# --- Pruebas rápidas ---
if __name__ == "__main__":
    db = ConexionDB()
    print("Host:", db.host, "User:", db.user, "DB:", db.database)

    # Prueba docentes
    resultado = db.listar_docentes()
    print(resultado)

    # Prueba especialidades
    esp = db.listar_especialidades()
    print(esp)
