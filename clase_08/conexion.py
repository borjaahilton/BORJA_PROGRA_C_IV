import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "Horarios_Marello"

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
            print(f"❌ Error al conectar con la base de datos: {e}")
            return None

    def cerrar(self, conexion):
        if conexion and conexion.is_connected():
            conexion.close()
            print("🔒 Conexión cerrada correctamente")

    # 🔹 Nueva función: Login de usuario
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


# --- Prueba directa (debug manual) ---
if __name__ == "__main__":
    db = ConexionDB()
    resultado = db.login_usuario("admin", "1234")
    print(resultado)
