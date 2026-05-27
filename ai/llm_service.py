def generate_sql_from_question(question):

    question = question.lower()

    if "total sales" in question or "revenue" in question:
        return """
        SELECT SUM(sales_amount) AS total_sales
        FROM sales_data;
        """

    elif "region" in question:
        return """
        SELECT region, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY region
        ORDER BY total_sales DESC;
        """

    elif "product" in question:
        return """
        SELECT product, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY product
        ORDER BY total_sales DESC;
        """

    elif "category" in question:
        return """
        SELECT category, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY category
        ORDER BY total_sales DESC;
        """

    else:
        return """
        SELECT *
        FROM sales_data
        LIMIT 10;
        """


def ask_ai(prompt):

    return """
Business Intelligence helps companies analyze data.
It supports better business decisions.
It improves sales and company performance.
"""