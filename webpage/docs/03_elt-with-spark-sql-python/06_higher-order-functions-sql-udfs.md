# Higher Order Functions and SQL UDFs (Hands On)

- This notebook explores **higher-order functions** and **user-defined functions (UDFs)** in Spark SQL using the bookstore dataset. 
- These capabilities allow complex transformations of nested structures and encapsulation of custom logic for reuse.

---

## Higher-Order Functions

Higher-order functions operate on complex types such as `arrays` and `maps`. They support functional transformations, enabling concise manipulation of nested structures.

### `filter`

Filters elements in an array based on a lambda expression.

#### Example

```sql
SELECT
  order_id,
  filter(books, book -> book.quantity >= 2) AS multiple_copies
FROM orders
```

* Extracts books ordered in quantities of 2 or more.
* Returns arrays of filtered items.

**Filtering Non-Empty Results**

Wrap in a subquery to eliminate empty arrays:

```sql
SELECT *
FROM (
  SELECT
    order_id,
    filter(books, book -> book.quantity >= 2) AS multiple_copies
  FROM orders
) t
WHERE size(multiple_copies) > 0
```

---

### `transform`

Applies a transformation to every element in an array and returns an array of results.

#### Example: Discount Calculation

```sql
SELECT
  order_id,
  transform(books, book -> book.subtotal * 0.9) AS discounted_subtotals
FROM orders
```

* Applies 10% discount to all book subtotals.
* Returns transformed array of numeric values.

---

## User-Defined Functions (SQL UDFs)

SQL UDFs encapsulate reusable logic and run natively within Spark SQL, maintaining parallelism and optimization.

### Creating a SQL UDF

Define a UDF using the `CREATE FUNCTION` statement.

#### Example: Domain Extraction from Email

```sql
CREATE OR REPLACE FUNCTION get_url(email STRING)
RETURNS STRING
RETURN 'http://' || split(email, '@')[1]
```

* Splits email at `@`
* Takes the domain (element at index 1)
* Prepends `http://` to produce a URL

### Using a SQL UDF

Invoke UDF in queries as any built-in function:

```sql
SELECT
  customer_id,
  email,
  get_url(email) AS domain_url
FROM customers
```

### Inspecting a UDF

Check metadata using:

```sql
DESCRIBE FUNCTION get_url
```

For detailed logic and registration info:

```sql
DESCRIBE FUNCTION EXTENDED get_url
```

* Shows the database, input and output types
* Displays logic in the `Body` field

---

### Complex Logic with CASE WHEN

UDFs can use conditional expressions such as `CASE WHEN`.

#### Example: Categorize Domain Extension

```sql
CREATE OR REPLACE FUNCTION domain_category(email STRING)
RETURNS STRING
RETURN CASE
  WHEN email LIKE '%.com' THEN 'Commercial'
  WHEN email LIKE '%.org' THEN 'Organization'
  WHEN email LIKE '%.edu' THEN 'Education'
  ELSE 'Unknown'
END
```

Apply the UDF:

```sql
SELECT
  customer_id,
  email,
  domain_category(email) AS category
FROM customers
```

---

### Dropping UDFs

Remove a UDF from the catalog:

```sql
DROP FUNCTION IF EXISTS get_url;
DROP FUNCTION IF EXISTS domain_category;
```

---

## Summary

| Feature               | Function                   | Purpose                                 |
| --------------------- | -------------------------- | --------------------------------------- |
| `filter`              | `filter(array, lambda)`    | Retain array elements meeting condition |
| `transform`           | `transform(array, lambda)` | Apply transformation to array elements  |
| SQL UDF (simple)      | `CREATE FUNCTION`          | Encapsulate logic like domain parsing   |
| SQL UDF (conditional) | `CASE WHEN` in `RETURN`    | Encode rule-based logic                 |
| Reusability           | UDFs stored in database    | Use across sessions and notebooks       |
| Optimization          | Native Spark execution     | Ensures distributed performance         |

Higher-order functions and UDFs provide powerful tools for expressive, reusable, and performant SQL transformations in Spark.
