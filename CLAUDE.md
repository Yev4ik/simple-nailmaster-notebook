# Simple nailmaster notebook 
A simple web app for nailmasters to track their earning and manage clients. This online notebook helps to save the information about clients and it makes easier for nailmaster not to forget when he/she has appointments. 

## Design 
I want everything in feminine, elegantic styles. The best color will be powder pink, so use it as the main color. 

## Rules 
- Prices in ukranian hryvnia 
- Time in 24 hour format
- For the visual design of each page, use your best judgment to make it look clean and elegant.

## Page details
The pages must include a navigation bar aside with logo, name and buttons: "Dashboard", "Clients", "Appointments", "Finance", "Checklists". When user is not logged in, show only "Login" and "Register" buttons. When logged in, show all 5 page buttons + "Logout". All pages except Login and Register require authentication — redirect unauthenticated users to login with message "Please sign in first". Each user sees only their own data.

### Login & Register
Two separate pages for authentication.

**Register form fields**: Name, Email, Phone, Password. Password must contain minimum 8 characters, one special character and one number. All fields are required. If email is already registered — show error message. On success — redirect to Dashboard.

**Login form fields**: Email, Password. All fields required. If user is not registered — show error "You haven't registered yet!". If credentials are wrong — show error "Wrong email or password". On success — redirect to Dashboard.

Both forms must have a password visibility toggle (show/hide). User data is saved to `users` table with fields: id, name, email, phone, password_hash.

### Dashboard 
Short description of the day. It is a landing page. It shows:
- Greetings and today's date and number of visits today
- 2 small containers lower with: numbers of visits today, total earnings for this month
- 2 big containers lower: first is with list of visits for today(time, client, procedure, price and time needed) and second is notifications which are collected automatically (for example birthdays of clients in next 7 days, or random motivational phrase randomly taken from references/motivational_phrases.md)

It does not save anything to database it only reads and shows data from other tables.

### Clients 
It is a page with the whole list of clients of master. It has search function when user writes name from hand and also has search based on clients' status (new, vip, regular). Clients are saved to `clients` table with fields: name, phone, birthday, notes, allergies, favourite colours, nail shape(square/oval/almond), status (new/regular/vip) and number of previous visits. This page must show CRUD operations with proper toast message. 

The clients are saved to the `clients` table, but number of visits is taken from `appointments` table

### Appointments 
Here you can see the list for a week with all visits(name and time). When adding an appointment you see free "windows" select already added client from list(If there is no such client in db add proper error handling), choose procedure and  date&time section and prices are added automatically. Be sure that between each visit must be minimum 5 minute break. So add error handling. Also add error handling if master is trying to add the client for past date. U can change client status (on plan, cancelled, did not come). There is also a posibility to add one client to different procedures but NOT ONE CLIENT FOR SAME PROCEDURES IN ONE DAY. Appointment is counted as done when after procedure time the status stayed on plan.

All the visits are saved to `appointments` table. But procedures, prices and durations are taken automatically from references/procedures.md

### Finance
Here is the page where you can track the number of earning for this months. All spendings you add by yourself and select the category(materials, rent, instruments, else). The application will count it and show the correct earning number already counted with these spendings. Earnings are calculated automatically from appointments where status = done. Add for this page proper error handling. The page also will show the percentage for spendings from all categories from the highest to lowest.

### Checklists
U can add tasks for a day, and complete them and put a check. User can perform CRUD operations on this tasks. Be sure that tasks are saved to the database so they be present on the next day.