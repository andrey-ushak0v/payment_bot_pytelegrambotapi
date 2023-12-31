create table bot_user (
    telegram_id bigint primary key,
    created_at timestamp default current_timestamp not null,
    user_status varchar not null
);

create table card (
    card_id varchar primary key,
    created_at timestamp default current_timestamp not null,
    last_four_nums integer not null, 
    brand varchar not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table replenishment (
    transaction_hash varchar primary key,
    created_at timestamp default current_timestamp not null,
    payment_type varchar not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table pasport_name (
    p_name varchar,
    created_at timestamp default current_timestamp not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table pasport_number (
    p_number int not null,
    created_at timestamp default current_timestamp not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table pasport_photo (
    p_photo_id varchar primary key not null,
    created_at timestamp default current_timestamp not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table pasport_selphe (
    p_photo_id varchar primary key not null,
    created_at timestamp default current_timestamp not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

create table transactions (
    transaction_id varchar primary key not null,
    created_at timestamp default current_timestamp not null,
    transaction_amount integer not null,
    transaction_status varchar not null,
    transaction_type varchar not null,
    id_card integer not null,
    foreign key(id_card) references card(card_id)
);

insert into card (card_id, last_four_nums, brand, user_id) values 
    ('6b553c78-3a93-4e3a-912a-1c7cf8a06303', 6823, 'VISA',761928168),
    ('fdcecc33-3b10-4eac-80e7-f43de82c0f57', 0388, 'VISA', 761928588);
