# Waiter Budget
#### Video Demo:  https://youtu.be/OJpgBjy7PLE
#### Description: Final project to conclude CS50 - Introduction to Computer Science

## **The Idea**
My final project is an expense tracker, geared towards the waiters in the restaurant business.
I got the inspiration for the application when I spoke to some of the waiters my girlfriend works with
and they are always unsure as to what their finances would be coming month end.

### Technologies used:

+ Flask Web Framework
+ SQLITE
+ Python
+ HTML
+ CSS
+ Jinja

### **How it works**
The program is a simple expense tracker. You can register a new user, and once logged in
for the first time, the program redirects you to the Income page. Selecting the month
and year, and then entering your hours worked for the month and what your rate of pay is.
Optionally you can enter Other income and finally save your income.

Once saved the page redirects to the waiter tips page where you select the day you wish
to capture along with cash tips and card transaction tips received. You can can then
choose to save and continue to the expenses page or save and add additional tips.

When you have captured all your tips, you are redirected to the expenses page.
Select the month and year you are capturing and then complete the expense(s)
you wish to capture.

Finally, you are redirected to the overview page, that will display the current months
data that was captured, if it was captured. If you completed more than one month,
you will be able to view each of those from the drop down selection.
Your Income, Tips, Total Income, Total Expenses and Total remaining funds are displayed
on the left had side of the screen and the current months expense each on the right-hand side.
You are able to update the expense of your choosing with a new value.

### **Database**
I created a database with four tables as a start
+ Users, to store username and password, with a unique index on the username field.
+ Income, to store all income data along with the month/year
+ Tips, to store only the data for all the tips entered
+ Expenses, to store all expenses and the total of all expenses

I have come to the conclusion that there is room for improvement with regards to the database setup.

### **Aesthetic**
I decided on a black and white colour scheme as I was thinking about waiters in a tuxedo and
thought the colours would work well with a minimalistic scheme.

## **Improvements**
The idea is something I like and know could have real world application.
There are various features I will be adding in the future.
+ Goals Tab
+ Update Income
+ Update Tips
+ Rework the Expenses Updating
+ Many more ideas floating in my head

Also there is some code I am not completely satisfied with and will be working
on the design of how some features are implemented. As mentioned, the database
can also use some improvement.

## **Thank You**
Thank you to David Malan and his team for the course and providing the building blocks to development.
The progress made and the knowledge gained is almost immeasurable, and this is only the start for me.

## **About CS50**
This is CS50x, Harvard University's introduction to the intellectual enterprises of computer science
and the art of programming for majors and non-majors alike, with or without prior programming experience.
An entry-level course taught by David J. Malan, CS50x teaches students how to think algorithmically and
solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation,
resource management, security, software engineering, and web development. Languages include C, Python,
SQL, and JavaScript plus CSS and HTML. Problem sets inspired by real-world domains of biology, cryptography,
finance, forensics, and gaming. The on-campus version of CS50x, CS50, is Harvard's largest course.
[Find Out More](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x)