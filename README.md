# HabCube

# Description

The "intelligent cube" is an IoT device that supports users in forming and maintaining daily habits. Habits are defined in a mobile application, which allows for their configuration and the presentation of statistics regarding progress.

# Introduction

The goal of this project is to create a complete Internet of Things (IoT) system designed to operate on a local network. The "Intelligent Cube" is an IoT device that supports users in building and maintaining daily habits. The system combines hardware (the physical cube) with a mobile application that allows users to define, configure, and track their habits, as well as view statistics on their progress.

The project integrates knowledge from electronics, computer science, network programming, and embedded systems engineering. The work covers both the hardware layer (the cube's design and implementation) and the software layer (server-side communication, backend, mobile user interface, and overall system integration).

# Project Goals

## General Goals

- To create a fully functional IoT system operating within a local network.

- To achieve high effectiveness in helping users build and sustain positive habits.

- To design a system that increases user motivation and engagement in the process of self-improvement.

- To develop a final product that genuinely improves users' quality of life by supporting them in achieving their habit-related goals.

## Educational Goals

- To understand the practical aspects of building end-to-end IoT systems.

- To learn how to integrate hardware and software into a single cohesive system.

- To develop teamwork and project management skills.

- To gain experience in planning, implementing, testing, and documenting a complex technical project.

- To learn which motivational mechanisms are most effective in habit formation and how to design engaging and intuitive user interactions.

# Project Scope

## Key Features

- **Habit Configuration**: Defining and managing habits through a mobile application.

- **Progress Tracking**: Monitoring user progress and presenting it through statistics.

- **Motivational Feedback**: Providing users with visual, sound, and light-based "dopamine hits" to reinforce positive actions.

## System Architecture

The system consists of three main components:

- The Intelligent Cube: A physical device based on an ESP32 microcontroller that acts as the primary user interaction point.

- Central Server: A backend service responsible for handling communication with the cube, processing data, and storing user statistics.

- Mobile Application: A user interface for configuring the cube, defining habits, and viewing progress data.

All components communicate over a local Wi-Fi network.

# Tools and Technologies

Hardware: ESP32, 4 OLED Screens(I2C, SPI), gyroscope, Multiplexer, 2 Tact switches, audio amplifier, speaker, leds.

Software:

Backend: To be determined (e.g., Python with FastAPI).

Mobile App/UI: To be determined.

Database: To be determined.

Project Management: GitHub Project (Kanban board).

Version Control: Git, GitHub.

# Expected Results

The final outcome of the project will be a functional IoT system that enables:

- Configuration and management of daily habits via a mobile app.

- Physical interaction with the cube to confirm habit completion.

- Real-time motivational feedback to the user.

- Visualization of progress data and statistics.

# Team

Piotr Ziobrowski - embedded programming 

Szymon Domagała - frontend, UI

Paweł Klocek - database, documentation

Aleksy Dąda - backend, docker

Patryk Kurek - hardware and embedded programmming and tech menago
