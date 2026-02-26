--
-- PostgreSQL database dump
--

\restrict a6xxiCXdskTMWy9L2yDc23ZVatP6PgRAWfEuffD2mcLdXkADQLplOkm98dRYgBO

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-02-26 13:59:32

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
-- TOC entry 234 (class 1259 OID 16943)
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comments (
    id bigint NOT NULL,
    task_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    comment_text text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.comments OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 16942)
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comments_id_seq OWNER TO postgres;

--
-- TOC entry 5123 (class 0 OID 0)
-- Dependencies: 233
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comments_id_seq OWNED BY public.comments.id;


--
-- TOC entry 228 (class 1259 OID 16871)
-- Name: components; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.components (
    id bigint NOT NULL,
    project_id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.components OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16870)
-- Name: components_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.components_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.components_id_seq OWNER TO postgres;

--
-- TOC entry 5124 (class 0 OID 0)
-- Dependencies: 227
-- Name: components_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.components_id_seq OWNED BY public.components.id;


--
-- TOC entry 220 (class 1259 OID 16803)
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id bigint NOT NULL,
    full_name text NOT NULL,
    email text NOT NULL,
    role text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16802)
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- TOC entry 5125 (class 0 OID 0)
-- Dependencies: 219
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- TOC entry 236 (class 1259 OID 16968)
-- Name: labels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.labels (
    id bigint NOT NULL,
    project_id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.labels OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16967)
-- Name: labels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.labels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.labels_id_seq OWNER TO postgres;

--
-- TOC entry 5126 (class 0 OID 0)
-- Dependencies: 235
-- Name: labels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.labels_id_seq OWNED BY public.labels.id;


--
-- TOC entry 224 (class 1259 OID 16829)
-- Name: project_members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_members (
    id bigint NOT NULL,
    project_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    member_role text NOT NULL,
    joined_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.project_members OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16828)
-- Name: project_members_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_members_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.project_members_id_seq OWNER TO postgres;

--
-- TOC entry 5127 (class 0 OID 0)
-- Dependencies: 223
-- Name: project_members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_members_id_seq OWNED BY public.project_members.id;


--
-- TOC entry 222 (class 1259 OID 16818)
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id bigint NOT NULL,
    name text NOT NULL,
    description text,
    start_date date,
    end_date date
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16817)
-- Name: projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.projects_id_seq OWNER TO postgres;

--
-- TOC entry 5128 (class 0 OID 0)
-- Dependencies: 221
-- Name: projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_id_seq OWNED BY public.projects.id;


--
-- TOC entry 226 (class 1259 OID 16854)
-- Name: sprints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sprints (
    id bigint NOT NULL,
    project_id bigint NOT NULL,
    name text NOT NULL,
    start_date date,
    end_date date
);


ALTER TABLE public.sprints OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16853)
-- Name: sprints_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sprints_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sprints_id_seq OWNER TO postgres;

--
-- TOC entry 5129 (class 0 OID 0)
-- Dependencies: 225
-- Name: sprints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sprints_id_seq OWNED BY public.sprints.id;


--
-- TOC entry 232 (class 1259 OID 16921)
-- Name: task_assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_assignments (
    id bigint NOT NULL,
    task_id bigint NOT NULL,
    employee_id bigint NOT NULL,
    assigned_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.task_assignments OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16920)
-- Name: task_assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_assignments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_assignments_id_seq OWNER TO postgres;

--
-- TOC entry 5130 (class 0 OID 0)
-- Dependencies: 231
-- Name: task_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_assignments_id_seq OWNED BY public.task_assignments.id;


--
-- TOC entry 238 (class 1259 OID 16985)
-- Name: task_labels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_labels (
    id bigint NOT NULL,
    task_id bigint NOT NULL,
    label_id bigint NOT NULL
);


ALTER TABLE public.task_labels OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16984)
-- Name: task_labels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_labels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_labels_id_seq OWNER TO postgres;

--
-- TOC entry 5131 (class 0 OID 0)
-- Dependencies: 237
-- Name: task_labels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_labels_id_seq OWNED BY public.task_labels.id;


--
-- TOC entry 230 (class 1259 OID 16888)
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id bigint NOT NULL,
    project_id bigint NOT NULL,
    sprint_id bigint,
    components_id bigint,
    title text NOT NULL,
    status text NOT NULL,
    priority text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16887)
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- TOC entry 5132 (class 0 OID 0)
-- Dependencies: 229
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- TOC entry 4913 (class 2604 OID 16946)
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments ALTER COLUMN id SET DEFAULT nextval('public.comments_id_seq'::regclass);


--
-- TOC entry 4907 (class 2604 OID 16874)
-- Name: components id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.components ALTER COLUMN id SET DEFAULT nextval('public.components_id_seq'::regclass);


--
-- TOC entry 4901 (class 2604 OID 16806)
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- TOC entry 4915 (class 2604 OID 16971)
-- Name: labels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels ALTER COLUMN id SET DEFAULT nextval('public.labels_id_seq'::regclass);


--
-- TOC entry 4904 (class 2604 OID 16832)
-- Name: project_members id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_members ALTER COLUMN id SET DEFAULT nextval('public.project_members_id_seq'::regclass);


--
-- TOC entry 4903 (class 2604 OID 16821)
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.projects_id_seq'::regclass);


--
-- TOC entry 4906 (class 2604 OID 16857)
-- Name: sprints id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sprints ALTER COLUMN id SET DEFAULT nextval('public.sprints_id_seq'::regclass);


--
-- TOC entry 4911 (class 2604 OID 16924)
-- Name: task_assignments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignments ALTER COLUMN id SET DEFAULT nextval('public.task_assignments_id_seq'::regclass);


--
-- TOC entry 4916 (class 2604 OID 16988)
-- Name: task_labels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_labels ALTER COLUMN id SET DEFAULT nextval('public.task_labels_id_seq'::regclass);


--
-- TOC entry 4908 (class 2604 OID 16891)
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- TOC entry 5113 (class 0 OID 16943)
-- Dependencies: 234
-- Data for Name: comments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comments (id, task_id, employee_id, comment_text, created_at) FROM stdin;
\.


--
-- TOC entry 5107 (class 0 OID 16871)
-- Dependencies: 228
-- Data for Name: components; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.components (id, project_id, name) FROM stdin;
\.


--
-- TOC entry 5099 (class 0 OID 16803)
-- Dependencies: 220
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, full_name, email, role, created_at) FROM stdin;
\.


--
-- TOC entry 5115 (class 0 OID 16968)
-- Dependencies: 236
-- Data for Name: labels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.labels (id, project_id, name) FROM stdin;
\.


--
-- TOC entry 5103 (class 0 OID 16829)
-- Dependencies: 224
-- Data for Name: project_members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_members (id, project_id, employee_id, member_role, joined_at) FROM stdin;
\.


--
-- TOC entry 5101 (class 0 OID 16818)
-- Dependencies: 222
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, name, description, start_date, end_date) FROM stdin;
\.


--
-- TOC entry 5105 (class 0 OID 16854)
-- Dependencies: 226
-- Data for Name: sprints; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sprints (id, project_id, name, start_date, end_date) FROM stdin;
\.


--
-- TOC entry 5111 (class 0 OID 16921)
-- Dependencies: 232
-- Data for Name: task_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_assignments (id, task_id, employee_id, assigned_at) FROM stdin;
\.


--
-- TOC entry 5117 (class 0 OID 16985)
-- Dependencies: 238
-- Data for Name: task_labels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_labels (id, task_id, label_id) FROM stdin;
\.


--
-- TOC entry 5109 (class 0 OID 16888)
-- Dependencies: 230
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, project_id, sprint_id, components_id, title, status, priority, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5133 (class 0 OID 0)
-- Dependencies: 233
-- Name: comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comments_id_seq', 1, false);


--
-- TOC entry 5134 (class 0 OID 0)
-- Dependencies: 227
-- Name: components_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.components_id_seq', 1, false);


--
-- TOC entry 5135 (class 0 OID 0)
-- Dependencies: 219
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 1, false);


--
-- TOC entry 5136 (class 0 OID 0)
-- Dependencies: 235
-- Name: labels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.labels_id_seq', 1, false);


--
-- TOC entry 5137 (class 0 OID 0)
-- Dependencies: 223
-- Name: project_members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_members_id_seq', 1, false);


--
-- TOC entry 5138 (class 0 OID 0)
-- Dependencies: 221
-- Name: projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_id_seq', 1, false);


--
-- TOC entry 5139 (class 0 OID 0)
-- Dependencies: 225
-- Name: sprints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sprints_id_seq', 1, false);


--
-- TOC entry 5140 (class 0 OID 0)
-- Dependencies: 231
-- Name: task_assignments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_assignments_id_seq', 1, false);


--
-- TOC entry 5141 (class 0 OID 0)
-- Dependencies: 237
-- Name: task_labels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_labels_id_seq', 1, false);


--
-- TOC entry 5142 (class 0 OID 0)
-- Dependencies: 229
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, false);


--
-- TOC entry 4932 (class 2606 OID 16956)
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- TOC entry 4926 (class 2606 OID 16881)
-- Name: components components_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT components_pkey PRIMARY KEY (id);


--
-- TOC entry 4918 (class 2606 OID 16816)
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- TOC entry 4934 (class 2606 OID 16978)
-- Name: labels labels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_pkey PRIMARY KEY (id);


--
-- TOC entry 4922 (class 2606 OID 16842)
-- Name: project_members project_members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_members
    ADD CONSTRAINT project_members_pkey PRIMARY KEY (id);


--
-- TOC entry 4920 (class 2606 OID 16827)
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (id);


--
-- TOC entry 4924 (class 2606 OID 16864)
-- Name: sprints sprints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sprints
    ADD CONSTRAINT sprints_pkey PRIMARY KEY (id);


--
-- TOC entry 4930 (class 2606 OID 16931)
-- Name: task_assignments task_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignments
    ADD CONSTRAINT task_assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 4936 (class 2606 OID 16993)
-- Name: task_labels task_labels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_labels
    ADD CONSTRAINT task_labels_pkey PRIMARY KEY (id);


--
-- TOC entry 4928 (class 2606 OID 16904)
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- TOC entry 4946 (class 2606 OID 16962)
-- Name: comments comments_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- TOC entry 4947 (class 2606 OID 16957)
-- Name: comments comments_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comments
    ADD CONSTRAINT comments_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- TOC entry 4940 (class 2606 OID 16882)
-- Name: components components_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.components
    ADD CONSTRAINT components_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 4948 (class 2606 OID 16979)
-- Name: labels labels_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 4937 (class 2606 OID 16848)
-- Name: project_members project_members_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_members
    ADD CONSTRAINT project_members_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- TOC entry 4938 (class 2606 OID 16843)
-- Name: project_members project_members_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_members
    ADD CONSTRAINT project_members_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 4939 (class 2606 OID 16865)
-- Name: sprints sprints_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sprints
    ADD CONSTRAINT sprints_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 4944 (class 2606 OID 16937)
-- Name: task_assignments task_assignments_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignments
    ADD CONSTRAINT task_assignments_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id) ON DELETE CASCADE;


--
-- TOC entry 4945 (class 2606 OID 16932)
-- Name: task_assignments task_assignments_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_assignments
    ADD CONSTRAINT task_assignments_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- TOC entry 4949 (class 2606 OID 16999)
-- Name: task_labels task_labels_label_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_labels
    ADD CONSTRAINT task_labels_label_id_fkey FOREIGN KEY (label_id) REFERENCES public.labels(id) ON DELETE CASCADE;


--
-- TOC entry 4950 (class 2606 OID 16994)
-- Name: task_labels task_labels_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_labels
    ADD CONSTRAINT task_labels_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- TOC entry 4941 (class 2606 OID 16915)
-- Name: tasks tasks_components_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_components_id_fkey FOREIGN KEY (components_id) REFERENCES public.components(id) ON DELETE SET NULL;


--
-- TOC entry 4942 (class 2606 OID 16905)
-- Name: tasks tasks_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE;


--
-- TOC entry 4943 (class 2606 OID 16910)
-- Name: tasks tasks_sprint_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_sprint_id_fkey FOREIGN KEY (sprint_id) REFERENCES public.sprints(id) ON DELETE SET NULL;


-- Completed on 2026-02-26 13:59:32

--
-- PostgreSQL database dump complete
--

\unrestrict a6xxiCXdskTMWy9L2yDc23ZVatP6PgRAWfEuffD2mcLdXkADQLplOkm98dRYgBO

