# Advanced Transformations (Hands On)

- This notebook demonstrates advanced Spark SQL transformations using the bookstore dataset, which includes `customers`, `orders`, and `books` tables.
- Key transformations include parsing JSON strings, handling arrays, using aggregations, applying set operations, and pivoting datasets.

---

## Parsing JSON Strings in Columns

### Accessing Nested JSON Values

Spark SQL allows direct access to nested JSON string values using colon syntax:

```sql
SELECT
  profile:firstname AS first_name,
  profile:address:country AS country
FROM customers
````

* Useful for lightweight access without transformation.
* Strings remain untyped and unstructured.

### Converting JSON Strings to Struct Types

Use `from_json` to convert JSON strings into native `struct` types:

```sql
SELECT
  from_json(profile, schema_of_json('{ "firstname": "Jane", "lastname": "Doe", "gender": "F", "address": { "street": "Main", "city": "NY", "country": "USA" } }')) AS profile_struct
FROM customers
```

* Requires a valid JSON schema (can be derived via `schema_of_json()`).
* Produces a typed `struct` column.

### Flattening Struct Columns

Use dot (`.`) notation to extract subfields from struct types:

```sql
SELECT
  profile_struct.firstname,
  profile_struct.lastname,
  profile_struct.gender,
  profile_struct.address.city
FROM parsed_customers
```

Or use `*` to explode all struct fields into individual columns:

```sql
SELECT
  profile_struct.*
FROM parsed_customers
```

---

## Working with Arrays

### Exploding Arrays into Rows

Use the `explode()` function to turn array elements into separate rows:

```sql
SELECT
  customer_id,
  order_id,
  explode(books) AS book
FROM orders
```

Each array element is extracted as a new row. Other columns are repeated.

### Flattening Nested Arrays

Combine `collect_set()` with `flatten()` and `array_distinct()` to aggregate and deduplicate array values:

```sql
SELECT
  customer_id,
  array_distinct(flatten(collect_set(books.book_id))) AS unique_books
FROM orders
GROUP BY customer_id
```

* `collect_set`: gathers unique arrays
* `flatten`: collapses nested arrays into a single array
* `array_distinct`: removes duplicate values

---

## Join Operations

Spark SQL supports standard join types:

* `INNER JOIN`
* `LEFT JOIN`
* `RIGHT JOIN`
* `FULL OUTER JOIN`
* `LEFT SEMI JOIN`
* `LEFT ANTI JOIN`
* `CROSS JOIN`

### Example: Enriching Orders with Book Details

```sql
SELECT
  o.customer_id,
  o.order_id,
  b.title,
  b.author,
  b.category
FROM exploded_orders o
INNER JOIN books b
ON o.book.book_id = b.book_id
```

---

## Set Operations

### UNION

Combines rows from two datasets:

```sql
SELECT * FROM orders
UNION
SELECT * FROM orders_updates
```

### INTERSECT

Returns only records present in both datasets:

```sql
SELECT * FROM orders
INTERSECT
SELECT * FROM orders_updates
```

### EXCEPT

Returns records present in the first dataset but not in the second:

```sql
SELECT * FROM orders
EXCEPT
SELECT * FROM orders_updates
```

---

## Pivoting Data

The `PIVOT` clause aggregates and rotates data columns into rows.

### Syntax

```sql
SELECT *
FROM (
  SELECT customer_id, book_id, price FROM orders
)
PIVOT (
  SUM(price) FOR book_id IN ('B01', 'B02', 'B03')
)
```

### Explanation

* The inner query defines the base dataset.
* `SUM(price)` is the aggregation function.
* `book_id` is the pivot key.
* `'B01', 'B02', 'B03'` become column headers.

**Use Case:** Flattening order data for each customer to prepare for visualization or machine learning pipelines.

---

## Summary

| Transformation        | Function / Syntax                | Use Case                                  |
| --------------------- | -------------------------------- | ----------------------------------------- |
| JSON traversal        | `json_column:key1:key2`          | Read values from JSON strings             |
| JSON to struct        | `from_json()`                    | Parse and type JSON content               |
| Explode arrays        | `explode()`                      | One row per array element                 |
| Flatten nested arrays | `flatten()` + `array_distinct()` | Remove nested array levels and duplicates |
| Joins                 | `JOIN` variants                  | Combine datasets                          |
| Set operations        | `UNION`, `INTERSECT`, `EXCEPT`   | Compare datasets                          |
| Pivoting              | `PIVOT`                          | Transform rows into columns               |

Spark SQL's advanced features allow deep data manipulation for analytics, ETL, and data science workflows.
