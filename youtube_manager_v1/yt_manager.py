import json


def load_data():
    try:
        with open('youtubeList.txt', 'r') as file:
            videos = json.load(file)
            return videos
    except FileNotFoundError:
        return []


def list_all_videos(videos):
    print("\n")
    print("*" * 35)
    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video['name']}, Duration : {video['time']}")
    print("*" * 35)


def add_video(videos):
    name = input("Enter the new video title : ")
    time = input("Enter the new video time : ")
    videos.append({'name': name, 'time': time})
    save_default(videos)


def update_video(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number you wish to update : "))

    if 1 <= index <= len(videos):
        name = input("Enter the new video title : ")
        time = input("Enter the new video time : ")
        videos[index-1] = {'name': name, 'time': time}
        save_default(videos)
    else:
        print("Please enter valid video number!!")


def delete_video(videos):
    list_all_videos(videos)
    index = int(input("Enter the video number you wish to update : "))

    if 1 <= index <= len(videos):
        del videos[index - 1]
        save_default(videos)
    else:
        print("Please enter valid video number!!")


def save_default(videos):
    with open("youtubeList.txt", "w") as file:
        json.dump(videos, file)


def main():
    videos = load_data()
    while True:

        print("****** YOUTUBE MANAGER ******")
        print("1. List all youtube videos")
        print("2. Add a youtube video")
        print("3. Update a youtube video")
        print("4. Delete a youtube video")
        print("5. Exit")
        print("\n")
        choice = input("Enter Your Choice : ")

        match choice:
            case '1':
                list_all_videos(videos)
            case '2':
                add_video(videos)
            case '3':
                update_video(videos)
            case '4':
                delete_video(videos)
            case '5':
                break
            case _:
                print("Invalid Choice : ")


if __name__ == "__main__":
    main()
