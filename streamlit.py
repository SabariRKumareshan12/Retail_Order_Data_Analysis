import streamlit as st
import pandas as pd
import numpy as np
import pg8000
import base64

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = pg8000.connect(
       host="projectdb.cp8qumsw6ssl.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="postgres",
        user="postgres",
        password="idlisambar"
    )
    return conn

# Function to execute a query and return the result as a pandas DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None  # Return None if connection failed
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def set_background_image(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    base64_image = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: fit;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}     
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image(r"image1.jpg")

Business_Insights=["Home","Top-Selling Products","Monthly Sales Analysis","Product Performance","Regional Sales Analysis","Discount Analysis"]

guvi_questions = [
    "1. # Find top 10 highest revenue generating products",
    "2. # Find the top 5 cities with the highest profit margins",
    "3. # Calculate the total discount given for each category",
    "4. # Find the average sale price per product category",
    "5. # Find the region with the highest average sale price",
    "6. # Find the total profit per category",
    "7. # Identify the top 3 segments with the highest quantity of orders",
    "8. # Determine the average discount percentage given per region",
    "9. # Find the product category with the highest total profit",
    "10. # Calculate the total revenue generated per year"
]

my_questions = [
    "11. # Determine the yearly sales trend by product category",
    "12. # List Top 10 cities that have purchased products from all sub-categories",
    "13. # Compare total revenue by region and category",
    "14. # Find the month with the highest total sales in each year",
    "15. # Calculate total sales, cost, and profit for each product category",
    "16. # Identify cities that only ordered from one product category",
    "17. # Calculate the total revenue generated on December month",
    "18. # Identify the top 3 most frequently ordered product categories",
    "19. # Identify the total number of products sold per year",
    "20. # Identify the sub-categories that consistently generate profit across all years"
]

Business_Insights_queries = [
    "select 'Welcome' as message",
    "select p.product_id,p.sub_category as product,sum(o.sale_price) as total_sales,rank() over(order by sum(o.sale_price) desc) as rank from product_detail as p join retail_order as o on p.product_id=o.product_id group by p.product_id, p.sub_category;",
    "with year1 as (select order_month, order_year,sum(sale_price)as total_sales from retail_order where order_year= 2023 group by order_month, order_year),year2 as (select order_month, order_year,sum(sale_price)as total_sales from retail_order where order_year= 2022 group by order_month, order_year) select year1.order_month, (((year1.total_sales - year2.total_sales) / year2.total_sales)*100) as Monthly_sales_Analysis, rank()over(order by (((year1.total_sales - year2.total_sales) / year2.total_sales)*100) desc) from year1 year1 join year2 year2 on year1.order_month=year2.order_month and year1.order_year=year2.order_year+1;",
    "select p.product_id,p.category,p.sub_category, round(sum(o.sale_price)::numeric,2) as total_sales, round(sum(o.profit)::numeric,2) as total_profit, case when sum(o.sale_price)=0 then 0 else round((sum(o.profit)/sum(o.sale_price))*100) end as profit_margin, case when sum(o.sale_price)>10000 then 'High Performer' when sum (sale_price) between 5000 and 10000 then 'Mid Performer' else 'Low Performer' end as performance_category, rank()over(order by round(sum(o.sale_price)::numeric,2)desc) from product_detail as p join retail_order as o on p.product_id=o.product_id group by p.product_id, p.category, p.sub_category;",
    "select region, round(sum(order_id)::numeric,2) as total_order, round(sum(sale_price)::numeric,2) as total_sales, round(sum(profit)::numeric,2) as total_profit, round((sum(profit)/sum(sale_price))*100) as profit_margin, rank()over(order by round(sum(sale_price)::numeric,2) desc) from retail_order group by region;",
    "select product_id, count(order_id) as total_orders, sum(quantity) as total_quantity, sum(discount_percent) as Total_discount_percent, round(sum(discount)::numeric,2) as total_discount, round(sum(sale_price)::numeric,2) as total_sale, round((sum(discount)::numeric/sum(sale_price)::numeric)*100,2) as discount_impact_percentage from retail_order group by product_id having sum(discount_percent)>20 order by discount_impact_percentage desc;"
    ]

guvi_queries = [
    "select p.sub_category as product, round(sum(o.sale_price)::numeric,2) as Total_sales,rank() over(order by sum(o.sale_price) desc) as rank from retail_order as o join product_detail as p on o.product_id = p.product_id group by p.sub_category order by Total_sales DESC limit 10;",
    "select o.city, avg(case when o.sale_price=0 then 0 else round((o.profit/o.sale_price)*100) end) as profit_margin from retail_order as o join product_detail as p on o.product_id=p.product_id group by o.city order by profit_margin desc limit 5;",
    "select p.category, round(sum(o.discount)::numeric,2) as total_discount from retail_order as o join product_detail as p on o.product_id=p.product_id group by p.category;",
    "select p.category, p.sub_category as product, round(avg(o.sale_price)::numeric,2) as average_sales_price from retail_order as o join product_detail as p on o.product_id=p.product_id group by p.category, p.sub_category;",
    "select o.region, round(avg(o.sale_price)::numeric,2) as Highest_average_sales_price from retail_order as o join product_detail as p on o.product_id=p.product_id group by o.region order by Highest_average_sales_price desc limit 1;",
    "select p.category, round(sum((o.sale_price-(o.cost_price*o.quantity)))::numeric,2) as total_profit from retail_order as o join product_detail as p on o.product_id=p.product_id group by p.category;",
    "select o.segment, sum(o.quantity) as Total_quantity from retail_order as o join product_detail as p on o.product_id=p.product_id group by o.segment order by Total_quantity desc limit 3;",
    "select o.region, avg(o.discount_percent) as avg_discount_percentage from retail_order as o join product_detail as p on o.product_id=p.product_id group by o.region;",
    "select p.category, p.sub_category as product, round(sum((o.sale_price-(o.cost_price*o.quantity)))::numeric,2) as total_profit from retail_order as o join product_detail as p on o.product_id=p.product_id group by p.category, p.sub_category;",
    "select o.order_year as year, round(sum(o.sale_price)::numeric,2) as Total_sales from retail_order as o join product_detail as p on o.product_id=p.product_id group by o.order_year order by Total_sales desc;"
]

my_queries = [
    "select o.order_year as year,p.category, round(sum(o.sale_price)::numeric,2) as total_sales from retail_order as o join product_detail as p on o.product_id = p.product_id group by o.order_year, p.category order by o.order_year, total_sales desc;",
    "select o.city, count(distinct p.sub_category) as unique_sub_categories from retail_order as o join product_detail as p on o.product_id = p.product_id group by o.city having count(distinct p.sub_category) >= 17;",
    "select o.region,p.category, round(sum(o.sale_price)::numeric,2) as Total_revenue from retail_order as o join product_detail as p on o.product_id = p.product_id group by o.region, p.category order by total_revenue desc;",
    "select order_year, order_month, round(sum(sale_price)::numeric,2) as Total_sales from retail_order group by order_year, order_month order by order_year, Total_sales desc;",
    "select p.category, sum(o.cost_price * o.quantity) as total_cost, round(sum(o.sale_price)::numeric,2) as Total_sales, round(sum(o.profit)::numeric,2) as total_profit from retail_order as o join product_detail as p on o.product_id = p.product_id group by p.category;",
    "select o.city, count(distinct p.category) as category_count from retail_order as o join product_detail as p on o.product_id = p.product_id group by o.city having count(distinct p.category) = 1;",
    "select o.order_year, o.order_month as month, round(sum(sale_price)::numeric,2) as Total_sales from retail_order as o join product_detail as p on o.product_id = p.product_id where o.order_month=12 group by o.order_year, o.order_month;",
    "select p.category, p.sub_category as products, count(o.order_id) as total_orders from retail_order as o join product_detail as p on o.product_id = p.product_id group by p.category, p.sub_category order by total_orders desc limit 3;",
    "select o.order_year, count(distinct o.product_id) as products_sold from retail_order as o join product_detail as p on o.product_id = p.product_id group by o.order_year order by o.order_year;",
    "select p.sub_category as products from retail_order as o join product_detail as p on o.product_id = p.product_id group by p.sub_category, o.order_year having sum(o.profit) > 0 intersect select p.sub_category from retail_order as o join product_detail as p on o.product_id = p.product_id group by p.sub_category having count(distinct o.order_year)=(select count(distinct order_year)from retail_order);"
]

st.title("Retail Order Data Analysis 📊:rocket:")
st.markdown("#### Welcome")
st.markdown("This dashboard provides insights into retail order data, including sales, profits, discounts, and more")
st.sidebar.title("Select a Query")
category = st.sidebar.radio("Select Query Category:", ["Business Insights","GUVI Questions", "My Questions"])

if category == "Business Insights":
    query_description = st.sidebar.selectbox("Choose a query:", Business_Insights)
    query_index = Business_Insights.index(query_description)
    selected_query = Business_Insights_queries[query_index]
elif category == "GUVI Questions":
    query_description = st.sidebar.selectbox("Choose a query:", guvi_questions)
    query_index = guvi_questions.index(query_description)
    selected_query = guvi_queries[query_index]
elif category == "My Questions":
    query_description = st.sidebar.selectbox("Choose a query:", my_questions)
    query_index = my_questions.index(query_description)
    selected_query = my_queries[query_index]

if query_description == "Home":
    st.markdown("###### 🧠 What you can do here:")
    st.markdown("""
         - Analyze **sales trends** over time" 
         - Understand **customer purchasing behavior** 
         - Discover **top-performing products**
         Navigate through the sidebar to explore specific analyses."""
    )
else:
    st.subheader(f"Selected Query: {query_description}")
    if st.sidebar.button("Submit Query", type="secondary"):
        try:
            result_df = run_query(selected_query)
            if result_df is not None:
                st.dataframe(result_df)  # Display the result
            else:
                st.error("Query execution failed.")
        except Exception as e:
            st.error(f"Error executing query: {e}")

st.markdown("Thank you :blush:")
