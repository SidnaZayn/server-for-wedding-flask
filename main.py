import base64
import json
from http import HTTPStatus

import cv2
from flask import Flask, redirect, request, jsonify, url_for
from flask_cors import CORS
from datetime import datetime
from mysql.connector import Error
from mysql.connector import pooling

from config import DevelopmentConfig as devconf

version = str(devconf.VERSION).lower()
url_prefix = str(devconf.URL_PREFIX).lower()
route_prefix = f"/{url_prefix}/{version}"
qrDecoder = cv2.QRCodeDetector()
directory = r'F:\Sidna\pythonProject-BE-Wedding\image'

app = Flask(__name__)
cors = CORS(app, resources={f"{route_prefix}/*": {"origins": "*"}})
x = datetime.now()
x = str(x)
connection_pool = pooling.MySQLConnectionPool(pool_name="pynative_pool",
                                              pool_size=10,
                                              pool_reset_session=True,
                                              host='127.0.0.1',
                                              database='undanga4_wedding',
                                              user='root',
                                              password='')


def get_response_msg(data, status_code):
    message = {
        'status': status_code,
        'data': data if data else 'No records found'
    }
    response_msg = jsonify(message)
    response_msg.status_code = status_code
    return response_msg


## /api/v1/health
@app.route(f"{route_prefix}/health", methods=['GET'])
def health():
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        print("Printing connection pool properties ")
        print("Connection Pool Name - ", connection_pool.pool_name)
        print("Connection Pool Size - ", connection_pool.pool_size)
        if connection_object.is_connected():
            db_Info = connection_object.get_server_info()
            print("Connected to MySQL database using connection pool ... MySQL Server version on ", db_Info)

            cursor = connection_object.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Your connected to - ", record)

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return ("MySQL connection is closed")

@app.route(f"{route_prefix}/lihat_data_tamu", methods=['GET'])
def get_all_tamu():
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute("select * from tb_guests")
            record = cursor.fetchall()
            print("sedang melihat data tamu pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return record


@app.route(f"{route_prefix}/tambah_tamu", methods=['POST'])
def tambah_tamu():
    nama = request.args.get('nama')
    alamat = request.args.get('alamat')
    jenis_tamu = request.args.get('jenis_tamu')

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            query = 'INSERT INTO tb_guests (name, alamat, jenis_tamu) VALUES (%s,%s,%s)'
            val = (nama, alamat, jenis_tamu)
            cursor.execute(query, val)
            connection_object.commit()

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            print("berhasil menambahkan data tamu pada:" + x)
            cursor.close()
            connection_object.close()
            return "data berhasil ditambahkan"


## /api/v1/edit_data_tamu
@app.route(f"{route_prefix}/edit_data_tamu", methods=['POST'])
def editdata():
    id = request.args.get('id')
    nama = request.args.get('nama')
    alamat = request.args.get('alamat')
    jenis_tamu = request.args.get('jenis_tamu')

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            query = f"UPDATE tb_guests SET name='{nama}',alamat='{alamat}',jenis_tamu='{jenis_tamu}' WHERE id={id}"
            cursor.execute(query)
            connection_object.commit()
            print("berhasil mengedit data tamu pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return "data berhasil diubah"


## /api/v1/lihat_data_satu_tamu
@app.route(f"{route_prefix}/lihat_data_satu_tamu", methods=['GET'])
def lihat_data_satu_tamu():
    id = request.args.get('id')
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute(f"select * from tb_guests WHERE id={id}")
            record = cursor.fetchall()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return record


## /api/v1/delete_data_satu_tamu
@app.route(f"{route_prefix}/delete_data_satu_tamu", methods=['DELETE'])
def delete_data_satu_tamu():
    id = int(request.args.get('id'))
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    try:
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        if connection_object.is_connected():
            cursor.execute(f"DELETE FROM `tb_guests` WHERE `id`={id}")
            connection_object.commit()
            print("id yang dihapus adalah : " + str(id) + " pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return get_response_msg("tamu tersebut sudah dihapus", HTTPStatus.OK)


## /api/1.0/ubah_kehadiran
@app.route(f"{route_prefix}/ubah_kehadiran", methods=['POST'])
def ubah_kehadiran():
    id = request.args.get('id')
    kehadiran = request.args.get('kehadiran')
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute(f"UPDATE tb_guests SET kehadiran='{kehadiran}' WHERE id={id}")
            connection_object.commit()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return "data berhasil diubah"


## /api/1.0/search
@app.route(f"{route_prefix}/search", methods=['GET'])
def search():
    params = request.args.get('params')
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute(f"SELECT * FROM tb_guests WHERE name LIKE '%{params}%'")
            record = cursor.fetchall()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return record


## /api/1.0/getsummary
@app.route(f"{route_prefix}/getsummary", methods=['GET'])
def getsummary():
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute(f"SELECT * FROM tb_guests WHERE kehadiran='BELUM KONFIRMASI'")
            record1 = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tb_guests WHERE kehadiran='AKAN HADIR'")
            record2 = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tb_guests WHERE kehadiran='TIDAK HADIR'")
            record3 = cursor.fetchall()
            cursor.execute(f"SELECT * FROM tb_guests WHERE kehadiran='SUDAH HADIR'")
            record4 = cursor.fetchall()
            response = [len(record1), len(record2), len(record3), len(record4)]
            response = get_response_msg(response, HTTPStatus.OK)

    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return response


## /api/1.0/readqr
@app.route(f"{route_prefix}/scanqr", methods=['POST'])
def readqr():
    print("sedang menggunakan API scanqr pada:" + x)
    data = json.loads(request.data)
    imgg = data['base64']
    name = str(data['time'])
    try:
        B64_decode = base64.b64decode(imgg)
        path = r'image'
        # write the decoded data back to original format in  file
        img_file = open(path + '\image_' + name + '.jpg', 'wb')
        img_file.write(B64_decode)
        img_file.close()

        img_arr = cv2.imread(path + '\image_' + name + '.jpg')
        print("berhasil menyimpan gambar pada:" + x)

        # Get connection object from a pool
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor()

        # Detect and decode the qrcode
        data, bbox, rectifiedImage = qrDecoder.detectAndDecode(img_arr)

        if len(data) > 0:
            output = format(data)
            cursor.execute(f"UPDATE tb_guests SET kehadiran='SUDAH HADIR' WHERE id={output}")
            connection_object.commit()
            print("id yang diupdate kehadirannya adalah" + output + " pada: " + x)
            cursor.execute(f"select * from tb_guests WHERE id={output}")
            record = cursor.fetchall()
            response = get_response_msg(record, HTTPStatus.OK)
        else:
            response = get_response_msg("QR Code not detected", HTTPStatus.NOT_FOUND)
            print("QR code tidak terbaca, proses ini dilakukan pada: " + x)
            cursor.close()
            connection_object.close()
            return response
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return response

#Ucapan
## /api/1.0/ucapan POST
@app.route(f"{route_prefix}/ucapan", methods=['POST'])
def tambah_ucapan():
    nama = request.args.get('nama')
    asal = request.args.get('asal')
    pesan = request.args.get('pesan')

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            query = 'INSERT INTO tb_ucapan (name, asal, pesan) VALUES (%s,%s,%s)'
            val = (nama, asal, pesan)
            cursor.execute(query, val)
            connection_object.commit()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            print("berhasil menambahkan data ucapan pada:" + x)
            cursor.close()
            connection_object.close()
            return "data berhasil ditambahkan"

## /api/1.0/ucapan GET
@app.route(f"{route_prefix}/ucapan", methods=['GET'])
def lihat_ucapan():
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute("select * from tb_ucapan")
            record = cursor.fetchall()
            print("sedang melihat data ucapan pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return record

#Konfirmasi Kehadiran dan Jumlah Tamu
## /api/1.0/jumlah_tamu POST
@app.route(f"{route_prefix}/jumlah_tamu", methods=['POST'])
def tambah_jumlah_tamu():
    nama = request.args.get('nama')
    asal = request.args.get('asal')
    jumlah_tamu = request.args.get('jumlah_tamu')

    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            query = 'INSERT INTO tb_tamu_akan_hadir (nama, asal, jumlah_tamu) VALUES (%s,%s,%s)'
            val = (nama, asal, jumlah_tamu)
            cursor.execute(query, val)
            connection_object.commit()
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            print("berhasil menambahkan data jumlah tamu pada:" + x)
            cursor.close()
            connection_object.close()
            return "data jumlah tamu berhasil ditambahkan"

## /api/1.0/jumlah_tamu GET
@app.route(f"{route_prefix}/jumlah_tamu", methods=['GET'])
def lihat_jumlah_tamu():
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    try:
        if connection_object.is_connected():
            cursor = connection_object.cursor()
            cursor.execute("select * from tb_tamu_akan_hadir")
            record = cursor.fetchall()
            print("sedang melihat data jumlah tamu pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return record

## /api/v1/jumlah_tamu
@app.route(f"{route_prefix}/jumlah_tamu", methods=['DELETE'])
def hapus_data_jumlah_tamu():
    id = int(request.args.get('id'))
    # Get connection object from a pool
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor()
    try:
        if (id == None):
            records = "id is must"
            response = get_response_msg(records, HTTPStatus.BAD_REQUEST)
            return response
        if connection_object.is_connected():
            cursor.execute(f"DELETE FROM `tb_tamu_akan_hadir` WHERE `id`={id}")
            connection_object.commit()
            print("id yang dihapus adalah : " + str(id) + " pada:" + x)
    except Error as e:
        print("Error while connecting to MySQL using Connection pool ", e)
    finally:
        # closing database connection.
        if connection_object.is_connected():
            cursor.close()
            connection_object.close()
            return get_response_msg("jumlah tamu tersebut sudah dihapus", HTTPStatus.OK)

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
    app.run(host="localhost", port=8008, debug='true')
