# DNS Server and Client Application

This application is a simple DNS server and client implemented in Python. The server responds to DNS queries with predefined DNS records, and the client sends DNS queries to the server and logs the responses.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/bantoinese83/DNS_Server_-and_Client_Application.git
    ```
2. Navigate to the project directory:
    ```bash
    cd yourrepository
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the DNS server and client, run the following command:

```bash
python app.py
```

The server will start listening for DNS queries on port 53, and the client will send DNS queries to the server and log the responses.

### Server Options

The server supports the following options:

- `--mode`: The mode in which the server should run. The available modes are `on-demand` and `continuous`. In `on-demand` mode, the server will respond to a fixed number of queries specified by the `--queries` option. In `continuous` mode, the server will respond to queries indefinitely. The default mode is `continuous`.
```bash
python app.py --mode on-demand --queries 10 
```
or
```bash
python app.py --mode continuous
```
## Contributing
Contributions are welcome! Please feel free to submit a pull request if you have any improvements or new features to add.


