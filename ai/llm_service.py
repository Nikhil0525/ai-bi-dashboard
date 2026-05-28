def generate_sql_from_question(question):

    question = question.lower()

    # ===============================
    # TOTAL SALES / REVENUE
    # ===============================
    if any(word in question for word in [
        "total sales",
        "total revenue",
        "overall revenue",
        "overall sales",
        "company revenue"
    ]):
        return """
        SELECT SUM(sales_amount) AS total_sales
        FROM sales_data;
        """

    # ===============================
    # REGION ANALYSIS
    # ===============================
    elif any(word in question for word in [
        "region",
        "sales by region",
        "revenue by region",
        "regional sales"
    ]):
        return """
        SELECT region, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY region
        ORDER BY total_sales DESC;
        """

    # ===============================
    # PRODUCT ANALYSIS
    # ===============================
    elif any(word in question for word in [
        "product",
        "top products",
        "best products",
        "product sales"
    ]):
        return """
        SELECT product, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY product
        ORDER BY total_sales DESC;
        """

    # ===============================
    # CATEGORY ANALYSIS
    # ===============================
    elif any(word in question for word in [
        "category",
        "sales by category",
        "category revenue"
    ]):
        return """
        SELECT category, SUM(sales_amount) AS total_sales
        FROM sales_data
        GROUP BY category
        ORDER BY total_sales DESC;
        """

    # ===============================
    # TOP SALES
    # ===============================
    elif any(word in question for word in [
        "top sales",
        "highest sales",
        "largest sales"
    ]):
        return """
        SELECT *
        FROM sales_data
        ORDER BY sales_amount DESC
        LIMIT 5;
        """

    # ===============================
    # DEFAULT
    # ===============================
    else:
        return """
        SELECT *
        FROM sales_data
        LIMIT 10;
        """


def ask_ai(prompt):

    prompt = prompt.lower()

    if "sales" in prompt:
        return """
📈 Sales Insight:
Revenue is growing steadily across major regions.
Focus on high-performing products to maximize profitability.
"""

    elif "region" in prompt:
        return """
🌍 Regional Insight:
Some regions are outperforming others significantly.
Consider increasing marketing investment in top-performing areas.
"""

    elif "product" in prompt:
        return """
🛒 Product Insight:
Top-selling products contribute most of the revenue.
Inventory optimization can further improve performance.
"""

    else:
        return """
🤖 AI Business Insight:
Your analytics platform is successfully processing business intelligence queries.
Use dashboards and AI insights to support strategic decisions.
"""
