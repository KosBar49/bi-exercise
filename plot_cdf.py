from connectors.database import DBConnection
import matplotlib.pyplot as plt

DB_CONFIG = 'database.ini'
FUNCTION_CREATE = 'plpgsql/cdf.sql'

def show_result(result):
    plt.figure()
    plt.plot(*zip(*result))
    plt.title('Cumulative Distribution Function Plot')
    plt.xlabel('trip_distance')
    plt.ylabel('cdf')
    plt.grid()
    plt.show()

if __name__ == "__main__":

    DBConnection.connect(DB_CONFIG)
    result = DBConnection.execute_query("SELECT version()", True)
    
    with open(FUNCTION_CREATE, 'r') as file_:
        query = file_.read()
        DBConnection.execute_query(query)

    result = DBConnection.execute_query("SELECT * from calc_cdf(ARRAY ['2019-12-18'::date, '2020-01-03'::date]);", True)
    show_result(result)

    result = DBConnection.execute_query("SELECT * from calc_cdf();", True)
    show_result(result)