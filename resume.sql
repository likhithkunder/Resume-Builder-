drop database if exists `resume_db`;
create database if not exists `resume_db`;
use `resume_db`;

drop table if exists `user`;
create table `user`(
    `user_id` varchar(15) not null,
    `user_name` varchar(15) not null,
    `password` varchar(15) not null,
    `email` varchar(20) not null,
    `name` varchar(20) not null,
    `dob` date,
    `phone_no` varchar(10) not null,
    primary key (`user_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `recruiter`;
create table `recruiter`(
    `recruiter_id` varchar(15) not null,
    `recruiter_name` varchar(15) not null,
    `password` varchar(15) not null,
    `email` varchar(20) not null,
    `name` varchar(20) not null,
    `dob` date,
    `phone_no` varchar(10) not null,
    primary key (`recruiter_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `education`;
create table `education`(
    `ed_id` varchar(10) not null,
    `user_id` varchar(15),
    `institute_name` varchar(20) not null,
    `degree` varchar(10) not null,
    `graduation_year` int not null,
    primary key (`ed_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `works_exp`;
create table `works_exp`(
    `exp_id` varchar(10) not null,
    `user_id` varchar(15),
    `company` varchar(15) not null,
    `job_title` varchar(15) not null,
    `job_desc` varchar(30) not null,
    `no_of_years` int not null,
    primary key (`exp_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `skills`;
create table `skills`(
    `skill_id` varchar(10) not null,
    `user_id` varchar(15),
    `skill_name` varchar(20) not null,
    `proficiency` varchar(10) not null,
    primary key (`skill_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `projects`;
create table `projects`(
    `project_id` varchar(10) not null,
    `user_id` varchar(15),
    `project_name` varchar(20) not null,
    `proj_desc` varchar(30) not null,
    primary key (`project_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `certificates`;
create table `certificates`(
    `c_id` varchar(10) not null,
    `user_id` varchar(15),
    `certificate_name` varchar(20) not null,
    `organisation` varchar(15) not null,
    `issue_date` date not null,
    primary key (`c_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;

drop table if exists `resume`;
create table `resume`(
    `resume_id` varchar(10) not null,
    `user_id` varchar(15),
    `template_name` varchar(15) not null,
    primary key (`resume_id`)
) engine=InnoDB default charset=utf8mb4 collate=utf8mb4_0900_ai_ci;
