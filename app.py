import streamlit as st
import pandas as pd
import os
from urllib.parse import quote
from datetime import datetime

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="Alfred Shanwari & Restaurant", page_icon="🍖", layout="wide")

# Owner's WhatsApp Number (Alfred Shanwari's actual number)
OWNER_WHATSAPP = "923317096731" 
ORDERS_FILE = "orders.csv"

# Initialize Session State for Cart
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- SHANWARI MENU DATABASE ---
MENU = {
    "Karahi (Desi Ghee & Fresh Meat)": [
        {"name": "Mutton Shanwari Karahi (1kg)", "price": 2800, "img": "https://images.unsplash.com/photo-1606471191009-63994c53433b?w=500&q=80"},
        {"name": "Chicken Namkeen Karahi (1kg)", "price": 1500, "img": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=500&q=80"}
    ],
    "BBQ & Grill": [
        {"name": "Beef Chapli Kebab (per piece)", "price": 250, "img": "https://images.unsplash.com/photo-1625938146369-adc83368bda7?w=500&q=80"},
        {"name": "Chicken Tikka Boti", "price": 600, "img": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=500&q=80"}
    ],
    "Rice & Drinks": [
        {"name": "Kabuli Pulao", "price": 850, "img": "https://images.unsplash.com/photo-1574484284002-952d92456975?w=500&q=80"},
        {"name": "Traditional Green Tea (Kahwa)", "price": 100, "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=500&q=80"}
    ]
}

# --- HELPER FUNCTIONS ---
def add_to_cart(item_name, item_price):
    st.session_state.cart.append({"name": item_name, "price": item_price})
    st.toast(f"Added {item_name} to cart! 🛒")

def clear_cart():
    st.session_state.cart = []

def save_order(name, phone, address, cart_items, total):
    order_data = {
        "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Customer Name": [name],
        "Phone": [phone],
        "Address": [address],
        "Items": [", ".join([item['name'] for item in cart_items])],
        "Total Amount": [total]
    }
    df = pd.DataFrame(order_data)
    if not os.path.isfile(ORDERS_FILE):
        df.to_csv(ORDERS_FILE, index=False)
    else:
        df.to_csv(ORDERS_FILE, mode='a', header=False, index=False)

# --- UI COMPONENTS ---
def render_header():
    st.markdown("""
        <div style='text-align: center; padding: 2.5rem 0; background-color: #8B0000; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin:0;'>🍖 Alfred Shanwari & Restaurant</h1>
            <p style='color: white; font-size: 1.2rem;'>Authentic Taste, Fresh Meat, and Traditional Spices</p>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN APP ROUTING ---
render_header()

# Navigation
tabs = st.tabs(["🏠 Home", "📖 Full Menu", "🛒 Cart & Checkout"])

# 1. HOME TAB
with tabs[0]:
    st.image("https://images.unsplash.com/photo-1555126634-323283e090fa?w=1200&q=80", use_container_width=True, caption="Experience the best traditional dining in Chowk Azam.")
    
    st.subheader("🌟 Signature Dishes")
    cols = st.columns(3)
    featured_items = [MENU["Karahi (Desi Ghee & Fresh Meat)"][0], MENU["BBQ & Grill"][0], MENU["Rice & Drinks"][0]]
    
    for i, col in enumerate(cols):
        with col:
            item = featured_items[i]
            st.image(item["img"], use_container_width=True)
            st.write(f"**{item['name']}**")
            st.write(f"Rs. {item['price']}")
            st.button("Add to Cart", key=f"feat_{i}", on_click=add_to_cart, args=(item["name"], item["price"]))

    st.markdown("---")
    st.subheader("📍 About Us & Contact")
    st.write("We bring you the authentic taste of Shanwari cuisine right in Chowk Azam. Known for our fresh meat, late-night food, and famous green tea, we provide the perfect atmosphere for families and friends.")
    st.write("**Address:** Layyah Rd, near dessert bit, Ward No. 2 Chowk Azam")
    st.write("**Hours:** Open 24 Hours (Mon-Sun)")
    st.write("**Phone:** 0302 6200764")

# 2. FULL MENU TAB
with tabs[1]:
    st.header("Explore Our Menu")
    for category, items in MENU.items():
        st.subheader(category)
        item_cols = st.columns(len(items))
        for i, col in enumerate(item_cols):
            with col:
                item = items[i]
                st.image(item["img"], use_container_width=True)
                st.write(f"**{item['name']}**")
                st.write(f"Rs. {item['price']}")
                st.button("Add to Cart", key=f"menu_{category}_{i}", on_click=add_to_cart, args=(item["name"], item["price"]))
        st.markdown("---")

# 3. CART & CHECKOUT TAB
with tabs[2]:
    st.header("🛒 Your Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is currently empty. Head over to the menu to order your favorite Karahi!")
    else:
        total_price = 0
        for i, item in enumerate(st.session_state.cart):
            st.write(f"{i+1}. {item['name']} - **Rs. {item['price']}**")
            total_price += item["price"]
            
        st.markdown(f"### Total Bill: Rs. {total_price}")
        st.button("Clear Cart", on_click=clear_cart)
        
        st.markdown("---")
        st.subheader("Checkout Details")
        
        with st.form("checkout_form"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            address = st.text_area("Delivery Address (Chowk Azam & Surrounding)")
            
            submit_order = st.form_submit_button("Place Order via WhatsApp")
            
            if submit_order:
                if name and phone and address:
                    # Save data to CSV
                    save_order(name, phone, address, st.session_state.cart, total_price)
                    
                    # Format WhatsApp Message
                    order_summary = "\n".join([f"- {item['name']}" for item in st.session_state.cart])
                    msg = f"*New Online Order!* 🍖\n\n*Customer:* {name}\n*Phone:* {phone}\n*Address:* {address}\n\n*Items Ordered:*\n{order_summary}\n\n*Total Bill:* Rs. {total_price}"
                    wa_link = f"https://wa.me/{OWNER_WHATSAPP}?text={quote(msg)}"
                    
                    # Success State
                    st.success("Order processed successfully!")
                    st.markdown(f"### 👉 **[CLICK HERE TO SEND ORDER VIA WHATSAPP]({wa_link})**")
                    
                    # Clear cart
                    st.session_state.cart = []
                else:
                    st.error("Please fill in your Name, Phone, and Address.")
