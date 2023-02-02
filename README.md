# MaleFashion 

## Project Summary

MaleFashion is a website built using the Django framework and Postgres as a database. Users can easily create an account by registering on the website, which requires minimal information. After registration, an email with a confirmation link is sent to the user's email address. The user must click on the link to confirm their registration and activate their account.

Once registered and confirmed, users can log in to their account to access their order history and manage their personal information. The website features an order system that allows users to add items to their cart, view their cart, and proceed to checkout.

After an order is placed, the customer will receive an email that includes a summary of the order, the total price, and shipping details. The email also serves as a record of the transaction and can be used for reference in the future. The website also includes a blog, where updates about products, fashion and more are posted every day.

---

## Running this project
To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```
Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project
```
virtualenv env
```
That will create a new folder env in your project directory. Next activate it with this command on mac/linux:
```
source env/bin/active
```
Then install the project dependencies with
```
pip install -r requirements.txt
```
Now you can run the project with this command
```
python manage.py runserver
```

**Note:** Before running the project, you should create a .env file inside the project directory and copy the template from .env-sample. Then fill in all of the needed information. Then migrate all of the migrations to the database.

---
## Screenshots and demo

Video demo: https://youtu.be/wGRGor7NuHI

`User Registration`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/register.png)

`Confirmation Email`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/order_successful.png)

`Shop`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/shop.png)

`Cart`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/cart.png)

`Order Successful`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/order_successful.png)

`Order Email`
![Image](https://github.com/mitko-stoyanov/Ecommerce-Store/blob/main/project%20screenshots/register_activation.png)