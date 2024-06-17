-- DBEAVER에 이미 프로시저 등록해놓음
CREATE PROCEDURE views_logic (
	IN pro_viewsId varchar(3000),
	IN pro_viewsSeq INT,
	IN pro_now_date DATETIME
)

BEGIN
	DECLARE check_poemSeq INT;
	
	SELECT viewsPoemSeq INTO check_poemSeq
	FROM isViewsTable
	WHERE viewsId = pro_viewsId AND viewsPoemSeq = pro_viewsSeq;
	
	IF check_poemSeq IS NULL THEN
		INSERT INTO isViewsTable (idSeq, viewsId, viesPoemSeq, view_date)
		VALUES (
			(
				SELECT userSeq
				FROM userTable
				WHERE userId = pro_viewsId
			),
			pro_viewsId,
			pro_viewsSeq,
			pro_now_date
		);
	
		UPDATE userPoemTable 
		SET views = views + 1
		WHERE id = pro_viewsId AND poemSeq = pro_viewsSeq;
	END IF;
END