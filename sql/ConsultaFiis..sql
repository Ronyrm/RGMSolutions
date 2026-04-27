SELECT 
GROUP_CONCAT(concat(F.ticker,'') ORDER BY F.ticker)
from fiis f 
WHERE 
(f.dy > 8 AND f.p_vp BETWEEN 0.8 AND 0.99
AND f.liquidez_media_diaria >= 5000000)  
/*OR f.ticker IN ('ALZR11','CPTS11','HGLG11','KNCR11','KNRI11','RECR11','XPML11')*/
ORDER BY f.dy DESC, f.liquidez_media_diaria
