-- DBEAVER에 이미 프로시저 등록해놓음

-- CREATE PROCEDURE toggle_like (
--     IN pro_goodsId VARCHAR(3000),
--     IN pro_goodsPoemSeq INT,
--     IN pro_now_date DATETIME
-- )


-- BEGIN
--     DECLARE like_status BOOLEAN;

--     -- 현재 좋아요 상태 확인
--     SELECT goods_status INTO like_status
--     FROM isGoodsTable
--     WHERE goodsId = pro_goodsId AND goodsPoemSeq = pro_goodsPoemSeq;

--     -- 좋아요 체크 또는 업데이트
--     IF like_status IS NULL THEN
--         INSERT INTO isGoodsTable (idSeq, goodsId, goodsPoemSeq, goods_date, goods_cancel_date) 
--         VALUES (
--             (SELECT userSeq FROM userTable WHERE userId = pro_goodsId),
--             pro_goodsId,
--             pro_goodsPoemSeq,
--             pro_now_date,
--             NULL
--         );

--         UPDATE userPoemTable
--         SET goods = goods + 1
--         WHERE id = pro_goodsId AND poemSeq = pro_goodsPoemSeq;
--     ELSEIF like_status = FALSE THEN
--         UPDATE isGoodsTable
--         SET goods_status = TRUE, goods_date = pro_now_date
--         WHERE goodsId = pro_goodsId AND goodsPoemSeq = pro_goodsPoemSeq;

--         UPDATE userPoemTable
--         SET goods = goods + 1
--         WHERE id = pro_goodsId AND poemSeq = pro_goodsPoemSeq;
--     ELSE
--         UPDATE isGoodsTable
--         SET goods_status = FALSE, goods_cancel_date = pro_now_date
--         WHERE goodsId = pro_goodsId AND goodsPoemSeq = pro_goodsPoemSeq;

--         UPDATE userPoemTable
--         SET goods = goods - 1
--         WHERE id = pro_goodsId AND poemSeq = pro_goodsPoemSeq;
--     END IF;
-- END 

CALL toggle_like(%s, %s, %s);
