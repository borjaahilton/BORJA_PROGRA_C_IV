from conexion import ConexionDB

if __name__ == '__main__':
    db = ConexionDB()
    res = db.listar_tablas()
    print(res)
