# ytlisten

`ytlisten` is a command-line based YouTube audio player that allows you to search and play YouTube videos as audio. This is a Python application that uses the YouTube API to search for and retrieve videos and uses the VLC media player to play the audio.

## Installation

1. Install the VLC app

    ```
    # Linux
    sudo apt-get install vlc # Linux
    
    # Mac
    brew install vlc
    ```

    Before installing ytlisten, you must first install the VLC media player. You can download it from the official VLC website at https://www.videolan.org/vlc/#download. Make sure to install the version that corresponds to your operating system.

2. Get a YouTube API Key from Google:

- Go to the [Google Developers Console](https://console.developers.google.com).
- Create a new project.
- In the left sidebar, click on "APIs & Services" and then "Library".
- Search for "YouTube Data API v3" and click on it.
- Click the "Enable" button.
- In the left sidebar, click on "Credentials".
- Click the "Create credentials" button and select "API key".
- Copy the generated API key.
- In your terminal, create a new environment variable called `YT_API_KEY` and set its value to your API key:

    ```
    export YT_API_KEY="YOUR_API_KEY_HERE"
    ```

3. Install `ylisten` using pip

    ```
    pip install ylisten
    ```

## Usage

Once installed, you can use the ytlisten command to search for and play audio tracks from Youtube. Here's an example:

```
ytlisten despacito
```

This will search Youtube for the keyword "despacito" and play the audio from the first video in the search results. You can also specify a Youtube video URL directly:

```
ytlisten https://www.youtube.com/watch?v=kJQP7kiw5Fk
```

That's it! You should now be able to run ytlisten and search for and listen to YouTube videos from the command line.

## Limitations

Please note that `ytlisten` is not an official YouTube client and is not affiliated with YouTube in any way. It's a simple command-line tool that uses the YouTube Data API to search for and play YouTube videos as audio files.

Also, keep in mind that the YouTube Data API has certain usage limits and quota restrictions. If you exceed these limits, your API key may be temporarily or permanently blocked by Google. Please refer to the official documentation for more information.

## Contributions / Development

Contributions are welcome!

```
python setup.py sdist bdist_wheel
twine upload dist/*
```

## License

[MIT License](LICENSE.md)