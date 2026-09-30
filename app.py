from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos (Puerto 3307)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="angel213",  # Coloca tu contraseña de MySQL si la tienes configurada
        database="cafeteria_universitaria"
    )

# =========================================================
# RUTA PRINCIPAL
# =========================================================
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# ENTIDAD: CLIENTES
# ==========================================
@app.route('/clientes')
def listar_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cliente")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cliente (nombre, email, telefono) VALUES (%s, %s, %s)",
            (nombre, email, telefono)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/clientes')

    return render_template('agregar_cliente.html')

@app.route('/actualizar_cliente/<int:id>', methods=['GET', 'POST'])
def actualizar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        cursor.execute("""
            UPDATE cliente 
            SET nombre=%s, email=%s, telefono=%s 
            WHERE idCliente=%s
        """, (nombre, email, telefono, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/clientes')

    cursor.execute("SELECT * FROM cliente WHERE idCliente = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('actualizar_cliente.html', cliente=cliente)

@app.route('/borrar_cliente/<int:id>')
def borrar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cliente WHERE idCliente = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/clientes')

# ==========================================
# ENTIDAD: PRODUCTOS
# ==========================================
@app.route('/productos')
def listar_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Producto")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        # 1. Leer los datos enviando el formulario
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        conn = get_db_connection()
        cursor = conn.cursor()

        # 2. IMPORTANTE: Usar nombre_producto (el nombre real en tu base de datos)
        sql = "INSERT INTO Producto (nombre_producto, categoria, precio, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, categoria, precio, stock))

        # 3. IMPORTANTE: Confirmar los cambios en MySQL
        conn.commit()

        cursor.close()
        conn.close()

        # 4. Redirigir a la lista de productos
        return redirect('/productos')

    return render_template('agregar_producto.html')

@app.route('/actualizar_producto/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # 1. Leer los datos del formulario
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        stock = request.form['stock']

        # 2. Consulta SQL usando el nombre correcto de la columna: nombre_producto
        sql = """
            UPDATE Producto 
            SET nombre_producto = %s, categoria = %s, precio = %s, stock = %s 
            WHERE idProducto = %s
        """
        cursor.execute(sql, (nombre, categoria, precio, stock, id))
        
        # 3. Confirmar los cambios en MySQL
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/productos')

    # Si es GET, cargamos los datos del producto para mostrarlos en el formulario
    cursor.execute("SELECT * FROM Producto WHERE idProducto = %s", (id,))
    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('actualizar_producto.html', producto=producto)

@app.route('/borrar_producto/<int:id>')
def borrar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Producto WHERE idProducto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/productos')

# ==========================================
# ENTIDAD: PEDIDOS
# ==========================================
@app.route('/pedidos')
def listar_pedidos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.idPedido, c.nombre AS cliente, p.fecha_pedido, p.estado 
        FROM Pedido p 
        JOIN cliente c ON p.idCliente = c.idCliente
    """)
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/agregar_pedido', methods=['GET', 'POST'])
def agregar_pedido():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        estado = request.form['estado']

        cursor.execute(
            "INSERT INTO Pedido (idCliente, fecha_pedido, estado) VALUES (%s, %s, %s)",
            (id_cliente, fecha, estado)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/pedidos')

    cursor.execute("SELECT idCliente, nombre FROM cliente")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('agregar_pedido.html', clientes=clientes)
@app.route('/actualizar_pedido/<int:id>', methods=['GET', 'POST'])
def actualizar_pedido(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        fecha = request.form['fecha']
        estado = request.form['estado']

        cursor.execute("""
            UPDATE Pedido 
            SET idCliente=%s, fecha_pedido=%s, estado=%s 
            WHERE idPedido=%s
        """, (id_cliente, fecha, estado, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/pedidos')

    cursor.execute("SELECT * FROM Pedido WHERE idPedido = %s", (id,))
    pedido = cursor.fetchone()

    cursor.execute("SELECT idCliente, nombre FROM cliente")
    clientes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('actualizar_pedido.html', pedido=pedido, clientes=clientes)


@app.route('/borrar_pedido/<int:id>')
def borrar_pedido(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Borrar primero registros en detalle_pedido por la clave foránea
        cursor.execute("DELETE FROM detalle_pedido WHERE idPedido = %s", (id,))
        # Borrar el pedido principal
        cursor.execute("DELETE FROM Pedido WHERE idPedido = %s", (id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar pedido: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/pedidos')

# ==========================================
# ENTIDAD: DETALLE PEDIDO
# ==========================================
@app.route('/detalles')
def listar_detalles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.idDetalle, d.idPedido, pr.nombre AS producto, d.cantidad, d.subtotal 
        FROM detalle_pedido d 
        JOIN Producto pr ON d.idProducto = pr.idProducto
    """)
    detalles = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('detalles.html', detalles=detalles)

if __name__ == '__main__':
    app.run(debug=True)