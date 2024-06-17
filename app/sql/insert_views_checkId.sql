INSERT INTO isViewsTable (idSeq, viewsId, viewsPoemSeq, views_date)
SELECT (SELECT userSeq FROM userTable WHERE userId = %s), %s, %s, %s
WHERE NOT EXISTS (
    SELECT 1 
    FROM isViewsTable
    WHERE viewsId = %s AND viewsPoemSeq = %s
);