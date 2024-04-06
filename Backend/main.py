from db_connection import test_function,DBConnection

connection = DBConnection()
connection.connect()

test_function()
