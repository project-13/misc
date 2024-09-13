WITH ranges AS (
    SELECT
        FLOOR(id / 100) AS truncated_id,
        FLOOR(id / 100) - LAG(FLOOR(id / 100), 1, FLOOR(id / 100)) OVER (ORDER BY FLOOR(id / 100)) AS diff_prev,
        LEAD(FLOOR(id / 100), 1, FLOOR(id / 100)) OVER (ORDER BY FLOOR(id / 100)) - FLOOR(id / 100) AS diff_next
    FROM
        your_table
)
SELECT
    CASE
        WHEN diff_prev = 1 AND diff_next = 1 THEN NULL
        WHEN diff_prev = 1 AND diff_next > 1 THEN TO_CHAR(truncated_id)
        WHEN diff_prev > 1 AND diff_next = 1 THEN TO_CHAR(truncated_id)
        WHEN diff_prev > 1 AND diff_next > 1 THEN TO_CHAR(truncated_id)
        ELSE TO_CHAR(LAG(truncated_id, 1) OVER (ORDER BY truncated_id)) || '-' || TO_CHAR(truncated_id)
    END AS range
FROM
    ranges
WHERE diff_prev > 1 OR diff_next > 1
OR truncated_id = (SELECT FLOOR(MIN(id) / 100) FROM your_table)
OR truncated_id = (SELECT FLOOR(MAX(id) / 100) FROM your_table);
