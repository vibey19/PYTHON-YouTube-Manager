import sqlite3
from pytube import YouTube

conn = sqlite3.connect('youtube_videos.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               channel TEXT NOT NULL,
               duration TEXT NOT NULL,
               views INTEGER NOT NULL,
               UNIQUE(title, channel)
    )
''')


def get_video_details(url):
    try:
        yt = YouTube(url)
        return yt.title, yt.author, yt.length, yt.views
    except Exception as e:
        print("An error occurred while fetching video details:", e)
        return None, None, None, None


def list_videos():
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()
    if not videos:
        print("No videos found in the database.")
    else:
        print("\n{:<5} {:<50} {:<30} {:<15} {:<10}".format(
            "ID", "Title", "Channel", "Duration", "Views"))
        print("-" * 110)
        for video in videos:
            hours = int(video[3]) // 3600
            remaining_seconds = int(video[3]) % 3600
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            print("{:<5} {:<50} {:<30} {:<15} {:<10}".format(
                video[0], video[1], video[2], duration, video[4]))
        print("-" * 110)


def add_video(url):
    title, channel, duration, views = get_video_details(url)
    cursor.execute("INSERT OR IGNORE INTO videos (title, channel, duration, views) VALUES (?, ?, ?, ?)",
                   (title, channel, duration, views))
    conn.commit()
    print("Video added successfully.")


def update_video(video_id, new_url):
    title, channel, duration, views = get_video_details(new_url)
    cursor.execute("UPDATE videos SET title = ?, channel = ?, duration = ?, views = ? WHERE id = ?",
                   (title, channel, duration, views, video_id))
    conn.commit()
    print("Video updated successfully.")


def delete_video(video_id):
    cursor.execute("DELETE FROM videos where id = ?", (video_id,))
    conn.commit()
    print("Video deleted successfully.")


def main():
    while True:
        print("\n ******* YouTube Manager App *******")
        print("1. List Videos")
        print("2. Add Video")
        print("3. Update Video")
        print("4. Delete Video")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_videos()
        elif choice == '2':
            url = input("Enter the YouTube video URL: ")
            add_video(url)
        elif choice == '3':
            video_id = input("Enter video ID to update: ")
            new_url = input("Enter the new YouTube video URL: ")
            update_video(video_id, new_url)
        elif choice == '4':
            video_id = input("Enter video ID to delete: ")
            delete_video(video_id)
        elif choice == '5':
            break
        else:
            print("Invalid Choice ")

    conn.close()


if __name__ == "__main__":
    main()
