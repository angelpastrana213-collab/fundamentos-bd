from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,                   
        user="root",
        password="angel213",                  
        database="cafeteria_universitaria"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            idProducto AS ID, 
            nombre_producto AS Producto, 
            categoria AS Categoría, 
            precio AS Precio, 
            stock AS Stock 
        FROM Producto
    """)
    lista_productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=lista_productos)

@app.route('/pedidos')
def pedidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT 
        p.idPedido AS id_pedido,
        c.nombre AS cliente,
        p.fecha_pedido AS fecha,
        p.estado AS estado,
        COALESCE(SUM(dp.cantidad * dp.precio_unitario), 0) AS total
    FROM Pedido p
    JOIN cliente c ON p.idcliente = c.idCliente
    LEFT JOIN detalle_pedido dp ON p.idPedido = dp.idpedido
    GROUP BY p.idPedido, c.nombre, p.fecha_pedido, p.estado
    """
    
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    

    gran_total = sum(ped['total'] for ped in lista_pedidos)
    
    cursor.close()
    conn.close()
    
    
    return render_template('pedidos.html', pedidos=lista_pedidos, gran_total=gran_total)
    
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('pedidos.html', pedidos=lista_pedidos)
  
    
    cursor.execute(query)
    lista_pedidos = cursor.fetchall()
    
    # Calcula la suma total acumulada de todos los pedidos
    gran_total = sum(ped['total'] for ped in lista_pedidos)
    
    cursor.close()
    conn.close()
    
    return render_template('pedidos.html', pedidos=lista_pedidos, gran_total=gran_total)

if __name__ == '__main__':
    app.run(debug=True)