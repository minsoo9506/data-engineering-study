# Starting with error handling
## Welcome
- TRY CATCH

```sql
-- Set up the TRY block
BEGIN TRY
	-- Add the constraint
	ALTER TABLE products
		ADD CONSTRAINT CHK_Stock CHECK (stock >= 0);
END TRY
-- Set up the CATCH block
BEGIN CATCH
	SELECT 'An error occurred!';
END CATCH
```

## Error anatomy and uncatchable erros
- error 메세지 관련 내용 (몰라도 될 듯)

## Giving information about errors
- 아래 예시처럼 함수들을 이용하여 error message를 잘 캐치할 수 있다.
```sql
-- Set up the TRY block
BEGIN TRY	
	SELECT 'Total: ' + SUM(price * quantity) AS total
  	FROM orders 
END TRY
-- Set up the CATCH block
BEGIN CATCH
	-- Show error information.
	SELECT  ERROR_NUMBER() AS number,  
        	ERROR_SEVERITY() AS severity_level,  
        	ERROR_STATE() AS state,
        	ERROR_LINE() AS line,  
        	ERROR_MESSAGE() AS message; 	    
END CATCH 
```

# Raising, throwing and customizing your errors
## RAISERROR
- python에서 raise 하는 것처럼 사용
```sql
RAISERROR ( { msg_str | msg_id | @local_variable_message },  
    severity, 
    state,
    [ argument [ ,...n ] ] )  
    [ WITH option [ ,...n ] ] 
```
```sql
DECLARE @product_id INT = 5;

IF NOT EXISTS (SELECT * FROM products WHERE product_id = @product_id)
	-- Invoke RAISERROR with parameters
	RAISERROR('No product with id %d.', 11, 1, @product_id);
ELSE 
	SELECT * FROM products WHERE product_id = @product_id;
```

## THROW
```sql
CREATE PROCEDURE insert_product
  @product_name VARCHAR(50),
  @stock INT,
  @price DECIMAL

AS

BEGIN TRY
	INSERT INTO products (product_name, stock, price)
		VALUES (@product_name, @stock, @price);
END TRY
-- Set up the CATCH block
BEGIN CATCH	
	-- Insert the error and end the statement with a semicolon
    INSERT INTO errors VALUES ('Error inserting a product');  
    -- Re-throw the error
	THROW;  
END CATCH

BEGIN TRY
	-- Execute the stored procedure
	EXEC insert_product 
    	-- Set the values for the parameters
    	@product_name = 'Trek Conduit+',
        @stock = 3,
        @price = 499.99;
END TRY
-- Set up the CATCH block
BEGIN CATCH
	-- Select the error message
	SELECT ERROR_MESSAGE();
END CATCH
```

## Customizing error messages in the THROW statement
```sql
DECLARE @first_name NVARCHAR(20) = 'Pedro';

-- Concat the message
DECLARE @my_message NVARCHAR(500) =
	CONCAT('There is no staff member with ', @first_name, ' as the first name.');

IF NOT EXISTS (SELECT * FROM staff WHERE first_name = @first_name)
	-- Throw the error
	THROW 50000, @my_message, 1;
```

```sql
FORMATMESSAGE ( { ' msg_string ' | msg_number } , 
                [ param_value [ ,...n ] ] )  
```

```sql
DECLARE @product_name AS NVARCHAR(50) = 'Trek CrossRip+ - 2018';
-- Set the number of sold bikes
DECLARE @sold_bikes AS INT = 10;
DECLARE @current_stock INT;

SELECT @current_stock = stock FROM products WHERE product_name = @product_name;

DECLARE @my_message NVARCHAR(500) =
	-- Customize the error message
	FORMATMESSAGE('There are not enough %s bikes. You have %d in stock.', @product_name, @current_stock);

IF (@current_stock - @sold_bikes < 0)
	-- Throw the error
	THROW 50000, @my_message, 1;
```

- you want to add your custom error message to the `sys.messages` catalog, by executing the `sp_addmessage` stored procedure. Once you have added the message, you can use it in the `FORMATMESSAGE` function.

```sql
sp_addmessage 
     msg_id , severity , msgtext,
     [ language ] 
```

```sql
EXEC sp_addmessage @msgnum = 50002, @severity = 16, @msgtext = 'There are not enough %s bikes. You only have %d in stock.', @lang = N'us_english';

DECLARE @product_name AS NVARCHAR(50) = 'Trek CrossRip+ - 2018';
--Change the value
DECLARE @sold_bikes AS INT = 10;
DECLARE @current_stock INT;

SELECT @current_stock = stock FROM products WHERE product_name = @product_name;

DECLARE @my_message NVARCHAR(500) =
	FORMATMESSAGE(50002, @product_name, @current_stock);

IF (@current_stock - @sold_bikes < 0)
	THROW 50000, @my_message, 1;
```

# Transactions in SQL Server

# Controlling the concurrency: Transaction isolation levels