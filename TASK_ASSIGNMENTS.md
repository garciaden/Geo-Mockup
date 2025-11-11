Heres your file converted cleanly into Markdown (`Development-Roadmap.md`):

---

# **Development Roadmap**

**Deadline:** November 25, 2025

**Duration:** 19 days (11/6 - 11/25)

---

## **Phases Overview**

| **Phase** | **Dates** | **Duration** | **Focus**                                        |
| --------------- | --------------- | ------------------ | ------------------------------------------------------ |
| Phase 1         | 11/6 - 11/9     | 4 days             | Dev environment, database, & HTML template integration |
| Phase 2         | 11/10 - 11/13   | 4 days             | Core features (projects, samples, users)               |
| Phase 3         | 11/14 - 11/17   | 4 days             | Upload functionality & workflows                       |
| Phase 4         | 11/18 - 11/21   | 4 days             | Authentication & security                              |
| Phase 5         | 11/22 - 11/25   | 4 days             | Testing & polish                                       |

---

## **Task Breakdown**

### **1. Database SQL Statements**

* Complete normalization (3NF/BCNF)
* Write `CREATE TABLE` statements for all entities
* Define constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`)
* Add indexes
* Create initialization script

### **2. Database Entities Setup**

* Execute SQL on PostgreSQL
* Verify all tables created correctly
* Set up database roles and permissions
* Configure connection parameters

### **3. Database Relationships & Keys**

* Implement all foreign key relationships
* Create junction tables for many-to-many relationships
* Set up CASCADE rules
* Test referential integrity

### **4. Development Environment Setup**

* Set up GitHub repository
* Create Docker configuration (`docker-compose.yml`, `Dockerfile`)
* Configure PostgreSQL container
* Install Python/Django dependencies
* Set up environment variables

### **5. Connect Database to Framework**

* Configure Django settings for PostgreSQL
* Create Django models for database entities
* Set up Django admin interface
* Test CRUD operations

### **6. Frontend Implementation**

* Integrate existing HTML templates into Django
* Set up Django template structure
* Connect templates to Django views

**Views to Implement:**

* Login page
* Homepage: Project list view
* Project view
* Sample view
* All-geo view
* All-micro view
* All-physical view
* Sample ingest view
* Profile management view
* Admin/Owner: Project/User management view
* Admin: All projects view
* Admin: All samples view
* Add search and filter functionality

### **7. Backend Implementation**

* Create Django views for core entities
* Implement URL routing
* Create business logic (project, sample, user management)
* Create API endpoints (if needed)
* Add validation and error handling

### **8. File Upload Functionality**

* Design CSV/JSON templates for sample upload
* Create file upload UI
* Implement file parsing (CSV/JSON)
* Validate uploaded data
* Implement bulk insert
* Handle errors gracefully
* Create upload audit trail

### **9. Authentication & Security (Lower Priority)**

* Implement user authentication (login/logout)
* Implement role-based access control (RBAC)
* Add password security
* Session management

---

## **Phase-by-Phase Plan**

### **Phase 1: 11/6 - 11/9 (Database & Environment)**

| **Task**                   | **Owner**     | **Duration** |
| -------------------------------- | ------------------- | ------------------ |
| Complete database normalization  | Matthew (lead), All | 1 day              |
| Write SQL DDL statements         | Matthew, Killian    | 1 day              |
| Set up GitHub repository         | Carlos              | 0.5 days           |
| Create Docker configuration      | Carlos              | 1.5 days           |
| Install dependencies             | Carlos              | 0.5 days           |
| Execute database creation        | Matthew             | 0.5 days           |
| Implement foreign keys & indexes | Matthew, Killian    | 1 day              |
| Test environment on all machines | All                 | 0.5 days           |

---

### **Phase 2: 11/10  - 11/13 (Backend & Framework)**

| **Task**                   | **Owner**  | **Duration** |
| -------------------------------- | ---------------- | ------------------ |
| Configure Django settings        | Carlos           | 0.5 days           |
| Create Django models             | Matthew, Carlos  | 2 days             |
| Run migrations                   | Matthew          | 0.5 days           |
| Set up Django admin              | Carlos           | 0.5 days           |
| Create Project views & logic     | Matthew, Killian | 1.5 days           |
| Create Sample views & logic      | Killian, Ian     | 1.5 days           |
| Implement authentication         | Carlos           | 1 day              |
| Implement RBAC                   | Killian, Carlos  | 1.5 days           |
| Create API endpoints (if needed) | Carlos, Ian      | 1.5 days           |
| Write unit tests                 | Ian, Matthew     | 1 day              |

---

### **Phase 3: 11/14 - 11/17 (Frontend)**

| **Task**                               | **Owner**  | **Duration** |
| -------------------------------------------- | ---------------- | ------------------ |
| Set up Django templates                      | Carlos           | 0.5 days           |
| Create base template                         | Ian, Killian     | 1 day              |
| Style with CSS                               | Ian, Killian     | 1 day              |
| Implement login page                         | Ian              | 0.5 days           |
| Implement homepage (project list view)       | Ian, Carlos      | 1 day              |
| Implement project view                       | Carlos, Ian      | 1 day              |
| Implement sample view                        | Killian, Ian     | 1 day              |
| Implement all-geo view                       | Killian          | 0.5 days           |
| Implement all-micro view                     | Killian          | 0.5 days           |
| Implement all-physical view                  | Matthew          | 0.5 days           |
| Implement sample ingest view                 | Matthew, Killian | 1 day              |
| Implement profile management view            | Ian              | 0.5 days           |
| Implement admin/owner management view        | Carlos, Matthew  | 1 day              |
| Implement admin: all projects view           | Carlos           | 0.5 days           |
| Implement admin: all samples view            | Matthew          | 0.5 days           |
| Create forms (project, sample, user, upload) | Ian, Carlos      | 1.5 days           |
| Add search and filter functionality          | Killian, Carlos  | 1 day              |

---

### **Phase 4: 11/18 - 11/21 (Integration & Workflows)**

| **Task**            | **Owner**  | **Duration** |
| ------------------------- | ---------------- | ------------------ |
| Design upload templates   | Killian, Matthew | 0.5 days           |
| Create upload UI          | Ian, Carlos      | 1 day              |
| Implement file parsing    | Matthew, Killian | 1.5 days           |
| Implement data validation | Killian, Matthew | 1 day              |
| Implement bulk insert     | Matthew, Carlos  | 1 day              |
| Handle upload errors      | Killian, Ian     | 1 day              |
| Create workflow models    | Carlos, Matthew  | 1 day              |
| Implement workflow UI     | Ian, Carlos      | 1.5 days           |
| Create audit logging      | Killian          | 1 day              |
| Integration testing       | All              | 1 day              |

---

### **Phase 5: 11/22 - 11/25 (Testing & Polish)**

| **Task**            | **Owner**          | **Duration** |
| ------------------------- | ------------------------ | ------------------ |
| Integration testing       | All                      | 2 days             |
| Bug fixing (critical)     | Carlos, Matthew, Killian | 2 days             |
| Bug fixing (non-critical) | Ian, Killian, Carlos     | 2 days             |
| Performance optimization  | Carlos, Matthew          | 1 day              |
| Security review           | Killian, Carlos          | 1 day              |
| Documentation             | Ian, Killian             | 2 days             |
| Prepare demo data         | Matthew, Ian             | 1 day              |
| Final deployment test     | All                      | 0.5 days           |

---

## **Task Assignments Summary**

* **Killian:** Architecture, RBAC, backend views, data views (geo/micro/physical), file parsing & validation, audit logging, security review, search functionality
* **Matthew:** Database normalization & SQL (lead), Django models, backend logic, admin views, file upload functionality, performance optimization
* **Carlos:** Dev environment setup (lead), Django config, authentication, frontend & backend integration, admin management views, workflow implementation
* **Ian:** UI implementation (lead), frontend views, forms, CSS, profile management, documentation, testing support

---

Would you like me to make this Markdown **GitHub-ready** (with collapsible `<details>` sections and emojis for tasks)? Itd make it easier to navigate during development reviews.
