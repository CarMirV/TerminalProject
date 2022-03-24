import mysql.connector as dbconnector

def main(subjectId):
    try:
        connection = dbconnector.connect(host='localhost', database='terminalProject', user='root', password='cmirandauam1610!')
        if(connection.is_connected()):
            dbInfo = connection.get_server_info()
            print("Connected to MYSQL Server version %s" % (dbInfo))
            cursor = connection.cursor()
            cursor.execute("SELECT imagePath FROM imagesPath ip WHERE ip.subjectId = %s;" % (subjectId))
            records = cursor.fetchall()
            print(records[0])
    except Error as e:
        print("Error conectando a la BD %s" % (e))
    finally:
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("La conexion con la BD se ha cerrado de manera exitosa")
            return records

if __name__ == '__main__':
    main(1)