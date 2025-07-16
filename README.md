# Blank Page

**Blank Page** is a modern, community-driven blogging platform where anyone can read, write, and share articles. Readers can browse high-quality posts, register to write their own, and interact with content through likes, dislikes, and bookmarks — while administrators ensure the quality and integrity of the published content.

---

## Team Members

| Name                        | Registration     | Role                                           |
| --------------------------- | ---------------- | ---------------------------------------------- |
| Rayhan Aziz Chowdhury Shafi | 0562310005101007 | Full Stack Development                         |
| Fatematuj Johura Mim        | 0562310005101032 | Full Stack Development, Testing, Documentation |

---

## Setup & Installation

Follow these steps to run **Blank Page** locally.

### Clone the Repository

```bash
git clone https://github.com/r-shafi/blank-page.git
cd blank-page
```

---

### Install & Run the **Frontend**

```bash
cd frontend
npm install
npm run dev
```

---

### Install & Run the **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### Access the App

- **Frontend:** [http://localhost:8080](http://localhost:8080)
- **Backend API:** [http://localhost:8000](http://localhost:8000)

---

## ✅ Features

- Public reading of published blogs
- User registration and post creation (drafts & publish flow)
- Like / Dislike / Bookmark articles
- Admin approval and moderation
- Contact form and newsletter subscription
- Secure role-based access and management
