# KickIntel-AI
## Overview
**KickIntel AI** is an advanced football analytics platform that leverages cutting-edge computer vision and artificial intelligence technologies to provide deep insights into football matches. This project focuses on providing real-time match data to offer more detailed analysis and enhance decision-making processes.
## Project Video

[Watch the project video demo](https://drive.google.com/file/d/1qqMumcxw_C-muFE0qtfpQjtfQV8UbXMz/view?usp=sharing)
## Features
- **Real-time Analysis**: Process live match footage to generate immediate insights.
- **Player and Ball Tracking**: Monitor player and ball movements and positions throughout the game.
- **Team Identification**: Automatically categorize each player into their respective teams.
- **Performance Metrics**: Discern the player currently in possession, overall team possession, and the number of passes made by both teams.
- **Interactive Dashboard**: Accessible and intuitive interface for real-time match analysis and data visualization.
- ## Installation

### Docker Setup (Recommended)

1. Make sure you have Docker installed on your system.

2. Clone the repository:
    ```sh
    git clone https://github.com/Prabhanshu76/KickIntel-AI.git
    cd KickIntelAI
    ```

3. Build and run the Docker container:
    ```sh
    docker-compose up --build
    ```
### Manual Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Prabhanshu76/KickIntel-AI.git
    cd KickIntelAI
    ```

#### Backend

2. Navigate to the backend directory:
    ```sh
    cd backend
    ```

3. Run setup script:
    ```sh
    python setup.py
    ```

4. Start the backend server:
    ```sh
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

#### Frontend

2. Navigate to the frontend directory:
    ```sh
    cd ../frontend
    ```

3. Install dependencies:
    ```sh
    npm install
    ```

4. Start the frontend server:
    ```sh
    npm start
    ```

## Usage

1. Once everything is set up, navigate to `http://localhost:8000` in your web browser.
2. Upload a football match video via the dashboard or try the demo video.
3. Explore the generated insights.
4. To upload a new video, click on the refresh button to clear any previous data, then upload the new video.

## References

This project is hugely inspired and referred from the Roboflow blog: Roboflow. (2022). Track Football Players Using Computer Vision [Blog post and Jupyter Notebook]. Retrieved from [Roboflow Blog](https://blog.roboflow.com/track-football-players/) and [Roboflow GitHub](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-track-football-players.ipynb).
