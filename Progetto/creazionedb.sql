--CREAZIONE TABELLE
drop table if exists immagine cascade;
drop table if exists macrocategoria cascade;
drop table if exists appartenenza cascade;
drop table if exists rete_neurale cascade;
drop table if exists classificazione cascade;
drop table if exists categoria cascade;
drop table if exists valorizzazione cascade;
drop table if exists composizione cascade;
drop table if exists prestazione cascade;
drop table if exists etnia cascade;
drop table if exists emozione cascade;
drop table if exists genere cascade;

create table immagine(
	codice serial primary key,
	image varchar(100) not null unique
);
	
create table macrocategoria(
	nome varchar(30) primary key,
	descrizione varchar(500) not null
);

create table appartenenza(
	id serial primary key,
	macrocategoria_id varchar(30) not null references macrocategoria(nome) on delete cascade on update cascade,
	immagine_id integer not null references immagine(codice) on delete cascade on update cascade,
	unique(macrocategoria_id, immagine_id)
);

create table rete_neurale(
	codice serial primary key,
	nome varchar(30) not null unique,
	descrizione varchar(500) not null,
	ultimo_ripristino date not null,
	macrocategoria_id varchar(30) not null references macrocategoria(nome) on delete restrict on update cascade
);

create table categoria(
	nome varchar(30) primary key,
	tipo varchar(30) not null,
	int_max integer
);

create table classificazione(
	id serial primary key,
	data date not null,
	rete_neurale_id integer not null references rete_neurale(codice) on delete restrict on update cascade,
	categoria_id varchar(30) not null references categoria(nome) on delete restrict on update cascade,
	immagine_id integer not null references immagine(codice) on delete restrict on update cascade,
	valore_rn varchar(30) not null,
	threshold numeric(3,2) not null default 0.4
);

create table valorizzazione(
	id serial primary key,
	categoria_id varchar(30) not null references categoria(nome) on delete restrict on update cascade,
	immagine_id integer not null references immagine(codice) on delete cascade on update cascade,
	valore_v varchar(30) not null,
	unique(categoria_id, immagine_id)
);

create table composizione(
	id serial primary key,
	macrocategoria_id varchar(30) not null references macrocategoria(nome) on delete cascade on update cascade,
	categoria_id varchar(30) not null references categoria(nome) on delete restrict on update cascade,
	unique(macrocategoria_id, categoria_id)
);

create table prestazione(
	id serial primary key,
	rete_neurale_id integer not null references rete_neurale(codice) on delete cascade on update cascade,
	categoria_id varchar(30) not null references categoria(nome) on delete restrict on update cascade,
	valore_p numeric(5,2) default null,
	unique(rete_neurale_id, categoria_id)
);

create table etnia(
	opzione varchar(50) primary key
);
create table emozione(
	opzione varchar(50) primary key
);
create table genere(
	opzione varchar(50) primary key
);


--FINE CREAZIONE TABELLE
