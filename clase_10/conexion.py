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
        cursor = conexion.cursor()
        try:
            cursor.execute("SHOW COLUMNS FROM %s" % tabla_nombre)
            cols = [row[0] for row in cursor.fetchall()]
            return {"status": True, "mensaje": "Columnas obtenidas", "data": cols}
        except Error as e:
            return {"status": False, "mensaje": str(e), "data": []}
        finally:
            cursor.close()
            self.cerrar(conexion)

    def listar_personas(self):
        """Devuelve todas las filas de la tabla persona."""
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos", "data": []}
        cursor = conexion.cursor(dictionary=True)
        try:
            try:
                cursor.execute("SELECT * FROM persona")
            except Error:
                cursor.execute("SELECT * FROM personas")
            filas = cursor.fetchall()
            return {"status": True, "mensaje": "Personas obtenidas", "data": filas}
        except Error as e:
            return {"status": False, "mensaje": str(e), "data": []}
        finally:
            cursor.close()
            self.cerrar(conexion)

    def _find_person_table_and_id(self, conexion):
        """Detecta si la tabla de personas se llama 'persona' o 'personas' y si la PK es 'id' o 'persona_id'.
        Devuelve una tupla (tabla, columna_id) o (None, None) si no se encuentra.
        """
        try:
            cursor = conexion.cursor()
            # Consultar INFORMATION_SCHEMA para comprobar existencia de tablas y columnas
            query = (
                "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_SCHEMA = %s AND TABLE_NAME IN ('persona','personas')"
            )
            cursor.execute(query, (self.database,))
            rows = cursor.fetchall()

            # Construir mapa table -> list of column names (original case)
            cols_by_table = {}
            for r in rows:
                tbl = r[0]
                col = r[1]
                cols_by_table.setdefault(tbl, []).append(col)
                try:
                    print(f"[DEBUG] _find_person_table_and_id cols_by_table={cols_by_table}")
                except Exception:
                    pass

            # Lista de candidatos (en orden de preferencia), comparar en minúsculas
            candidates = ['id', 'persona_id', 'personaid', 'personaid']

            # Prioridad por tabla y por candidato
            for tbl in ['persona', 'personas']:
                cols = cols_by_table.get(tbl, [])
                cols_lower_map = {c.lower(): c for c in cols}
                for cand in candidates:
                    if cand in cols_lower_map:
                        return tbl, cols_lower_map[cand]

            return None, None
        except Exception:
            return None, None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def actualizar_persona(self, persona_id, campos: dict):
        """Actualiza campos de una persona dado su id. campos es un dict columna->valor."""
        if not campos:
            return {"status": False, "mensaje": "No hay campos para actualizar"}
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}
        try:
            cursor = conexion.cursor()
            # Construir SET dinámico
            columnas = []
            valores = []
            for k, v in campos.items():
                columnas.append(f"{k} = %s")
                valores.append(v)
            # Determinar tabla y columna id correcta
            table, id_col = self._find_person_table_and_id(conexion)
            if not table or not id_col:
                return {"status": False, "mensaje": "No se pudo detectar la tabla/columna de personas en la base de datos"}
            valores.append(persona_id)
            sql = f"UPDATE {table} SET {', '.join(columnas)} WHERE {id_col} = %s"
            # Debug: imprimir SQL y parámetros
            try:
                print(f"[SQL DEBUG] actualizar_persona -> table={table}, id_col={id_col}, sql={sql}, params={tuple(valores)}")
            except Exception:
                pass
            cursor.execute(sql, tuple(valores))
            conexion.commit()
            # Informar si no se afectó ninguna fila (id inexistente quizá)
            rows = cursor.rowcount if hasattr(cursor, 'rowcount') else None
            if rows == 0:
                return {"status": False, "mensaje": f"No se actualizó ninguna fila (id={persona_id}). SQL: {sql}", "rows_affected": 0}
            return {"status": True, "mensaje": "Registro actualizado", "rows_affected": rows}
        except Error as e:
            return {"status": False, "mensaje": str(e)}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def eliminar_persona(self, persona_id):
        """Elimina una persona por id."""
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}
        try:
            cursor = conexion.cursor()
            table, id_col = self._find_person_table_and_id(conexion)
            if not table or not id_col:
                return {"status": False, "mensaje": "No se pudo detectar la tabla/columna de personas en la base de datos"}
            sql = f"DELETE FROM {table} WHERE {id_col} = %s"
            try:
                print(f"[SQL DEBUG] eliminar_persona -> table={table}, id_col={id_col}, sql={sql}, params={(persona_id,)}")
            except Exception:
                pass
            cursor.execute(sql, (persona_id,))
            conexion.commit()
            rows = cursor.rowcount if hasattr(cursor, 'rowcount') else None
            if rows == 0:
                return {"status": False, "mensaje": f"No se eliminó ninguna fila (id={persona_id}). SQL: {sql}", "rows_affected": 0}
            return {"status": True, "mensaje": "Registro eliminado", "rows_affected": rows}
        except Error as e:
            return {"status": False, "mensaje": str(e)}
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
