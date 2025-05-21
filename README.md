# 🚀 OUR OWN

**OUR OWN** is a fully functional service-based web application built with **Django**. It offers dynamic public pages for services, blogs, testimonials, FAQs, contact, and booking, alongside a robust admin dashboard for content management.

---

## ✨ Features

### 🌐 Public Pages
* **Homepage** with dynamic content
* **About Us** section
* **Services** list
* **FAQs** with dynamic management
* **Testimonials** from clients
* **Blog** with list/detail views
* **Contact Page** with a working contact form
* **Booking Page** where users can submit service requests 📅

### 🔐 Admin Dashboard
Accessible at `/dashboard/`, admins can:
* ✅ Create, update, and delete:
    * Services
    * Blog Posts
    * FAQs
    * Testimonials
* ✅ View and delete:
    * Contact Messages
    * Bookings

All admin views are styled using **Bootstrap**, and form fields are rendered manually for better UI control.

---

## 🛠 Tech Stack

* **Backend**: Django, Django ORM
* **Frontend**: HTML, CSS (Bootstrap)
* **Database**: SQLite (default), can be replaced with PostgreSQL/MySQL
* **Templating**: Django Templates

---

## 🧪 How to Run the Project

1.  **Clone the repo** ⬇️

    ```bash
    git clone https://github.com/sarojoffl/OUR-OWN.git
    cd OUR-OWN
    ```

2.  **Create and activate a virtual environment** 💻

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: .\env\Scripts\activate
    ```

3.  **Install dependencies** 📦

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations** 🔄

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser** 👤

    ```bash
    python manage.py createsuperuser
    ```

6.  **Start the development server** ▶️

    ```bash
    python manage.py runserver
    ```

### Access:

* **Public Site**: `http://localhost:8000/`
* **Admin Dashboard**: `http://localhost:8000/dashboard/`
