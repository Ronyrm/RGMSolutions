SELECT 
f.*
from fiis f 
WHERE f.dy > 8 AND f.p_vp BETWEEN 0.8 AND 0.99
AND f.liquidez_media_diaria >= 5000000
ORDER BY f.dy DESC, f.liquidez_media_diaria
/* http://127.0.0.1:5000/get/fiis */; 