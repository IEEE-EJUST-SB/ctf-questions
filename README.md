# IEEE EJSUT DEV STORM CTF

Welcome to the official repository for the **IEEE EJSUT DEV STORM** Capture The Flag (CTF) competition. This repository contains the source code and deployment files for the challenges hosted during the event.

## About the Competition

The DEV STORM CTF was designed to test participants' skills in various cybersecurity domains, including Web Exploitation, Cryptography, and Digital Forensics. The challenges range from beginner to advanced levels.

## Challenges

### Web Exploitation
*   **cashpuzzle**
*   **jwtf**
*   **legal_snacks**
*   **todo**
*   **workerdb**
*   **command**
*   **sqli**
*   **ssrf**
*   **inspect**

### Cryptography
*   **breakme**
*   **Pure Randomness**
*   **UAE Cipher-Crypto**
*   **elementary**
*   **lottery**
*   **cipher**
*   **rsa**

### Forensics
*   **Algorithm**
*   **Disk**
*   **Hex**

## Repository Structure

The challenges are organized by category. Each challenge directory typically contains:
*   Source code
*   `Dockerfile` and `docker-compose.yaml` (for containerized challenges)
*   Solution scripts or flags (where applicable)

```
.
├── Crypto/
├── Web/
└── Forensics/
```

## Credits

*   **Challenge Authors**: Created by Shehab Mohamed Gamal and Mohamed Yasser for IEEE EJSUT.
*   **External Challenges**: This repository also includes challenges sourced from the [ctf-archives](https://github.com/sajjadium/ctf-archives) which were hosted as part of the competition.

## Running the Challenges

Most web challenges are dockerized. To run a challenge locally:

1.  Navigate to the challenge directory (e.g., `Web/sqli`).
2.  Run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
3.  Access the challenge via the port specified in the `docker-compose.yaml` file.
# ctf-questions
