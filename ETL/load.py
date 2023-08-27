from localSQLConfig import host_name, user_name, user_password
import mysql.connector
from mysql.connector import Error


def connect_local_sql_db():
    # https://www.freecodecamp.org/news/connect-python-with-sql/
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def close_local_sql_db(connection):
    connection.close()
    print('\tClosed connection')


def insert_restaurant_data(connection, data):
    """
    place_id, restaurant_name, fk_census_tract_id,
    price_level, rating, user_rating_total, avg_calories,
    avg_fat, avg_protein, avg_carbs
    """
    restaurant_vals = [(x['place_id'], x['name'], x['census_id'],
                        x['price_level'], x['rating'], x['user_ratings_total'],
                        x['avg_calories'], x['avg_protein'], x['avg_fat'],
                        x['avg_carbs'])
                       for index, x in data.iterrows()]
    # Excute query
    execute_list_query(connection, pop_restaurant(), restaurant_vals)


def insert_census_data(connection, data):
    """
        census_tract_id, LILATracts_1And10, state, county
        latitude, longitude
        """
    census_vals = [(x['CensusTract'], x['LILATracts_1And10'], x['State'],
                    x['County'], x['census_lat'], x['census_lon'])
                   for index, x in data.iterrows()]
    # Excute query
    execute_list_query(connection, pop_census(), census_vals)

def pop_census():
    sql = """
            INSERT INTO census_tract (census_tract_id, LILATracts_1And10, state, county, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    return sql


def pop_restaurant():
    sql = """
            INSERT INTO restaurant (place_id, restaurant_name, census_tract_id, price_level, rating, \
            user_rating_total, avg_calories, avg_protein, avg_fat, avg_carbs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    return sql


def execute_query(connection, query):
    # https://www.freecodecamp.org/news/connect-python-with-sql/
    cursor = connection.cursor()
    try:
        cursor.execute('USE fooddesert')
        cursor.execute(query)
        connection.commit()
        # print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql, val):
    # https://www.freecodecamp.org/news/connect-python-with-sql/
    cursor = connection.cursor()
    try:
        cursor.execute('USE fooddesert')
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_scripts_from_file(connection, filename):
    cursor = connection.cursor()

    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:

        command = command.replace("\n", '')
        command = command.replace("\t", ' ')

        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            cursor.execute(command)
        except Error as err:
            print(f"Error: '{err}'")
