#!/usr/bin/env python3
"""
Image Color Palette Generator
=============================

A tiny Streamlit web app that lets users upload an image and instantly
extract the 10 most dominant colours (in HEX). Inspired by
https://flatuicolors.com and day 76 of 100 Days of Code.

How to run
----------

1.  Make sure you have Python 3.9+.
2.  Install the dependencies once:

    pip install streamlit pillow scikit-learn numpy

3.  Save this file as **main.py**.
4.  Start the app:

    streamlit run main.py

Visit the local URL Streamlit prints (usually http://localhost:8501).

"""
import io
from typing import List, Tuple

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
import streamlit as st


# ---------- Utility helpers -------------------------------------------------
def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Convert an (R, G, B) tuple (0-255 each) to a HEX string, e.g. #1A2B3C."""
    return '#{:02X}{:02X}{:02X}'.format(*map(int, rgb))


def extract_palette(img: Image.Image, k: int = 10) -> List[str]:
    """
    Down-sample *img* and run k-means to find *k* dominant colours.

    Returns a list of HEX strings, ordered by cluster weight (largest first).
    """
    # Resize big pictures to speed things up (keep aspect ratio).
    max_pixels = 160_000  # ~400×400px
    scale = (max_pixels / (img.width * img.height)) ** 0.5
    if scale < 1:
        img = img.resize((int(img.width * scale), int(img.height * scale)))

    pixels = np.array(img.convert('RGB')).reshape(-1, 3)

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init='auto',  # silence futurewarning in scikit-learn ≥1.5
    ).fit(pixels)

    counts = np.bincount(kmeans.labels_)
    order = np.argsort(counts)[::-1]          # most common first
    centres = kmeans.cluster_centers_[order]  # shape (k, 3)

    return [rgb_to_hex(c) for c in centres]


def palette_strip(hex_codes: List[str], block_px: int = 60) -> Image.Image:
    """
    Build a horizontal PIL image showing one block per colour in *hex_codes*.
    """
    strip = Image.new('RGB', (block_px * len(hex_codes), block_px))
    for i, h in enumerate(hex_codes):
        strip.paste(h, box=(i * block_px, 0, (i + 1) * block_px, block_px))
    return strip


# ---------- Streamlit UI ----------------------------------------------------
st.set_page_config(page_title='Image Colour Palette Generator', page_icon='🎨')

st.title('🎨 Image Colour Palette Generator')
st.caption('Upload a photo and get its 10 dominant colours in HEX.')

file = st.file_uploader(
    'Choose an image',
    type=('png', 'jpg', 'jpeg', 'webp', 'bmp', 'tiff')
)

if file:
    image = Image.open(io.BytesIO(file.read()))
    st.image(image, caption='Uploaded image', use_container_width=True)

    with st.spinner('Crunching the pixels...'):
        palette = extract_palette(image, k=10)

    st.subheader('Dominant Colours')
    # Display as 2 rows of 5 blocks for a tidy layout
    cols = st.columns(5)
    for i, hex_code in enumerate(palette):
        with cols[i % 5]:
            st.markdown(
                f"""
                <div style="width:100%;height:80px;border-radius:6px;
                            background:{hex_code};border:1px solid #ccc"></div>
                <p style="text-align:center;font-weight:bold;
                          margin-top:0.3em">{hex_code}</p>
                """,
                unsafe_allow_html=True
            )

    # Show a single horizontal strip as a quick preview
    st.image(palette_strip(palette), caption='Palette preview', use_container_width=True)

    # Allow downloading the palette as a plain-text file
    st.download_button(
        label='Download HEX list',
        data='\n'.join(palette),
        file_name='palette.txt',
        mime='text/plain'
    )
else:
    st.info('⬆️ Drag and drop an image (or click) to begin.')
