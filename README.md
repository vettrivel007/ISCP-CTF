# ISCP-CTF
Real-time PII Defense - 100 points

# Storyline: The Echo of a Breach
Flixkart, a leading e-commerce platform, has recently undergone a security audit. While our primary data repositories are fortified, a significant vulnerability has been identified: a potential data leakage through unmonitored assets.

A recent fraud incident, where a customer's personal details (name and address) were used to create a fraudulent order, traced back to logs from an external API integration. These logs were passing through a network ingress layer and were not being adequately sanitized. This PII leak led to a series of telephonic frauds where customers were scammed into giving away OTPs, resulting in unauthorized orders and refund scams. Furthermore, unmonitored endpoints were found to be storing PII in plain text, and some PII was even being rendered in internal web applications, creating further security risks.

Your mission is to join "Project Guardian 2.0" and develop a solution to plug this security gap. You must create a system that can accurately identify and redact PII from data streams without introducing significant latency. The ultimate goal is to prevent similar PII-related frauds from happening in the future.

# Part 1: The Challenge (2 Hours)
Your task is to provide two key deliverables:

# 1. Code a PII Detector & Redactor (Python is preferred)
Write a program that takes a CSV file as input.
The program must iterate through each record and identify if it contains PII based on the provided definitions.
It should output a new CSV file with two key modifications:
A new column named is_pii with a True or False value, representing your detection.
All identified PII data points must be redacted or masked (e.g., [REDACTED_PII] or a masked version like 98XXXXX4321).
Your solution will be judged on its accuracy, efficiency, and how well it handles false positives.
Hint: Consider using techniques like regular expressions for well-structured data, or more advanced methods like Named Entity Recognition (NER) and other machine learning approaches for unstructured data. A hybrid approach that combines these methods is often a robust solution.

# 2. Propose a Deployment Strategy
Based on the conceptual architecture, propose a detailed deployment strategy for your PII solution.
The proposed solution can be at any layer (e.g., a DaemonSet, a Sidecar container, an API Gateway plugin, a Browser extension, a BotManager plugin, etc.).
Think critically about where your solution would be most effective. Should it live at the network level, a specific application layer, or even within an internal tool? Explain where your code would live and justify your choices in terms of scalability, latency, cost-effectiveness, and ease of integration.
Your proposal must be a brief text document (e.g., in Markdown).

# Definition of PII & Non-PII
Your solution must adhere strictly to these definitions to achieve a high score.

# A. PII (Standalone)
These data points are PII on their own and can be used to uniquely identify an individual.

Phone Number: Any 10-digit number.
Aadhar Card Number: A 12-digit number (e.g., 1234 5678 9012).
Passport Number: A common alphanumeric format (e.g., P1234567).
UPI ID: A username-based or number-based ID (e.g., user@upi, 9876543210@ybl).
# B. PII (Combinatorial)
These data points become PII only when two or more of them appear in the same record.

Name: Full names with both first and last names.
Email Address: Any valid email format.
Physical Address: An address with street, city, and pin code.
Device ID / IP Address: Only when tied to a specific user context.
# C. Non-PII (False Positives to Avoid)
These are examples of data that should NOT be classified as PII, even if they might look like it. Correctly classifying these as non-PII is crucial for your score.

A first name or a last name alone (e.g., "John," "Smith").
An email address appearing without any other combinatorial PII in the same record.
A standalone city, state, or pin code.
A transaction ID, order ID, or product description.
Any single attribute from list B not combined with another from list B.

# Scoring System
Your code will be run against a hidden test dataset. The final score is based on the following:

# Detection Accuracy (70%)
F1-score on True/False labels
+1 point: Correct PII identification
-0.5 points: False positive
-1 point: Missed PII
# Redaction Quality (20%)
Proper masking of identified PII
# Code Quality (10%)
Clean, efficient implementation
Target: F1-Score ≥ 0.85 for passing, ≥ 0.95 for excellence

# Deployment Feasibility (30%)
The quality and practicality of your architectural proposal.
How well it addresses the constraints of latency, cost, and scale.
Creativity and novelty of the solution.
# Rules of Engagement
To ensure a fair and objective assessment, the following rules apply:

The challenge is designed to be completed in 2 hours.
Your solution must be your own work. The use of general-purpose large language models or AI tools (e.g., ChatGPT, Gemini, etc.) to generate the code or the deployment proposal is strictly prohibited and will lead to immediate disqualification.
You may use standard libraries and open-source frameworks for your chosen programming language. (Python preferred)
Your solution must be self-contained and runnable from a single script.

# Deliverables
- Python File: detector_full_candidate_name.py
- Generated Output: redacted_output_candidate_full_name.csv
- Execution Command: python3 detector_full_candidate_name.py iscp_pii_dataset.csv
- Github Url With all the files: upload all the files and share the github url in flag input
# Input Format
CSV file with columns: record_id, Data_json
# All JSON Keys in the Dataset:
customer_id, phone, order_value, name, email, city, first_name, product, category, aadhar, transaction_type, product_id, address, ip_address, pin_code, product_category, upi_id, amount, last_name, order_id, passport, booking_reference, device_id, app_version, transaction_id, status, order_date, state, product_name, age, verification_status, query_type, merchant, product_description, price, sms_consent, username, last_login, kyc_status, region, warehouse_code, contact, carrier, subscription_type, renewal_date, brand, model, size, currency, exchange_rate, notification_preference, product_rating, review_count, family_size, delivery_zone, app_name, version, issue_date, profession, address_proof, ticket_id, search_query, filters, auto_debit, state_code, gst_number, feature_flag, enabled, discount_code, validity, nationality, wishlist_count, biometric_status, payment_gateway, transaction_fee, travel_insurance, coverage, military_service, ncc_certificate, conference_call, participants_limit, jewelry_insurance, premium, diplomatic_immunity, official_travel, property_registration, stamp_duty, music_streaming, offline_downloads, concert_tickets, artist_alerts, artist_visa, multi_entry, performance_permit, comedy_club, performance_rights

# Expected Output Format
CSV file with columns: `record_id, redacted_data_json, is_pii`
Example Output:
```record_id,redacted_data_json,is_pii
1,"{""phone"": ""98XXXXXX10"", ""order_value"": 1299}",True
2,"{""name"": ""JXXX SXXXX"", ""email"": ""joXXX@gmail.com""}",True
```
