trigger_cests_before_insert_drop = "DROP TRIGGER IF EXISTS cests_before_insert;"
trigger_cests_before_insert= "CREATE TRIGGER cests_before_insert BEFORE INSERT ON cests \n"\
"FOR EACH ROW BEGIN\n"\
"SET NEW.idncm = (SELECT ncms.id FROM ncms WHERE ncms.codigo=NEW.codncm);\n"\
"END\n"


trigger_itemdieta_after_delete_drop = "DROP TRIGGER IF EXISTS itemdieta_after_delete;"
trigger_itemdieta_after_delete = "CREATE TRIGGER itemdieta_after_delete AFTER DELETE ON itemdieta \n"\
"FOR EACH ROW BEGIN\n"\
"		UPDATE dieta\n"\
"		SET dieta.totalcarbo = dieta.totalcarbo - old.totalcarbo,\n"\
"		dieta.totalproteina = dieta.totalproteina - old.totalproteina,\n"\
"		dieta.totalgordura = dieta.totalgordura - old.totalgordura,\n"\
"		dieta.totalfibras = dieta.totalfibras - old.totalfibras,\n"\
"		dieta.totalsodio = dieta.totalsodio - old.totalsodio,\n"\
"		dieta.totalcalorias = dieta.totalcalorias - old.totalcalorias\n"\
"	WHERE dieta.id = old.iddieta;\n"\
"END\n"


trigger_itemdieta_after_insert_drop = "DROP TRIGGER IF EXISTS itemdieta_after_insert"
trigger_itemdieta_after_insert = "CREATE TRIGGER itemdieta_after_insert AFTER INSERT ON itemdieta\n"\
"FOR EACH ROW BEGIN\n"\
"	UPDATE dieta\n"\
"		SET dieta.totalcarbo = dieta.totalcarbo + NEW.totalcarbo,\n"\
"		dieta.totalproteina = dieta.totalproteina + NEW.totalproteina,\n"\
"		dieta.totalgordura = dieta.totalgordura + NEW.totalgordura,\n"\
"		dieta.totalfibras = dieta.totalfibras + NEW.totalfibras,\n"\
"		dieta.totalsodio = dieta.totalsodio + NEW.totalsodio,\n"\
"		dieta.totalcalorias = dieta.totalcalorias + NEW.totalcalorias\n"\
"	WHERE dieta.id = NEW.iddieta;\n"\
"END\n"


trigger_itemdieta_after_update_drop = "DROP TRIGGER IF EXISTS itemdieta_after_update;"
trigger_itemdieta_after_update = "CREATE TRIGGER itemdieta_after_update AFTER UPDATE ON itemdieta \n"\
"FOR EACH ROW BEGIN\n"\
"		UPDATE dieta\n"\
"		SET dieta.totalcarbo = dieta.totalcarbo - old.totalcarbo,\n"\
"		dieta.totalproteina = dieta.totalproteina - old.totalproteina,\n"\
"		dieta.totalgordura = dieta.totalgordura - old.totalgordura,\n"\
"		dieta.totalfibras = dieta.totalfibras - old.totalfibras,\n"\
"		dieta.totalsodio = dieta.totalsodio - old.totalsodio,\n"\
"		dieta.totalcalorias = dieta.totalcalorias - old.totalcalorias\n"\
"		WHERE dieta.id = old.iddieta;\n"\
"		UPDATE dieta\n"\
"		SET dieta.totalcarbo = dieta.totalcarbo + NEW.totalcarbo,\n"\
"		dieta.totalproteina = dieta.totalproteina + NEW.totalproteina,\n"\
"		dieta.totalgordura = dieta.totalgordura + NEW.totalgordura,\n"\
"		dieta.totalfibras = dieta.totalfibras + NEW.totalfibras,\n"\
"		dieta.totalsodio = dieta.totalsodio + NEW.totalsodio,\n"\
"		dieta.totalcalorias = dieta.totalcalorias + NEW.totalcalorias\n"\
"		WHERE dieta.id = NEW.iddieta;\n"\
"END\n"

trigger_metaatleta_after_update_drop = "DROP TRIGGER IF EXISTS metaatleta_after_update;"
trigger_metaatleta_after_update = "CREATE TRIGGER metaatleta_after_update AFTER UPDATE ON metaatleta \n"\
"FOR EACH ROW BEGIN\n"\
"	IF(NEW.status='F')THEN\n"\
"		UPDATE atleta\n"\
"		SET atleta.peso = NEW.pesofinalizado\n"\
"		WHERE atleta.id = NEW.idatleta;\n"\
"	END IF;\n"\
"END\n"

sql_array = {0:trigger_itemdieta_after_delete_drop,
             1:trigger_itemdieta_after_insert_drop,
             2:trigger_itemdieta_after_update_drop,
             3:trigger_metaatleta_after_update_drop,
             4:trigger_itemdieta_after_delete,
             5:trigger_itemdieta_after_insert,
             6:trigger_itemdieta_after_update,
             7:trigger_metaatleta_after_update,
             8:trigger_cests_before_insert_drop,
             9:trigger_cests_before_insert}





