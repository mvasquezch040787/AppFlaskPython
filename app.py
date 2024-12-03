from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Obtén la configuración de la base de datos desde una variable de entorno
db_config = {
    'host': os.getenv('DB_HOST', 'autorack.proxy.rlwy.net'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'pIzwVCKPDraXvMZYRsGfPDbSKGfEkStT'),
    'database': os.getenv('DB_NAME', 'gestion_inventarios'),
    'port': int(os.getenv('DB_PORT', 48564))
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta para gestionar productos
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(productos)

    elif request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                       (data['nombre'], data['cantidad'], data['precio']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Producto creado'}), 201

if __name__ == '__main__':
    app.run(debug=True)
