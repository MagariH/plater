# Plater 🍲🌱
> Hyper-local food rescue & surplus matching platform.
> Connecting local businesses with neighbors to turn surplus food into affordable meals before it goes to waste.

Built for **Neighborhood Hacks**.

## 🌟 Key Features
- **Merchant Surplus Dashboard:** Local bakeries and cafes can post surplus meals in under 30 seconds.
- **Neighborhood Feed:** Real-time visibility of available meals, discount tiers, and pickup windows.
- **Instant Claim Verification:** One-tap reserving that issues a secure pickup token (`PLT-XXXX`).
- **Zero Food Waste Impact:** Helping neighbors save money while supporting local shops.

## 🛠️ Built With
- Python & FastAPI
- SQLite
- HTML5, Tailwind CSS, JavaScript
- 
## 💻 How to Run Locally

To run this project on your own machine, you need Python installed. Follow these quick steps:

**1. Install the required libraries:**
Open your terminal or command prompt and install the necessary Python packages:
```bash
pip install fastapi uvicorn pydantic
2. Start the application server:
Navigate to the folder containing plater.py and run the following command to start the Uvicorn web server:
python -m uvicorn plater:app --reload

3. Open the app:
Once the server is running, open your web browser and go to:
http://127.0.0.1:8000
