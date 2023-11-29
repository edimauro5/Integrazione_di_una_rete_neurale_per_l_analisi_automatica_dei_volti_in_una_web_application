
--CREAZIONE TRIGGER
DROP TRIGGER IF EXISTS modify_performance ON classificazione;
DROP TRIGGER IF EXISTS reset_performance ON rete_neurale;
DROP TRIGGER IF EXISTS ins_macrocategoria ON macrocategoria;
DROP TRIGGER IF EXISTS ins_categoria ON categoria;
DROP TRIGGER IF EXISTS ins_immagine ON immagine;

CREATE OR REPLACE FUNCTION modify_performance()
RETURNS TRIGGER AS
$BODY$
DECLARE
	t varchar(30);
	num numeric(5,2);
	ult_rip date;
	prest numeric(5,2);
BEGIN
	SELECT V.valore_v INTO t FROM valorizzazione AS V 
	WHERE V.categoria_id = NEW.categoria_id 
		AND V.immagine_id = NEW.immagine_id;
   SELECT count(*) INTO num FROM classificazione AS C, rete_neurale AS RN 
	WHERE C.rete_neurale_id = RN.codice 
		AND C.rete_neurale_id = NEW.rete_neurale_id 
		AND C.categoria_id=NEW.categoria_id 
		AND C.data >= RN.ultimo_ripristino;
	SELECT RN.ultimo_ripristino into ult_rip FROM rete_neurale AS RN 
	WHERE RN.codice=NEW.rete_neurale_id;
	SELECT P.valore_p into prest FROM prestazione AS P 
	WHERE P.rete_neurale_id=new.rete_neurale_id 
		AND P.categoria_id=NEW.categoria_id;
	IF (prest IS NULL) THEN 
		prest = 0;
	END IF;
	IF (NEW.data >= ult_rip) THEN 
		IF(SUBSTRING(t,1,1)>'0' AND SUBSTRING(t,1,1)<'9') THEN
			UPDATE prestazione 
			SET valore_p = (
				prest * (num-1) + 
				ABS(
					cast(t as numeric(5,2)) - 
					cast(NEW.valore_rn as numeric(5,2))
					)
						   )/(num) 
			WHERE prestazione.rete_neurale_id=NEW.rete_neurale_id 
				AND prestazione.categoria_id=NEW.categoria_id;
		ELSE
			UPDATE prestazione 
			SET valore_p = ( 
				prest * (num-1) + 
				cast(upper(t)=upper(NEW.valore_rn) as integer)
							)/(num) 
			WHERE prestazione.rete_neurale_id=NEW.rete_neurale_id 
			AND prestazione.categoria_id=NEW.categoria_id;
		END IF;
	END IF;
	RETURN NEW;	
END;
$BODY$
LANGUAGE PLPGSQL;


CREATE TRIGGER modify_performance
AFTER INSERT
ON classificazione
FOR EACH ROW
EXECUTE PROCEDURE modify_performance();



CREATE OR REPLACE FUNCTION reset_performance()
RETURNS TRIGGER AS
$BODY$
BEGIN
	UPDATE prestazione as P 
	SET valore_p=NULL 
	WHERE P.rete_neurale_id=new.codice;
	RETURN NEW;
END;
$BODY$
LANGUAGE PLPGSQL;



CREATE TRIGGER reset_performance
AFTER UPDATE OF ultimo_ripristino
ON rete_neurale
FOR EACH ROW
EXECUTE PROCEDURE reset_performance();


CREATE OR REPLACE FUNCTION ins_macrocategoria()
RETURNS TRIGGER AS
$BODY$
BEGIN
IF( NOT EXISTS ( SELECT * FROM composizione 
				 WHERE macrocategoria_id=NEW.nome)) THEN
 	RAISE EXCEPTION 
		'Nessuna Categoria associata alla Macrocategoria %',NEW.nome;
END IF;
RETURN NULL;
END $BODY$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER ins_macrocategoria
AFTER INSERT ON macrocategoria
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE PROCEDURE ins_macrocategoria();


CREATE OR REPLACE FUNCTION ins_categoria()
RETURNS TRIGGER AS
$BODY$
BEGIN
IF( NOT EXISTS ( SELECT * FROM composizione 
				 WHERE categoria_id=NEW.nome)) THEN
	RAISE EXCEPTION 
		'Nessuna Macrocategoria associata alla Categoria %',NEW.nome;
END IF;
RETURN NULL;
END $BODY$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER ins_categoria
AFTER INSERT ON categoria
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE PROCEDURE ins_categoria();


CREATE OR REPLACE FUNCTION ins_immagine()
RETURNS TRIGGER AS
$BODY$
DECLARE
num_cat integer;
num_val integer;
BEGIN
IF( NOT EXISTS ( SELECT * FROM appartenenza
				 WHERE immagine_id=NEW.codice)) THEN
 	RAISE EXCEPTION 
		'Nessuna Macrocategoria associata all''Immagine scelta';
ELSE 
   SELECT count(*) INTO num_cat FROM composizione as C, appartenenza as A
   WHERE A.immagine_id=new.codice 
   		 AND A.macrocategoria_id=C.macrocategoria_id;
	SELECT count(*) INTO num_val FROM valorizzazione 
	WHERE immagine_id=new.codice;
	IF (num_cat<>num_val ) THEN
	   RAISE EXCEPTION 
		'Non tutte le Categorie associate all''Immagine sono valorizzate';
	END IF;
END IF;
RETURN NULL;
END $BODY$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER ins_immagine
AFTER INSERT ON immagine
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE PROCEDURE ins_immagine();

--FINE CREAZIONE TRIGGER
