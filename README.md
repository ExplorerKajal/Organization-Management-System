# Organization-Management-System

A full-stack web application developed to organize and manage employees, departments, projects, tasks, and internal collaboration within an organization.

This platform integrates employee management, project tracking, and team communication into a single system, acting as a compact solution similar to tools like Jira and Slack.

🚀 Features
👤 Employee Management

Create, update, and manage employee records

Role-based access control: Admin, Team Lead, Employee

Secure authentication and authorization

Employees mapped to their respective departments

🏢 Department Management

Create and maintain departments

Assign department heads or managers

View employees based on departments

📁 Project Management

Team Leads can initiate and manage projects

Assign employees to projects

Monitor project timelines and completion status

🧩 Project Phases

Divide projects into multiple phases

Track timelines and progress of each phase

✅ Task Management

Assign tasks to employees

Update task status (Pending / In Progress / Completed)

Manage task priorities and deadlines

Track overall project progress

💬 Team Collaboration (Chat & Groups)

Create collaboration groups

Add or remove group members

Group-based chat system

Persistent message history

📎 Resource Sharing

Upload and share documents within groups

Download shared files securely

🔔 Notification System

Task assignment alerts

Deadline and reminder notifications

Project and group activity updates

🏗 System Architecture

Frontend: React.js

Backend: Flask (Python)

Database: MySQL / PostgreSQL

Authentication: JWT

ORM: SQLAlchemy

🧠 Database Entities

Employee

Department

Project

ProjectMembers (Many-to-Many)

Phase

Task

Group

GroupMembers

Message

Resource

Notification

🌐 API Modules

Authentication

Login

Token validation

Employees

Add employee

View employee list

Projects

Create project

Add project members

View project details

Tasks

Create tasks

Assign tasks

Update task status

Collaboration

Create groups

Manage members

Send messages

Upload resources

🎨 Frontend Pages

Login / Register

Dashboard

Employees

Departments

Projects

Project Details

Task Board

Groups & Chat

Notifications

🔮 Future Enhancements

Real-time chat using WebSockets

Email notification system

Cloud-based file storage (AWS S3)

Analytics and reporting dashboard

Fully responsive mobile-friendly UI

🎯 Learning Outcomes

This project helps in understanding:

Full-stack application development

RESTful API design

Database relationships (One-to-Many, Many-to-Many)

Authentication and authorization mechanisms

Collaborative and real-time systems

📌 Conclusion

This project represents a real-world enterprise workflow solution where employee management, project execution, communication, and resource sharing are integrated into a single efficient platform.
