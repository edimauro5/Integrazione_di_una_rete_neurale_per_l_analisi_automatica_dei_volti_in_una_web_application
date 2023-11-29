--POPOLAMENTO DB
-- ALTER SEQUENCE immagine_codice_seq RESTART WITH 1;
-- ALTER SEQUENCE appartenenza_id_seq RESTART WITH 1;
-- ALTER SEQUENCE rete_neurale_codice_seq RESTART WITH 1;
-- ALTER SEQUENCE classificazione_id_seq RESTART WITH 1;
-- ALTER SEQUENCE valorizzazione_id_seq RESTART WITH 1;
-- ALTER SEQUENCE composizione_id_seq RESTART WITH 1;
-- ALTER SEQUENCE prestazione_id_seq RESTART WITH 1;

--start inserimento categoria e macrocategorie
begin transaction;
insert into macrocategoria(nome, descrizione) values('Face Counting', 'Conteggio numero di volti in foto');
insert into categoria(nome, tipo, int_max) values('Numero Volti','Number', 70);
insert into composizione(macrocategoria_id, categoria_id) values ('Face Counting', 'Numero Volti');
commit;

begin transaction;
insert into macrocategoria(nome, descrizione) values('People Counting', 'Conteggio numero di persone in foto');
insert into categoria(nome, tipo, int_max) values('Numero Persone','Number', 70);
insert into composizione(macrocategoria_id, categoria_id) values ('People Counting', 'Numero Persone');
commit;

begin transaction;
insert into macrocategoria(nome, descrizione) values('Vehicle Counting', 'Conteggio numero di veicoli in foto');
insert into categoria(nome, tipo, int_max) values('Numero Veicoli','Number', 70);
insert into composizione(macrocategoria_id, categoria_id) values ('Vehicle Counting', 'Numero Veicoli');
commit;

begin transaction;
insert into macrocategoria(nome, descrizione) values('Face Analysis', 'Valutazione caratteristiche di un volto in foto');
insert into categoria(nome, tipo, int_max) values('Età','Number',120);
insert into categoria(nome, tipo) values('Etnia','Select');
insert into categoria(nome, tipo) values('Emozione','Select');
insert into categoria(nome, tipo) values('Genere','Radio');
insert into composizione(macrocategoria_id, categoria_id) values ('Face Analysis', 'Età');
insert into composizione(macrocategoria_id, categoria_id) values ('Face Analysis', 'Genere');
insert into composizione(macrocategoria_id, categoria_id) values ('Face Analysis', 'Etnia');
insert into composizione(macrocategoria_id, categoria_id) values ('Face Analysis', 'Emozione');
commit;
--end inserimento categoria e macrocategoria

--rete neurale
insert into rete_neurale(nome, descrizione, ultimo_ripristino, macrocategoria_id) values ('Count Faces', 'Effettua il conteggio dei volti in una foto', current_date, 'Face Counting');
insert into rete_neurale(nome, descrizione, ultimo_ripristino, macrocategoria_id) values ('Count People', 'Effettua il conteggio delle persone in una foto', current_date, 'People Counting');
insert into rete_neurale(nome, descrizione, ultimo_ripristino, macrocategoria_id) values ('Count Vehicles', 'Effettua il conteggio dei veicoli in una foto', current_date, 'Vehicle Counting');
insert into rete_neurale(nome, descrizione, ultimo_ripristino, macrocategoria_id) values ('Face Bio', 'Effettua l''analisi dei volti in una foto', current_date, 'Face Analysis');

--prestazione
insert into prestazione(rete_neurale_id, categoria_id) values(1, 'Numero Volti');
insert into prestazione(rete_neurale_id, categoria_id) values(2, 'Numero Persone');
insert into prestazione(rete_neurale_id, categoria_id) values(3, 'Numero Veicoli');
insert into prestazione(rete_neurale_id, categoria_id) values(4, 'Età');
insert into prestazione(rete_neurale_id, categoria_id) values(4, 'Genere');
insert into prestazione(rete_neurale_id, categoria_id) values(4, 'Etnia');
insert into prestazione(rete_neurale_id, categoria_id) values(4, 'Emozione');

--genere
insert into genere(opzione) values('M');
insert into genere(opzione) values('F');

--etnia
insert into etnia(opzione) values('Afro-Americana');
insert into etnia(opzione) values('Asiatico-Indiana');
insert into etnia(opzione) values('Caucaso-Latina');
insert into etnia(opzione) values('Est-Asiatica');

--emozione
insert into emozione(opzione) values('Disgusto');
insert into emozione(opzione) values('Gioia');
insert into emozione(opzione) values('Neutra');
insert into emozione(opzione) values('Paura');
insert into emozione(opzione) values('Rabbia');
insert into emozione(opzione) values('Sorpresa');
insert into emozione(opzione) values('Tristezza');

--FINE POPOLAMENTO