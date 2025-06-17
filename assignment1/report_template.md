# Generic Report Template for ECE 572

**Use this template for all three assignments and modify if needed**

**This template is made by GenAI help, if you believe some changes are required or some parts need revision, feel free to send a merge request or send an email!**

---

**Course**: ECE 572; Summer 2025
**Instructor**: Dr. Ardeshir Shojaeinasab
**Student Name**: Zhang Zhang  
**Student ID**: V01046193  
**Assignment**: Assignment 1
**Date**: June 16, 2025
**GitHub Repository**: https://github.com/Zzzzzzzach/ECE572_Summer2025_SecureText

---

## Executive Summary

<!-- 
Provide a brief overview of what you accomplished in this assignment. 
For Assignment 1: Focus on vulnerabilities found and security improvements made
For Assignment 2: Focus on authentication enhancements and Zero Trust implementation  
For Assignment 3: Focus on cryptographic protocols and end-to-end security
Keep this section to 1-2 paragraphs.
-->

[Write your executive summary here]

---

## Table of Contents

1. [Introduction](#introduction)
2. [Task Implementation](#task-implementation)
   - [Task 1 Security Vulnerability Analysis](#task-x)
   - [Task Y](#task-y)
   - [Task Z](#task-z)
3. [Security Analysis](#security-analysis)
4. [Attack Demonstrations](#attack-demonstrations)
5. [Performance Evaluation](#performance-evaluation)
6. [Lessons Learned](#lessons-learned)
7. [Conclusion](#conclusion)
8. [References](#references)

---

## 1. Introduction

### 1.1 Objective
<!-- Describe the main objectives of this assignment -->

### 1.2 Scope
<!-- Define what you implemented and what you focused on -->

### 1.3 Environment Setup
<!-- Briefly describe your development environment -->
- **Operating System**: MacOS Sequoia
- **Python Version**: 3.13.0
- **Key Libraries Used**: 
- **Development Tools**: 

---

## 2. Task Implementation

<!-- Replace Task X, Y, Z with actual task numbers and names  -->

### 2.1 Task 1: Security Vulnerability Analysis
**Objective**: Analyze the provided insecure messenger application and identify security weaknesses.

#### 1. No Password Complexity Requirements
**Category**: Authentication
**Description**: The application allows users to set any password without checking complexity rules such as minimum length, character diversity, or blacklisting common passwords.
**Impact**: This exposes user accounts to brute-force and dictionary attacks.
**Principles**: "Security of a password-based authentication system rests
entirely on the attacker’s inability to guess the password in a small
number of guesses." So increasing length or character diversity will make harder for the attacker to breach the system.

##### Attack Scenarios
**What the attacker needs**
Access to the login interface and a dictionary of common passwords.

**What they could achieve**
The attacker could brute-force or guess a user’s password in a small number of attempts. This leads to full account compromise.

**Final thoughts and solution**
Systems should enforce password complexity rules.

#### 2. Password Reset Requires No Identity Verification
**Category**: Authentication
**Description**: The password reset functionality does not require the user’s current password, nor does it perform any meaningful identity verification. The security question is hard-coded with the same answer for all users and not used during the reset process.
**Impact**: An attacker who knows a valid username can easily reset the corresponding password and take over the account.
**Principles**: “The implementation must verify reset through secure means.” The Sarah Palin email hack case highlights the dangers of relying on easily guessable or publicly available reset information. However, in this application, the password can be changed without even requiring the original password
##### Attack Scenarios
**What the attacker needs**
A known username and access to the reset command.

**What they could achieve**
The attacker could take over another user's account by resetting their password without proving ownership.

**Final thoughts and solution**
Reset functions must include robust identity verification such as original password, secret questions, email verification.

#### 3. Plaintext Storage of Usernames and Passwords on Disk
**Category**: Data Protection
**Description**: User credentials are stored in a local JSON file in plaintext. There is no encryption or hashing applied to the data.
**Impact**: Anyone who gains access to the disk or file system can directly read all usernames and passwords.
**Principles**: According to Kerckhoff’s Principle, “The only thing that we keep secret from the adversary are the system’s secret keys.”. However, in this application, passwords are stored in plaintext, meaning that if the storage is exposed, all user secrets are immediately compromised.

##### Attack Scenarios
**What the attacker needs**
File system access to users.json

**What they could achieve**
Instant access to all usernames and passwords in plaintext.

**Final thoughts and solution**
Sensitive user data should never be stored in plaintext. Passwords must be hashed using salted password hashing functions.

#### 4. Messages Transmitted in Plaintext Over TCP
**Category**: Communication Security
**Description**: The application uses raw TCP sockets to transmit authentication data and chat messages without any encryption.
**Impact**: This leaves all data vulnerable to interception and tampering by a network-level attacker.
**Principles**: Application need to protect against eavesdropping attacks and active attacks, recommending the use of challenge-response protocols and digital signatures for secure communication.

##### Attack Scenarios
**What the attacker needs**
Ability to sniff network traffic

**What they could achieve**
Intercept and read messages, usernames, and passwords. The attacker could also inject or modify messages by doing man-in-the-middle attacks.

**Final thoughts and solution**
All communication must be encrypted through TLS or other methods.


#### 5. No Account Lockout or Rate Limiting on Login
**Category**: Authentication
**Description**: The application does not enforce any limits on login attempts, nor does it introduce delays or blocks after failed attempts.
**Impact**: This allows an attacker to repeatedly guess passwords without resistance, making brute-force attacks feasible.
**Principles**: The course discussed the importance of rate limiting and guess caps to prevent online password guessing, especially in systems that rely on weak user-chosen passwords.

##### Attack Scenarios
**What the attacker needs**
Access to the login interface.

**What they could achieve**
They could perform an online brute-force attack, testing hundreds or thousands of passwords until one works.

**Final thoughts and solution**
Application could use protections such as rate limiting, exponential backoff, and account lockouts to prevent brute-force attacks on authentication endpoints.


### 2.2 Task Y: [Task Name]

#### 2.2.1 Objective
<!-- What was the goal of this task? -->

#### 2.2.2 Implementation Details
<!-- Describe your implementation approach -->

#### 2.2.3 Challenges and Solutions
<!-- What problems did you encounter and how did you solve them? -->

#### 2.2.4 Testing and Validation
<!-- How did you test that your implementation works correctly? -->

---

### 2.3 Task Z: [Task Name]

#### 2.3.1 Objective
<!-- What was the goal of this task? -->

#### 2.3.2 Implementation Details
<!-- Describe your implementation approach -->

#### 2.3.3 Challenges and Solutions
<!-- What problems did you encounter and how did you solve them? -->

#### 2.3.4 Testing and Validation
<!-- How did you test that your implementation works correctly? -->

---

## 3. Security Analysis

### 3.1 Vulnerability Assessment
<!-- For Assignment 1: Document vulnerabilities found in the base application -->
<!-- For Assignment 2/3: Analyze security improvements made -->

**Identified Vulnerabilities** (Assignment 1):
| Vulnerability | Severity | Impact | Location(function/action) | Mitigation |
|---------------|----------|---------|----------|------------|
| N/A | N/A | N/A | N/A | N/A |
| N/A | N/A | N/A | N/A | N/A |
| N/A | N/A | N/A | N/A | N/A |

### 3.2 Security Improvements
<!-- Document the security enhancements you implemented -->

**Before vs. After Analysis**:
- **Authentication**: [If applicable otherwise remove][How it improved]
- **Authorization**: [If applicable otherwise remove][How it improved]  
- **Data Protection**: [If applicable otherwise remove][How it improved]
- **Communication Security**: [If applicable otherwise remove][How it improved]

### 3.3 Threat Model
<!-- Describe the threats your implementation addresses -->

**Use the following security properties and threat actors in your threat modeling. You can add extra if needed.**

**Threat Actors**:
1. **Passive Network Attacker**: Can intercept but not modify traffic
2. **Active Network Attacker**: Can intercept and modify traffic
3. **Malicious Server Operator**: Has access to server and database
4. **Compromised Client**: Attacker has access to user's device

**Security Properties Achieved**:
- [ ] Confidentiality
- [ ] Integrity  
- [ ] Authentication
- [ ] Authorization
- [ ] Non-repudiation
- [ ] Perfect Forward Secrecy
- [ ] Privacy

---

## 4. Attack Demonstrations

### 4.1 Attack 1: [Attack Name]

#### 4.1.1 Objective
<!-- What vulnerability does this attack exploit? -->

#### 4.1.2 Attack Setup
<!-- Describe your attack setup and tools used -->

**Tools Used**:
- Tool 1: [Purpose]
- Tool 2: [Purpose]

#### 4.1.3 Attack Execution
<!-- Step-by-step description of the attack -->

1. Step 1: [Description]
2. Step 2: [Description]
3. Step 3: [Description]

#### 4.1.4 Results and Evidence
<!-- Show evidence of successful attack -->

**Evidence**:
![Attack Screenshot](images/attack_1_evidence.png)

```
Attack Output:
[Include relevant logs or outputs]
```

#### 4.1.5 Mitigation
<!-- How did you fix this vulnerability? -->

---

### 4.2 Attack 2: [Attack Name]

#### 4.2.1 Objective
#### 4.2.2 Attack Setup  
#### 4.2.3 Attack Execution
#### 4.2.4 Results and Evidence
#### 4.2.5 Mitigation

---

## 5. Performance Evaluation
Basic test results in terms of resources used in terms of hardware and time. Also, if the test has limitations and fix worked properly(test passed or failed)

**Measurement Setup**:
- Test Environment: [Descriptions+Screenshots]
- Test Data: [Descriptions+Screenshots]
- Measurement Tools/Methods: [Descriptions+Screenshots]
- Test Results: [Descriptions+Screenshots]

---

## 6. Lessons Learned

### 6.1 Technical Insights
<!-- What did you learn about security implementations? -->

1. **Insight 1**: [Description]
2. **Insight 2**: [Description]
.
.
.
N. **Insight N**: [Description]

### 6.2 Security Principles
<!-- How do your implementations relate to fundamental security principles? -->

**Applied Principles**:
- **Defense in Depth**: [How you applied this]
- **Least Privilege**: [How you applied this]
- **Fail Secure**: [How you applied this]
- **Economy of Mechanism**: [How you applied this]

---

## 7. Conclusion

### 7.1 Summary of Achievements
<!-- Summarize what you accomplished -->

### 7.2 Security and Privacy Posture Assessment
<!-- How secure is your final implementation? -->

**Remaining Vulnerabilities**:
- Vulnerability 1: [Description and justification]
- Vulnerability 2: [Description and justification]

**Suggest an Attack**: In two lines mention a possible existing attack to your current version in abstract

### 7.3 Future Improvements
<!-- What would you do if you had more time? -->

1. **Improvement 1**: [Description]
2. **Improvement 2**: [Description]

---

## 8. References

<!-- 
Include all sources you referenced, including:
- Course materials and lecture notes
- RFCs and standards
- Academic papers
- Documentation and libraries used
- Tools and software references
-->

---

## Submission Checklist

Before submitting, ensure you have:

- [ ] **Complete Report**: All sections filled out with sufficient detail
- [ ] **Evidence**: Screenshots, logs, and demonstrations included
- [ ] **Code**: Well-named(based on task and whether it is an attack or a fix) and well-commented and organized in your GitHub repository deliverable directory of the corresponding assignment
- [ ] **Tests**: Security and functionality tests implemented after fix
- [ ] **GitHub Link**: Repository link included in report and Brightspace submission
- [ ] **Academic Integrity**: All sources properly cited, work is your own

---

**Submission Instructions**:
1. Save this report as PDF: `[StudentID]_Assignment[X]_Report.pdf`
2. Submit PDF to Brightspace
3. Include your GitHub repository fork link in the Brightspace submission comments
4. Ensure your repository is private until after course completion otherwise you'll get zero grade

**Final Notes**:
- Use **GenAI** for help but do not let **GenAI** to do all the work and you should understand everything yourself
- If you used any **GenAI** help make sure you cite the contribution of **GenAI** properly
- Be honest about limitations and challenges
- Focus on demonstrating understanding, not just working code
- Proofread for clarity and technical accuracy

Good luck!
