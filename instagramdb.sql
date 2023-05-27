--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: followernew; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followernew (
    userid character varying(120) NOT NULL,
    username character varying(120) NOT NULL,
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.followernew OWNER TO postgres;

--
-- Name: followerold; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followerold (
    userid character varying(120),
    username character varying(120),
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.followerold OWNER TO postgres;

--
-- Name: followerrecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.followerrecord (
    userid character varying(120) NOT NULL,
    username character varying(120) NOT NULL,
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.followerrecord OWNER TO postgres;

--
-- Name: instascript_tracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instascript_tracker (
    no integer NOT NULL,
    unique_id character varying(10),
    status character varying(2),
    date character varying(120)
);


ALTER TABLE public.instascript_tracker OWNER TO postgres;

--
-- Name: instascript_tracker_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.instascript_tracker_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instascript_tracker_no_seq OWNER TO postgres;

--
-- Name: instascript_tracker_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.instascript_tracker_no_seq OWNED BY public.instascript_tracker.no;


--
-- Name: status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.status (
    no integer NOT NULL,
    status character varying(200),
    reason character varying(200000),
    ended_time character varying(120)
);


ALTER TABLE public.status OWNER TO postgres;

--
-- Name: status_no_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.status_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_no_seq OWNER TO postgres;

--
-- Name: status_no_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.status_no_seq OWNED BY public.status.no;


--
-- Name: temp_follower; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.temp_follower (
    userid character varying(120),
    username character varying(120),
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.temp_follower OWNER TO postgres;

--
-- Name: temp_unfollower; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.temp_unfollower (
    userid character varying(120),
    username character varying(120),
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.temp_unfollower OWNER TO postgres;

--
-- Name: unfollowerrecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.unfollowerrecord (
    userid character varying(120),
    username character varying(120),
    fullname character varying(120),
    url character varying(120),
    dateadded character varying(120)
);


ALTER TABLE public.unfollowerrecord OWNER TO postgres;

--
-- Name: instascript_tracker no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instascript_tracker ALTER COLUMN no SET DEFAULT nextval('public.instascript_tracker_no_seq'::regclass);


--
-- Name: status no; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status ALTER COLUMN no SET DEFAULT nextval('public.status_no_seq'::regclass);


-
--
-- Name: followernew all_follower_current_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followernew
    ADD CONSTRAINT all_follower_current_pkey PRIMARY KEY (userid);


--
-- Name: followernew all_follower_current_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followernew
    ADD CONSTRAINT all_follower_current_username_key UNIQUE (username);


--
-- Name: followerrecord all_follower_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.followerrecord
    ADD CONSTRAINT all_follower_pkey PRIMARY KEY (userid);


--
-- Name: instascript_tracker instascript_tracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instascript_tracker
    ADD CONSTRAINT instascript_tracker_pkey PRIMARY KEY (no);

alter table public.temp_follower rename to follower;
alter table public.temp_unfollower rename to unfollower;
alter table public.followernew rename to follower_latest;
alter table public.followerold rename to follower_old;
ALTER TABLE public.follower_latest ALTER COLUMN userid TYPE bigint USING userid::bigint;
ALTER TABLE public.followerrecord DROP CONSTRAINT all_follower_pkey;
create table public.parameters(id serial primary key,parametername varchar(10000) unique,value varchar(10000))
