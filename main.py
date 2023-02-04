import base64
import json
import os
from http import HTTPStatus

import cv2
import pymysql
from flask import Flask, redirect, request, jsonify, url_for, abort
from flask_cors import CORS

from config import DevelopmentConfig as devconf
from db import Database

host = os.environ.get('FLASK_SERVER_HOST', devconf.HOST)
port = os.environ.get('FLASK_SERVER_PORT', devconf.PORT)
version = str(devconf.VERSION).lower()
url_prefix = str(devconf.URL_PREFIX).lower()
route_prefix = f"/{url_prefix}/{version}"
qrDecoder = cv2.QRCodeDetector()
directory = r'F:\Sidna\pythonProject-BE-Wedding\image'


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={f"{route_prefix}/*": {"origins": "*"}})
    app.config.from_object(devconf)
    return app


def get_response_msg(data, status_code):
    message = {
        'status': status_code,
        'data': data if data else 'No records found'
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg


app = create_app()
wsgi_app = app.wsgi_app
db = Database(devconf)


## ==============================================[ Routes - Start ]
## /api/v1/tambah_tamu
@app.route(f"{route_prefix}/tambah_tamu", methods=['POST'])
def tambah_tamu():
    if request.method == "POST":
        nama = request.args.get('nama')
        alamat = request.args.get('alamat')
        jenis_tamu = request.args.get('jenis_tamu')
        query = f"INSERT INTO tb_guests (name, alamat, jenis_tamu) VALUES ('{nama}','{alamat}','{jenis_tamu}')"
        db.run_query(query=query)
        record = "data berhasil ditambahkan"
        response = get_response_msg(record, HTTPStatus.OK)
        db.close_connection()
        return response
    else:
        response = get_response_msg("error", HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


## /api/v1/lihat_data_tamu
@app.route(f"{route_prefix}/lihat_data_tamu", methods=['GET'])
def getdata():
    try:
        query = f"SELECT * FROM tb_guests"
        records = db.run_query(query=query)
        response = get_response_msg(records, HTTPStatus.OK)
        db.close_connection()
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/edit_data_tamu
@app.route(f"{route_prefix}/edit_data_tamu", methods=['POST'])
def editdata():
    try:
        id = request.args.get('id')
        nama = request.args.get('nama')
        alamat = request.args.get('alamat')
        jenis_tamu = request.args.get('jenis_tamu')
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        else:
            query = f"UPDATE tb_guests SET name='{nama}',alamat='{alamat}',jenis_tamu='{jenis_tamu}' WHERE id={id}"
            records = db.run_query(query=query)
            response = get_response_msg(records, HTTPStatus.OK)
            db.close_connection()
            return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/lihat_data_satu_tamu
@app.route(f"{route_prefix}/lihat_data_satu_tamu", methods=['GET'])
def getcitycodes():
    if request.method == 'GET':
        try:
            tamu_id = request.args.get('id')
            query = f"SELECT * FROM tb_guests WHERE id={tamu_id}"
            records = db.run_query(query=query)
            response = get_response_msg(records, HTTPStatus.OK)
            db.close_connection()
            return response
        except pymysql.MySQLError as sqle:
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
        except Exception as e:
            abort(HTTPStatus.BAD_REQUEST, description=str(e))
    else:
        response = get_response_msg("error", HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


## /api/1.0/ubah_kehadiran
@app.route(f"{route_prefix}/ubah_kehadiran", methods=['POST'])
def ubah_kehadiran():
    id = request.args.get('id')
    kehadiran = request.args.get('kehadiran')
    query = f"UPDATE tb_guests SET kehadiran='{kehadiran}' WHERE id={id}"
    records = db.run_query(query=query)
    response = get_response_msg(records, HTTPStatus.OK)
    return response


## /api/1.0/getsummary
@app.route(f"{route_prefix}/getsummary", methods=['GET'])
def getsummary():
    try:
        query = f"SELECT * FROM tb_guests WHERE kehadiran='BELUM KONFIRMASI'"
        query1 = f"SELECT * FROM tb_guests WHERE kehadiran='AKAN HADIR'"
        query2 = f"SELECT * FROM tb_guests WHERE kehadiran='TIDAK HADIR'"
        query3 = f"SELECT * FROM tb_guests WHERE kehadiran='SUDAH HADIR'"
        records = db.run_query(query=query)
        records1 = db.run_query(query=query1)
        records2 = db.run_query(query=query2)
        records3 = db.run_query(query=query3)
        response = [len(records), len(records1), len(records2), len(records3)]
        response = get_response_msg(response, HTTPStatus.OK)
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/1.0/search
@app.route(f"{route_prefix}/search", methods=['GET'])
def search():
    try:
        params = request.args.get('params')
        query = f"SELECT * FROM tb_guests WHERE name LIKE '%{params}%'"
        records = db.run_query(query=query)
        response = get_response_msg(records, HTTPStatus.OK)
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## /api/v1/health
@app.route(f"{route_prefix}/health", methods=['GET'])
def health():
    try:
        db_status = "Connected to DB" if db.db_connection_status else "Not connected to DB"
        response = get_response_msg("I am fine! " + db_status, HTTPStatus.OK)
        return response
    except pymysql.MySQLError as sqle:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=str(sqle))
    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=str(e))


## QRCode reader
@app.route(f"{route_prefix}/readqr", methods=['POST'])
def qr_reader():
    try:
        img = json.loads(request.data)
        imgg = img['base64']
        name = str(img['time'])
        B64_decode = base64.b64decode(imgg)
        path = f'F:\Sidna\pythonProject-BE-Wedding\image'

        # write the decoded data back to original format in  file
        img_file = open(path + '\image_' + name + '.jpg', 'wb')
        img_file.write(B64_decode)
        img_file.close()

        # response = get_response_msg(str(img_file11), HTTPStatus.OK)
        img_arr = cv2.imread(path + '\image_' + name + '.jpg')

        # Detect and decode the qrcode
        data, bbox, rectifiedImage = qrDecoder.detectAndDecode(img_arr)
        print(len(data))
        if len(data) > 0:
            output = format(data)
            query = f"UPDATE tb_guests SET kehadiran='SUDAH HADIR' WHERE id={output}"
            query2 = f"SELECT * FROM tb_guests WHERE id={output}"
            db.run_query(query=query)
            records = db.run_query(query=query2)
            response = get_response_msg(records, HTTPStatus.OK)
            print(records)
            return response
        else:
            response = get_response_msg("QR Code not detected", HTTPStatus.NOT_FOUND)
            return response
    except:
        response = get_response_msg("Internal Error", HTTPStatus.INTERNAL_SERVER_ERROR)
        return response


## /
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('health'))


## =================================================[ Routes - End ]

## ================================[ Error Handler Defined - Start ]
## HTTP 404 error handler
@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
    return get_response_msg(data=str(e), status_code=HTTPStatus.NOT_FOUND)


## HTTP 400 error handler
@app.errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(e):
    return get_response_msg(str(e), HTTPStatus.BAD_REQUEST)


## HTTP 500 error handler
@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(e):
    return get_response_msg(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


## ==================================[ Error Handler Defined - End ]

if __name__ == '__main__':
    ## Launch the application 
    app.run(host=host, port=port)
