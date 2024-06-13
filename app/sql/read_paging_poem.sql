SELECT poemSeq, title, writer, write_date, views, goods 
from userPoemTable WHERE id = %s  
LIMIT %s OFFSET %s;