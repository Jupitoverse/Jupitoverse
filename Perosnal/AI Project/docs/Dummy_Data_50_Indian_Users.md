# Dummy Data: 50 Indian Users with Hierarchy

Used for development, demos, and testing workflow assignment and data visibility. All names are fictional.

---

## Hierarchy and Roles

- **Admin** (1) — Full access; sees all workflows, tasks, queues.
- **Ops Lead** (2) — Reports to Admin; manages Ops and projects.
- **Ops** (3) — Reports to Ops Lead; project/batch setup, upload, export.
- **Manager / Reviewer Lead** (3) — Reports to Admin; review queue ownership.
- **Reviewer** (10) — Reports to Manager; reviews tasks in their queue.
- **Annotator / Rater** (31) — Report to Ops or Reviewer Lead; complete form/annotation tasks.

Total: 50 users.

---

## User List (CSV-friendly)

| id | full_name       | email              | role      | reports_to_id |
|----|-----------------|--------------------|-----------|---------------|
| 1  | Arjun Mehta     | arjun.mehta@demo   | admin     | null          |
| 2  | Kavita Nair     | kavita.nair@demo   | ops_lead  | 1             |
| 3  | Vikram Singh    | vikram.singh@demo  | ops_lead  | 1             |
| 4  | Anjali Desai    | anjali.desai@demo  | ops       | 2             |
| 5  | Rohan Iyer      | rohan.iyer@demo    | ops       | 2             |
| 6  | Sneha Reddy     | sneha.reddy@demo   | ops       | 3             |
| 7  | Deepak Joshi    | deepak.joshi@demo  | manager   | 1             |
| 8  | Pooja Sharma    | pooja.sharma@demo  | manager   | 1             |
| 9  | Karan Malhotra  | karan.malhotra@demo| manager   | 1             |
| 10 | Neha Gupta     | neha.gupta@demo    | reviewer  | 7             |
| 11 | Rahul Verma     | rahul.verma@demo   | reviewer  | 7             |
| 12 | Divya Patel     | divya.patel@demo   | reviewer  | 7             |
| 13 | Akash Kumar     | akash.kumar@demo   | reviewer  | 8             |
| 14 | Priya Rao       | priya.rao@demo     | reviewer  | 8             |
| 15 | Manish Tiwari   | manish.tiwari@demo | reviewer  | 8             |
| 16 | Shreya Bhat     | shreya.bhat@demo   | reviewer  | 9             |
| 17 | Aditya Kapoor   | aditya.kapoor@demo | reviewer  | 9             |
| 18 | Kirti Saxena    | kirti.saxena@demo  | reviewer  | 9             |
| 19 | Ravi Chopra     | ravi.chopra@demo   | reviewer  | 7             |
| 20 | Nidhi Agarwal   | nidhi.agarwal@demo | reviewer  | 8             |
| 21 | Arjun Krishnan  | arjun.k@demo       | rater     | 2             |
| 22 | Meera Pillai    | meera.pillai@demo  | rater     | 2             |
| 23 | Suresh Nair     | suresh.nair@demo   | rater     | 2             |
| 24 | Lakshmi Menon   | lakshmi.menon@demo | rater     | 3             |
| 25 | Venkat Rao      | venkat.rao@demo    | rater     | 3             |
| 26 | Geeta Subramanian| geeta.s@demo      | rater     | 3             |
| 27 | Arun Prakash    | arun.prakash@demo  | rater     | 4             |
| 28 | Bhavya Shah     | bhavya.shah@demo   | rater     | 4             |
| 29 | Chirag Modi     | chirag.modi@demo   | rater     | 4             |
| 30 | Devika Nambiar  | devika.n@demo      | rater     | 5             |
| 31 | Esha Varma      | esha.varma@demo    | rater     | 5             |
| 32 | Farhan Khan     | farhan.khan@demo   | rater     | 5             |
| 33 | Gita Venkatesh  | gita.v@demo        | rater     | 6             |
| 34 | Harshad Trivedi | harshad.t@demo     | rater     | 6             |
| 35 | Indira Das      | indira.das@demo    | rater     | 6             |
| 36 | Jayesh Bhatt    | jayesh.bhatt@demo  | rater     | 7             |
| 37 | Komal Shah      | komal.shah@demo    | rater     | 7             |
| 38 | Lokesh Gowda    | lokesh.gowda@demo  | rater     | 8             |
| 39 | Maya Krishnan   | maya.k@demo        | rater     | 8             |
| 40 | Naveen Rajan    | naveen.rajan@demo  | rater     | 9             |
| 41 | Ojasvi Reddy    | ojasvi.reddy@demo  | rater     | 9             |
| 42 | Pranav Menon    | pranav.menon@demo  | rater     | 2             |
| 43 | Qasim Ali       | qasim.ali@demo     | rater     | 3             |
| 44 | Radhika Iyer    | radhika.iyer@demo  | rater     | 4             |
| 45 | Sanjay Pillai   | sanjay.pillai@demo | rater     | 5             |
| 46 | Tanvi Nambiar   | tanvi.n@demo       | rater     | 6             |
| 47 | Uday Chopra     | uday.chopra@demo   | rater     | 7             |
| 48 | Varsha Rao      | varsha.rao@demo    | rater     | 8             |
| 49 | Yash Joshi      | yash.joshi@demo    | rater     | 9             |
| 50 | Zara Khan       | zara.khan@demo     | rater     | 2             |

**Password (dummy):** e.g. `demo` or `password123` for all (set in seed).

---

## Workflow Examples (Conceptual)

1. **Annotation + Review** — Form node (upload image, add labels) → Review node (Manager queue) → Done.
2. **Multi-stage** — Form → API call (enrich) → DB update → Review → Done.
3. **Child workflow** — Parent node “Quality check” starts child workflow (e.g. two-step review); child completes → parent continues.

Work queues can be configured by **role** (e.g. all `reviewer`) or by **reports_to** (e.g. tasks for users reporting to Manager 7). Admin sees all tasks; others see only tasks in their queue or assigned to them.
