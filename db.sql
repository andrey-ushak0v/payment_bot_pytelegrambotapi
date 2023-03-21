create table bot_user (
    telegram_id bigint primary key,
    created_at timestamp default current_timestamp not null
);

create table card (
    card_id varchar primary key,
    created_at timestamp default current_timestamp not null,
    brand varchar not null,
    user_id integer not null,
    foreign key(user_id) references bot_user(telegram_id)
);

insert into card (card_id, brand ,user_id) values 
    ('6b553c78-3a93-4e3a-912a-1c7cf8a06303', 'VISA',761928168),
    ('1637261966778548225', 'MASTERCARD', 761928168);
