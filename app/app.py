from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'awardData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': ' Sakthi '}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, awards=result)


@app.route('/view/<int:award_id>', methods=['GET'])
def record_view(award_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE id=%s', award_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', award=result[0])


@app.route('/edit/<int:award_id>', methods=['GET'])
def form_edit_get(award_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE id=%s', award_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', award=result[0])


@app.route('/edit/<int:award_id>', methods=['POST'])
def form_update_post(award_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('year'), request.form.get('age'), request.form.get('name'),
                 request.form.get('movie'), award_id)
    sql_update_query = """UPDATE oscarAgeMale t SET t.year = %s, t.age = %s, t.name = %s, t.movie = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/awards/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar AwardForm')


@app.route('/awards/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('year'), request.form.get('age'),
                 request.form.get('name'), request.form.get('movie'))
    sql_insert_query = """INSERT INTO oscarAgeMale (id,`year`,age,`name`,movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:award_id>', methods=['POST'])
def form_delete_post(award_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscarAgeMale WHERE id = %s """
    cursor.execute(sql_delete_query, award_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/awards', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/awards/<int:award_id>', methods=['GET'])
def api_retrieve(award_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE Id=%s', award_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/awards/<int:award_id>', methods=['PUT'])
def api_edit(award_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['year'], content['age'], content['name'],
                 content['movie'], award_id)
    sql_update_query = """UPDATE oscarAgeMale t SET t.year = %s, t.age = %s, t.name = %s, t.movie = 
        %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/awards', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['id'], content['year'], content['age'], content['name'],
                 content['movie'])
    sql_insert_query = """INSERT INTO oscarAgeMale (id,year,age,name,movie) VALUES (%s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/awards/<int:award_id>', methods=['DELETE'])
def api_delete(award_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscarAgeMale WHERE Id = %s """
    cursor.execute(sql_delete_query, award_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
