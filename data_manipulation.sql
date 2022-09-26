-- MariaDB dump 10.19  Distrib 10.4.24-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_chaplygy
-- ------------------------------------------------------
-- Server version	10.6.7-MariaDB-log


--
-- Cashiers
--

-- Get all cashiers for the cashier page
SELECT cashier_id, first_name, last_name FROM Cashiers

-- Get all of a single cashier's data to update
SELECT * FROM Cashiers WHERE cashier_id = :cashier_id_selected

-- Update a single cashier's data
UPDATE Cashiers SET first_name = :first_name_input, last_name = :last_name_input, day_total = :day_total_input, day_worked = :day_worked_input, lane = :lane_input WHERE cashier_id = :cashier_id_input

-- Add a new cashier
INSERT INTO Cashiers (first_name, last_name, day_total, day_worked, lane) VALUES (:first_name_input, :last_name_input, :day_total_input, :day_worked_input, :lane_input)

-- Delete a cashier
DELETE FROM Cashiers WHERE cashier_id = :cashier_id_input


--
-- Customers
--

-- Get all customers for the customer page
SELECT customer_id, first_name, last_name FROM Customers

-- Get all of a single customer's data to update
SELECT * FROM Customers WHERE customer_id = :customer_id_selected

-- Update a single customer's data
UPDATE Customers SET first_name = :first_name_input, last_name = :last_name_input, customer_phone = :customer_phone_input, customer_email = :customer_email_input WHERE customer_id = :customer_id_input

-- Add a new customer
INSERT INTO Customers (first_name, last_name, customer_phone, customer_email) VALUES (:first_name_input, :last_name_input, :customer_phone_input, :customer_email_input)

-- Delete a customer
DELETE FROM Customers WHERE customer_id = :customer_id_input


--
-- Products
--

-- Get all products for the product page
SELECT product_id, product_name FROM Products

-- Get all of a single product's data to update
SELECT * FROM Products WHERE product_id = :product_id_selected

-- Update a single product's data
UPDATE Products SET product_name = :product_name_input, product_price = :product_price_input, stock = :stock_input, type = :type_input WHERE product_id = :product_id_input

-- Add a new product
INSERT INTO Products (product_name, product_price, stock, type) VALUES (:product_name_input, :product_price_input, :stock_input, :type_input)

-- Delete a product
DELETE FROM Products WHERE product_id = :product_id_input


--
-- Purchases
--

-- Get all purchases for the purchase page
SELECT purchase_id, purchase_date FROM Purchases

-- Get all of a single purchase's data to update
SELECT * FROM Purchases WHERE purchase_id = :purchase_id_selected

-- Update a single purchase's data
UPDATE Purchases SET purchase_date = :purchase_date_input, total_price = :total_price_input, purchase_complete = :purchase_complete WHERE purchase_id = :purchase_id_input

-- Add a new purchase
INSERT INTO Purchases (purchase_date, total_price, purchase_complete, Customers.customer_id, Cashiers.cashier_id) VALUES (:purchase_date_input, :total_price_input, :purchase_complete_input, :Customers.customer_id_input, :Cashiers.cashier_id_input)

-- Delete a purchase
DELETE FROM Purchases WHERE purchase_id = :purchase_id_input


--
-- Purchases_Products
--

-- Get all purchases for the purchases_products page
SELECT * FROM Purchases_Products
SELECT purchases_id AS pid FROM Purchases
SELECT product_id AS cid FROM Products

-- Update data for a relationship
UPDATE Purchases_Products SET quantity = :quantity_input WHERE pid = :pid_input

-- Add a new relationship
INSERT INTO Purchases_Products (pid, cid, quantity) VALUES (:pid_input, :cid_input, :quantity_input)

-- Add relationship attributes to individual pages
--INSERT INTO Purchases () VALUES ()
--INSERT INTO Products () VALUES ()

-- Deletion from individual pages
--DELETE FROM Purchases WHERE purchase_id = :purchase_id_input
--DELETE FROM Products WHERE product_id = :product_id_input

-- Deletion from M:M page
DELETE FROM Purchases_Products WHERE pid = :pid_input AND cid = :cid_input
