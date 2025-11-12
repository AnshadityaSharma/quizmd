# Software Engineering Lecture Notes

## Introduction to Software Engineering

Software engineering is the application of engineering principles to software development. It involves designing, developing, testing, and maintaining software systems. The field emerged in the 1960s as a response to the "software crisis" - the difficulty of writing correct, understandable, and verifiable computer programs.

## Agile Methodology

Agile is an iterative approach to software development that emphasizes flexibility, collaboration, and customer feedback. Unlike traditional waterfall methods, Agile breaks projects into small increments with minimal planning.

### Core Principles

The Agile Manifesto, created in 2001, outlines four core values:
- Individuals and interactions over processes and tools
- Working software over comprehensive documentation
- Customer collaboration over contract negotiation
- Responding to change over following a plan

### Agile Frameworks

There are several popular Agile frameworks, including Scrum, Kanban, and Extreme Programming (XP).

## Scrum Framework

Scrum is one of the most widely used Agile frameworks. It provides a structured approach to managing complex product development.

### Scrum Roles

Scrum defines three primary roles:

1. **Product Owner**: Responsible for maximizing the value of the product and managing the product backlog. They represent the stakeholders and ensure the team is building the right features.

2. **Scrum Master**: Facilitates the Scrum process, removes impediments, and ensures the team follows Scrum practices. The Scrum Master leads the daily Scrum meetings and serves the team, not manage it.

3. **Development Team**: A self-organizing, cross-functional group responsible for delivering potentially shippable increments of the product.

### Scrum Events

Scrum includes several time-boxed events:

- **Sprint Planning**: At the start of each sprint, the team plans what work will be done. Typically lasts 2-4 hours for a 2-week sprint.

- **Daily Scrum**: A 15-minute daily meeting where the team synchronizes activities and plans for the next 24 hours. The Scrum Master facilitates this meeting.

- **Sprint Review**: At the end of each sprint, the team demonstrates what was accomplished. Stakeholders provide feedback.

- **Sprint Retrospective**: The team reflects on the sprint and identifies improvements for the next sprint.

### Scrum Artifacts

- **Product Backlog**: An ordered list of everything that might be needed in the product.

- **Sprint Backlog**: The set of product backlog items selected for the sprint, plus a plan for delivering them.

- **Increment**: The sum of all product backlog items completed during a sprint.

### Sprint Duration

A standard Scrum sprint is typically 2-4 weeks long, with 2 weeks being the most common duration. The sprint length should remain consistent once established.

## Software Testing

Software testing is a critical part of the software development lifecycle. It involves executing software to find defects and ensure quality.

### Testing Levels

1. **Unit Testing**: Tests individual components or functions in isolation. Usually written by developers.

2. **Integration Testing**: Tests how different components work together.

3. **System Testing**: Tests the complete, integrated system to verify it meets requirements.

4. **Acceptance Testing**: Validates that the system meets business requirements and is ready for deployment.

### Testing Types

- **Functional Testing**: Verifies that the software functions correctly according to specifications.

- **Non-Functional Testing**: Tests aspects like performance, security, usability, and reliability.

- **Regression Testing**: Ensures that new changes don't break existing functionality.

- **User Acceptance Testing (UAT)**: Final testing performed by end users before release.

### Test-Driven Development (TDD)

TDD is a development approach where tests are written before the code. The cycle follows:
1. Write a failing test
2. Write code to make the test pass
3. Refactor the code
4. Repeat

## Version Control

Version control systems track changes to code over time, allowing multiple developers to collaborate effectively.

### Git

Git is the most popular distributed version control system. Key concepts include:

- **Repository**: A collection of files and their complete history
- **Commit**: A snapshot of changes at a specific point in time
- **Branch**: A parallel line of development
- **Merge**: Combining changes from different branches

### Common Git Commands

- `git clone`: Copy a repository from a remote location
- `git add`: Stage changes for commit
- `git commit`: Save changes to the repository
- `git push`: Upload changes to a remote repository
- `git pull`: Download and merge changes from a remote repository

## Software Design Patterns

Design patterns are reusable solutions to common problems in software design. They provide templates for solving recurring design challenges.

### Creational Patterns

- **Singleton**: Ensures a class has only one instance
- **Factory**: Creates objects without specifying the exact class
- **Builder**: Constructs complex objects step by step

### Structural Patterns

- **Adapter**: Allows incompatible interfaces to work together
- **Decorator**: Adds new functionality to objects dynamically
- **Facade**: Provides a simplified interface to a complex subsystem

### Behavioral Patterns

- **Observer**: Notifies multiple objects about state changes
- **Strategy**: Defines a family of algorithms and makes them interchangeable
- **Command**: Encapsulates requests as objects

## Conclusion

Software engineering is a broad field that requires understanding of methodologies, frameworks, testing, version control, and design principles. Continuous learning and adaptation are essential for success in this field.

