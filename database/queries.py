from database.connection import run_query


def get_all_sales():

    query = """
    SELECT * FROM sales_data;
    """

    return run_query(query)


def get_total_revenue():

    query = """
    SELECT SUM(sales_amount) AS total_revenue
    FROM sales_data;
    """

    return run_query(query)

from database.connection import run_query


def get_all_sales():

    query = """
    SELECT * FROM sales_data;
    """

    return run_query(query)


def get_total_revenue():

    query = """
    SELECT SUM(sales_amount) AS total_revenue
    FROM sales_data;
    """

    return run_query(query)


def get_sales_by_region():

    query = """
    SELECT
        region,
        SUM(sales_amount) AS total_sales
    FROM sales_data
    GROUP BY region
    ORDER BY total_sales DESC;
    """

    return run_query(query)


def get_top_products():

    query = """
    SELECT
        product,
        SUM(sales_amount) AS revenue
    FROM sales_data
    GROUP BY product
    ORDER BY revenue DESC;
    """

    return run_query(query)