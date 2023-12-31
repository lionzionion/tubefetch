import streamlit as st
from pytube import YouTube
import requests
from tqdm import tqdm

def download_youtube_video(url, download_path="."):
    try:
        st.info("Downloading...")

        # Get video stream
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        # Get video size for progress bar
        video_size = video.filesize
        block_size = 1024  # 1 Kibibyte

        # Create progress bar
        progress_bar = st.progress(0)

        # Download the video with progress bar
        response = requests.get(video.url, stream=True)
        with open(f"{download_path}/{yt.title}.mp4", 'wb') as f, tqdm(
                desc=yt.title,
                total=video_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=block_size):
                f.write(data)
                bar.update(len(data))
                progress_bar.progress(bar.n / video_size)

        st.success("Download completed!")
        st.balloons()
    except Exception as e:
        st.error(f"An error occurred: {e}")

def main():
    # Set background color of the entire app to black
    st.markdown("""
        <style>
            body {
                background-color: black;
                color: white;  /* Set text color to white for better visibility */
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("YouTube Video Downloader")

    # Get YouTube video URL from user
    url = st.text_input("Enter YouTube video URL:")

    if st.button("Download"):
        download_youtube_video(url)

    # Set red frame around names
    st.markdown("""
        <style>
            .css-1q2q54k {
                border: 2px solid red;
                padding: 8px;
                margin: 8px 0;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

