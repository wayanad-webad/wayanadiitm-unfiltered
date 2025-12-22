# Deployment Guide (Free Tier)

You can deploy this application for **$0/month** using the following services:
1.  **Database**: MongoDB Atlas (Free M0 Cluster)
2.  **Backend**: Render (Free Web Service)
3.  **Frontend**: Vercel (Free Static Hosting)

## Step 1: Database (MongoDB Atlas)
1.  Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and sign up.
2.  Create a **Free M0 Cluster**.
3.  Create a database user (e.g., `admin`) and save the password.
4.  In "Network Access", allow access from **Anywhere (0.0.0.0/0)** (necessary for cloud hosting).
5.  Get your Connection String: `mongodb+srv://admin:<password>@cluster...`

## Step 2: Render (Frontend + Backend in One)
1.  Push your code to **GitHub**.
2.  Sign up or Log in to [Render](https://render.com/).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repo.
5.  **Settings**:
    -   **Name**: `wayanad-hushup`
    -   **Runtime**: **Docker** (This is the key step!)
    -   **Region**: Choose closest to you (e.g., Singapore/Frankfurt).
    -   **Branch**: `main` (or master).
6.  **Environment Variables**:
    -   `MONGO_URI`: (Paste connection string from Step 1)
    -   `SECRET_KEY`: (Random string)
    -   `JWT_SECRET_KEY`: (Random string)
7.  Deploy!
    - Render will detect the `Dockerfile` in the root.
    - It will build the frontend, build the backend, and combine them.
    - You will get a single URL (e.g., `https://wayanad-hushup.onrender.com`).

## Summary
- **App URL**: https://wayanad-hushup.onrender.com (Serves both frontend & backend)
- **Database**: MongoDB Atlas Cloud

**Important**: 
- The free instance on Render spins down after inactivity. The first request might take a minute.
- Since it's all in one place, you don't need to configure cors or API URLs manually; the frontend uses relative paths (or defaults) and Flask serves it all.
