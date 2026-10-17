import os
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Plater", description="Hyper-local Food Rescue & Surplus Matching Platform")

# Mock adatbázis a demonstrációhoz
listings_db = [
    {
        "id": 1,
        "business_name": "Corner Bakery & Cafe",
        "category": "Bakery",
        "title": "Fresh Pastry & Bagel Mystery Box",
        "original_price": 14.50,
        "discount_price": 4.50,
        "pickup_window": "19:00 - 19:45",
        "status": "active",
        "claim_code": None
    },
    {
        "id": 2,
        "business_name": "Green Leaf Grocers",
        "category": "Produce",
        "title": "Seasonal Fruit & Veggie Surplus Bag",
        "original_price": 18.00,
        "discount_price": 5.00,
        "pickup_window": "18:30 - 19:15",
        "status": "active",
        "claim_code": None
    },
    {
        "id": 3,
        "business_name": "Neighborhood Deli",
        "category": "Prepared Food",
        "title": "Artisan Sandwiches & Soup Bundle",
        "original_price": 16.00,
        "discount_price": 0.00,
        "pickup_window": "20:00 - 20:30",
        "status": "active",
        "claim_code": None
    }
]

class ListingCreate(BaseModel):
    business_name: str
    category: str
    title: str
    original_price: float
    discount_price: float
    pickup_window: str

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plater - Save Food, Feed Neighbors</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>body { font-family: 'Plus Jakarta Sans', sans-serif; }</style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen">
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-40">
        <div class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <span class="text-2xl">🍲</span>
                <span class="text-2xl font-bold tracking-tight text-emerald-600">plater</span>
                <span class="hidden sm:inline-block ml-2 px-2 py-0.5 text-xs font-medium bg-emerald-100 text-emerald-800 rounded-full">Neighborhood Hacks</span>
            </div>
            <button onclick="toggleModal('addModal')" class="bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm px-4 py-2 rounded-lg shadow-sm transition">
                + Post Surplus
            </button>
        </div>
    </nav>

    <header class="max-w-5xl mx-auto px-4 pt-8 pb-4 text-center">
        <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">Rescue fresh food in your neighborhood</h1>
        <p class="mt-2 text-slate-600 max-w-xl mx-auto text-sm sm:text-base">
            Local bakeries & restaurants have surplus fresh meals today. Claim them before closing time at steep discounts.
        </p>
    </header>

    <main class="max-w-5xl mx-auto px-4 py-6">
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-slate-900">Available Near You Today</h2>
            <span class="text-xs text-slate-500 font-medium">Real-time status</span>
        </div>

        <div id="listingsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Loaded dynamically via JS -->
        </div>
    </main>

    <!-- Modal: Success -->
    <div id="claimModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-sm w-full p-6 text-center shadow-xl">
            <div class="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">🎉</div>
            <h3 class="text-xl font-bold text-slate-900">Meal Rescued!</h3>
            <p id="claimModalItem" class="text-sm text-slate-600 mt-1 font-medium"></p>
            <div class="mt-4 p-4 bg-emerald-50 border border-emerald-200 rounded-2xl">
                <span class="text-xs font-semibold text-emerald-800 tracking-wider uppercase">Your Pickup Code</span>
                <p id="claimModalCode" class="text-3xl font-extrabold text-emerald-700 tracking-widest mt-1">PLT-0000</p>
            </div>
            <p id="claimModalWindow" class="text-xs text-slate-500 mt-3"></p>
            <button onclick="toggleModal('claimModal'); loadListings();" class="mt-6 w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2.5 rounded-xl transition">Done</button>
        </div>
    </div>

    <!-- Modal: Add -->
    <div id="addModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-xl">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold text-slate-900">Post Surplus Meal</h3>
                <button onclick="toggleModal('addModal')" class="text-slate-400 hover:text-slate-600 text-xl font-bold">&times;</button>
            </div>
            <form id="addListingForm" onsubmit="submitNewListing(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Business Name</label>
                    <input type="text" id="business_name" required placeholder="e.g. Sunny Bakery" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Category</label>
                        <select id="category" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                            <option>Bakery</option>
                            <option>Produce</option>
                            <option>Prepared Food</option>
                            <option>Cafe / Drinks</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Pickup Window</label>
                        <input type="text" id="pickup_window" required placeholder="e.g. 19:30 - 20:00" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-slate-700 mb-1">Listing Title</label>
                    <input type="text" id="title" required placeholder="e.g. 3x Sourdough Loaf" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Original Price ($)</label>
                        <input type="number" step="0.5" id="original_price" required placeholder="12.00" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Rescue Price ($)</label>
                        <input type="number" step="0.5" id="discount_price" required placeholder="3.50" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-emerald-500 outline-none">
                    </div>
                </div>
                <button type="submit" class="w-full mt-4 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2.5 rounded-xl transition shadow-sm">Publish to Neighborhood</button>
            </form>
        </div>
    </div>

    <script>
        function toggleModal(id) { document.getElementById(id).classList.toggle('hidden'); }

        async function loadListings() {
            const res = await fetch('/api/listings');
            const items = await res.json();
            const grid = document.getElementById('listingsGrid');
            grid.innerHTML = '';
            
            items.forEach(item => {
                const isActive = item.status === 'active';
                const priceHtml = item.discount_price === 0 ? '<span class="text-xl font-extrabold text-emerald-600">FREE</span>' : `<span class="text-xl font-extrabold text-slate-900">$${item.discount_price.toFixed(2)}</span>`;
                
                grid.innerHTML += `
                    <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">${item.category}</span>
                                <span class="flex items-center text-xs font-semibold ${isActive ? 'text-emerald-700 bg-emerald-50' : 'text-slate-400 bg-slate-100'} px-2 py-0.5 rounded-full">
                                    <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-500' : 'bg-slate-400'} mr-1.5"></span> ${isActive ? 'Available' : 'Claimed'}
                                </span>
                            </div>
                            <h3 class="font-bold text-slate-900 text-lg leading-snug">${item.title}</h3>
                            <p class="text-sm font-medium text-slate-500 mt-1">${item.business_name}</p>
                            <div class="mt-4 p-3 bg-amber-50 rounded-xl border border-amber-100">
                                <p class="text-xs text-amber-800 font-medium">⏱️ <strong>Pickup Window:</strong> ${item.pickup_window}</p>
                            </div>
                        </div>
                        <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                            <div>
                                <div class="flex items-baseline space-x-2">
                                    ${priceHtml}
                                    <span class="text-xs text-slate-400 line-through">$${item.original_price.toFixed(2)}</span>
                                </div>
                            </div>
                            ${isActive ? `<button onclick="claimItem(${item.id})" class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm px-4 py-2 rounded-xl transition shadow-sm">Claim Meal</button>` : `<button disabled class="bg-slate-200 text-slate-400 font-semibold text-sm px-4 py-2 rounded-xl cursor-not-allowed">Claimed</button>`}
                        </div>
                    </div>
                `;
            });
        }

        async function claimItem(id) {
            const res = await fetch(`/api/listings/${id}/claim`, { method: 'POST' });
            const data = await res.json();
            if (!res.ok) { alert(data.detail); return; }
            document.getElementById('claimModalItem').innerText = data.item_title;
            document.getElementById('claimModalCode').innerText = data.claim_code;
            document.getElementById('claimModalWindow').innerText = `Please pick up during: ${data.pickup_window}`;
            toggleModal('claimModal');
        }

        async function submitNewListing(e) {
            e.preventDefault();
            const payload = {
                business_name: document.getElementById('business_name').value,
                category: document.getElementById('category').value,
                title: document.getElementById('title').value,
                pickup_window: document.getElementById('pickup_window').value,
                original_price: parseFloat(document.getElementById('original_price').value),
                discount_price: parseFloat(document.getElementById('discount_price').value)
            };
            const res = await fetch('/api/listings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                toggleModal('addModal');
                loadListings();
            }
        }

        loadListings();
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

@app.get("/api/listings")
def get_listings():
    return listings_db

@app.post("/api/listings")
def create_listing(listing: ListingCreate):
    new_item = listing.dict()
    new_item["id"] = len(listings_db) + 1
    new_item["status"] = "active"
    new_item["claim_code"] = None
    listings_db.append(new_item)
    return new_item

@app.post("/api/listings/{item_id}/claim")
def claim_listing(item_id: int):
    for item in listings_db:
        if item["id"] == item_id:
            if item["status"] != "active":
                raise HTTPException(status_code=400, detail="Már lefoglalták!")
            claim_code = f"PLT-{random.randint(1000, 9999)}"
            item["status"] = "claimed"
            item["claim_code"] = claim_code
            return {
                "message": "Sikeres mentés!",
                "claim_code": claim_code,
                "item_title": item["title"],
                "pickup_window": item["pickup_window"]
            }
    raise HTTPException(status_code=404, detail="Nem található")
