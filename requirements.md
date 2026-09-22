# URL Shortener

## Core requirements

Users can create shortened URLs.

A shortened URL contains:

- Target URL
- Unique alias
- Full shortened URL
- Creation time
- Click count

Users may optionally provide a custom alias.

If the user does not provide an alias, the application generates one.

Aliases must be unique.

Visiting a shortened URL redirects the user to the original URL.

Each redirect increments the click count.

Users can retrieve metadata about a shortened URL.


## API

### POST /urls/shorten

Create a shortened URL.

Example request:

```json
{
  "target_url": "https://example.com/some/long/path",
  "custom_alias": "example"
}