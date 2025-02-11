create  table meeting(mid serial primary key,
ccode varchar,
starttime timestamp,
endtime timestamp,
cdays varchar(5));

create table room(rid serial primary key ,
building varchar,
room_number varchar,
capacity integer);

create table class(cid serial primary key,
cname varchar,
ccode varchar,
cdesc varchar,
term varchar,
years varchar,
cred int,
csyllabus varchar);

create table section(sid serial primary key,
roomid integer references room(rid),
cid integer references class(cid),
mid integer references meeting(mid),
semester varchar,
years varchar,
capacity int);

create table syllabus(
    chunkid serial primary key,
    courseid integer references class(cid),
    embedding_text vector,
    chunk varchar
);


create table requisite(classid integer references class(cid),
reqid integer references class(cid),
prereq boolean,
primary key (classid, reqid));


create table users(id serial primary key,
username varchar(50) not null unique,
password varchar(255) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp
);


alter table room
add constraint UniqueRooms unique (building, room_number);

 SELECT setval('room_rid_seq', (SELECT COALESCE(MAX(rid),0) FROM room));

alter table class
add constraint UniqueClasses unique (cname, ccode, csyllabus);

 SELECT setval('class_cid_seq', (SELECT COALESCE(MAX(cid),0) FROM class));

alter table requisite
add constraint UniquePrereq unique (classid, reqid);

alter table meeting
add constraint UniqueMeetings unique (ccode, starttime, endtime, cdays);
alter table meeting
add constraint UniqueCode unique(ccode);

 SELECT setval('meeting_mid_seq', (SELECT COALESCE(MAX(mid),0) FROM meeting));

alter table meeting
alter column endtime type time;

alter table section
add constraint UniqueSections unique (mid,roomid, cid, years, semester);

 SELECT setval('section_sid_seq', (SELECT COALESCE(MAX(sid),0)FROM section));