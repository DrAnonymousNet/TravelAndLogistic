# TravelAndLogistic
An API for Travel Ticket Management created Django Rest Framework. It allows authenticated user to book and pay for ticket 
for already defined Traveling Company. Authentication System with Djoser Framework and Flutterwave Payment Gateway 

# Live Link
This project is live at [GoWithEase](gowithease.herokuapp.com)

# Features

1. Robust Authentication System created with Djoser
2. OTP verification with Termi
3. Payment Gateway using Flutterwave
4. Documented with Swagger


# TO DO

1. Refactor Code
2. Add more documentation


# Documentation Guild To Use

Most of the endpooints are authentication protected. To test the endpoints in the documentation page:

1. Create a new user with valid email using the `User Create Endpoint`
2. Check Email for Activation Code. It will be in the format `/activate/{UID}/{Token}`
3. Copy the UID and Token and activate your account with the User Activation Endpoint
4. Create a `JWT Access and Refresh` token with the `JWT Create Endpoint`
5. Copy the `JWT Access Token` 
6. Authorize yourself, Authorization token in the format `JWT {Jwt access token}`
7. You can use other endpoints now.

# General Description

An authenticated user can book a Ticket with a traveling company. Each company has already defined parks 
