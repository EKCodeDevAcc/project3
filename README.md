This is Edward Kang's Project 3.

This is a web allows users to login, logout, check menus, select items, put those in the cart, checkout, and check their orders.

Superuser account
- username: admin
- Email: admin@example.com
- password: summer18

README.md
- Include a short writeup describing the project, what's contained in each file.

index.js
- Contains all JS codes.

style.css
- It is css file for basic design of this website.

forms.py
- Extension of UserCreationForm that requires users to input their first name, last name and email address when they sign up.

views.py
- It is backend side codes.
- It checks user status like logged in status, whether superuser or not.
- It contains most functions this website uses.
- It renders webpages or send HttpResposne, JsonReponse back to webpages.
- It create, update db objects, pass results of queries.

layout.html
- It contains common features of websites like title, welcome text, displaying username, logout button, link to adminorder page.
- It calls bootstrap, local css, external js file.
- It calls title and body blocks.
- When a user clicks title, 'Edward Kang's Project 1!', if a user is logged in, it redirects a user to main page.
- If not, it redirects a user to login page.

login.html
- A user can input username and password to login to the website.
- If a user types wrong username/password combination, display error message.
- Click sign up button allows a user to go to sign up page.
- If input username/password exist, redirects to main page.
- If user logged out, redirect to this page and display a message.

signUp.html
- A user can create new account.
- it displays an error message depends on situation liek too simple password, already exist, two passwords does not match.

index.html
- It is main page, when user first logged in, directs to here.
- Just display simple advertisment, nothing else.

my_orders.html
- It contains a list of orders of current user.
- List displays date, price, status, check details button of each orders.
- If user select check button, pops out modal with a list of items of the order.
- List displays type, name, size, toppings, price, and status of each items.
- On the bottom of the modal, displays total price of all items.

menu.html
- It contains all menu items of the restaurants.

order.html
- It contains a list of links of menu order pages.
- It contains cart section on the right side that displays list of items in the current user's cart.
- Cart section displays items name, size, toppings, price, and remove button.
- User can take out menu from the cart by clicking this remove button.
- If a user clicks checkout button in cart sections, redirect to checkout page.

order regular pizza, order sicilian pizza.html
- User can see list of pizzas and select.
- If a user select cheese pizzas, add them to cart right away.
- If not, pops out pizza toppings modal that contains list of toppings.
- Depends on the pizza user choose, it force a user to choose the number of toppings they have to.
- After user selects all toppings, it adds the pizza with toppings in the cart.

order_subs.html
- User can see list of subs and select.
- Pops ouit subs toppings modal that contains list of toppings.
- If it is steak & cheese subs, display mushrooms, green peppers, onions, and extra cheese as topping options.
- If not, display extra cheese only.
- Add extra cost depends on the number of toppings.
- After user selects all toppings, it adds the subs with toppings in the cart.

order pasta, order salads, order dinner platters.html
- User can see list of pasta, salads, and dinner platters.
- User can add a selected item in the cart.

checkout.html
- Display all items in the cart with total price.
- If user click place order button, create new order and placed items in the order.
- Then pops out alret and redirect a user to myOrder page.

admin order, admin order done.html
- Only superuser can access.
- Can access to this page by clicking adminorder link under web title that only superuser can see.
- Display list of order placed list or delivered order list.
- Superuser can select list of orders and change their status either delivered or order placed.