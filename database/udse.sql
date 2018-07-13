--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: consist; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE consist (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE consist OWNER TO postgres;

--
-- Name: consist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE consist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE consist_id_seq OWNER TO postgres;

--
-- Name: consist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE consist_id_seq OWNED BY consist.id;


--
-- Name: contract; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE contract (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE contract OWNER TO postgres;

--
-- Name: contract_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE contract_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE contract_id_seq OWNER TO postgres;

--
-- Name: contract_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE contract_id_seq OWNED BY contract.id;


--
-- Name: file; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE file (
    id integer NOT NULL,
    data bytea,
    info jsonb,
    security jsonb
);


ALTER TABLE file OWNER TO postgres;

--
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE file_id_seq OWNER TO postgres;

--
-- Name: file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE file_id_seq OWNED BY file.id;


--
-- Name: group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "group" (
    id character varying NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE "group" OWNER TO postgres;

--
-- Name: inquiry; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE inquiry (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE inquiry OWNER TO postgres;

--
-- Name: inquiry_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE inquiry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE inquiry_id_seq OWNER TO postgres;

--
-- Name: inquiry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE inquiry_id_seq OWNED BY inquiry.id;


--
-- Name: location; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE location (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE location OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE location_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE location_id_seq OWNER TO postgres;

--
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE location_id_seq OWNED BY location.id;


--
-- Name: log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE log (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE log OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE log_id_seq OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: order; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "order" (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE "order" OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE order_id_seq OWNER TO postgres;

--
-- Name: order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE order_id_seq OWNED BY "order".id;


--
-- Name: partner; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE partner (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE partner OWNER TO postgres;

--
-- Name: partner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE partner_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE partner_id_seq OWNER TO postgres;

--
-- Name: partner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE partner_id_seq OWNED BY partner.id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE product (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE product OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_id_seq OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE product_id_seq OWNED BY product.id;


--
-- Name: release; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE release (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE release OWNER TO postgres;

--
-- Name: release_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE release_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE release_id_seq OWNER TO postgres;

--
-- Name: release_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE release_id_seq OWNED BY release.id;


--
-- Name: service; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE service (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE service OWNER TO postgres;

--
-- Name: service_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE service_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE service_id_seq OWNER TO postgres;

--
-- Name: service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE service_id_seq OWNED BY service.id;


--
-- Name: template; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE template (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE template OWNER TO postgres;

--
-- Name: template_id_seq1; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE template_id_seq1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE template_id_seq1 OWNER TO postgres;

--
-- Name: template_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE template_id_seq1 OWNED BY template.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "user" (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE "user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: verify; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE verify (
    id integer NOT NULL,
    data jsonb,
    security jsonb
);


ALTER TABLE verify OWNER TO postgres;

--
-- Name: verify_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE verify_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE verify_id_seq OWNER TO postgres;

--
-- Name: verify_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE verify_id_seq OWNED BY verify.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY consist ALTER COLUMN id SET DEFAULT nextval('consist_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY contract ALTER COLUMN id SET DEFAULT nextval('contract_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY file ALTER COLUMN id SET DEFAULT nextval('file_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY inquiry ALTER COLUMN id SET DEFAULT nextval('inquiry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY location ALTER COLUMN id SET DEFAULT nextval('location_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "order" ALTER COLUMN id SET DEFAULT nextval('order_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY partner ALTER COLUMN id SET DEFAULT nextval('partner_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY product ALTER COLUMN id SET DEFAULT nextval('product_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY release ALTER COLUMN id SET DEFAULT nextval('release_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY service ALTER COLUMN id SET DEFAULT nextval('service_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY template ALTER COLUMN id SET DEFAULT nextval('template_id_seq1'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY verify ALTER COLUMN id SET DEFAULT nextval('verify_id_seq'::regclass);


--
-- Data for Name: consist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY consist (id, data, security) FROM stdin;
\.


--
-- Name: consist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('consist_id_seq', 1, false);


--
-- Data for Name: contract; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY contract (id, data, security) FROM stdin;
\.


--
-- Name: contract_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('contract_id_seq', 4, true);


--
-- Data for Name: file; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY file (id, data, info, security) FROM stdin;
36	\\x5b4465736b746f7020456e7472795d0a56657273696f6e3d312e300a547970653d4c696e6b0a4e616d653d4578616d706c65730a4e616d655b61615d3d4365656c616c6c6f0a4e616d655b6163655d3d436f6e746f680a4e616d655b61665d3d566f6f726265656c64650a4e616d655b616d5d3de1889de188b3e1888ce18b8ee189bd0a4e616d655b616e5d3d4578656d706c6f730a4e616d655b61725d3dd8a3d985d8abd984d8a90a4e616d655b6173745d3d4578656d706c6f730a4e616d655b617a5d3d4ec3bc6d756ec9996cc999720a4e616d655b62655d3dd09fd180d18bd0bad0bbd0b0d0b4d18b0a4e616d655b62675d3dd09fd180d0b8d0bcd0b5d180d0b80a4e616d655b626e5d3de0a689e0a6a6e0a6bee0a6b9e0a6b0e0a6a30a4e616d655b62725d3d536b6f756572696fc3b90a4e616d655b62735d3d5072696d6a6572690a4e616d655b63615d3d4578656d706c65730a4e616d655b63614076616c656e6369615d3d4578656d706c65730a4e616d655b636b625d3dd986d985d988d986d987e2808cd983d8a7d9860a4e616d655b63735d3d556bc3a17a6b790a4e616d655b6373625d3d50727ac3ab6d69c3b472c3ab0a4e616d655b63795d3d456e67687265696666746961750a4e616d655b64615d3d456b73656d706c65720a4e616d655b64655d3d426569737069656c650a4e616d655b64765d3dde89dea8de90dea7de8ddeaade8cdea6de81deb00a4e616d655b656c5d3dcea0ceb1cf81ceb1ceb4ceb5ceafceb3cebcceb1cf84ceb10a4e616d655b656e5f41555d3d4578616d706c65730a4e616d655b656e5f43415d3d4578616d706c65730a4e616d655b656e5f47425d3d4578616d706c65730a4e616d655b656f5d3d456b7a656d706c6f6a0a4e616d655b65735d3d456a656d706c6f730a4e616d655b65745d3d4ec3a46964697365640a4e616d655b65755d3d41646962696465616b0a4e616d655b66615d3dd986d985d988d986d987e2808cd987d8a70a4e616d655b66695d3d4573696d65726b6b656ac3a40a4e616d655b66696c5d3d4d67612068616c696d626177610a4e616d655b666f5d3d44c3b86d69720a4e616d655b66725d3d4578656d706c65730a4e616d655b6675725d3d4573656d706c69730a4e616d655b66795d3d466f617262796c64656e0a4e616d655b67615d3d53616d706c61c3ad0a4e616d655b67645d3d4275696c6c2d656973696d706c6569720a4e616d655b676c5d3d4578656d706c6f730a4e616d655b67755d3de0aaa6e0ab83e0aab7e0ab8de0aa9fe0aabee0aaa8e0ab8de0aaa4e0ab8b0a4e616d655b67765d3d53616d706c657972796e0a4e616d655b68655d3dd793d795d792d79ed790d795d7aa0a4e616d655b68695d3de0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a30a4e616d655b68725d3d5072696d6a6572690a4e616d655b68745d3d45677a616e700a4e616d655b68755d3d4d696e74c3a16b0a4e616d655b68795d3dd595d680d5abd5b6d5a1d5afd5b6d5a5d6800a4e616d655b69645d3d436f6e746f680a4e616d655b69735d3d53c3bd6e6973686f726e0a4e616d655b69745d3d4573656d70690a4e616d655b6a615d3de382b5e383b3e38397e383ab0a4e616d655b6b615d3de1839ce18398e1839be183a3e183a8e18394e18391e183980a4e616d655b6b6b5d3dd09cd18bd181d0b0d0bbd0b4d0b0d1800a4e616d655b6b6c5d3d41737365727375757469740a4e616d655b6b6d5d3de19ea7e19e91e19eb6e19ea0e19e9ae19e8ee19f8d0a4e616d655b6b6e5d3de0b289e0b2a6e0b2bee0b2b9e0b2b0e0b2a3e0b386e0b297e0b2b3e0b3810a4e616d655b6b6f5d3dec9888ec8b9c0a4e616d655b6b755d3d4dc3ae6e616b0a4e616d655b6b775d3d456e73616d706c6f770a4e616d655b6b795d3dd09cd0b8d181d0b0d0bbd0b4d0b0d1800a4e616d655b6c625d3d4265697370696c6c65720a4e616d655b6c745d3d506176797a64c5be69c5b3206661696c61690a4e616d655b6c765d3d506172617567690a4e616d655b6d675d3d4f68617472610a4e616d655b6d68725d3dd09fd180d0b8d0bcd0b5d1802dd0b2d0bbd0b0d0ba0a4e616d655b6d695d3d5461756972610a4e616d655b6d6b5d3dd09fd180d0b8d0bcd0b5d180d0b80a4e616d655b6d6c5d3de0b489e0b4a6e0b4bee0b4b9e0b4b0e0b4a3e0b499e0b58de0b499e0b4b3e0b58de2808d0a4e616d655b6d725d3de0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a3e0a5870a4e616d655b6d735d3d436f6e746f682d636f6e746f680a4e616d655b6d795d3de180a5e18095e18099e180ace18099e180bbe180ace180b80a4e616d655b6e625d3d456b73656d706c65720a4e616d655b6e64735d3d42697370656c656e0a4e616d655b6e655d3de0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a3e0a4b9e0a4b0e0a5820a4e616d655b6e6c5d3d566f6f726265656c642d62657374616e64656e0a4e616d655b6e6e5d3d44c3b86d650a4e616d655b6e736f5d3d4d65686c616c610a4e616d655b6f635d3d4578656d706c65730a4e616d655b70615d3de0a889e0a8a6e0a8bee0a8b9e0a8b0e0a8a8e0a8bee0a8820a4e616d655b706c5d3d50727a796bc5826164790a4e616d655b70745d3d4578656d706c6f730a4e616d655b70745f42525d3d4578656d706c6f730a4e616d655b726f5d3d4578656d706c650a4e616d655b72755d3dd09fd180d0b8d0bcd0b5d180d18b0a4e616d655b73635d3d4573656d70697573750a4e616d655b73636f5d3d4578616d706c65730a4e616d655b73645d3dd985d8abd8a7d984d988d9860a4e616d655b73655d3d4f7664616d6561726b6b61740a4e616d655b73686e5d3de18090e180b0e1809de180bae1809ae181a2e18084e180bae182870a4e616d655b73695d3de0b6b1e0b792e0b6afe0b783e0b794e0b6b1e0b78a0a4e616d655b736b5d3d5072c3ad6b6c6164790a4e616d655b736c5d3d5a676c6564690a4e616d655b736d6c5d3d536167612053617570616d610a4e616d655b736e5d3d4d6979656e7a616e69736f0a4e616d655b73715d3d5368656d62756a740a4e616d655b73725d3dd09fd180d0b8d0bcd0b5d180d0b80a4e616d655b73765d3d4578656d70656c0a4e616d655b73775d3d4d6966616e6f0a4e616d655b737a6c5d3d42616a737a70696c650a4e616d655b74615d3de0ae89e0aea4e0aebee0aeb0e0aea3e0ae99e0af8de0ae95e0aeb3e0af8d0a4e616d655b74615f4c4b5d3de0ae89e0aea4e0aebee0aeb0e0aea3e0ae99e0af8de0ae95e0aeb3e0af8d0a4e616d655b74655d3de0b089e0b0a6e0b0bee0b0b9e0b0b0e0b0a3e0b0b2e0b1810a4e616d655b74675d3dd09dd0b0d0bcd183d0bdd0b0d2b3d0be0a4e616d655b74685d3de0b895e0b8b1e0b8a7e0b8ade0b8a2e0b988e0b8b2e0b8870a4e616d655b74725d3dc396726e656b6c65720a4e616d655b74745d3dd09cd0b8d181d0b0d0bbd0bbd0b0d1800a4e616d655b75675d3dd985d989d8b3d8a7d984d984d8a7d8b10a4e616d655b756b5d3dd09fd180d0b8d0bad0bbd0b0d0b4d0b80a4e616d655b75725d3dd985d8abd8a7d984db8cdaba0a4e616d655b757a5d3dd09dd0b0d0bcd183d0bdd0b0d0bbd0b0d1800a4e616d655b7665635d3d4573656d70690a4e616d655b76695d3d4de1baab752076c3ad2064e1bba50a4e616d655b7761655d3d426973636862696c0a4e616d655b7a685f434e5d3de7a4bae4be8b0a4e616d655b7a685f484b5d3de7af84e4be8b0a4e616d655b7a685f54575d3de7af84e4be8b0a436f6d6d656e743d4578616d706c6520636f6e74656e7420666f72205562756e74750a436f6d6d656e745b61615d3d5562756e74756820616464617474696e6f68206365656c616c6c6f0a436f6d6d656e745b6163655d3d436f6e746f682061736f206b65205562756e74750a436f6d6d656e745b61665d3d566f6f726265656c6420696e686f756420766972205562756e74750a436f6d6d656e745b616d5d3de18b9de188ade18b9de188ad20e1889de188b3e1888ce18b8ee189bd20e1888820e18aa1e189a1e18a95e189b10a436f6d6d656e745b616e5d3d436f6e74656e69752064276578656d706c6f207461205562756e74750a436f6d6d656e745b61725d3dd8a3d985d8abd984d8a920d985d8add8aad988d98920d984d8a3d988d8a8d988d986d8aad9880a436f6d6d656e745b6173745d3d436f6e74656ec3ad752064656c206578656d706c75207061205562756e74750a436f6d6d656e745b617a5d3d5562756e747520c3bcc3a7c3bc6e206ec3bc6d756ec999206d6174657269616c0a436f6d6d656e745b62655d3dd0a3d0b7d0bed180d18b20d0b4d0b0d0bad183d0bcd0b5d0bdd182d0b0d19e20d0b4d0bbd18f205562756e74750a436f6d6d656e745b62675d3dd09fd180d0b8d0bcd0b5d180d0bdd0be20d181d18ad0b4d18ad180d0b6d0b0d0bdd0b8d0b520d0b7d0b0205562756e74750a436f6d6d656e745b626e5d3de0a689e0a6ace0a781e0a6a8e0a78de0a69fe0a78120e0a6b8e0a682e0a695e0a78de0a6b0e0a6bee0a6a8e0a78de0a6a420e0a6a8e0a6aee0a781e0a6a8e0a6be20e0a6a4e0a6a5e0a78de0a6af0a436f6d6d656e745b62725d3d536b6f756572656e6e20656e64616c63276861642065766974205562756e74750a436f6d6d656e745b62735d3d5072696d6a657220736164727a616a61207a61205562756e74750a436f6d6d656e745b63615d3d436f6e74696e677574732064276578656d706c65207065722061206c275562756e74750a436f6d6d656e745b63614076616c656e6369615d3d436f6e74696e677574732064276578656d706c65207065722061206c275562756e74750a436f6d6d656e745b636b625d3dd986d985d988d988d986db95db8c20d986d8a7d988db95da95db86daa9db8edaa920d8a8db8620d8a6d988d8a8d988d988d986d8aad9880a436f6d6d656e745b63735d3d556bc3a17a6b6f76c3bd206f627361682070726f205562756e74750a436f6d6d656e745b6373625d3d50727ac3ab6d69c3b4726f77c3b4207a616d6bc5826f736320646cc3b4205562756e74750a436f6d6d656e745b63795d3d43796e6e77797320656e676872616966667420617220677966657220205562756e74750a436f6d6d656e745b64615d3d456b73656d70656c20696e64686f6c642074696c205562756e74750a436f6d6d656e745b64655d3d426569737069656c696e68616c742066c3bc72205562756e74750a436f6d6d656e745b64765d3dde87deaade84deaade82deb0de93deaa20de87dea7de87dea820de87deacde86dea6de81deadde82dea620de89dea8de90dea7de8ddeaade8cdea6de87deb00a436f6d6d656e745b656c5d3dcea0ceb1cf81ceb1ceb4ceb5ceafceb3cebcceb1cf84ceb120cf80ceb5cf81ceb9ceb5cf87cebfcebcceadcebdcebfcf8520ceb3ceb9ceb120cf84cebf205562756e74750a436f6d6d656e745b656e5f41555d3d4578616d706c6520636f6e74656e7420666f72205562756e74750a436f6d6d656e745b656e5f43415d3d4578616d706c6520636f6e74656e7420666f72205562756e74750a436f6d6d656e745b656e5f47425d3d4578616d706c6520636f6e74656e7420666f72205562756e74750a436f6d6d656e745b656f5d3d456b7a656d706c6120656e6861766f20706f72205562756e74750a436f6d6d656e745b65735d3d436f6e74656e69646f20646520656a656d706c6f2070617261205562756e74750a436f6d6d656e745b65745d3d5562756e7475206ec3a4696469736661696c69640a436f6d6d656e745b65755d3d416469626964657a6b6f206564756b6961205562756e747572616b6f0a436f6d6d656e745b66615d3dd985d8add8aad988db8cd8a7d8aa20d986d985d988d986d98720d8a8d8b1d8a7db8c20d8a7d988d8a8d988d986d8aad9880a436f6d6d656e745b66695d3d4573696d65726b6b69736973c3a46c74c3b66ac3a4205562756e74756c6c650a436f6d6d656e745b66696c5d3d48616c696d626177616e67206c616d616e2070617261207361205562756e74750a436f6d6d656e745b666f5d3d44c3b86d697320696e6e6968616c642066797269205562756e74750a436f6d6d656e745b66725d3d436f6e74656e752064276578656d706c6520706f7572205562756e74750a436f6d6d656e745b6675725d3d436f6e7469676ec3bb7473206469206573656d706c6920706172205562756e74750a436f6d6d656e745b66795d3d466f617262796c642066616e20796e68c3a26c6420666f6172205562756e74750a436f6d6d656e745b67615d3d496e6e6561636861722073616d706c61636820646f205562756e74750a436f6d6d656e745b67645d3d456973696d706c65697220646520736875736261696e7420616972736f6e205562756e74750a436f6d6d656e745b676c5d3d436f6e7469646f20646f206578656d706c6f2070617261205562756e74750a436f6d6d656e745b67755d3d5562756e747520e0aaaee0aabee0aa9fe0ab8720e0aa89e0aaa6e0aabee0aab9e0aab0e0aaa320e0aab8e0ab82e0aa9ae0ab800a436f6d6d656e745b67765d3d53746f6f2053616e706c65797220736f6e205562756e74750a436f6d6d656e745b68655d3dd7aad795d79bd79f20d79cd793d795d792d79ed79420d7a2d791d795d7a820d790d795d791d795d7a0d798d7950a436f6d6d656e745b68695d3de0a489e0a4ace0a581e0a4a8e0a58de0a49fe0a58220e0a4b9e0a587e0a4a4e0a58120e0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a320e0a4b8e0a4bee0a4b0e0a4bee0a482e0a4b60a436f6d6d656e745b68725d3d5072696d6a6572692073616472c5be616a61207a61205562756e74750a436f6d6d656e745b68745d3d4b6f6e746e692065677a616e706cc3a820706f75205562756e74750a436f6d6d656e745b68755d3d4d696e746174617274616c6f6d205562756e7475686f7a0a436f6d6d656e745b68795d3dd4b2d5b8d5bed5a1d5b6d5a4d5a1d5afd5b8d682d5a9d5b5d5a1d5b620d685d680d5abd5b6d5a1d5afd5b6d5a5d680d5a8205562756e7475d68ad5ab20d5b0d5a1d5b4d5a1d6800a436f6d6d656e745b69645d3d436f6e746f68206973692062616769205562756e74750a436f6d6d656e745b69735d3d53c3bd6e6973686f726e206679726972205562756e74750a436f6d6d656e745b69745d3d436f6e74656e757469206469206573656d70696f20706572205562756e74750a436f6d6d656e745b6a615d3d5562756e7475e381aee382b5e383b3e38397e383abe382b3e383b3e38386e383b3e383840a436f6d6d656e745b6b615d3de183a3e18391e183a3e1839ce183a2e183a3e183a120e183a1e18390e1839ce18398e1839be183a3e183a8e1839d20e183a8e18398e18392e18397e18390e18395e183a1e183980a436f6d6d656e745b6b6b5d3d5562756e747520d29bd2b1d0b6d0b0d182d182d0b0d18020d0bcd18bd181d0b0d0bbd0b4d0b0d180d18b0a436f6d6d656e745b6b6c5d3d5562756e74752d6d757420696d6172697361616e7574206173736572737575740a436f6d6d656e745b6b6d5d3de19ea7e19e91e19eb6e19ea0e19e9ae19e8ee19f8de19e9fe19e98e19f92e19e9ae19eb6e19e94e19f8be19ea2e19eb6e19e94e19f8be19e94e19f8ae19ebbe19e93e19e92e19ebc0a436f6d6d656e745b6b6e5d3de0b289e0b2ace0b381e0b282e0b29fe0b381e0b297e0b38620e0b289e0b2a6e0b2bee0b2b9e0b2b0e0b2a3e0b386e0b297e0b2b3e0b3810a436f6d6d656e745b6b6f5d3dec9ab0ebb684ed88ac20ecbba8ed8590ecb8a020ec9888ec8b9c0a436f6d6d656e745b6b755d3d4a6920626f205562756e7475206dc3ae6e616b61206e617665726f6bc3aa0a436f6d6d656e745b6b795d3d5562756e74752dd0bdd183d0bd20d0bcd0b8d181d0b0d0bb20d0b4d0bed0bad183d0bcd0b5d0bdd182d182d0b5d180d0b80a436f6d6d656e745b6c625d3d4265697370696c6c696e68616c7420666972205562756e74750a436f6d6d656e745b6c745d3dc4ae7661697269c5b320646f6b756d656e74c5b32c2070617665696b736cc4976c69c5b32c2067617273c5b320626569207661697a64c5b320706176797a64c5be6961690a436f6d6d656e745b6c765d3d5061726175676120736174757273205562756e74752076696465690a436f6d6d656e745b6d675d3d4f686174726120686f20616e2769205562756e74750a436f6d6d656e745b6d68725d3d5562756e74752dd0bbd0b0d0bd20d0b4d0bed0bad183d0bcd0b5d0bdd1822dd0b2d0bbd0b0d0bad18bd0bd20d0bfd180d0b8d0bcd0b5d1802dd0b2d0bbd0b0d0ba0a436f6d6d656e745b6d695d3d4d61746120746175697261206f205562756e74750a436f6d6d656e745b6d6b5d3dd09fd180d0b8d0bcd0b5d18020d181d0bed0b4d180d0b6d0b8d0bdd0b020d0b7d0b020d0a3d0b1d183d0bdd182d1830a436f6d6d656e745b6d6c5d3de0b489e0b4ace0b581e0b4a3e0b58de0b49fe0b581e0b4b5e0b4bfe0b4a8e0b58120e0b4b5e0b587e0b4a3e0b58de0b49fe0b4bfe0b4afe0b581e0b4b3e0b58de0b4b320e0b489e0b4a6e0b4bee0b4b9e0b4b0e0b4a3e0b499e0b58de0b499e0b4b3e0b58de2808d0a436f6d6d656e745b6d725d3de0a489e0a4ace0a482e0a49fe0a582e0a4b8e0a4bee0a4a0e0a58020e0a498e0a49fe0a495e0a4bee0a482e0a49ae0a58020e0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a3e0a5870a436f6d6d656e745b6d735d3d4b616e64756e67616e20636f6e746f6820756e74756b205562756e74750a436f6d6d656e745b6d795d3d5562756e747520e180a1e18090e180bde18080e180ba20e18094e18099e180b0e18094e180ac20e18099e180ace18090e180ade18080e180ac0a436f6d6d656e745b6e625d3d456b73656d70656c696e6e686f6c6420666f72205562756e74750a436f6d6d656e745b6e655d3de0a489e0a4ace0a4a8e0a58de0a49fe0a581e0a495e0a4be20e0a4b2e0a4bee0a497e0a4bf20e0a489e0a4a6e0a4bee0a4b9e0a4b0e0a4a320e0a4b8e0a4bee0a4aee0a497e0a58de0a4b0e0a5800a436f6d6d656e745b6e6c5d3d566f6f726265656c64696e686f756420766f6f72205562756e74750a436f6d6d656e745b6e6e5d3d456b73656d70656c696e6e68616c6420666f72205562756e74750a436f6d6d656e745b6e736f5d3d4d6f686c616c612077612064696b61676172652074c5a161205562756e74750a436f6d6d656e745b6f635d3d4578656d706c657320646520636f6e74656e67757420706572205562756e74750a436f6d6d656e745b70615d3de0a889e0a8ace0a8a4e0a982e0a9b020e0a8b2e0a88820e0a8a8e0a8aee0a982e0a8a8e0a8be20e0a8b8e0a8aee0a9b1e0a897e0a8b0e0a9800a436f6d6d656e745b706c5d3d50727a796bc58261646f7761207a61776172746fc59bc48720646c61205562756e74750a436f6d6d656e745b70745d3d436f6e7465c3ba646f206465206578656d706c6f2070617261206f205562756e74750a436f6d6d656e745b70745f42525d3d4578656d706c6f20646520636f6e7465c3ba646f2070617261205562756e74750a436f6d6d656e745b726f5d3d436f6ec89b696e7574206578656d706c752070656e747275205562756e74750a436f6d6d656e745b72755d3dd09fd180d0b8d0bcd0b5d180d18b20d0b4d0bed0bad183d0bcd0b5d0bdd182d0bed0b220d0b4d0bbd18f205562756e74750a436f6d6d656e745b73635d3d4573656d706975206465206361626964752070726f205562756e74750a436f6d6d656e745b73636f5d3d4578616d706c6520636f6e74656e7420667572205562756e74750a436f6d6d656e745b73645d3dd8a7d988d8a8d986d9bdd98820d984d8a7d8a1d99020d985d8abd8a7d98420d8b7d988d8b120da8fd986d98420d985d988d8a7d8af0a436f6d6d656e745b73686e5d3de18090e180b0e1809de180bae18287e1809ae181a2e18084e180bae18287e1809ce18099e180bae180b8e181bce18282e180bae180b820e18090e18283e18287205562756e74750a436f6d6d656e745b73695d3de0b68be0b6b6e0b794e0b6b1e0b78ae0b6a7e0b79420e0b783e0b6b3e0b784e0b78f20e0b68be0b6afe0b78fe0b784e0b6bbe0b6ab20e0b685e0b6b1e0b78ae0b6ade0b6bbe0b78ae0b69ce0b6ade0b6bae0b6b1e0b78a0a436f6d6d656e745b736b5d3d556bc3a1c5be6b6f76c3bd206f6273616820707265205562756e74750a436f6d6d656e745b736c5d3d506f6e617a6f72697476656e612076736562696e61207a61205562756e74750a436f6d6d656e745b736d6c5d3d53617570616d61204973696e61205562756e74750a436f6d6d656e745b736e5d3d4d7579656e7a616e69736f207765687569737761206b756974697261205562756e74750a436f6d6d656e745b73715d3d5368656d62756c6c20692070c3ab726d62616a746a65732070c3ab72205562756e74750a436f6d6d656e745b73725d3dd0a1d0b0d0b4d180d0b6d0b0d19820d0bfd180d0b8d0bcd0b5d180d0b020d0b7d0b020d0a3d0b1d183d0bdd182d1830a436f6d6d656e745b73765d3d4578656d70656c696e6e6568c3a56c6c2066c3b672205562756e74750a436f6d6d656e745b73775d3d426964686161206d66616e6f207961205562756e74750a436f6d6d656e745b737a6c5d3d42616a737a70696c6ec58f20747265c59bc48720646cc58f205562756e74750a436f6d6d656e745b74615d3de0ae89e0aeaae0af81e0aea3e0af8de0ae9fe0af81e0aeb5e0aebfe0aeb1e0af8de0ae95e0aebee0aea920e0ae8ee0ae9fe0af81e0aea4e0af8de0aea4e0af81e0ae95e0aebee0ae9fe0af8de0ae9fe0af8120e0ae89e0aeb3e0af8de0aeb3e0ae9fe0ae95e0af8de0ae95e0ae99e0af8de0ae95e0aeb3e0af8d0a436f6d6d656e745b74615f4c4b5d3de0ae89e0aeaae0af81e0aea3e0af8de0ae9fe0af81e0aeb5e0aebfe0aeb1e0af8de0ae95e0aebee0aea920e0ae8ee0ae9fe0af81e0aea4e0af8de0aea4e0af81e0ae95e0aebee0ae9fe0af8de0ae9fe0af8120e0ae89e0aeb3e0af8de0aeb3e0ae9fe0ae95e0af8de0ae95e0ae99e0af8de0ae95e0aeb3e0af8d0a436f6d6d656e745b74655d3d5562756e747520e0b0b5e0b0bee0b0a1e0b181e0b09520e0b0b5e0b0bfe0b0a7e0b0bee0b0a820e0b0a8e0b0aee0b182e0b0a8e0b0bee0b0b2e0b1810a436f6d6d656e745b74675d3dd09cd3afd2b3d182d0b0d0b2d0bed0b820d0bdd0b0d0bcd183d0bdd0b0d0b2d3a320d0b1d0b0d180d0bed0b8205562756e74750a436f6d6d656e745b74685d3de0b895e0b8b1e0b8a7e0b8ade0b8a2e0b988e0b8b2e0b887e0b882e0b989e0b8ade0b8a1e0b8b9e0b8a5e0b8aae0b8b3e0b8abe0b8a3e0b8b1e0b89a205562756e74750a436f6d6d656e745b74725d3d5562756e74752069c3a7696e20c3b6726e656b2069c3a76572696b0a436f6d6d656e745b74745d3d5562756e747520d3a9d187d0b5d0bd20d0b4d0bed0bad183d0bcd0b5d0bdd18220d0bcd0b8d181d0b0d0bbd0bbd0b0d180d18b0a436f6d6d656e745b75675d3dd8a6db87d8a8db87d986d8aadb87d986d989daad20d985d989d8b3d8a7d984d984d989d8b1d9890a436f6d6d656e745b756b5d3dd09fd180d0b8d0bad0bbd0b0d0b4d0b820d0bad0bed0bdd182d0b5d0bdd182d18320d0b4d0bbd18f205562756e74750a436f6d6d656e745b75725d3ddb8cd988d8a8d986d9b9d98820daa9db8cd984d8a6db9220d985d8abd8a7d984db8c20d985d988d8a7d8af0a436f6d6d656e745b757a5d3d5562756e747520d183d187d183d0bd20d0bdd0b0d0bcd183d0bdd0b020d182d0b0d180d0bad0b8d0b1d0b80a436f6d6d656e745b7665635d3d436f6e74656e757469206465206573656d70696f206465205562756e74750a436f6d6d656e745b76695d3d4de1baab752076c3ad2064e1bba52063686f205562756e74750a436f6d6d656e745b7761655d3d44275562756e747520626973636862696c646174696ac3a40a436f6d6d656e745b7a685f434e5d3d5562756e747520e7a4bae4be8be58685e5aeb90a436f6d6d656e745b7a685f484b5d3d5562756e747520e79a84e7af84e4be8be585a7e5aeb90a436f6d6d656e745b7a685f54575d3d5562756e747520e79a84e7af84e4be8be585a7e5aeb90a55524c3d66696c653a2f2f2f7573722f73686172652f6578616d706c652d636f6e74656e742f0a49636f6e3d666f6c6465720a582d5562756e74752d476574746578742d446f6d61696e3d6578616d706c652d636f6e74656e740a0a	{"md5": "189e725f4587b679740f0f7783745056", "name": "examples", "path": "/home/evgen/examples.desktop", "size": 8980, "type": "desktop", "added": "2018-03-28 17:52:34.442000+03:00", "dataID": 253, "dataType": "test", "modified": 1522246632.5325928}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
\.


--
-- Name: file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('file_id_seq', 36, true);


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "group" (id, data, security) FROM stdin;
group	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
security	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
administrators	{"members": [1, 2]}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
user	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
contract	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
template	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
fff	{"members": [1]}	{"read": ["administrators", 2, "users"], "write": ["administrators", 2], "privacy": 0}
partner	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
order	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
inquiry	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
file	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
product	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
log	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
release	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
users	{"members": [1, 2, 10, 9]}	{"read": ["administrators", 1, "users"], "write": ["administrators", 1], "privacy": 0}
service	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
verify	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
location	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
consist	{}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
test	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
test2	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
test3	{}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
\.


--
-- Data for Name: inquiry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY inquiry (id, data, security) FROM stdin;
\.


--
-- Name: inquiry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('inquiry_id_seq', 1, false);


--
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY location (id, data, security) FROM stdin;
\.


--
-- Name: location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('location_id_seq', 1, true);


--
-- Data for Name: log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY log (id, data, security) FROM stdin;
\.


--
-- Name: log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('log_id_seq', 1, false);


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "order" (id, data, security) FROM stdin;
\.


--
-- Name: order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('order_id_seq', 1, false);


--
-- Data for Name: partner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY partner (id, data, security) FROM stdin;
\.


--
-- Name: partner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('partner_id_seq', 3, true);


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY product (id, data, security) FROM stdin;
253	{"path": [0], "type": "test", "files": [[36, {"name": "examples", "path": "/home/evgen/examples.desktop", "size": 8980, "type": "desktop", "added": "2018.03.28.17.52.36", "modified": 1522246632.5325928}]], "title": "esrtyghsrh", "params": [["QDateEdit", "rrrrrrrr", "2018.05.09"], ["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["QLineEdit", "string1", "666"], ["Link", "hhhhhh", [["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]]], "typeIcon": ":/icons/icons/18.png", "composition": [], "description": "9"}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
254	{"path": [0], "type": "qwerty", "files": [], "title": "Новый элемент", "params": [["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["QLineEdit", "string1", "666"], ["Link", "hhhhhh", [["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["QDateEdit", "rrrrrrrr", "2018.05.09"]], "typeIcon": "", "composition": [], "description": ""}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
\.


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('product_id_seq', 254, true);


--
-- Data for Name: release; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY release (id, data, security) FROM stdin;
753	{"path": [0], "type": "yyyyy", "files": [], "title": "yyyyyy", "params": [], "typeIcon": "", "composition": [], "description": ""}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
754	{"path": [0], "type": "test", "files": [], "title": "esrtyghsrh", "params": [["QDateEdit", "rrrrrrrr", "2018.05.09"], ["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["QLineEdit", "string1", "666"], ["Link", "hhhhhh", [["release", 753, ["yyyyy", "", "yyyyyy", ""]]]], ["Link", "link1", [["product", 253, ["test", "", "esrtyghsrh", "9"]], ["release", 753, ["yyyyy", "", "yyyyyy", ""]]]]], "typeIcon": ":/icons/icons/18.png", "composition": [], "description": "9"}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
\.


--
-- Name: release_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('release_id_seq', 754, true);


--
-- Data for Name: service; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY service (id, data, security) FROM stdin;
\.


--
-- Name: service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('service_id_seq', 1, false);


--
-- Data for Name: template; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY template (id, data, security) FROM stdin;
\.


--
-- Name: template_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('template_id_seq1', 27, true);


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "user" (id, data, security) FROM stdin;
1	{"login": "root", "domain": "", "privacy": 9, "pwdHash": "0182bd0bd4444bf836077a718ccdf409:259745cb123a52aa2e693aaacca2db52"}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
2	{"name": "dfsfgdfgdf", "login": "nikitin.s", "domain": "rubin-dc", "privacy": 0, "pwdHash": ""}	{"read": [1, "administrators", "users"], "write": [1, "administrators"], "privacy": 0}
5	{"mail": "", "name": "", "login": "fff", "domain": "", "privacy": 0, "pwdHash": "sdsdf"}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
9	{"mail": "ilyushko@rubin-spb.ru", "name": "Ильюшко Дмитрий", "login": "ilyushko", "domain": "rubin-dc", "privacy": 0, "pwdHash": ""}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
10	{"mail": "pvn@rubin-spb.ru", "name": "Прищенко Василий", "login": "prischenko", "domain": "rubin-dc", "privacy": 0, "pwdHash": ""}	{"read": [2, "administrators", "users"], "write": [2, "administrators"], "privacy": 0}
\.


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('user_id_seq', 10, true);


--
-- Data for Name: verify; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY verify (id, data, security) FROM stdin;
\.


--
-- Name: verify_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('verify_id_seq', 1, false);


--
-- Name: consist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY consist
    ADD CONSTRAINT consist_pkey PRIMARY KEY (id);


--
-- Name: contract_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY contract
    ADD CONSTRAINT contract_pkey PRIMARY KEY (id);


--
-- Name: file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY file
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- Name: group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: inquiry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY inquiry
    ADD CONSTRAINT inquiry_pkey PRIMARY KEY (id);


--
-- Name: location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "order"
    ADD CONSTRAINT order_pkey PRIMARY KEY (id);


--
-- Name: partner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY partner
    ADD CONSTRAINT partner_pkey PRIMARY KEY (id);


--
-- Name: product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: release_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY release
    ADD CONSTRAINT release_pkey PRIMARY KEY (id);


--
-- Name: service_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY service
    ADD CONSTRAINT service_pkey PRIMARY KEY (id);


--
-- Name: template_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY template
    ADD CONSTRAINT template_pkey1 PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: verify_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY verify
    ADD CONSTRAINT verify_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

