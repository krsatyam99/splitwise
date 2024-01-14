# Splitwise

This web application is designed to efficiently manage transaction between user and fellow mates within the system, facilitate the addition of new bill , and streamline splits/share tracking.

- [Demo Link](#demo-link)
- [LinkedIn](https://www.linkedin.com/in/kumar-satyam-769340243/)

  # Table of Contents

- [Prerequisites](#prerequisites)
- [Libraries Used](#libraries-used)
- [Setting up the Project](#setting-up-the-project)
  - [Clone the Project]
  - [Install Dependencies]
  - [Apply Database Migrations]
  - [Create a Superuser (Admin User)]
  - [Run the Development Server]
  - [Setting up Celery]
  - [Run Database Migrations]
- [Important API Endpoints](#important-api-endpoints)
- ["Celery Performing Interval-Based Email Sending"](#celery-performing-interval-based-email-sending)
- [Design Pattern](#design-pattern)
  - [User Profile Pattern](#user-profile-pattern)
  - [Expense Management System](#expense-management-system)
  - [Balance Calculation](#balance-calculation)
- [Schema](#schema)
  - [UserProfile](#userprofile)
  - [Expense](#expense)
  - [ExpenseParticipant](#expenseparticipant)
  - [Balance](#balance)



## Problem Statements

Task 1: Creating Splits Accordance to 3 different cases mainly divided equally, custom division. one to one division.

Task 2: Mail to pay the share weekly using Celery. 

Task 3:Balance Management and payment verification.


## Prerequisites

- Python
- Django


### Libraries Used

- Celery
- Celery Beats
- Redis
- django-extension
- 
### Setting up the project
###### 1. Clone the project
git clone https://github.com/krsatyam99/splitwise.git
###### 2. Install dependencies
pip install -r requirements.txt

###### 3. Apply database migrations
python manage.py makemigrations
python manage.py migrate



###### 4. Create a superuser (admin user)
python manage.py createsuperuser

###### 5. Run the development server
python manage.py runserver




#### Setting up celery
- Adding celery and redis configuration in settings.py
- Initating the celery worker
  
  - - command :  celery -A expense_manager.celery worker -l info
    - ![Screenshot (51)](https://github.com/krsatyam99/splitwise/assets/103446420/bb8f61ac-8473-48e2-b49a-e4ffb3951292)


- Initating the Celery beat
   - - command :celery -A expense_manager beat -l info
     - ![Screenshot (50)](https://github.com/krsatyam99/splitwise/assets/103446420/08f22e45-4df2-4ce3-9ee5-d1580b839335)

       
- python amange.py migrate
### Important API endpoints

-  http://127.0.0.1:8000/expense/login/
-  http://127.0.0.1:8000/expense/split_bill
-  http://127.0.0.1:8000/expense/total_amount_to_pay
-  http://127.0.0.1:8000/expense/amount_to_pay_for_expense
-  http://127.0.0.1:8000/expense/mark_expense_as_paid


## "Celery performing interval-based email sending."


![Untitled](https://github.com/krsatyam99/splitwise/assets/103446420/817a5f7e-eb4e-4181-8c10-5d75150b4723)


## Design Pattern:
The design pattern used in this Django application involves several components, including user profiles, expenses, expense participants, and balances. Here are the key aspects of the design:

1. **User Profile Pattern**:
    - The `UserProfile` model extends the default Django `User` model using a **OneToOneField** relationship. This pattern allows you to store additional user-related data without modifying the core `User` model.
    - By creating a separate `UserProfile` model, you keep the `User` model focused on authentication and authorization, adhering to the single responsibility principle.
    - The `UserProfile` model includes fields such as `email`, `mobile_number`, and `net_balance`.

2. **Expense Management System**:
    - The `Expense` model represents individual expenses. It includes fields for `name`, `amount`, and a foreign key reference to the `User` who created the expense (`creator`).
    - The `participants` field establishes a **ManyToMany** relationship with users through the `ExpenseParticipant` model. This allows multiple users to be associated with an expense.
    - The `ExpenseParticipant` model serves as an intermediary table between users and expenses. It includes fields for `user`, `expense`, `share` (the user's share of the expense), `paid` (whether the user has paid their share), `utr_no` (transaction reference), and `receipt` (an optional file upload).

3. **Balance Calculation**:
    - The `Balance` model represents the financial balance between users. It includes fields for `debtor` (the user who owes money) and `creditor` (the user who is owed money).
    - The `amount` field specifies the outstanding balance amount.
    - The `update_balances` class method calculates and updates balances based on an expense. It considers the shares paid by participants and adjusts balances accordingly.

## Schema:
Here's a summary of the schema for the provided models:

1. **UserProfile**:
    - `user`: One-to-one relationship with the default `User` model.
    - `userId`: A unique UUID field.
    - `email`: User's email address.
    - `mobile_number`: User's mobile number.
    - `net_balance`: User's net balance (decimal field).

2. **Expense**:
    - `name`: Name of the expense.
    - `amount`: Total expense amount.
    - `creator`: Foreign key reference to the user who created the expense.
    - `participants`: Many-to-many relationship with users through `ExpenseParticipant`.

3. **ExpenseParticipant**:
    - `user`: Foreign key reference to a user participating in the expense.
    - `expense`: Foreign key reference to the associated expense.
    - `share`: Decimal field representing the user's share of the expense.
    - `paid`: Boolean field indicating whether the user has paid their share.
    - `utr_no`: Transaction reference (optional).
    - `receipt`: File upload field for expense receipts (optional).

4. **Balance**:
    - `debtor`: Foreign key reference to the user who owes money.
    - `creditor`: Foreign key reference to the user who is owed money.
    - `amount`: Decimal field representing the outstanding balance.



