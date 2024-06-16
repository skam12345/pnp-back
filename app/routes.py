from flask import Blueprint, request, jsonify
import pymysql
import os
from app.constant import POEM_LIMIT, VIEW_PAGE_LIMIT
import math
import arrow


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
    write_date = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    
    if not title or not content or not writer or not id:
        return jsonify({'code': 101, 'message': 'Missing title or content or writer or id or'})
    
    sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'write_poem.sql')
    write_poem = load_sql(sql_file_path)
    
    connection = get_db_connection()
    
    try:
        with connection.cursor() as corsor:
            corsor.execute(write_poem, (title, content, writer, id, write_date))
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

@bp.route('/read-paging-poem', methods=['POST'])
def read_paging_poem():
    data = request.json
    id = data.get('id')
    page = data.get('page')
    
    if not id or not page:
        return jsonify({'code': 101, 'message': 'Missing id or page'})

    
    
    sql_paging_path = os.path.join(os.path.dirname(__file__), 'sql', 'read_paging_poem.sql')
    sql_read_all_path = os.path.join(os.path.dirname(__file__), 'sql', 'read_all_poem.sql')
    read_paging_poem = load_sql(sql_paging_path)
    read_all_poem = load_sql(sql_read_all_path)
    
    connection = get_db_connection()
    
    result = []
    first_paging = 0
    last_paging= 0
    try:
        with connection.cursor() as cursor:
            cursor.execute(read_all_poem)
            all_poem = cursor.fetchone()
            number_all_poem  = int(all_poem[0])
            first = (int(page) -1) * POEM_LIMIT
            last = first + POEM_LIMIT - 1 
            if last > number_all_poem:
                last = number_all_poem
            
            all_count_page = math.ceil(number_all_poem / POEM_LIMIT)
            
            page_group = math.ceil(int(page) / VIEW_PAGE_LIMIT)
            
            if math.ceil(number_all_poem / POEM_LIMIT) == 0:
                all_count_page += 1
            if number_all_poem % POEM_LIMIT < 10 and number_all_poem > 10:
                all_count_page += 1
            if all_count_page - (VIEW_PAGE_LIMIT - 1) <= 0:
                first_paging = 1
            else :
                first_paging = all_count_page - (VIEW_PAGE_LIMIT - 1)
            
            if page_group * VIEW_PAGE_LIMIT > all_count_page:
                last_paging = all_count_page
            else :
                last_paging = page_group * VIEW_PAGE_LIMIT
            
            cursor.execute(read_paging_poem, (id, first, last))
            for data in cursor.fetchall():
                result.append({
                    'poemSeq': data[0],
                    'title': data[1],
                    'writer': data[2],
                    'write_date': data[3],
                    'views': data[4],
                    'goods': data[5],
                })
                    
    except:
        return jsonify({
                'code': 501,
                'message': 'Sql Error from occured that wrong some parameters'
            })
    finally:
        connection.close()
    
    return jsonify({
        'code': 200,
        'data': {
            'poem': result,
            'first_paging': first_paging,
            'last_paging': last_paging
        },
        'message': 'Read Data Successfully'
    })

@bp.route('/read-one-poem', methods=['POST'])
def read_one_poem():
    data = request.json
    poemSeq = data.get('poemSeq')
    
    if not poemSeq:
        return jsonify({'code': 101, 'message': 'Missing poemSeq'})
    
    sql_file_path = os.path.join(os.path.dirname(__file__), 'sql', 'read_one_poem.sql')
    write_poem = load_sql(sql_file_path)
    
    connection = get_db_connection()
    result = {}
    try:
        with connection.cursor() as corsor:
            corsor.execute(write_poem, (poemSeq))
            data = corsor.fetchone()
            result = {
                'poemSeq': data[0],
                'title': data[1],
                'content': data[2],
                'writer': data[3],
                'id': data[4],
            }
            
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
    
    
    
    
    
     
    
    