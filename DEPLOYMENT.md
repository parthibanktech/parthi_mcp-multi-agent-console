# 🚀 Deployment Guide: Multi-Agent MCP Console

This guide covers how to deploy the Multi-Agent MCP application. The project is containerized, meaning it runs the Streamlit Client, Finance Agent, and HR Agent all in one isolated environment.

## 📂 Project Structure for Deployment

- **`Dockerfile`**: Defines the environment (Python 3.11) and installation steps.
- **`start.sh`**: The startup script that launches all 3 services (Finance, HR, Streamlit) simultaneously.
- **`docker-compose.yml`**: For running the application locally with one command.
- **`render.yaml`**: Configuration for automated deployment on Render.

---

## 🛠 Option 1: Run Locally with Docker Compose (Recommended)

This is the best way to test before deploying to the cloud.

1.  **Prerequisites**: Ensure you have Docker Desktop installed.
2.  **Set API Key**:
    *   Create a `.env` file in this directory (if not exists) and add:
        ```bash
        OPENAI_API_KEY=sk-proj-...
        ```
    *   *Or* pass it directly in the command.
3.  **Run**:
    ```bash
    docker-compose up --build
    ```
4.  **Access**: Open [http://localhost:8501](http://localhost:8501).

---

## ☁️ Option 2: Deploy to Render (Cloud)

We have configured the project to work seamlessly with Render's Docker runtime.

### Method A: "Deploy to Render" Button (Blueprints)
1.  Push your code to GitHub.
2.  Log in to [Render.com](https://render.com).
3.  Go to **Blueprints** -> **New Blueprint Instance**.
4.  Connect your repository.
5.  Render will read `render.yaml` and set up the service automatically.
6.  **Important**: You will be prompted to enter your `OPENAI_API_KEY` in the dashboard during setup.

### Method B: Manual Web Service Setup
1.  Push your code to GitHub.
2.  On Render, click **New +** -> **Web Service**.
3.  Connect your repository.
4.  **Runtime**: Select **Docker**.
5.  **Region**: Choose one close to you (e.g., Oregon, Frankfurt).
6.  **Environment Variables**:
    *   Add `OPENAI_API_KEY` with your actual key.
7.  Click **Create Web Service**.

---

## ℹ️ Technical Details

### Networking
*   **Internal**: The Streamlit app talks to the MCP servers via `http://127.0.0.1:8010` and `http://127.0.0.1:8011`. This works because they share the same container network namespace.
*   **External**: Only the Streamlit port (default `8501`) is exposed to the outside world.

### Troubleshooting
*   **"Port already in use"**: The `start.sh` script tries to handle this, but if you restart the container rapidly, give it a moment.
*   **Logs**: Check the Render logs to see the output of all three services (Streamlit, Finance, HR) interleaved.
