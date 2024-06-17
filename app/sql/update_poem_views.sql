UPDATE userPoemTable AS myUser
LEFT JOIN (
    SELECT viewsId
    FROM isViewsTable
) AS sub ON sub.viewsId = %s
WHERE myUSer.id NOT IN (
    SELECT viewsId
    FROM isViewsTable
    WHERE sub.viewsId = %s
) AND myUser.poemSeq = %s