from neo4j import GraphDatabase
import streamlit as st
import google.generativeai as genai
import pandas as pd

uri = "DATABASE_URI"
user = "DATABASE_USERNAME"
password = "DATABASE_PASSWORD"


genai.configure(api_key="API_KEY")

driver = GraphDatabase.driver(uri, auth=(user, password))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text

def execute_query(cypher_query):
    with driver.session() as session:
        result = session.run(cypher_query)
        records = result.data()
        return records if records else "No results found."


prompts = {
    'Products': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has a table called Products with the following columns: ProductID, ProductName, Category.

For example:
- How many products are there? 
  The Cypher query would be: MATCH (p:Product) RETURN COUNT(p);
- What are the names of all products in the Electronics category? 
  The Cypher query would be: MATCH (p:Product) WHERE p.Category = 'Electronics' RETURN p.ProductName;

Do not include ``` or the word 'Cypher' in the output.
""",
    'Suppliers': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has a table called Suppliers with the following columns: SupplierID, SupplierName.

For example:
- How many suppliers are there? 
  The Cypher query would be: MATCH (s:Supplier) RETURN COUNT(s);
- What is the name of the supplier with ID 'S001'? 
  The Cypher query would be: MATCH (s:Supplier {SupplierID: 'S001'}) RETURN s.SupplierName;

Do not include ``` or the word 'Cypher' in the output.
""",
    'Inventory': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has a table called Inventory with the following columns: InventoryID, ProductID, StockLevel, LastUpdated.

For example:
- What is the stock level of the product with ID 'P001'? 
  The Cypher query would be: MATCH (i:Inventory {ProductID: 'P001'}) RETURN i.StockLevel;
- How many items are in the inventory? 
  The Cypher query would be: MATCH (i:Inventory) RETURN COUNT(i);

Do not include ``` or the word 'Cypher' in the output.
""",
    'Supplies': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has a table called Supplies with the following columns: SupplyID, ProductID, SupplierID, Quantity, Date.

For example:
- How many supplies were made in 2023? 
  The Cypher query would be: MATCH (s:Supply) WHERE s.Date >= '2023-01-01' AND s.Date < '2024-01-01' RETURN COUNT(s);
- What quantity of product with ID 'P001' was supplied by 'S001'? 
  The Cypher query would be: MATCH (s:Supply {ProductID: 'P001', SupplierID: 'S001'}) RETURN s.Quantity;

Do not include ``` or the word 'Cypher' in the output.
""",
    'Sales': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has a table called Sales with the following columns: SaleID, ProductID, QuantitySold, SaleDate.

For example:
- How many items were sold on '2024-08-05'? 
  The Cypher query would be: MATCH (sa:Sale {SaleDate: '2024-08-05'}) RETURN SUM(sa.QuantitySold);
- What are the total sales for product with ID 'P001'? 
  The Cypher query would be: MATCH (sa:Sale {ProductID: 'P001'}) RETURN SUM(sa.QuantitySold);

Do not include ``` or the word 'Cypher' in the output.
""", 
'Complex Queries': """
You are an expert in converting English questions to Cypher queries for Neo4j.
The database has the following tables:
- Products: ProductID, ProductName, Category
- Suppliers: SupplierID, SupplierName
- Inventory: InventoryID, ProductID, StockLevel, LastUpdated
- Supplies: SupplyID, ProductID, SupplierID, Quantity, Date
- Sales: SaleID, ProductID, QuantitySold, SaleDate

For example:
- What is the total quantity supplied and sold for each product?
  The Cypher query would be: MATCH (p:Product)
  OPTIONAL MATCH (p)<-[:CONTAINS]-(i:Inventory)
  OPTIONAL MATCH (p)<-[:INCLUDES]-(sa:Sale)
  OPTIONAL MATCH (p)<-[:SUPPLIED_BY]-(su:Supply)
  RETURN p.ProductName AS Product, 
         COALESCE(SUM(i.StockLevel), 0) AS TotalStockLevel, 
         COALESCE(SUM(sa.QuantitySold), 0) AS TotalSold,
         COALESCE(SUM(su.Quantity), 0) AS TotalSupplied
  ORDER BY TotalSold DESC;

Do not include ``` or the word 'Cypher' in the output.
"""
}


st.set_page_config(page_title="Quipy")
st.image("logo.png", width=200)
st.markdown("<h1>Quipy</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.3em;'>Efficiently turn your business queries into actionable insights with Quipy. Designed for streamlined data analysis, it provides quick answers to complex supply chain questions.</p>", unsafe_allow_html=True)


table_choice = st.selectbox("Select the data category", list(prompts.keys()))

question = st.text_input("Ask your data question:")
submit = st.button("Submit Query")

if submit:
    if question:
        prompt = prompts[table_choice]
        cypher_query = get_gemini_response(question, prompt)
        result = execute_query(cypher_query)
        
        st.subheader("Query Results")
        if isinstance(result, str):
            st.markdown(f"<h3 style='font-size: 24px;'>{result}</h3>", unsafe_allow_html=True)
        else:
            if result:
                df = pd.DataFrame(result)
                st.write(df.to_html(index=False, header=False, escape=False), unsafe_allow_html=True)
            else:
                st.markdown("<h3 style='font-size: 24px;'>No results found.</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='font-size: 24px;'>Please enter a query.</h3>", unsafe_allow_html=True)