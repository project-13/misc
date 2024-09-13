WITH ranges AS (
    SELECT
        id,
        id - LAG(id, 1, id) OVER (ORDER BY id) AS diff_prev,
        LEAD(id, 1, id) OVER (ORDER BY id) - id AS diff_next
    FROM
        your_table
)
SELECT
    CASE
        WHEN diff_prev = 1 AND diff_next = 1 THEN NULL
        WHEN diff_prev = 1 AND diff_next > 1 THEN TO_CHAR(id)
        WHEN diff_prev > 1 AND diff_next = 1 THEN TO_CHAR(id)
        WHEN diff_prev > 1 AND diff_next > 1 THEN TO_CHAR(id)
        ELSE TO_CHAR(LAG(id, 1) OVER (ORDER BY id)) || '-' || TO_CHAR(id)
    END AS range
FROM
    ranges
WHERE diff_prev > 1 OR diff_next > 1
OR id = (SELECT MIN(id) FROM your_table)
OR id = (SELECT MAX(id) FROM your_table);
