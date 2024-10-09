# 🌟 Marketplace Repricer & Analytics Platform

Welcome to the **Marketplace Repricer and Analytics Platform**, a powerful tool designed for marketplace sellers to help optimize pricing strategies, monitor performance, and boost profitability. Equipped with real-time dashboards and automation tools, it's your one-stop solution for efficient marketplace management.

---

## 🚀 Features at a Glance

- **🔄 Repricing Strategies**: Automate your pricing with multiple customizable strategies.
- **📊 Real-Time Analytics Dashboards**: Get visual insights into your sales, pricing, and inventory in real time.
- **📈 Automated Reports**: Schedule and receive performance reports directly via Telegram and other channels.
- **🔔 Notifications**: Stay up to date with real-time WebSocket notifications.
- **🔐 Secure Access**: Robust user authentication and password encryption to ensure data security.

---

## 🛠️ Built With

| Tech Stack      | Description                                  |
| --------------- | -------------------------------------------- |
| **Flask**       | Web framework for building the backend       |
| **Celery**      | Task queue for background processing         |
| **Redis**       | Message broker for Celery tasks              |
| **Flask-SocketIO** | WebSockets for real-time notifications     |
| **SQLite3**     | Lightweight database for persistent storage  |
| **Pandas**      | Data manipulation and analysis               |
| **SQLAlchemy**  | SQL toolkit and Object-Relational Mapping    |
| **Telebot**     | Integration for Telegram notifications       |
| **Flask-Login** | User authentication and session management   |
| **Flask-Bcrypt**| Password hashing for secure logins           |
| **Eventlet**    | Asynchronous task handling                   |
| **Openpyxl**    | Excel report generation and export           |
| **Gunicorn**    | Production-grade WSGI server                 |

---

## 🖥️ Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.7+
- Redis server

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Redis** (Ensure Redis is up and running):
   ```bash
   redis-server
   ```

4. **Start the Celery Worker**:
   ```bash
   celery -A app.celery worker --loglevel=info
   ```

5. **Start the Flask Application**:
   ```bash
   flask run
   ```

6. **For Production, Use Gunicorn**:
   ```bash
   gunicorn --worker-class eventlet -w 1 app:application
   ```

---

## ⚙️ How It Works

### 🔄 Repricing Automation
The platform supports various dynamic repricing strategies tailored to your business needs. It fetches real-time sales data, adjusts prices automatically based on selected strategies, and syncs it back to the marketplace.

### 📊 Data-Driven Insights
The analytics dashboard visualizes key metrics—sales trends, pricing history, and product performance—offering valuable insights into what strategies work best for you.

### 🗓️ Scheduled Tasks
Celery handles scheduled tasks such as fetching updated sales data, performing price checks, and generating reports. Redis serves as the message broker, ensuring efficient task distribution.

### 🔔 Real-Time Notifications
Receive notifications on task completions, new sales reports, or pricing updates through integrated WebSocket support, which ensures instant communication between the server and client.

---

## 📦 Project Structure

```
├── app.py               # Main Flask app
├── tasks.py             # Celery task definitions
├── templates/           # HTML templates for Flask
├── static/              # Static files (CSS, JS)
├── function/            # Modular functions for core features
│   ├── login.py         # User login handling
│   ├── singin.py        # User sign-up handling
│   ├── mydata.py        # Data processing functions
│   ├── payment.py       # Payment processing
│   └── settings.py      # User settings management
└── db/                  # SQLite databases
```

---

## 🛡️ Security

We take security seriously. User authentication is managed via **Flask-Login**, while passwords are hashed using **Flask-Bcrypt** to ensure data protection. All communications use secure context for HTTPS.

---

## 🛠️ Tools & Libraries

| Library         | Purpose                                      |
| --------------- | -------------------------------------------- |
| **Flask**       | Core web framework                           |
| **Celery**      | Asynchronous task queue                      |
| **Redis**       | Message broker for task management           |
| **Flask-SocketIO** | WebSockets for real-time updates          |
| **Pandas**      | Data manipulation                            |
| **SQLAlchemy**  | ORM for database management                  |
| **Telebot**     | Telegram bot integration for notifications   |
| **Openpyxl**    | Handling Excel reports and exports           |
| **Gunicorn**    | Production server for deployment             |
| **Eventlet**    | Async library for non-blocking I/O           |

---

## 🏁 Deployment

For production deployment, use **Gunicorn** with **Eventlet** for efficient task handling:

```bash
gunicorn --worker-class eventlet -w 1 app:application
```

Make sure Redis is running, and Celery workers are active to handle background tasks.

---

## 📋 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 💬 Contact

For more information or inquiries, please contact us via [support@example.com](mailto:support@example.com).

---

Made with ❤️ for marketplace sellers!
