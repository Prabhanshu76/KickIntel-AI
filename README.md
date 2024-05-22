# Football-Analytics-CV
Our project is dedicated to revolutionizing real-time soccer match analysis by leveraging cutting-edge technologies such as YOLOv5 and ByteTracker. We have successfully implemented a range of features that enhance soccer video analysis through precise player identification, accurate ball tracking, and the identification of crucial in-game events.

## YOLOv5 Integration
With the integration of YOLOv5, we've achieved remarkable accuracy and speed in player and ball detection within live match footage. YOLOv5 has proven to be an invaluable asset, allowing us to reliably spot players and the soccer ball even in fast-paced game scenarios.

## ByteTracker Tracking System
In tandem with YOLOv5, we've incorporated ByteTracker, a sophisticated tracking system. ByteTracker's efficiency ensures seamless and continuous tracking of players and the ball across frames, providing a reliable way to monitor their movements throughout the game.

## Implemented Features
Our project boasts a comprehensive set of features, enhancing soccer match analysis:

- **Player and Ball Detection:**
  - Leveraging YOLOv5, our system accurately identifies and tracks players and the soccer ball in real time.

- **Player in Possession Detection:**
  - The system intelligently identifies the player currently in possession of the ball during the match.

- **Team Identification/Classification:**
  - Our system classifies and identifies teams based on jersey colors, contributing to comprehensive team analysis.

- **Team Possession Count:**
  - We provide insights into team possession counts, helping teams understand and analyze their control over the ball during the game.

- **Team Pass Count:**
  - The system counts and analyzes the passes made by each team, offering a valuable metric for assessing teamwork and strategic plays.

## Project Goals
Our overarching goal is to provide coaches and analysts with a tool that offers deep insights into team strategies and player performances. By enabling comprehensive soccer analytics, we aim to support smarter decision-making in coaching and enhance overall performance analysis. Our ultimate objective is to contribute to the advancement of soccer analysis methods, offering teams valuable insights to refine their strategies and tactics.

---

## Project Setup
To get started with our project, follow these steps:

1. **Download and Copy ByteTrack Folder:** [Custom ByteTrack Folder](https://drive.google.com/file/d/12Yzo3-L2uiR4ivmQkLLFM501_4nXU_ue/view?usp=sharing)
   - Copy this custom ByteTrack folder to your project directory.

2. **Download Model:**
   - Download the model from this [link](https://drive.google.com/file/d/1_3nIEdVzW3674-lumMaU0OY7nhKTwdSL/view?usp=sharing)
   - Edit `config.ini` to set the correct path for the downloaded model.

3. **Setup:**
   - Run `setup.py` to ensure all dependencies are installed.

4. **Launch:**
   - Run `app.py` to start the application.
  
After launching, open the following URL in your web browser: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

#### Configuring Jersey Color Ranges

Open the `config.ini` file and navigate to the `[Boundaries_HSV]` section. Adjust the HSV parameters for each team to match the specific colors of their jerseys:

```ini
[Boundaries_HSV]
team1_h_min = ...
team1_s_min = ...
team1_v_min = ...
team1_h_max = ...
team1_s_max = ...
team1_v_max = ...

team2_h_min = ...
team2_s_min = ...
team2_v_min =...
team2_h_max = ...
team2_s_max = ...
team2_v_max = ...
```

##Input Video 
https://drive.google.com/file/d/1y8l2LFBI_I8JZbpyFxQzxMHuRlDFouUs/view?usp=sharing

##Output Video
https://drive.google.com/file/d/1rV_ib7MFLPu8kYvxj0eibML2f3NSCfm5/view?usp=sharing

---
## References
Please find the relevant references below:

1. Roboflow. (2022). Track Football Players Using Computer Vision [Blog post and Jupyter Notebook]. Retrieved from [Roboflow Blog](https://blog.roboflow.com/track-football-players/) and [Roboflow GitHub](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-track-football-players.ipynb)
2. Liu, Jia Tong, Xiaofeng Li, Wenlong Zhang, Yimin Wang, Hongqi. (2009). Automatic player detection, labeling and tracking in broadcast soccer video. Pattern Recognition Letters, 30, 103-113. DOI: [10.1016/j.patrec.2008.02.011](https://doi.org/10.1016/j.patrec.2008.02.011)
3. Ren, Jinchang Orwell, James Jones, Graeme Xu, Ming. (2009). Tracking the soccer ball using multiple fixed cameras. Computer Vision and Image Understanding, 113, 633-642. DOI: [10.1016/j.cviu.2008.01.007](https://doi.org/10.1016/j.cviu.2008.01.007)
4. Mavrogiannis, P., Maglogiannis, I. (2022). Amateur football analytics using computer vision. Neural Comput Applic, 34, 19639–19654. DOI: [10.1007/s00521-022-07692-6](https://doi.org/10.1007/s00521-022-07692-6)
5. Murat Durus. (n.d.). Ball Tracking and Action Recognition of Soccer Players in TV Broadcast Videos. Retrieved from [PDF](https://mediatum.ub.tum.de/doc/1145077/870316.pdf)
6. Darapaneni, Narayana Kumar, Prashant Malhotra, Nikhil Sundaramurthy, Vigneswaran Thakur, Abhaya Chauhan, Shivam Thangeda, Krishna Paduri, Anwesh. (2022). Detecting key Soccer match events to create highlights using Computer Vision.
7. Huang, Yu Llach, Joan Bhagavathy, Sitaram. (2007). Players and Ball Detection in Soccer Videos Based on Color Segmentation and Shape Analysis. 4577, 416-425. DOI: [10.1007/978-3-540-73417-8_50](https://doi.org/10.1007/978-3-540-73417-8_50)
8. Banoth, Thulasya Hashmi, Mohammad Farukh. (2022). YOLOv3-SORT: detection and tracking player/ball in soccer sport. Journal of Electronic Imaging, 32. DOI: [10.1117/1.JEI.32.1.011003](https://doi.org/10.1117/1.JEI.32.1.011003)
