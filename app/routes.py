from flask import Blueprint, request, jsonify
import pymysql
import os
import json

bp = Blueprint('main', __name__)

def get_db_connection():
    connection = pymysql.connect(
        host='pnpdb.ctmkgk4os29w.ap-northeast-2.rds.amazonaws.com',
        port=3306,
        user='root',
        password='xkzhdizl12',
        db='pnpDB',
        charset='utf8'
    )
    return connection

def load_sql(file_path):
    with open(file_path, 'r') as file:
        sql = file.read()
        
    return sql


@bp.route('/upload-image', methods=['POST'])
def upload_image():
    data = request.json
    uploadImgUrl = data.get('uploadImgUrl')
    userId = 'skam123'

    if not uploadImgUrl or not userId:
        return jsonify({'code': 101, 'message': 'Missing uploadImgUrl or userId'})

    sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'insert_user_image.sql')
    insert_sql = load_sql(sql_file_path)
    print(insert_sql)
    connection = get_db_connection()
    print(connection)

    try:
        with connection.cursor() as cursor:
            for obj in uploadImgUrl:
                image = obj.split('photo/')[1]
                cursor.execute(insert_sql, (image, userId))
            connection.commit()
    finally:
        connection.close()

    return jsonify({
        'code': 200,
        'message': 'Image Uploaded Successfully'
    })

@bp.route('/read-all-img', methods=['POST'])
def read_all_img():
    data = request.json
    userId = data.get('id')
    
    
    if not userId:
        return jsonify({'code': 101, 'message': 'Missing userId'})

    sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'read_all_image.sql')
    read_all_sql = load_sql(sql_file_path)
    
    connection = get_db_connection()
    result = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(read_all_sql, (userId))
            for data in cursor.fetchall():
                result.append(data)
    except:
        return jsonify({
            'code': 501,
            'message': 'Sql Error from occured that wrong some parameters'
        })
    finally:
        connection.close()
        
    
    return jsonify({
        'code': 200,
        'data': result,
        'message': 'Read Data Successfully'
    })

@bp.route('/write-poem', methods=['POST'])
def write_poem():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    writer = data.get('writer')
    id= data.get('id')
    
    if not title or not content or not writer or not id:
        return jsonify({'code': 101, 'message': 'Missing title or content or writer or id'})
    
    sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'write_poem.sql')
    write_poem = load_sql(sql_file_path)
    
    connection = get_db_connection()
    
    try:
        with connection.cursor() as corsor:
            corsor.execute(write_poem, (title, content, writer, id))
            connection.commit()
    except:
        return jsonify({
            'code': 501,
            'message': 'Sql Error from occured that wrong some parameters'
        })
    finally:
        connection.close()
    
    return jsonify({
        'code': 200,
        'message': 'Write Data Successfully'
    })
    
    
     
    
    