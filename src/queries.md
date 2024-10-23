Here are some example queries based on your database instance, categorized into simple and complex queries.

### Simple Queries

1. **Get the names of all suppliers.**
   - **Cypher Query:** `MATCH (s:Supplier) RETURN s.SupplierName;`
   - **Question:** "What are the names of all suppliers?"

2. **Find the stock level of the product with ID 'P001'.**
   - **Cypher Query:** `MATCH (i:Inventory {ProductID: 'P001'}) RETURN i.StockLevel;`
   - **Question:** "What is the stock level of the product with ID 'P001'?"

3. **List all products in the 'Electronics' category.**
   - **Cypher Query:** `MATCH (p:Product {Category: 'Electronics'}) RETURN p.ProductName;`
   - **Question:** "Which products are in the 'Electronics' category?"

4. **Get the total quantity of product 'P002' supplied.**
   - **Cypher Query:** `MATCH (s:Supply {ProductID: 'P002'}) RETURN SUM(s.Quantity);`
   - **Question:** "What is the total quantity of product 'P002' supplied?"

5. **Find all sales with a quantity sold greater than 10.**
   - **Cypher Query:** `MATCH (sa:Sale) WHERE sa.QuantitySold > 10 RETURN sa.SaleID, sa.QuantitySold;`
   - **Question:** "Which sales have a quantity sold greater than 10?"

### Complex Queries

1. **Get the total quantity supplied and sold for each product, along with the stock level.**
   - **Cypher Query:** 
     ```cypher
     MATCH (p:Product)
     OPTIONAL MATCH (i:Inventory {ProductID: p.ProductID})
     OPTIONAL MATCH (sa:Sale {ProductID: p.ProductID})
     OPTIONAL MATCH (su:Supply {ProductID: p.ProductID})
     RETURN p.ProductName AS Product,
            COALESCE(SUM(i.StockLevel), 0) AS TotalStockLevel,
            COALESCE(SUM(sa.QuantitySold), 0) AS TotalSold,
            COALESCE(SUM(su.Quantity), 0) AS TotalSupplied
     ORDER BY TotalSold DESC;
     ```
   - **Question:** "What is the total quantity supplied and sold for each product, and what is the current stock level?"

2. **Find the total sales amount for each supplier, considering only those who supplied products in 2023.**
   - **Cypher Query:** 
     ```cypher
     MATCH (su:Supply)-[:SUPPLIED_BY]->(s:Supplier)
     MATCH (sa:Sale {ProductID: su.ProductID})
     WHERE su.Date >= '2023-01-01' AND su.Date < '2024-01-01'
     RETURN s.SupplierName AS Supplier,
            SUM(sa.QuantitySold) AS TotalSales
     ORDER BY TotalSales DESC;
     ```
   - **Question:** "What is the total sales amount for each supplier who supplied products in 2023?"

3. **Get a list of products along with the total quantity sold and supplied, and the supplier names.**
   - **Cypher Query:** 
     ```cypher
     MATCH (p:Product)
     OPTIONAL MATCH (sa:Sale {ProductID: p.ProductID})
     OPTIONAL MATCH (su:Supply {ProductID: p.ProductID})-[:SUPPLIED_BY]->(s:Supplier)
     RETURN p.ProductName AS Product,
            COALESCE(SUM(sa.QuantitySold), 0) AS TotalSold,
            COALESCE(SUM(su.Quantity), 0) AS TotalSupplied,
            COLLECT(s.SupplierName) AS Suppliers
     ORDER BY TotalSold DESC;
     ```
   - **Question:** "List all products with their total quantity sold, total quantity supplied, and the names of suppliers."

4. **Find the most recent inventory update for each product, along with its stock level and category.**
   - **Cypher Query:** 
     ```cypher
     MATCH (p:Product)
     OPTIONAL MATCH (i:Inventory {ProductID: p.ProductID})
     RETURN p.ProductName AS Product,
            p.Category AS Category,
            i.StockLevel AS StockLevel,
            i.LastUpdated AS LastUpdated
     ORDER BY i.LastUpdated DESC;
     ```
   - **Question:** "What is the most recent inventory update for each product, including its stock level and category?"

5. **Determine the number of sales per shipping method, assuming each sale is associated with a shipping method.**
   - **Cypher Query:** 
     ```cypher
     MATCH (sa:Sale)-[:SHIPPED_BY]->(sh:Shipping)
     RETURN sh.ShippingMethod AS ShippingMethod,
            COUNT(sa) AS NumberOfSales
     ORDER BY NumberOfSales DESC;
     ```
   - **Question:** "How many sales are associated with each shipping method?"
