import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trailer Optimization Tool", layout="centered")

st.title("Trailer Optimization Tool")
st.write("Calculate the best trailer size (53', 48', or 45') based on your freight load.")

# Trailer dimensions (in feet)
trailers = {
    "53' Trailer": {"length": 53, "width": 8.5, "height": 9},
    "48' Trailer": {"length": 48, "width": 8.5, "height": 9},
    "45' Trailer": {"length": 45, "width": 8.5, "height": 9},
}

# Convert to cubic feet
for t in trailers:
    trailers[t]["volume"] = (
        trailers[t]["length"] * trailers[t]["width"] * trailers[t]["height"]
    )

st.subheader("Freight Information")

num_pallets = st.number_input("Number of Pallets", min_value=0, step=1)
pallet_length = st.number_input("Pallet Length (inches)", min_value=1, value=48)
pallet_width = st.number_input("Pallet Width (inches)", min_value=1, value=40)
pallet_height = st.number_input("Pallet Height (inches)", min_value=1, value=60)

# Convert pallet size to cubic feet
pallet_volume = (pallet_length / 12) * (pallet_width / 12) * (pallet_height / 12)
total_freight_volume = pallet_volume * num_pallets

st.write(f"**Total Freight Volume:** {total_freight_volume:.2f} cubic feet")

# Calculate load percentages
results = []
for name, data in trailers.items():
    load_pct = (total_freight_volume / data["volume"]) * 100
    results.append([name, data["volume"], load_pct])

df = pd.DataFrame(results, columns=["Trailer", "Volume (cu ft)", "Load %"])

st.subheader("Trailer Load Comparison")
st.dataframe(df.style.format({"Volume (cu ft)": "{:.0f}", "Load %": "{:.2f}%"}))

# Recommendation
best_fit = df[df["Load %"] <= 100].sort_values("Load %").head(1)

st.subheader("Recommendation")

if best_fit.empty:
    st.error("Freight does NOT fit in any trailer size.")
else:
    trailer_name = best_fit.iloc[0]["Trailer"]
    load_pct = best_fit.iloc[0]["Load %"]
    st.success(f"Best Trailer: **{trailer_name}** ({load_pct:.2f}% full)")
