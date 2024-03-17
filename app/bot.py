from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chatbot = ChatBot("Chatpot")


trainer = ListTrainer(chatbot)
trainer.train([
    "Hello", 
    "Hello. How may I help you today",
])
trainer.train([
    "Hi", 
    "Welcome friend. How may I help you",
])
trainer.train([
    "Who are you",
    "I am an Eshop assistant.Any questions today?"
])
trainer.train([
    
"What payment methods are accepted on Eshop",

'''We accept two payment methods including:

1. payment via M-pesa

2.Payment via Credit Cart(Stripe)'''
])
trainer.train([
    
"How secure is my payment information on Eshop",

'''Eshop  prioritizes customer payment security with encryption, and secure servers. Regular monitoring and auditing are also performed to maintain a secure environment for transactions.'''
])
trainer.train([
"What do I do if my payment is declined",

'''If your payment is declined, you can check the following to resolve the issue:

 

For M-Pesa; 

Check if you have sufficient funds .

 Ensure your phone number is not linked to another account on jumia. 

Ensure you have entered the correct pin 

 
For Card;

Check the spelling and billing information you entered for accuracy.

Ensure that your credit card has sufficient funds or that your bank account has enough balance.

Check if there are any restrictions on your card, such as a daily spending limit.

Make sure your card has not expired.'''

 
])
trainer.train([

"Can I pay cash on delivery for my orders?",

"Unfortunately for now you need to pay for your Eshop orders before delivery using Mpesa or visacard."
])
trainer.train([
    
"What should I do if I have been charged twice for the same order?",

'''If you have been charged twice for the same order, you can contact eshop -admin through eshopecommerce@gmail.com for assistance in resolving the issue.

Please provide the following information to admin when reporting a double charge:

Your name and email address used to place the order.

Order number and date of purchase.

Details of the double charge (amount, date, and transaction number).

eshp customer service will assist you in resolving the issue and arranging for a refund if applicable.'''
])
trainer.train([

"How do I know if my payment has been processed successfully?",

"You can check your email for product the status of your payment and delivery info"
])
trainer.train([
    
"How long does it take for my payment to be processed",

"Most payments on Eshop are processed immediately when completed. However, specific processing times may vary depending on the payment method."
])
trainer.train([
    
"Can I cancel my order and get a refund after payment has been made",

'''If the order hasn't been shipped yet, you can cancel and get a refund by contacting the admin'''
])

trainer.train([
"What if I am not available to receive my delivery?",

'''If you are not available to receive your delivery, you have the following options:

You can arrange for someone else to receive it on your behalf by providing their name and contact information to the delivery agent. It is important to ensure that this person is available at the same address that was provided when placing your order.

Contact the delivery agent to reschedule the delivery for a more convenient time.'''])
trainer.train([
"Can I change my delivery address after placing an order?",

'''It is important to carefully review and confirm the accuracy of your delivery information, such as your address and phone number, before placing an order on Jumia. Once the order has been placed, it is not possible to make changes to the delivery information'''
])
trainer.train([
"What is the delivery fee?",

"The delivery fee is the cost incurred by eshop and its logistics partners for delivering your order to the selected address."
])
trainer.train([
"What do I do if my delivery has not arrived within the estimated time frame?",

'''If your delivery has not arrived within the estimated time frame, you can follow these steps:

Check the order information page in your Eshop account for any updates on the delivery status.

Monitor communication sent through push notifications, emails, and the APP INBOX for any updates on the delivery status of your order.'''
])
trainer.train([
"Who do I contact if there is a problem with my delivery",
"Please provide the order information to admin through eshopecommerce@gmail.com to resolve your issue:"

])
trainer.train([
"What happens if my delivery is damaged upon arrival",

"In case your delivery arrives damaged, reach out to the admin team through eshopecommerce@gmail.com customer care line at 0716241697 with details about the damage. Our customer service representatives will assist you in resolving the issue and, if eligible, arrange for a refund. Remember to promptly inspect your delivery upon arrival and report any damages."
])
trainer.train([
"What types of products does Eshop offer",

"Eshop is Kenya's leading online store, providing customers with an extensive selection of products in multiple categories. From electronics, apparel and home décor to health and beauty products. "
])
trainer.train([
"How do I search for a specific product?",

"You can search for a specific product on Eshop by using the search bar located at the top of the website. Enter the name of the product you are looking for into the bar, and then click the 'search' button. You will be presented with a list of results which match your criteria."
])
trainer.train([
"How can I view product details and specifications?",

"Product details and specifications for items sold on Eshop can be easily accessed by clicking on the product's listing. "
])
trainer.train([
    
"How do I create an account on Eshop?",

'''Creating an account on Eshop is easy and only takes a few steps. 

Step 1: Go to the eshop website at HTTPS://WWW.eshop.CO.KE/. 

 

Step 2: Click on the “profile” option at the navigation bar of the page. 

 

Step 3: Select the “login” option and you will be directed to the login page. 

Step 4: Underneath the login page you will find the registration page'''
])

trainer.train([
"How do I reset my password?",

'''You can reset your password by following these steps:

Step 1: First, go to the eshop website, and click on the login button in the navigation bar.

Step 2: Then, click on the “Forgot Password”

Step 3: We will send a password reset link to your email.
insert the code
Step 4: The link will redirect you to a password reset page.

Step 5: You will then be able to submit your password reset and use your new password'''
])
trainer.train(['Thankyou', 'You are welcome'])
trainer.train(['Ok', 'Welcome'])
trainer.train(['Thanks', 'Anytime friend'])

# exit_conditions = (":q", "quit", "exit")
# while True:
#     query = input("> ")
#     if query in exit_conditions:
#         break
#     else:
#         print(f"🪴 {chatbot.get_response(query)}")
