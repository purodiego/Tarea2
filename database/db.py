import pymysql
from datetime import datetime

DB_NAME = "tarea2"
DB_USERNAME = "root"
DB_PASSWORD = "Manzana12345"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn



def insertar_actividad(comuna_id, sector, nombre, email, celular, fecha_inicio, fecha_termino, descripcion):
	conn = get_conn()
	cursor = conn.cursor()
	sql = """
	INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
	"""
	cursor.execute(sql, (comuna_id, sector, nombre, email, celular, fecha_inicio, fecha_termino, descripcion))
	actividad_id = cursor.lastrowid
	conn.commit()
	cursor.close()
	conn.close()
	return actividad_id

def insertar_contacto(nombre_contacto, identificador, actividad_id):
	conn = get_conn()
	cursor = conn.cursor()
	sql = """
	INSERT INTO contactar_por (nombre, identificador, actividad_id)
	VALUES (%s, %s, %s)
	"""
	cursor.execute(sql, (nombre_contacto, identificador, actividad_id))
	conn.commit()
	cursor.close()
	conn.close()

def insertar_tema(tema, glosa_otro, actividad_id):
	conn = get_conn()
	cursor = conn.cursor()
	sql = """
	INSERT INTO actividad_tema (tema, glosa_otro, actividad_id)
	VALUES (%s, %s, %s)
	"""
	cursor.execute(sql, (tema, glosa_otro, actividad_id))
	conn.commit()
	cursor.close()
	conn.close()

def insertar_foto(ruta_archivo, nombre_archivo, actividad_id):
	conn = get_conn()
	cursor = conn.cursor()
	sql = """
	INSERT INTO foto (ruta_archivo, nombre_archivo, actividad_id)
	VALUES (%s, %s, %s)
	"""
	cursor.execute(sql, (ruta_archivo, nombre_archivo, actividad_id))
	conn.commit()
	cursor.close()
	conn.close()



def get_actividades_paginadas(offset=0, limit=5):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            a.id,
            a.dia_hora_inicio,
            a.dia_hora_termino,
            c.nombre AS comuna,
            a.sector,
            at.tema,
            at.glosa_otro,
            a.nombre AS organizador,
            COUNT(f.id) AS total_fotos
        FROM actividad a
        JOIN comuna c ON a.comuna_id = c.id
        LEFT JOIN actividad_tema at ON at.actividad_id = a.id
        LEFT JOIN foto f ON f.actividad_id = a.id
        GROUP BY a.id, a.dia_hora_inicio, a.dia_hora_termino, c.nombre, a.sector, at.tema, at.glosa_otro, a.nombre
        ORDER BY a.id DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()
    return actividades

def get_actividad_por_id(actividad_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
			a.dia_hora_inicio,
            a.dia_hora_termino,
			c.nombre AS comuna,
            r.nombre AS region,
            a.sector,
			at.tema,
			at.glosa_otro,
			a.nombre,
			a.email,
            cp.nombre AS tipo_contacto,       
			cp.identificador,
            a.descripcion,
            f.ruta_archivo
        FROM actividad a
        JOIN comuna c ON a.comuna_id = c.id
        JOIN region r ON c.region_id = r.id
        LEFT JOIN contactar_por cp ON cp.actividad_id = a.id
        LEFT JOIN actividad_tema at ON at.actividad_id = a.id
        LEFT JOIN foto f ON f.actividad_id = a.id
        WHERE a.id = %s
    """, (actividad_id,))
    actividad = cursor.fetchone()
    cursor.close()
    conn.close()
    return actividad



def get_ultimas_actividades(limit=5):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
        a.id,
        a.dia_hora_inicio,
        a.dia_hora_termino,
        c.nombre AS comuna,
        a.sector AS sector,
        at.tema,
        at.glosa_otro,
        (SELECT f.ruta_archivo FROM foto f WHERE f.actividad_id = a.id LIMIT 1) AS ruta_archivo
    FROM actividad a
    JOIN comuna c ON a.comuna_id = c.id
    LEFT JOIN actividad_tema at ON at.actividad_id = a.id
    ORDER BY a.id DESC
    LIMIT %s
    """, (limit,))
    actividades = cursor.fetchall()
    cursor.close()
    conn.close()
    return actividades

def get_total_actividades():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM actividad")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def insertar_comentario(actividad_id, nombre, texto):
    conn = get_conn()
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO comentario (actividad_id, nombre, texto, fecha)
        VALUES (%s, %s, %s, %s)
    """, (actividad_id, nombre, texto, fecha_actual))

    conn.commit()
    cursor.close()
    conn.close()



def get_comentarios_por_actividad(actividad_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, texto
        FROM comentario
        WHERE actividad_id = %s
        ORDER BY id DESC
    """, (actividad_id,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"nombre": n, "texto": t} for n, t in resultados]


