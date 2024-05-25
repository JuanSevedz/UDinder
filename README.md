# Welcome to UDinder

1. [About](#about-udinderfinal_project)
2. [Develop_process](#user-stories)
3. [Diagrams](#diagrams)
    - [Deployment Diagram](#deployment-diagram)
    - [Activity Diagram](#activity-diagrams)
    - [Sequence Diagram](#sequence-diagram)
    - [State Diagram](#state-diagrams)
    - [Class Diagram](#class-diagram)
    - [CRC cards](#crc-cards)

4. [Poster(Beta)](#poster)
5. [Paper](#paper)
6. [Technical Report](#technical-report)

## About UDinder(Final_project)

The project involves creating a monolithic software for an online platform. In terms of technical decisions, the project focused on key processes such as sign-in, sign-up, authentication, profile completion, and interaction with other user profiles.

Backend development was carried out using Python, leveraging the FastAPI framework. For the frontend graphical interface, HTML, CSS, and JavaScript were chosen, along with the Apache server and the Django framework.

For managing the database, SQLAlchemy was selected due to its ability to handle database relationships with a syntax similar to that of the programming language.

## Process Of Development

Firts, we create the UML diagrams of __Deployment__,__Activities__, __Sequence__, __State__, __Class__ and the __CRC__ cards of each class.

## User Stories

- __As a user__, I want to be able to sign up for the app so that I can create a profile and start using the platform.
- __As a developer__, I want to continuously monitor and improve the app's security to protect user data and privacy.
- __As an administrator__, I want to be able to access the database to view user information and activity for moderation purposes.
- __As a user__, I want to be able to sign in to the app with my username and password so that I can access my profile and interact with other users.
- __As an administrator__, I want to be able to block or suspend users who violate the app's community guidelines or terms of service.
- __As a developer__, I want to implement user authentication functionality to allow users to sign up and sign in securely.
- __As a user__, I want to be able to view suggested profiles so that I can find potential matches.
- __As a user__, I want to be able to swipe right or left on profiles to indicate my interest or disinterest.
- __As an administrator__, I want to be able to review reported profiles and messages to ensure they comply with the app's policies.
- __As a developer__, I want to implement profile management features to allow users to update their profiles and preferences.
- __As a user__, I want to receive notifications when I have a match with another user so that I can start messaging them.
- __As a developer__, I want to implement the matching algorithm to suggest compatible profiles to users.
- __As a developer__, I want to implement the messaging functionality to allow users to communicate with their matches.
- __As a user__, I want to be able to send messages to my matches to start a conversation and get to know them better.
- __As a user__, I want to be able to view my matches and their profiles so that I can keep track of my interactions.
- __As an administrator__, I want to be able to respond to user inquiries and provide assistance with any issues they may encounter.
- __As a developer__, I want to implement a reporting system to allow users to report inappropriate behavior or content.
- __As a developer__, I want to optimize the app's performance and scalability to handle a large number of users and interactions.

## Diagrams

### Deployment Diagram

<img src="docs/Deployment diagram/deployment_diagram.png" alt="This is The Deploymen Diagram" style="display: block; margin: auto; border: 1px solid black;">

***

### Activities Diagrams

- Authentication:
<img src="docs/Activity Diagrams/authentication_ad.png" alt="This is The Authentication_AD" style="display: block; margin: auto; border: 1px solid black;">

- Complete Profile:
<img src="docs/Activity Diagrams/Complete_profile_ad.png" alt="This is The Authentication_AD" style="display: block; margin: auto; border: 1px solid black;">

- Verify User:
<img src="docs/Activity Diagrams/Gen.png" alt="This is The Verification_AD" style="display: block; margin: auto; border: 1px solid black;">

- Sing Up:
<img src="docs/Activity Diagrams/Sign_up_AD.png" alt="This is The Sing_up_AD" style="display: block; margin: auto; border: 1px solid black;">

- Swipe Profiles:
<img src="docs/Activity Diagrams/swipe_funtion_AD.png" alt="This is The Swipe_AD" style="display: block; margin: auto; border: 1px solid black;">

- User Interaction:
<img src="docs/Activity Diagrams/User_interaction_AD.png" alt="This is The User_interaction_AD" style="display: block; margin: auto; border: 1px solid black;">

***

### Sequence Diagram

<img src="docs/Sequence diagram/sequence_diagram.png" alt="This is The Sequence_D" style="display: block; margin: auto; border: 1px solid black;">

***

### State Diagrams

- Log_in_std:
<img src="docs/State diagrams/authentication_SD.png" alt="This is The LogIn_std" style="display: block; margin: auto; border: 1px solid black;">

- Interaction_std:
<img src="docs/State diagrams/Idle_SD.png" alt="This is Interaction_users_std" style="display: block; margin: auto; border: 1px solid black;">

- User_std:
<img src="docs/State diagrams/user_sd.png" alt="This is The full_procces_std" style="display: block; margin: auto; border: 1px solid black;">

***

### Class Diagram

<img src="docs/Class Diagrams/CD_relation_classes.png" alt="This is The Class Diagram" style="display: block; margin: auto; border: 1px solid black;">

***

### CRC cards

- All:
<img src="docs/CRC Cards/All_CRC.png" alt="This is All_cards_crc" style="display: block; margin: auto; border: 1px solid black;">

- DB:
<img src="docs/CRC Cards/DB_CRC.png" alt="This is DB_crc" style="display: block; margin: auto; border: 1px solid black;">

- Interaction:
<img src="docs/CRC Cards/InteractionProfiles_CRC.png" alt="This is Interaction_profiles_crc" style="display: block; margin: auto; border: 1px solid black;">

- Complete_profile:
<img src="docs/CRC Cards/Profile_CRC.png" alt="This is complete_profile_crc" style="display: block; margin: auto; border: 1px solid black;">

- User:
<img src="docs/CRC Cards/User_CRC.png" alt="This is User_crc" style="display: block; margin: auto; border: 1px solid black;">

- User_interface:
<img src="docs/CRC Cards/UserInterface_CRC.png" alt="This is User_interface_crc" style="display: block; margin: auto; border: 1px solid black;">

***

## Poster
<img src="research/poster/UDinder_poster.png" alt="This is the poster" style="display: block; margin: auto; border: 1px solid black;">

## Paper

[Download](research/paper/UDinder.pdf)

## Technical Report

[Download](research/UDinder_TechnicalReport.pdf)
