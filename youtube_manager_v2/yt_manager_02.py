import json
from pytube import YouTube

# Function to get video details


def get_video_details(url):
    try:
        yt = YouTube(url)
        return yt.title, yt.author, yt.length, yt.views
    except Exception as e:
        print("An error occurred while fetching video details:", e)
        return None, None, None, None

# Function to load video data from file


def load_data():
    try:
        with open('youtubeList.txt', 'r') as file:
            videos = json.load(file)
            for video in videos:
                if 'url' in video:
                    try:
                        title, author, duration, views = get_video_details(
                            video['url'])
                        video['name'] = title
                        video['author'] = author
                        video['time'] = duration
                        video['views'] = views
                    except Exception as e:
                        print(f"An error occurred while loading video details for {
                              video['url']}: {e}")
                        video['name'] = "Not Available"
                        video['author'] = "Not Available"
                        video['time'] = "Not Available"
                        video['views'] = "Not Available"
                else:
                    print("URL not found for a video entry.")
            return videos
    except FileNotFoundError:
        return []

# Function to list all videos


def list_all_videos(videos):
    print("\n{:<5} {:<50} {:<30} {:<20} {:<10}".format(
        "ID", "Title", "Channel", "Duration", "Views"))
    print("-" * 115)
    for index, video in enumerate(videos, start=1):
        hours = video['time'] // 3600
        minutes = (video['time'] % 3600) // 60
        seconds = video['time'] % 60
        duration = f"{hours}h {minutes}m {seconds}s"
        print("{:<5} {:<50} {:<30} {:<20} {:<10}".format(
            index, video['name'], video['author'], duration, video['views']))
    print("-" * 115)

# Function to add a video


def add_video(videos):
    url = input("Enter the YouTube URL: ")
    try:
        title, author, duration, views = get_video_details(url)
        videos.append({'name': title, 'author': author,
                      'time': duration, 'views': views, 'url': url})
        save_default(videos)
        print("Video added successfully.")
    except Exception as e:
        print("An error occurred:", e)

# Function to update a video


def update_video(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number you wish to update: "))
    if 1 <= index <= len(videos):
        url = input("Enter the new YouTube URL: ")
        try:
            title, author, duration, views = get_video_details(url)
            videos[index-1] = {'name': title, 'author': author,
                               'time': duration, 'views': views, 'url': url}
            save_default(videos)
            print("Video updated successfully.")
        except Exception as e:
            print("An error occurred:", e)
    else:
        print("Please enter a valid video number!")

# Function to delete a video


def delete_video(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number you wish to delete: "))
    if 1 <= index <= len(videos):
        del videos[index - 1]
        save_default(videos)
        print("Video deleted successfully.")
    else:
        print("Please enter a valid video number!")

# Function to save video data to file


def save_default(videos):
    with open("youtubeList.txt", "w") as file:
        json.dump(videos, file)

# Main function


def main():
    videos = load_data()
    while True:
        print("\n****** YOUTUBE MANAGER ******")
        print("1. List all YouTube videos")
        print("2. Add a YouTube video")
        print("3. Update a YouTube video")
        print("4. Delete a YouTube video")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            list_all_videos(videos)
        elif choice == '2':
            add_video(videos)
        elif choice == '3':
            update_video(videos)
        elif choice == '4':
            delete_video(videos)
        elif choice == '5':
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
