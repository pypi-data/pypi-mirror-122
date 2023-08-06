# Pushover plugin

This plugin sends a message to pushover service.

# Requirements

To use this plugin you must register at https://pushover.net and obtain API_TOKEN and USER_KEY.

# Configuration

## Resource configuration

```json
{
  "token": "API_TOKEN from PushOver",
  "user": "USER_KEY from PushOver"
}
```

## Plugin configuration

```json
{
  "source": {
    "name": "pushover",
    "id": "49a3b3ce-3bba-42aa-9ba6-559576cfdfa"
  },
  "message": "message"
}
```

# Input

This plugin does not take any input

# Output

Output returns status and response body from PushOver service.

```json
{
  "status": 200,
  "body": {
    "status": 1,
    "request": "c759f16e-c10a-4066-b91d-05fd06504790"
  }
}
```
