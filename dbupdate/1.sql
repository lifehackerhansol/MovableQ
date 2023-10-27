-- V1: Initial commit
-- Create all required tables

create table jobs
(
    job_id BIGINT PRIMARY KEY,
    id0 varchar(32) NOT NULL,
    lfcs varchar(8) DEFAULT NULL,
    friend_code varchar(12) DEFAULT NULL,
    system_id varchar(16) DEFAULT NULL,
    keyY varchar(32) DEFAULT NULL,
);
