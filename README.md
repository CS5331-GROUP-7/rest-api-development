# rest-api-development

CS5331 Assignment 1 Project Reference Repository

## Instructions

Your objective is to implement a web application that provides the endpoints
specified here: https://cs5331-assignments.github.io/rest-api-development/.

The project has been packaged in an easy to set-up docker container with the
skeleton code implemented in Python Flask. You are not restricted in terms of
which language, web stack, or database you desire to use. However, please note
that very limited support can be given to those who decide to veer off the
beaten path.

You may be required to modify the following files/directories:

- Dockerfile - contains the environment setup scripts to ensure a homogenous
  development environment
- src/ - contains the front-end code in `html` and the skeleton Flask API code
  in `service`
- img/ - contains images used for this README

Assuming you're developing on an Ubuntu 16.04 machine, the quick instructions
to get up and running are:

```
# Install Docker

sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce

# Verify Docker Works

sudo docker run hello-world

# Run the skeleton implementation

sudo ./run.sh
```

(Docker CE installation instructions are from this
[link](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository).)

**Please consult your assignment hand-out for detailed setup information.**

## Grading

The implementation will be graded in an automated fashion on an Ubuntu 16.04
virtual machine by building the docker container found in your repository and
running it. The grading script will interact with your API.

The following ports are expected to be accessible:

1. 80, on which static HTML content, including the front-end, is served.
2. 8080, on which the API is exposed.

To verify this, please run the following commands:

```
sudo ./run.sh
```

On a different window:

```
curl http://localhost:80
curl http://localhost:8080
```

If a response is received, you're good to go.

**Please replace the details below with information relevant to your team.**

## Screenshots

Please replace the example screenshots with screenshots of your completed
project. Feel free to include more than one.

![Sample Screenshot](./img/samplescreenshot.png)

## Administration and Evaluation

Please fill out this section with details relevant to your team.

### Team Members

1. Member 1 Name
2. Member 2 Name
3. Member 3 Name
4. Member 4 Name

### Short Answer Questions

#### Question 1: Briefly describe the web technology stack used in your implementation.

Answer: Linux -> Apache -> MongoDB -> Python


#### Question 2: Are there any security considerations your team thought about?

Answer: 1. Since we use http instead of https, password is transmitted by plaintext. Before saved to the database, password is encrypted.
2. For user authentication, token is used and this method is not safe since hacker can get the token and use it to authenticate. We check the user's IP address to make sure that this is the user who owns the token.
3. In diary delete and permission adjust API, only diary id and token are given. Users can delete diary which may not belong to them. We check the token owner and diary owner before processing the diary.  

#### Question 3: Are there any improvements you would make to the API specification to improve the security of the web application?

Answer: 1. Encrypt the password, token and diary before transmitting.
2. For diary delete and permission adjust, processing a group of diaries by given ids rather than one id would be a good idea
3. Response code

#### Question 4: Are there any additional features you would like to highlight?

Answer: In order to develop this app in the future, we add debug mode which can test the APIs and show the status of the database. It is very convinient.

#### Question 5: Is your web application vulnerable? If yes, how and why? If not, what measures did you take to secure it?

Answer: Yes. Data (password, token, text...) is not encrypted during the transmision. Hacker can get it and make our app unsafe.
At the same time, there is no limitation for response times. This app is vulnerable under flooding attack.

#### Feedback: Is there any other feedback you would like to give?

Answer: Please replace this sentence with your answer.

### Declaration

#### Please declare your individual contributions to the assignment:

1. Member 1 Name
    - Integrated feature x into component y
    - Implemented z
2. Member 2 Name
    - Wrote the front-end code
3. Member 3 Name
    - Designed the database schema
4. Member 4 Name
    - Implemented x

