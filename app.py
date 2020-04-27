from flask import Flask, jsonify, request, redirect, render_template, flash
from products import products
from flask_mysqldb import MySQL


def create_app():
    app = Flask(__name__)
    return app


app = create_app()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)

# Session en FLASK
app.secret_key = 'mysecretkey'


@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute('select name,price,stock,id from Products')
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', products=data)


@app.route('/add/product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Products (name,price,stock) VALUES (%s,%s,%s);",
                [name, price, stock])
    mysql.connection.commit()
    flash('Success Insert')
    return redirect('/')


@app.route('/edit/product/<int:id>', methods=['GET'])
def edit_product(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "select name,price,stock,id from Products where id like %s", [id])
    data = cur.fetchall()
    cur.close()

    return render_template('edit.html', product=data[0])


@app.route('/edit/product/<int:id>', methods=['POST'])
def edit_product_post(id):
    name, price, stock = request.form['name'], request.form['price'], request.form['stock']

    cur = mysql.connection.cursor()
    cur.execute('UPDATE Products SET name = %s, price = %s, stock =%s WHERE id like %s', [
                name, price, stock, id])
    cur.connection.commit()
    return redirect('/')

@app.route('/delete/product/<int:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM Products WHERE id LIKE %s',[id])    
    cur.connection.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
