from connectors.database import DBConnection
import matplotlib.pyplot as plt

DB_CONFIG = 'config/database.ini'
FUNCTION_CREATE = 'plpgsql/cdf.sql'
TABLE_NAME = 'taxi_table'


def show_result(result, filename, show=False):
    plt.figure()
    plt.plot(*zip(*result))
    plt.title('Cumulative Distribution Function Plot')
    plt.xlabel('trip_distance')
    plt.ylabel('cdf')
    plt.grid()
    if show:
        plt.show()
    plt.savefig(filename)


if __name__ == "__main__":

    DBConnection.connect(DB_CONFIG)

    with open(FUNCTION_CREATE, 'r') as file_:
        query = file_.read().replace('{table}', TABLE_NAME)
        DBConnection.execute_query(query)

    result = DBConnection.execute_query(
        "SELECT * from calc_cdf(ARRAY ['2019-12-18'::date, '2020-01-03'::date]);", True)
    show_result(result, 'results/cdf_window.png')

    result = DBConnection.execute_query(
        "SELECT * from calc_cdf(ARRAY ['2020-01-29'::date, '2020-01-30'::date]);", True)
    show_result(result, 'results/cdf_window2.png')

    result = DBConnection.execute_query("SELECT * from calc_cdf();", True)
    show_result(result, 'results/cdf_all.png')
