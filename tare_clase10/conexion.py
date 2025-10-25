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

    def actualizar_docente_completo(self, docente_id, datos):
        """
        Actualiza los datos de un docente y su persona asociada.
        """
        print(f"🔄 Iniciando actualización para docente_id: {docente_id}")
        print(f"📝 Datos recibidos para actualizar: {datos}")
        
        if not docente_id:
            return {"status": False, "mensaje": "ID de docente no proporcionado"}
            
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}

        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Convertir el docente_id a entero si es necesario
            try:
                docente_id = int(docente_id)
            except (TypeError, ValueError):
                return {"status": False, "mensaje": "ID de docente inválido"}

            # 1. Obtener el persona_id
            cursor.execute("""
                SELECT persona_id 
                FROM docentes 
                WHERE docente_id = %s
            """, (docente_id,))
            
            resultado = cursor.fetchone()
            if not resultado:
                return {"status": False, "mensaje": "No se encontró el docente"}
            
            persona_id = resultado['persona_id']

            print(f"🔍 Encontrado persona_id: {persona_id}")

            # 2. Actualizar la tabla personas
            query_personas = """
                UPDATE personas 
                SET nombres = %s,
                    apellidos = %s
                WHERE persona_id = %s
            """
            valores_personas = (datos['nombres'], datos['apellidos'], persona_id)
            print(f"📝 Actualizando personas con: {valores_personas}")
            cursor.execute(query_personas, valores_personas)
            print(f"✅ Personas actualizadas: {cursor.rowcount} filas")

            # 3. Actualizar la tabla docentes
            query_docentes = """
                UPDATE docentes 
                SET codigo_docente = %s,
                    activo = %s,
                    observaciones = %s,
                    actualizado_en = CURRENT_TIMESTAMP
                WHERE docente_id = %s
            """
            valores_docentes = (
                datos['codigo_docente'],
                datos['activo'],
                datos['observaciones'],
                docente_id
            )
            print(f"📝 Actualizando docentes con: {valores_docentes}")
            cursor.execute(query_docentes, valores_docentes)
            print(f"✅ Docentes actualizados: {cursor.rowcount} filas")

            # Confirmar los cambios
            conexion.commit()
            
            return {
                "status": True,
                "mensaje": "Docente actualizado correctamente"
            }

        except Exception as e:
            if conexion:
                conexion.rollback()
            return {"status": False, "mensaje": f"Error al actualizar: {str(e)}"}
            
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

    def eliminar_docente(self, docente_id: int):
        """Elimina un docente de la base de datos."""
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}

        try:
            cursor = conexion.cursor()
            
            # Primero desactivamos el docente en lugar de eliminarlo físicamente
            query = """
                UPDATE docentes 
                SET activo = FALSE,
                    actualizado_en = CURRENT_TIMESTAMP
                WHERE docente_id = %s
            """
            cursor.execute(query, (docente_id,))
            conexion.commit()
            
            return {
                "status": True,
                "mensaje": "Docente desactivado correctamente"
            }

        except Error as e:
            if conexion:
                conexion.rollback()
            return {"status": False, "mensaje": f"Error al desactivar el docente: {str(e)}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

    def actualizar_docente(self, docente_id: int, datos: dict):
        """Actualiza los datos de un docente."""
        print(f"🔍 Iniciando actualización para docente_id: {docente_id}")
        print(f"📝 Datos recibidos: {datos}")
        conexion = self.conectar()
        if not conexion:
            return {"status": False, "mensaje": "Error al conectar con la base de datos"}

        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Primero obtenemos el persona_id asociado al docente
            print(f"🔍 Buscando persona_id para docente_id: {docente_id}")
            cursor.execute("SELECT persona_id FROM docentes WHERE docente_id = %s", (docente_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                print("❌ No se encontró el docente en la base de datos")
                return {"status": False, "mensaje": "No se encontró el docente"}
            
            print(f"✅ Encontrado persona_id: {resultado['persona_id']}")
            persona_id = resultado['persona_id']
            
            # Actualizamos la tabla personas
            if datos.get('nombres') or datos.get('apellidos'):
                print("📝 Actualizando datos personales...")
                query_persona = """
                    UPDATE personas 
                    SET nombres = %s, 
                        apellidos = %s
                    WHERE persona_id = %s
                """
                valores = (datos.get('nombres'), datos.get('apellidos'), persona_id)
                print(f"SQL: {query_persona}")
                print(f"Valores: {valores}")
                cursor.execute(query_persona, valores)
                print(f"✅ Filas afectadas en personas: {cursor.rowcount}")
            
            # Actualizamos la tabla docentes
            print("📝 Actualizando datos del docente...")
            query_docente = """
                UPDATE docentes 
                SET codigo_docente = %s,
                    activo = %s,
                    observaciones = %s,
                    actualizado_en = CURRENT_TIMESTAMP
                WHERE docente_id = %s
            """
            valores_docente = (
                datos.get('codigo_docente'),
                datos.get('activo', True),
                datos.get('observaciones', ''),
                docente_id
            )
            print(f"SQL: {query_docente}")
            print(f"Valores: {valores_docente}")
            cursor.execute(query_docente, valores_docente)
            print(f"✅ Filas afectadas en docentes: {cursor.rowcount}")
            
            conexion.commit()
            return {
                "status": True,
                "mensaje": "Docente actualizado correctamente"
            }
            
        except Exception as e:
            if conexion:
                conexion.rollback()
            return {
                "status": False,
                "mensaje": f"Error al actualizar: {str(e)}"
            }
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)

        try:
            cursor = conexion.cursor(dictionary=True)
            
            # Primero actualizamos la tabla personas
            query_persona = """
                UPDATE personas p
                INNER JOIN docentes d ON p.persona_id = d.persona_id
                SET p.nombres = %s, p.apellidos = %s
                WHERE d.docente_id = %s
            """
            cursor.execute(query_persona, (
                datos.get("nombres"),
                datos.get("apellidos"),
                docente_id
            ))

            # Luego actualizamos la tabla docentes
            query_docente = """
                UPDATE docentes
                SET codigo_docente = %s,
                    activo = %s,
                    observaciones = %s,
                    actualizado_en = CURRENT_TIMESTAMP
                WHERE docente_id = %s
            """
            cursor.execute(query_docente, (
                datos.get("codigo_docente"),
                datos.get("activo"),
                datos.get("observaciones"),
                docente_id
            ))

            conexion.commit()
            return {
                "status": True,
                "mensaje": "Docente actualizado correctamente"
            }

        except Error as e:
            if conexion:
                conexion.rollback()
            return {"status": False, "mensaje": f"Error en la actualización: {str(e)}"}
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.cerrar(conexion)
