URL Shortener REST API Service

Tech stack python/fastAPI

We will be connecting our service to a postgresql db in digital ocean where we will also be deploying our app there

Build a production-ready REST API Service that accepts a long URL, generates a shortened URL (alias), redirects users to the original URL, and returns metadata about the created short links

Bitly clone

Functional requirements:
User sends a long URL and we generate a unique shortened URL
Support either automatically generated short codes or user-defined custom aliases (ensure proper validation)
Redirect user to the original URL when the shortened link is accessed
Return metadata about the shortened URL and allow the retrieval of metadata for an existing short URL

Out of scope:
User sign up
UI
Database migration



