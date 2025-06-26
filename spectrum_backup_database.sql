--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.2

-- Started on 2025-06-26 17:39:16

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- TOC entry 220 (class 1259 OID 81954)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    id integer NOT NULL,
    email character varying,
    username character varying,
    hashed_password character varying,
    is_active boolean,
    last_login timestamp without time zone,
    last_login_ip character varying
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 81953)
-- Name: admins_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.admins_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admins_id_seq OWNER TO postgres;

--
-- TOC entry 4827 (class 0 OID 0)
-- Dependencies: 219
-- Name: admins_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.admins_id_seq OWNED BY public.admins.id;


--
-- TOC entry 222 (class 1259 OID 81966)
-- Name: spectrum_licenses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spectrum_licenses (
    license_id integer NOT NULL,
    user_id integer NOT NULL,
    is_active boolean,
    created_at timestamp without time zone,
    expires_at timestamp without time zone,
    description character varying,
    current_status character varying NOT NULL,
    subband_range character varying,
    power_level character varying,
    geographical_area character varying,
    license_key character varying NOT NULL
);


ALTER TABLE public.spectrum_licenses OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 81965)
-- Name: spectrum_licenses_license_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.spectrum_licenses_license_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.spectrum_licenses_license_id_seq OWNER TO postgres;

--
-- TOC entry 4828 (class 0 OID 0)
-- Dependencies: 221
-- Name: spectrum_licenses_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.spectrum_licenses_license_id_seq OWNED BY public.spectrum_licenses.license_id;


--
-- TOC entry 218 (class 1259 OID 81941)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying,
    username character varying,
    hashed_password character varying,
    last_login timestamp without time zone,
    last_login_ip character varying,
    company character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 81940)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4829 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4652 (class 2604 OID 81957)
-- Name: admins id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins ALTER COLUMN id SET DEFAULT nextval('public.admins_id_seq'::regclass);


--
-- TOC entry 4653 (class 2604 OID 81969)
-- Name: spectrum_licenses license_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spectrum_licenses ALTER COLUMN license_id SET DEFAULT nextval('public.spectrum_licenses_license_id_seq'::regclass);


--
-- TOC entry 4651 (class 2604 OID 81944)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4819 (class 0 OID 81954)
-- Dependencies: 220
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (id, email, username, hashed_password, is_active, last_login, last_login_ip) FROM stdin;
6	isla.evans@spectrumcreate.com	islaevans	$2b$12$SpM48CWjjiRyFrZM21C8ieAG1Hx29CS6vsu6Oomffe2vSzgLOvf0C	t	2025-06-26 15:22:44.926158	127.0.0.1
7	noah.morgan@spectrumcreate.com	noahmorgan	$2b$12$RcSfflaj2.LmHNwsVCRtKu8sSNigIrtNH0zhn6z1PDfRNdR.aU.S2	t	2025-06-26 15:22:58.066384	127.0.0.1
10	sophia.moore@spectrumcreate.com	sophiamoore	$2b$12$Zrmlmt1k9T1mHt9DgUc5R.fKkAku3vpQnffnboKuKip1JT06MHtAW	t	2025-06-26 15:23:44.004901	127.0.0.1
11	ethan.clark@spectrumcreate.com	ethanclark	$2b$12$ojWkeKbSct/uJIFh8YXhW..J0i0yBwfoEhMFlBOEjpZ.cGnExWOgC	t	2025-06-26 15:23:59.780063	127.0.0.1
12	mia.hill@spectrumcreate.com	miahill	$2b$12$kYN4p5aEshNPGdUP9j/W2uypDhAtx8U4VdhSBx7yMKMAbryifsGSu	t	2025-06-26 15:24:16.501801	127.0.0.1
8	ava.thomas@spectrumcreate.com	avathomas	$2b$12$5Q92D0w025kmme58.k0HL.BWE.0yiDVK5uRIU3TpkCtRVHHej0O9i	t	2025-06-26 16:25:36.141145	127.0.0.1
9	jacob.scott@spectrumcreate.com	jacobscott	$2b$12$BAz0ap1WMiGzXgx7QvUFq.MfXM.sS0ObEkh73E8AIWQvMwydQn/T2	t	2025-06-26 17:00:30.429823	127.0.0.1
3	oliver.jenkins@spectrumcreate.com	oliverjenkins	$2b$12$49ykr3/BVQHYMWkdPWB1nOQIp419gL9FyDM.OrAQ3.8gSgEKAEGwa	t	2025-06-26 17:04:03.423432	127.0.0.1
4	amelia.wright@spectrumcreate.com	ameliawright	$2b$12$LsNCaDmxxpK1YYURJ/mv3uQHBb/4DrJElEtIB2Yft9Br7Sk16GpzS	t	2025-06-26 15:21:25.004641	127.0.0.1
5	liam.harris@spectrumcreate.com	liamharris	$2b$12$p4KW7ex7z5Ph/l6Gvfb1N.ybHLvj26wHhuoU/HqzOeBf0bRlPV8ze	t	2025-06-26 15:21:42.445239	127.0.0.1
\.


--
-- TOC entry 4821 (class 0 OID 81966)
-- Dependencies: 222
-- Data for Name: spectrum_licenses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spectrum_licenses (license_id, user_id, is_active, created_at, expires_at, description, current_status, subband_range, power_level, geographical_area, license_key) FROM stdin;
23	15	f	2025-06-26 16:51:27.015511	\N	Echolicence2	application submitted	100	10	Birmingham	406358c4-feac-4ad5-a703-0c3c06c8279e
22	15	f	2025-06-26 16:51:15.157308	\N	Echolicence1	revoked	150	15	London	cc2cca72-1d72-484d-821d-6dcb8112f79f
27	11	f	2025-06-26 16:54:38.452125	\N	AlphaCorpFirst	application submitted	2000	20	Scotland	ce3da29d-560e-4e46-a117-9c7429018552
29	14	f	2025-06-26 16:57:09.464325	\N	DeltaWorksNonOfficial	application submitted	650	95	Birmingham	93710aa7-cfa1-45a1-a6a8-377aabfe7ac3
32	18	f	2025-06-26 16:59:34.147016	\N	HotelAlphasSecondtKey	revoked	150	45	London	33baee6f-efae-4918-a0cf-a348465d1aab
24	19	t	2025-06-26 16:52:18.111904	2025-07-26 16:01:07.616575	IndiaLicenceEchoLTD	license active	100	10	Glasgow	72031510-4263-44bf-aa48-95231da2473b
28	14	f	2025-06-26 16:56:51.698946	\N	DeltaWorksOfficial	revoked	1000	15	Scotland	747445b4-f211-4154-9e8d-466dac15133d
26	16	f	2025-06-26 16:53:43.8453	\N	FoxtrotSecond	declined	6000	80	Northern ireland	eda01f67-915c-49b0-a5e5-64c7545d4d79
25	16	t	2025-06-26 16:53:31.485106	2025-07-26 16:02:20.044645	Foxtrot	license active	5500	80	Northern ireland	cfd4f50b-dad3-4ab2-b41d-81bfa5ca54c3
30	18	f	2025-06-26 16:58:38.361894	\N	HotelAlpha'sFirstKey	declined	150	45	London	a1294c7b-ab4b-41f9-a9e2-08f2e73ac3dd
\.


--
-- TOC entry 4817 (class 0 OID 81941)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, username, hashed_password, last_login, last_login_ip, company) FROM stdin;
17	golfplayer1@gmail.com	golfplayer1	$2b$12$BK15ymbROgF0yxlKgpQEd.gExM6QfDjKXkz/fkkyhis51MQLBzfOq	2025-06-26 15:07:43.623765	127.0.0.1	GolfCo
15	echo.user5@gmail.com	echouser5	$2b$12$wzQNcis/NHVjVSU.6N4wX.hwiZ8Cd62pRTjOgG4jnCy9wOzjkA6CK	2025-06-26 15:50:51.515496	127.0.0.1	EchoEnterprises
19	india_echo3@gmail.com	indiaecho3	$2b$12$hLVAj41FGfn/3pyWqT1hvucklgyLAqSSXvs9/.xVYkMNQogJvqGXK	2025-06-26 15:51:57.757436	127.0.0.1	IndiaEchoLtd
16	foxtrot99@gmail.com	foxtrot99	$2b$12$LGjygFP2Yx143poaYrsFIuE97QM8YtNGoU7EmzsHcA.hNYLlDyUWK	2025-06-26 15:52:52.333893	127.0.0.1	FoxtrotLLC
11	alphauser23@gmail.com	alphauser23	$2b$12$kcy74UNqG3vyZaltihJ.auoLrq/XncmPIXYTdP/he1w5tSFuChThy	2025-06-26 15:54:09.98245	127.0.0.1	AlphaCorp
18	hotelalpha7@gmail.com	hotelalpha7	$2b$12$9ptEh2AIQeng7r.rVnZn0uV1XoZZTcctUTU23sZVGvF8g3sG.z4L.	2025-06-26 15:58:18.660483	127.0.0.1	HotelAlphaGroup
10	testuser1@gmail.com	testuser1	$2b$12$nlypKk5lgpVJRmRw3.K9pe0yE6p7Qj28yrsXHah5d6snqrn.ovA6.	2025-06-26 16:04:43.740175	127.0.0.1	testuser1company
12	bravo2025@gmail.com	bravo2025	$2b$12$dD.rV88GDaslbTVYYTQtgOVR0iaZiE9ODjDM.gzG6CxpOEtK6jrs2	2025-06-26 17:06:48.961823	127.0.0.1	BravoTech
14	delta_user8@gmail.com	deltauser8	$2b$12$DgfLadQqgxm6R2vg8CN6OOqce0WGnr70o4U9IowKxqUbGtc1Mies.	2025-06-26 17:08:42.126773	127.0.0.1	DeltaWorks
13	charlie_xyz@inbox.com	charliexyz	$2b$12$FyUfolU1u4dQ92jxcGam5.XJQ04LgkYK8./U6x6nQEvRwHgq/i5WC	2025-06-26 17:25:53.450276	127.0.0.1	CharlieSolutions
\.


--
-- TOC entry 4830 (class 0 OID 0)
-- Dependencies: 219
-- Name: admins_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.admins_id_seq', 12, true);


--
-- TOC entry 4831 (class 0 OID 0)
-- Dependencies: 221
-- Name: spectrum_licenses_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.spectrum_licenses_license_id_seq', 32, true);


--
-- TOC entry 4832 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 19, true);


--
-- TOC entry 4661 (class 2606 OID 81961)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- TOC entry 4667 (class 2606 OID 90159)
-- Name: spectrum_licenses spectrum_licenses_license_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spectrum_licenses
    ADD CONSTRAINT spectrum_licenses_license_key_key UNIQUE (license_key);


--
-- TOC entry 4669 (class 2606 OID 81973)
-- Name: spectrum_licenses spectrum_licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spectrum_licenses
    ADD CONSTRAINT spectrum_licenses_pkey PRIMARY KEY (license_id);


--
-- TOC entry 4659 (class 2606 OID 81948)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4662 (class 1259 OID 81963)
-- Name: ix_admins_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admins_email ON public.admins USING btree (email);


--
-- TOC entry 4663 (class 1259 OID 81962)
-- Name: ix_admins_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admins_id ON public.admins USING btree (id);


--
-- TOC entry 4664 (class 1259 OID 81964)
-- Name: ix_admins_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admins_username ON public.admins USING btree (username);


--
-- TOC entry 4665 (class 1259 OID 81979)
-- Name: ix_spectrum_licenses_license_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_spectrum_licenses_license_id ON public.spectrum_licenses USING btree (license_id);


--
-- TOC entry 4654 (class 1259 OID 81951)
-- Name: ix_users_company; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_company ON public.users USING btree (company);


--
-- TOC entry 4655 (class 1259 OID 81949)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 4656 (class 1259 OID 81950)
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- TOC entry 4657 (class 1259 OID 81952)
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- TOC entry 4670 (class 2606 OID 81974)
-- Name: spectrum_licenses spectrum_licenses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spectrum_licenses
    ADD CONSTRAINT spectrum_licenses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


-- Completed on 2025-06-26 17:39:16

--
-- PostgreSQL database dump complete
--

