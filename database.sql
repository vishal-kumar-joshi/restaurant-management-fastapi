create database restorent_db;

use restorent_db;

create table admins (
	id int auto_increment primary key,
    username varchar(50) unique not null,
    password varchar(255) not null ,
    created_at timestamp default current_timestamp
    );
    
create table categories (
id int auto_increment primary key,
name varchar(100) not null unique
);
    
  
create table restaurant_tables (
id int auto_increment primary key,
table_number int not null unique,
qr_code varchar(255)
);

create table menu_items (
id int auto_increment primary key,
category_id int,
name varchar(150) not null,
description text,
price decimal (10,2) not null,
image varchar(255),
is_veg boolean default true,
available boolean default true,
created_at timestamp default current_timestamp,
foreign key (category_id) references categories(id) on delete set null
);

create table orders (
id int auto_increment primary key,
table_id int not null,
total_amount decimal(10,2) default 0,
payment_mode enum('cash' , 'online') not null,
payment_status enum('pending','paid','failed','refunded' ) default 'pending',
order_status enum('pending','preparing','served','cancelled') default 'pending',
customer_note text,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
foreign key (table_id) references restaurant_tables(id) on delete cascade
);


create table order_items (
id int auto_increment primary key,
order_id int not null,
menu_item_id int not null,
quantity int not null,
price decimal(10,2) not null,
foreign key(order_id) references orders(id) on delete cascade,
foreign key(menu_item_id) references menu_items(id) on delete cascade
);

