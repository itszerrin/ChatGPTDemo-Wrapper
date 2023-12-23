# ChatGPTDemo-Wrapper

## Overview

ChatGPTDemo-Wrapper is a local Flask server that serves as a reverse-proxy for the site [https://chat.chatgptdemo.net](https://chat.chatgptdemo.net). The primary purpose of this project is for educational use, providing a demonstration of how to interact with the ChatGPT API. The server supports proxy configurations and allows for seamless integration into other applications.

## Features

- **Reverse Proxy:** Hosts a local server that acts as a reverse-proxy for the ChatGPT API.
- **Educational Purpose:** Designed for educational purposes to showcase API interactions and proxy support.
- **Proxy Support:** Offers the option to use proxies for enhanced privacy and security.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/) (3.9 or higher, 3.10 tested)
- Install dependencies using `pip install -r requirements.txt`

### Configuration

Modify the `assets/config.json` file to configure proxy usage:

```json
{
    "use_proxies": false
}
```

### Running the Server

Execute the following command to start the server:

```bash
python app.py
```

The server will be accessible at [http://localhost:5000](http://localhost:5000).

## API Endpoints

1. **Chat Completions**
   - **Endpoint:** `/chat/completions`
   - **Method:** `POST`
   - **Description:** Handles chat completions and supports streaming.
   - **Request Body:**
     ```json
     {
         "messages": [{"role": "user", "content": "Hello"}],
         "stream": true
     }
     ```

2. **Get Model Information**
   - **Endpoint:** `/models`
   - **Method:** `GET`
   - **Description:** Returns information about the current model available for chat.

3. **Home Page**
   - **Endpoint:** `/`
   - **Method:** `GET`
   - **Description:** Displays a simple HTML page confirming that the reverse proxy is working as expected.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Legal Notice

Please refer to [LEGAL_NOTICE](LEGAL_NOTICE) for important legal information regarding the usage of this repository.

## Contributors

- [Recentaly](https://github.com/Recentaly)

## Disclaimer

This project is for educational purposes only. Users are solely responsible for their actions and must comply with all applicable laws and regulations. The author assumes no responsibility for any consequences, damages, or losses resulting from the use or misuse of this repository.

---
<br>
<table>
  <tr>
     <td>
       <p align="center"> <img src="https://miro.medium.com/v2/resize:fit:1024/1*dEy_wxit00QBXp58H-YRRQ.png" width="90%" height="70%"></img>
    </td>
    <td> 
      <img src="https://img.shields.io/badge/MIT_LICENSE-red.svg"/> <br> 
This project is licensed under the <a href="./LICENSE">MIT license</a>.<img width=2300/>
    </td>
  </tr>
</table>
