import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

# ============================================================
# APP & RESTAURANT CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Alfred Shanwari & Restaurant",
    page_icon="🍖",
    layout="wide"
)

# Put the exact topic you subscribed to in the ntfy mobile app here:
NTFY_TOPIC = "alfred_orders_chowk99" 
ORDERS_FILE = "orders.csv"
GOOGLE_MAPS_LINK = "https://maps.app.goo.gl/hBRGvxccnKNYkEAAA"
DELIVERY_FEE = 150

# Initialize Cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ============================================================
# COMPREHENSIVE MENU
# ============================================================
MENU_DATA = [
    {
        "category": "🍗 Shinwari & Karahi Specials",
        "items": [
            {
                "id": "sk_1",
                "name": "Special Mutton Shinwari Karahi",
                "price": 2900,
                "portion": "1 KG (Fresh Meat & Desi Ghee)",
                "img": "https://images.unsplash.com/photo-1606471191009-63994c53433b?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_2",
                "name": "Chicken Namkeen Shinwari",
                "price": 1600,
                "portion": "1 KG (Salt & Tomato Gravy)",
                "img": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_3",
                "name": "Chicken White Karahi",
                "price": 1750,
                "portion": "1 KG (Creamy Yogurt Base)",
                "img": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "sk_4",
                "name": "Half Mutton Karahi",
                "price": 1550,
                "portion": "0.5 KG (Cooked to Order)",
                "img": "https://images.unsplash.com/photo-1545247181-516773cae754?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "🔥 Charcoal BBQ & Grills",
        "items": [
            {
                "id": "bbq_1",
                "name": "Peshawari Chapli Kebab",
                "price": 320,
                "portion": "1 Large Piece (Tender Beef)",
                "img": "https://images.unsplash.com/photo-1625938146369-adc83368bda7?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_2",
                "name": "Chicken Malai Boti",
                "price": 650,
                "portion": "8 Succulent Melt-in-Mouth Skewers",
                "img": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_3",
                "name": "Mutton Tikka Boti",
                "price": 950,
                "portion": "Charcoal Smoked Spicy Cubes",
                "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bbq_4",
                "name": "Beef Seekh Kebab",
                "price": 550,
                "portion": "4 Seasoned Minced Skewers",
                "img": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "🍚 Rice & Tandoor",
        "items": [
            {
                "id": "rt_1",
                "name": "Peshawari Kabuli Pulao",
                "price": 850,
                "portion": "With Braised Meat, Raisins & Carrots",
                "img": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_2",
                "name": "Special Chicken Biryani",
                "price": 450,
                "portion": "Aromatic Spiced Basmati Rice",
                "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_3",
                "name": "Special Roghani Naan",
                "price": 70,
                "portion": "Sesame & Pure Butter Glaze",
                "img": "https://images.unsplash.com/photo-1626074353765-517a681e40be?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "rt_4",
                "name": "Tandoori Sada Roti",
                "price": 25,
                "portion": "Fresh Whole Wheat Flatbread",
                "img": "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=600&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "category": "☕ Traditional Beverages",
        "items": [
            {
                "id": "bv_1",
                "name": "Peshawari Qahwa (Kahwa)",
                "price": 100,
                "portion": "Cardamom & Saffron Green Tea",
                "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_2",
                "name": "Fresh Mint Margarita",
                "price": 250,
                "portion": "Chilled Mint & Lemon Cooler",
                "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_3",
                "name": "Sweet Meethi Lassi",
                "price": 180,
                "portion": "Thick Traditional Churned Yogurt",
                "img": "https://images.unsplash.com/photo-1571006682878-8378d3869255?w=600&auto=format&fit=crop&q=80"
            },
            {
                "id": "bv_4",
                "name": "Soft Drink (Can)",
                "price": 120,
                "portion": "250ml Chilled",
                "img": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&auto=format&fit=crop&q=80"
            }
        ]
    }
]

# Quick ID Lookup map
ITEM_LOOKUP = {
    item["id"]: {**item, "category": cat["category"]}
    for cat in MENU_DATA
    for item in cat["items"]
}

# ============================================================
# UNIFORM CARD STYLING & COMPACT BANNER CSS
# ============================================================
st.markdown("""
<style>
    /* Compact Banner Styling */
    .hero-banner {
        position: relative;
        height: 220px;
        border-radius: 14px;
        background-image: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.65)), url('https://images.unsplash.com/photo-1555126634-323283e090fa?w=1200&auto=format&fit=crop&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        padding: 15px;
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-size: 32px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .hero-banner p {
        color: #F0F0F0;
        font-size: 15px;
        margin: 6px 0 0 0;
    }

    /* Fixed Card Height & Unified Area */
    .menu-card {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.03);
    }
    .menu-card-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .menu-card-title {
        font-size: 16px;
        font-weight: 700;
        color: #1E1E1E;
        height: 42px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        line-height: 1.3;
    }
    .menu-card-portion {
        font-size: 12px;
        color: #777777;
        height: 32px;
        overflow: hidden;
        margin-top: 4px;
    }
    .menu-card-price {
        font-size: 16px;
        font-weight: 800;
        color: #8B0000;
        margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_item(item_id):
    st.session_state.cart[item_id] = st.session_state.cart.get(item_id, 0) + 1
    st.toast(f"Added {ITEM_LOOKUP[item_id]['name']} to cart! 🛒")

def remove_item(item_id):
    if item_id in st.session_state.cart:
        if st.session_state.cart[item_id] > 1:
            st.session_state.cart[item_id] -= 1
        else:
            del st.session_state.cart[item_id]

def clear_entire_cart():
    st.session_state.cart = {}

def record_order_locally(name, phone, address, cart_dict, grand_total):
    items_desc = ", ".join([
        f"{ITEM_LOOKUP[k]['name']} (x{qty})" 
        for k, qty in cart_dict.items()
    ])
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
        f"👤 Customer: {name}\n"
        f"📞 Phone: {phone}\n"
        f"📍 Address: {address}\n"
        f"📝 Instructions: {note if note else 'None'}\n\n"
        f"🍽️ ORDER ITEMS:\n{summary_text}\n\n"
        f"Subtotal: Rs. {subtotal}\n"
        f"Delivery Fee: Rs. {DELIVERY_FEE}\n"
        f"💰 TOTAL BILL: Rs. {grand_total}"
    )
    
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        data=body.encode("utf-8"),
        headers={
            "Title": f"🚨 NEW ORDER: Rs. {grand_total} ({name})",
            "Priority": "urgent",
            "Tags": "meat_on_bone,bell,dollar"
        },
        timeout=8
    )

# ============================================================
# COMPACT BANNER (REPLACES GIANT IMAGE)
# ============================================================
st.markdown("""
<div class="hero-banner">
    <h1>🍖 Alfred Shanwari & Restaurant</h1>
    <p>Authentic Shinwari Karahi, Fresh Charcoal BBQ & Traditional Kahwa • Chowk Azam</p>
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tabs = st.tabs(["📖 Full Menu", "🛒 Cart & Checkout", "📍 Restaurant Location"])

# ============================================================
# TAB 1: MENU WITH UNIFORM SIZED CARDS
# ============================================================
with tabs[0]:
    search_query = st.text_input("🔍 Quick Search Menu", placeholder="Search Karahi, Chapli Kebab, Naan...").strip().lower()

    for category_block in MENU_DATA:
        # Filter items by search
        filtered_items = [
            it for it in category_block["items"]
            if not search_query or search_query in it["name"].lower() or search_query in it["portion"].lower()
        ]
        
        if not filtered_items:
            continue

        st.subheader(category_block["category"])
        
        # Display cards in a rigid 4-column grid
        cols = st.columns(4)
        for idx, itm in enumerate(filtered_items):
            current_col = cols[idx % 4]
            with current_col:
                # Custom uniform HTML Card with fixed height & cover images
                st.markdown(f"""
                <div class="menu-card">
                    <img class="menu-card-img" src="{itm['img']}" />
                    <div class="menu-card-title">{itm['name']}</div>
                    <div class="menu-card-portion">{itm['portion']}</div>
                    <div class="menu-card-price">Rs. {itm['price']:,}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic Add/Quantity buttons
                current_qty = st.session_state.cart.get(itm["id"], 0)
                if current_qty == 0:
                    st.button("Add to Cart 🛒", key=f"add_{itm['id']}", on_click=add_item, args=(itm["id"],), use_container_width=True)
                else:
                    b1, b2, b3 = st.columns([1, 1.2, 1])
                    with b1:
                        st.button("−", key=f"min_{itm['id']}", on_click=remove_item, args=(itm["id"],), use_container_width=True)
                    with b2:
                        st.markdown(f"<div style='text-align:center;font-weight:700;padding-top:6px;'>{current_qty}</div>", unsafe_allow_html=True)
                    with b3:
                        st.button("+", key=f"pls_{itm['id']}", on_click=add_item, args=(itm["id"],), use_container_width=True)
                
                st.write("") # Margin spacing

# ============================================================
# TAB 2: CART & NTFY CHECKOUT
# ============================================================
with tabs[1]:
    st.subheader("🛒 Current Order Details")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Click '+ Add to Cart' on any dish in the menu to begin.")
    else:
        # Table of items
        subtotal = 0
        for itm_id, qty in list(st.session_state.cart.items()):
            details = ITEM_LOOKUP[itm_id]
            line_total = details["price"] * qty
            subtotal += line_total
            
            c1, c2, c3 = st.columns([4, 2, 1])
            with c1:
                st.markdown(f"**{details['name']}**  \n<small>{details['portion']}</small>", unsafe_allow_html=True)
            with c2:
                st.write(f"Rs. {details['price']} × {qty} = **Rs. {line_total}**")
            with c3:
                if st.button("✕", key=f"del_{itm_id}"):
                    del st.session_state.cart[itm_id]
                    st.rerun()

        grand_total = subtotal + DELIVERY_FEE
        st.markdown("---")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write(f"Subtotal: **Rs. {subtotal}**")
            st.write(f"Delivery Charge: **Rs. {DELIVERY_FEE}**")
            st.markdown(f"### Grand Total: Rs. {grand_total}")
        with col_s2:
            st.button("Clear Entire Cart", on_click=clear_entire_cart)
            
        st.markdown("---")
        st.subheader("📦 Delivery Information")
        
        with st.form("ntfy_order_form"):
            cust_name = st.text_input("Full Name *", placeholder="e.g., Muhammad Ali")
            cust_phone = st.text_input("Phone Number *", placeholder="03001234567")
            cust_address = st.text_area("Complete Address *", placeholder="House/Shop #, Street, Mohallah / Ward, Chowk Azam")
            cust_notes = st.text_input("Special Cooking Request (Optional)", placeholder="Less spicy, extra lemons, soft naan...")
            
            submit_btn = st.form_submit_button("Confirm & Place Order", type="primary", use_container_width=True)
            
            if submit_btn:
                if not cust_name.strip() or not cust_phone.strip() or not cust_address.strip():
                    st.error("Please complete Name, Phone, and Delivery Address before checking out.")
                else:
                    try:
                        # 1. Store order to disk
                        record_order_locally(cust_name, cust_phone, cust_address, st.session_state.cart, grand_total)
                        
                        # 2. Transmit instant alert straight to owner's ntfy app
                        push_ntfy_notification(cust_name, cust_phone, cust_address, cust_notes, st.session_state.cart, subtotal, grand_total)
                        
                        # 3. Present confirmation to client
                        st.balloons()
                        st.success("🎉 Your order has been placed successfully! The kitchen has received your details and is preparing your food.")
                        clear_entire_cart()
                    except Exception as err:
                        st.error(f"Could not dispatch instant push notification: {err}")

# ============================================================
# TAB 3: LOCATION & CONTACT
# ============================================================
with tabs[2]:
    st.subheader("📍 Alfred Shanwari & Restaurant")
    st.write("**Address:** Layyah Rd, near dessert bit, Ward No. 2, Chowk Azam")
    st.write("**Hours:** Open 24 Hours • 7 Days a Week")
    st.write("**Call & Support:** 0320 4335045")
    st.link_button("🗺️ Open Google Maps Directions", GOOGLE_MAPS_LINK, use_container_width=True)
