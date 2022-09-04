submitted_cases11_table = """
    create table if not exists submitted_cases11
    (
        case_id varchar(64) not null primary key,
        submitted_by varchar(24) not null,
        name varchar(64) not null,
        father_name varchar(64) not null,
        loc varchar(64) not null,
        age integer not null,
        mobile bigint,
        face_encoding jsonb,
        image varchar(200000),
        updated_on timestamp default CURRENT_TIMESTAMP not null,
        status varchar(24) not null
    )"""
users11_tables = """
    create table if not exists users11
    (
        username varchar(20) not null constraint users11_pk primary key,
        password varchar(64) not null,
        role varchar(10) not null
    )"""

admin_user11_query = (
    "insert into users11(username, password, role) values('admin', 'admin', 'RW')"
)
