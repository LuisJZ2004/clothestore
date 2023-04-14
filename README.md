# Closet
'Closet' is a simple and not so simple clothes ecommerce made with Django. This ecommerce counts with search, cart, user register and filtering systems. It was an old project I took up and got it better.

Video of the project: https://youtu.be/pIR4yR-1W8M

## Required knowledge
- Intermediate/advanced Python and Django.
- Basic HTML and CSS.
- SQL and MySQL (or any SQL manager like PostgreSQL or SQLite3)
- Git

## Database
### Independant models
We count with six models, User, HomeSet, ClothingType, Brand, Color and Size:

1. User: the auth user model.
2. HomeSet: The set of clothes that will be in the main page.
3. ClothingType: the type of clothing that a garment belongs.
4. Brand: The brand that a garment belongs.
5. Color: A garment can have several colors.
6. Size: A garment has several sizes depending on the color (in the PledgeColorSet bellow it will be better understood)

### Dependant models
There are four dependant models (ManyToMany tables are not in here):

1. Pledge: it's the product per se, it'll have different sets with different colors/images in that color, and those sets, different sizes with a ManyToMany table. (It is 'garment' I thought it meant that before and I made a mistake, by then it was too late).
2. PledgeColorSet: A garment has different prices and different sizes in base to the color, that is the PledgeColorSet, a set with a respective color, with an image of the garment int that color, a price and different sizes. These will be the data showed in base to the garments.
3. Cart: The place where the products to buy will be added.
4. CartPledge: When a product gets in the cart, we have to specify the size, that is te objective of this model.

### Flowchart
![](https://i.postimg.cc/dtn4D8PH/clothestore-database-flowchart.jpg)

## Apps
It has seven apps with different goals.

#### extra_logic
Any extra algorythm or hard enough algorythm I need to make for any app is made in here, in order to have more readbility in the code. Filters, paginations or search algorythms are made in this app. The little rule in this app is to create a new folder with the name of an app, add the method '__init__.py', and then, start creating the modules to write the logic you want for each app.

#### accounts
In this app the user can log and sign in. It has no models, only uses the default User model from authentication Django module.

#### brands
The model 'Brand' is created in here, as well as the views belonging to the model data. In this app all the available brands are showed and their garments in their respective views.

#### cart
The model 'Cart' is created in here. Adds, removes and shows all the products added and not added for the user. All the views here are obviously protected with 'login_required' decorator.

#### clothes
The jewel in the crown. All related to the clothes is in this app, the models 'ClothingType', 'Pledge' and 'PledgeColorSet' are in here, as well as the models 'Size' and 'Color'. the pledges are set in list that can be filtered through an extra algorythm made in 'extra_logic'. the garments are showed thanks to this app.

#### home
The main page. The base layout HTML is in this app. It has only one view, the one that shows all the HomeSets and almost always the first one the user will see.

#### search
Searching products through the search bar in the header is the goal of this app.

------------

This was a brief introduction about what this project is and does. Feel free to prove the page/result of all I wrote and also read all you can the code. I'm overt to any critic to get better and grow up, feel free to that too.
