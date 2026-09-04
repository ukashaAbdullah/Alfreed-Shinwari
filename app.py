import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# ============================================================
# APP CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Alfred Shinwari & Restaurant",
    page_icon="🍗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Put your exact ntfy topic name here:
NTFY_TOPIC = "alfred_orders_chowk99" 

ORDERS_FILE = "orders.csv"
GOOGLE_MAPS_LINK = "https://maps.app.goo.gl/hBRGvxccnKNYkEAAA"
DELIVERY_FEE = 150

# Initialize Cart State
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ============================================================
# COMPLETE MENU DATA
# ============================================================
MENU_DATA = [
    {
        "category": "SHINWARI & KARAHI",
        "items": [
            {
                "id": "sk_1", "name": "Mutton Shinwari Karahi (Full)", "price": 2900,
                "desc": "1 KG Fresh Mutton prepared in Desi Ghee & Tomatoes",
                "img": "https://images.unsplash.com/photo-1545247181-516773cae754?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_2", "name": "Mutton Shinwari Karahi (Half)", "price": 1550,
                "desc": "0.5 KG Freshly Prepared Shinwari Style Karahi",
                "img": "https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_3", "name": "Chicken Namkeen Karahi (Full)", "price": 1600,
                "desc": "1 KG Traditional Namkeen recipe with Green Chillies",
                "img": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_4", "name": "Chicken Namkeen Karahi (Half)", "price": 850,
                "desc": "0.5 KG Traditional Namkeen recipe",
                "img": "https://images.unsplash.com/photo-1606471191009-63994c53433b?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_5", "name": "Chicken White Karahi (Full)", "price": 1750,
                "desc": "1 KG Creamy Mild Curry with Fresh Yogurt & Almonds",
                "img": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_6", "name": "Desi Murgh Karahi", "price": 2200,
                "desc": "1 KG Free-range Chicken cooked in traditional spices",
                "img": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "CHARCOAL BBQ & GRILLS",
        "items": [
            {
                "id": "bbq_1", "name": "Peshawari Chapli Kebab", "price": 320,
                "desc": "Large Tender Pan-Fried Spiced Minced Beef Patty",
                "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_2", "name": "Chicken Malai Boti", "price": 650,
                "desc": "8 Tender Skewers marinated in Velvet Fresh Cream",
                "img": "https://unsplash.com/photos/cooked-food-on-white-ceramic-plate-OeNoC9Wx7ao"
            },
            {
                "id": "bbq_3", "name": "Mutton Tikka Boti", "price": 950,
                "desc": "Charcoal Smoked Spicy Juicy Mutton Cuts",
                "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_4", "name": "Beef Seekh Kebab", "price": 550,
                "desc": "4 Hand-Rolled Charcoal Grilled Minced Skewers",
                "img": "https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_5", "name": "Chicken Tikka (Leg/Breast)", "price": 350,
                "desc": "Quarter Chicken piece marinated in spicy yogurt",
                "img": "https://images.unsplash.com/photo-1628296068228-5696df3f4ddb?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_6", "name": "Reshmi Kebab", "price": 600,
                "desc": "4 Pieces of Silky Chicken Minced Skewers",
                "img": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "RICE & TANDOOR",
        "items": [
            {
                "id": "rt_1", "name": "Special Kabuli Pulao", "price": 850,
                "desc": "Aromatic Saffron Basmati topped with Raisins & Braised Beef",
                "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_2", "name": "Chicken Biryani", "price": 450,
                "desc": "Classic Spiced Chicken Biryani with Raita",
                "img": "https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_3", "name": "Sesame Roghani Naan", "price": 70,
                "desc": "Clay-Oven Baked with Pure Butter & Sesame Seeds",
                "img": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_4", "name": "Garlic Naan", "price": 80,
                "desc": "Infused with fresh garlic and coriander",
                "img": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_5", "name": "Tandoori Roti", "price": 25,
                "desc": "Fresh whole wheat flatbread",
                "img": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "BEVERAGES",
        "items": [
            {
                "id": "bv_1", "name": "Peshawari Green Qahwa", "price": 100,
                "desc": "Traditional Cardamom, Mint & Saffron Green Tea",
                "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_2", "name": "Fresh Mint Margarita", "price": 250,
                "desc": "Chilled Fresh Mint Cooler with Lemon Spritz",
                "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_3", "name": "Sweet Lassi", "price": 180,
                "desc": "Thick Traditional Churned Sweet Yogurt",
                "img": "https://images.unsplash.com/photo-1571006682878-8378d3869255?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_4", "name": "Soft Drink (Can)", "price": 120,
                "desc": "250ml Chilled Assorted Soda",
                "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_5", "name": "Mineral Water (Large)", "price": 100,
                "desc": "1.5L Chilled Water Bottle",
                "img": "https://images.unsplash.com/photo-1548839140-29a749e1bc4c?w=600&auto=format&fit=crop&q=80"
            }
        ]
    }
]

ITEM_LOOKUP = {
    item["id"]: {**item, "category": cat["category"]}
    for cat in MENU_DATA
    for item in cat["items"]
}

# ============================================================
# KFC-INSPIRED STYLING (CSS)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@600;700;800&family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #F8F9FA;
        font-family: 'Inter', sans-serif;
    }

    .kfc-navbar {
        background-color: #FFFFFF;
        border-bottom: 2px solid #EAEAEA;
        padding: 14px 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -4rem -5rem 2rem -5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .kfc-brand {
        font-family: 'Oswald', sans-serif;
        font-size: 28px;
        font-weight: 800;
        color: #E4002B;
        letter-spacing: 1.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .kfc-pills {
        display: flex;
        gap: 12px;
    }
    .kfc-pill-active {
        background-color: #FFFFFF;
        border: 2px solid #E4002B;
        color: #E4002B;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 18px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kfc-pill-dim {
        background-color: #F1F1F1;
        border: 1px solid #E0E0E0;
        color: #666666;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 18px;
        border-radius: 4px;
        text-transform: uppercase;
    }

    .kfc-section-title {
        font-family: 'Oswald', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #111111;
        letter-spacing: 0.5px;
        margin: 25px 0 15px 0;
        border-bottom: 3px solid #E4002B;
        display: inline-block;
        padding-bottom: 4px;
    }

    .kfc-card {
        background-color: #FFFFFF;
        border: 1px solid #E8E8E8;
        border-radius: 8px;
        padding: 16px 14px 10px 14px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 8px;
        transition: transform 0.2s ease;
    }
    .kfc-card:hover {
        transform: translateY(-2px);
    }

    .kfc-stripes {
        display: flex;
        gap: 4px;
        margin-bottom: 12px;
    }
    .kfc-stripe {
        width: 6px;
        height: 18px;
        background-color: #E4002B;
        border-radius: 1px;
    }

    .kfc-title {
        font-family: 'Oswald', sans-serif;
        font-size: 19px;
        font-weight: 700;
        color: #111111;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        height: 48px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 6px;
    }

    .kfc-price-badge {
        position: absolute;
        right: 0;
        top: 65px;
        background-color: #E4002B;
        color: #FFFFFF;
        font-family: 'Oswald', sans-serif;
        font-weight: 700;
        font-size: 15px;
        padding: 4px 14px 4px 12px;
        border-radius: 4px 0 0 4px;
        box-shadow: -2px 2px 5px rgba(228, 0, 43, 0.3);
        z-index: 2;
    }

    .kfc-img-wrapper {
        width: 100%;
        height: 175px;
        overflow: hidden;
        border-radius: 6px;
        margin: 10px 0 8px 0;
        background-color: #F8F9FA;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .kfc-img-wrapper img {
        width: 100% !important;
        height: 175px !important;
        object-fit: cover !important;
        object-position: center !important;
    }

    .kfc-desc {
        font-size: 12px;
        color: #6E6E6E;
        height: 36px;
        overflow: hidden;
        line-height: 1.3;
        margin-bottom: 6px;
    }

    div.stButton > button {
        background-color: #E4002B !important;
        color: #FFFFFF !important;
        font-family: 'Oswald', sans-serif !important;
        font-size: 16px !important;
        letter-spacing: 0.8px !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 6px 12px !important;
        box-shadow: 0 2px 6px rgba(228, 0, 43, 0.25) !important;
    }
    div.stButton > button:hover {
        background-color: #C00024 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOP BRANDING NAVBAR
# ============================================================
total_cart_items = sum(st.session_state.cart.values())
cart_text = f"🛒 CART ({total_cart_items})" if total_cart_items > 0 else "🛒 CART (0)"

st.markdown(f"""
<div class="kfc-navbar">
    <div class="kfc-brand">🍗 ALFRED SHINWARI</div>
    <div class="kfc-pills">
        <span class="kfc-pill-active">🛵 DELIVERY</span>
        <span class="kfc-pill-dim">🏪 PICKUP</span>
    </div>
    <div style="font-family:'Oswald',sans-serif; font-size:16px; font-weight:700; color:#E4002B;">
        {cart_text}
    </div>
</div>
""", unsafe_allow_html=True)

tabs = st.tabs(["🔥 FULL MENU", "🛒 CART & CHECKOUT", "📍 LOCATION & CONTACT"])

# ============================================================
# HELPER ACTIONS
# ============================================================
def add_item(item_id):
    st.session_state.cart[item_id] = st.session_state.cart.get(item_id, 0) + 1
    st.toast(f"Added {ITEM_LOOKUP[item_id]['name']}! 🍗")

def remove_item(item_id):
    if item_id in st.session_state.cart:
        if st.session_state.cart[item_id] > 1:
            st.session_state.cart[item_id] -= 1
        else:
            del st.session_state.cart[item_id]

def record_order_locally(name, phone, address, cart_dict, grand_total):
    items_desc = ", ".join([f"{ITEM_LOOKUP[k]['name']} (x{qty})" for k, qty in cart_dict.items()])
    record = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Customer": [name],
        "Phone": [phone],
        "Address": [address],
        "Items": [items_desc],
        "Total": [grand_total]
    }
    df = pd.DataFrame(record)
    if not os.path.isfile(ORDERS_FILE):
        df.to_csv(ORDERS_FILE, index=False)
    else:
        df.to_csv(ORDERS_FILE, mode='a', header=False, index=False)

def push_ntfy_notification(name, phone, address, note, cart_dict, subtotal, grand_total):
    lines = [f"• {ITEM_LOOKUP[k]['name']} x {qty} = Rs. {ITEM_LOOKUP[k]['price'] * qty}" for k, qty in cart_dict.items()]
    summary_text = "\n".join(lines)
    
    body = (
        f"Customer: {name}\n"
        f"Phone: {phone}\n"
        f"Address: {address}\n"
        f"Instructions: {note if note else 'None'}\n\n"
        f"ORDER ITEMS:\n{summary_text}\n\n"
        f"Subtotal: Rs. {subtotal}\n"
        f"Delivery Fee: Rs. {DELIVERY_FEE}\n"
        f"TOTAL BILL: Rs. {grand_total}"
    )
    
    requests.post(
        "https://ntfy.sh",
        json={
            "topic": NTFY_TOPIC,
            "title": f"New Order: Rs. {grand_total} ({name})",
            "message": body,
            "priority": 5,
            "tags": ["poultry_leg", "rotating_light", "dollar"]
        },
        timeout=10
    )

# ============================================================
# TAB 1: KFC STYLE MENU
# ============================================================
with tabs[0]:
    search_query = st.text_input("Search menu", placeholder="🔍 Search Karahi, Chapli Kebab, Naan...", label_visibility="collapsed").strip().lower()

    for category_block in MENU_DATA:
        items_to_show = [
            it for it in category_block["items"]
            if not search_query or search_query in it["name"].lower() or search_query in it["desc"].lower()
        ]
        
        if not items_to_show:
            continue

        st.markdown(f'<div class="kfc-section-title">{category_block["category"]}</div>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        for idx, itm in enumerate(items_to_show):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="kfc-card">
                    <div class="kfc-stripes">
                        <div class="kfc-stripe"></div>
                        <div class="kfc-stripe"></div>
                        <div class="kfc-stripe"></div>
                    </div>
                    <div class="kfc-title">{itm['name']}</div>
                    <div class="kfc-price-badge">Rs {itm['price']:,}</div>
                    <div class="kfc-img-wrapper">
                        <img src="{itm['img']}" />
                    </div>
                    <div class="kfc-desc">{itm['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

                current_qty = st.session_state.cart.get(itm["id"], 0)
                if current_qty == 0:
                    st.button("ADD TO BUCKET 🛒", key=f"add_{itm['id']}", on_click=add_item, args=(itm["id"],), use_container_width=True)
                else:
                    b1, b2, b3 = st.columns([1, 1.2, 1])
                    with b1:
                        st.button("−", key=f"min_{itm['id']}", on_click=remove_item, args=(itm["id"],), use_container_width=True)
                    with b2:
                        st.markdown(f"<div style='text-align:center;font-family:Oswald;font-weight:700;font-size:18px;padding-top:4px;'>{current_qty}</div>", unsafe_allow_html=True)
                    with b3:
                        st.button("+", key=f"pls_{itm['id']}", on_click=add_item, args=(itm["id"],), use_container_width=True)
                st.write("")

# ============================================================
# TAB 2: CART & CHECKOUT
# ============================================================
with tabs[1]:
    st.markdown('<div class="kfc-section-title">YOUR ORDER BUCKET</div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your bucket is currently empty. Head over to the menu to add your favorite Shinwari items!")
    else:
        subtotal = 0
        for itm_id, qty in list(st.session_state.cart.items()):
            details = ITEM_LOOKUP[itm_id]
            line_total = details["price"] * qty
            subtotal += line_total
            
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.markdown(f"**{details['name']}**  \n<small style='color:#666;'>{details['desc']}</small>", unsafe_allow_html=True)
            with c2:
                st.write(f"Rs {details['price']:,} × {qty} = **Rs {line_total:,}**")
            with c3:
                if st.button("✕", key=f"del_{itm_id}"):
                    del st.session_state.cart[itm_id]
                    st.rerun()

        grand_total = subtotal + DELIVERY_FEE
        st.markdown("---")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write(f"Subtotal: **Rs {subtotal:,}**")
            st.write(f"Delivery Fee: **Rs {DELIVERY_FEE:,}**")
            st.markdown(f"### Total Payable: Rs {grand_total:,}")
        with col_s2:
            if st.button("Empty Bucket"):
                st.session_state.cart = {}
                st.rerun()
            
        st.markdown("---")
        st.markdown('<div class="kfc-section-title">DELIVERY DETAILS</div>', unsafe_allow_html=True)
        
        with st.form("kfc_checkout_form"):
            cust_name = st.text_input("Full Name *", placeholder="e.g. Tariq Khan")
            cust_phone = st.text_input("Phone Number *", placeholder="03001234567")
            cust_address = st.text_area("Complete Address *", placeholder="House/Shop #, Street, Mohallah / Ward, Chowk Azam")
            cust_notes = st.text_input("Special Cooking Request (Optional)", placeholder="Less spicy, extra lemons...")
            
            submit_btn = st.form_submit_button("PLACE ORDER NOW", use_container_width=True)
            
            if submit_btn:
                if not cust_name.strip() or not cust_phone.strip() or not cust_address.strip():
                    st.error("Please complete Name, Phone, and Delivery Address before checking out.")
                else:
                    try:
                        record_order_locally(cust_name, cust_phone, cust_address, st.session_state.cart, grand_total)
                        push_ntfy_notification(cust_name, cust_phone, cust_address, cust_notes, st.session_state.cart, subtotal, grand_total)
                        st.balloons()
                        st.success("🎉 Your order has been placed! The restaurant kitchen has received your ticket.")
                        st.session_state.cart = {}
                    except Exception as err:
                        st.error(f"Could not transmit instant alert: {err}")

# ============================================================
# TAB 3: RESTAURANT INFO
# ============================================================
with tabs[2]:
    st.markdown('<div class="kfc-section-title">VISIT ALFRED SHINWARI</div>', unsafe_allow_html=True)
    st.write("**Address:** Layyah Rd, near dessert bit, Ward No. 2, Chowk Azam")
    st.write("**Operating Hours:** Open 24 Hours • 7 Days a Week")
    st.write("**Phone Order Hotline:** 0302 6200764")
    st.link_button("🗺️ Open in Google Maps", GOOGLE_MAPS_LINK, use_container_width=True)
