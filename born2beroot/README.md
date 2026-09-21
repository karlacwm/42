*This project has been created as part of the 42 curriculum by <wcheung>*

#Born2beRoot

#Description
is an introductory system administration and virtualization project. The goal is to create and configure a secure virtual machine hosting a Linux server (Debian, in my case), while enforcing strict security and configuration rules.

#Installation & Execution
1. Create a virtual machine using VirtualBox (or UTM).
2. Install Debian (minimal installation).
3. Configure users, sudo, SSH, firewall, and security policies.
4. Apply password and monitoring requirements.
5. Verify system compliance according to project rules.

#Resources
- Guide https://noreply.gitbook.io/born2beroot
- Debian Documentation
- Linux LVM Documentation
- AppArmor Documentation
- sudo & UFW manuals

#Use of AI
AI was used for:
- Clarifying concepts and mechanisms, as well as key terms and my confusions around virtual machines and about setting up the system
- Providing me background knowledge for the topic and explaining when my understanding is not accurate
- Assisting with configuration explanations and comparisons

#Operating System Choice
Debian
Pros: stable, lightweight, extensive documentation, large community
Cons: slower release cycle, older package versions

#Main Design Choices
Partitioning: LVM-based partitioning to improve flexibility and disk management
Security Policies: AppArmor enabled for mandatory access control
User Management: sudo configured with strict rules, no root SSH login
Services Installed: SSH, UFW firewall, cron, zip, wget, WordPress, lighttpd, PHP, MariaDB, Redis
Password Policy: strong password rules with expiration and complexity enforcement 

#Comparisons
1. Debian vs Rocky Linux
Debian focuses on simplicity and stability
Rocky Linux targets enterprise environments and RHEL compatibility

2. AppArmor vs SELinux
AppArmor: easier to configure, profile-based
SELinux: more powerful but complex, label-based security

3. UFW vs firewalld
UFW: simple and beginner-friendly
firewalld: more dynamic and flexible, enterprise-oriented

4. VirtualBox vs UTM
VirtualBox: cross-platform, widely supported
UTM: macOS-focused, optimized for Apple Silicon
