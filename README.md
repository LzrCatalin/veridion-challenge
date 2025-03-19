# Website Logo Similarity

This project is a Python-based challenge aimed at finding similarities between logos of different websites. The program uses various image processing and machine learning techniques to analyze and compare logo images, providing a similarity group of them.

## Project Description

Websites are stored in a `.parquet` file inside the `src/dataset/` folder. Using **BeautifulSoup**, the program scrapes the websites and saves their logos. After scraping, **OpenCV** is used to open, resize, and extract features such as:

- **HuMoments**: For shape-based features.
- **SIFT (Scale-Invariant Feature Transform)**: For detecting and describing local features in images.
- **ORB (Oriented FAST and Rotated BRIEF)**: For efficient feature detection and matching.

These features are then used to compute similarity scores between the logos.

## Getting Started

To run this program on your local machine, follow the steps below:

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/your-username/veridion-challenge.git
   cd website-logo-similarity

2. **Create environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install required dependencies**:
   ```bash
   pip install -r requirments.txt

4. **Run the program**:
   ```bash
   python main.py
