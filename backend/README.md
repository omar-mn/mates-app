# 🚀 Mates Backend

Backend service for **Mates**, a real-time chat & community platform built with Django, REST APIs, and WebSockets.

> ⚡ Designed as a scalable backend system with real-time communication using Django Channels.

---

## 🧠 Overview

**Mates** is a chat-driven platform where users can:

- Join public or private rooms
- Communicate in real-time
- Build and manage small communities

This project focuses on building a **clean backend architecture** with:
- RESTful APIs
- JWT authentication
- Real-time messaging (WebSockets)

---

## 🛠 Tech Stack

- **Python**
- **Django & Django REST Framework**
- **PostgreSQL**
- **JWT Authentication (dj-rest-auth)**
- **Django Channels (WebSockets)**

---

## ⚡ Core Features

### ✅ MVP Features

- 🔐 Authentication (Register / Login)
- 🔑 JWT-based session management
- 🏠 Public & private chat rooms
- 👥 Room membership system
- 💬 Real-time messaging via WebSockets
- 📜 Message history per room

---

## 🚧 Planned Features

- 1-to-1 private chat
- User profile & avatars
- Email verification
- Online users indicator
- Reactions & emojis
- File uploads
- Notifications system

---

## 🧱 Architecture

The project follows a modular structure:

```
backend/
├── Mates/        # Core settings
├── Users/        # Authentication & custom user model
├── Rooms/        # Room logic & memberships
├── Messages/     # Messaging + WebSocket consumers
```

### 🔹 Design Approach

- **Models** → Database layer  
- **Serializers** → Data transformation  
- **API Views** → REST endpoints  
- **Consumers** → Real-time WebSocket handling  

---

## 🌐 API Overview

### 🔐 Auth
- `POST /api/auth/registration/`
- `POST /api/auth/login/`
- `GET /api/auth/user/`

### 💬 Rooms
- `GET /api/rooms/`

### 📨 Messages
- `GET /api/messages/<room_id>/`

---

## ⚡ WebSocket Usage

```
ws://{base_url}/ws/message/<room_id>/?token=<JWT_TOKEN>
```

---

## 🗄 Database Models

- **Account** → Custom user model  
- **Room** → Chat rooms  
- **Membership** → Access control  
- **JoinRequest** → Private room requests  
- **Message** → Chat messages  

---

## ⚙️ Run Locally

```bash
git clone https://github.com/omar-mn/mates-backend.git
cd mates-backend

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

> ⚠️ Make sure PostgreSQL is configured properly.

---

## 📡 API Documentation

👉 https://sudoers-3102.postman.co/workspace/5ea84f5f-1961-427e-8ca4-98dc629e550b

---

## 📊 Project Status

🚧 **MVP — actively improving**

---

## 🔗 Related Projects

- Frontend: https://github.com/omar-mn/mates-frontend

---

## 👨‍💻 Author

Built by **Omar Ali**   
Fullstack Developer → Future DevOps Engineer ☁️
